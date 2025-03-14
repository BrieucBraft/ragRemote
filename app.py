import sys
import asyncio
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from ollama import AsyncClient  # Import the async client from Ollama
from fastapi.templating import Jinja2Templates
from fastapi import UploadFile, File, BackgroundTasks
import os

from get_embedding_function import get_embedding_function
import time

app = FastAPI()
templates = Jinja2Templates(directory="templates")

CHROMA_PATH = "chroma"
MODEL = "gemma3"

PROMPT_TEMPLATE = """
Here is some context that can help you provide information to the question

{context}

---

Knowing that only the context is true, lead the human to the legitimate information about his question considering the above context: {question}
"""

DATA_PATH = "data"

@app.post("/upload_pdf")
async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Accepts PDF uploads and processes them asynchronously."""
    file_path = os.path.join(DATA_PATH, file.filename)

    # Save file to disk
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Process the uploaded file in the background
    background_tasks.add_task(populate_chroma)

    return {"message": f"{file.filename} uploaded successfully. Processing in the background."}

async def populate_chroma():
    """Runs the PDF processing script in the background to avoid blocking requests."""
    os.system("python pop_data.py")

# Wait for Ollama to be ready
@app.on_event("startup")
async def startup_event():
    print("Waiting for Ollama to be ready...")
    client = AsyncClient(host="http://localhost:11434")
    max_retries = 10
    for i in range(max_retries):
        try:
            models = await client.list()
            print(f"Ollama is ready. Available models: {models}")
            break
        except Exception as e:
            print(f"Ollama not ready yet. Retry {i+1}/{max_retries}. Error: {e}")
            if i == max_retries - 1:
                print("Failed to connect to Ollama after maximum retries.")
            else:
                time.sleep(5)
async def load_chroma():
    global db
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    print("ChromaDB loaded and ready!")

@app.get("/")
async def home(request: Request):
    # Return some basic information or a simple response
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query")
async def query(request: Request):
    """FastAPI route to accept a POST request with JSON input."""
    data = await request.json()
    query_text = data.get("query_text", "")

    if not query_text:
        raise HTTPException(status_code=400, detail="query_text parameter is required")

    # Return a StreamingResponse that uses the async generator
    return StreamingResponse(query_rag(query_text), media_type="text/plain")

async def query_rag(query_text: str):
    """Asynchronous function to process the query using RAG + Ollama."""
    # Prepare the vector database.
    # embedding_function = get_embedding_function()
    # db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    global db
    if not db:
        raise HTTPException(status_code=500, detail="ChromaDB not initialized.")

    # Timer for the embedding phase.
    start_embedding = time.perf_counter()
    results = await asyncio.to_thread(db.similarity_search_with_score, query_text, k=3)
    embedding_time = time.perf_counter() - start_embedding
    print(f"Embedding phase took: {embedding_time:.2f} seconds\n")

    # Build context from retrieved documents.
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Prepare the message list for Ollama.
    messages = [{"role": "user", "content": prompt}]

    print(prompt)

    # Initialize the async client.
    client = AsyncClient()

    # Timer for the LLM response phase.
    start_llm = time.perf_counter()
    
    # Get the response stream
    response = await client.chat(model=MODEL, messages=messages, stream=True)
    
    # Process each chunk
    async for chunk in response:
        content = chunk["message"]["content"]
        print(content, end="", flush=True)
        yield content
    
    llm_time = time.perf_counter() - start_llm
    print(f"\nLLM response took: {llm_time:.2f} seconds\n")

    # Print out source IDs.
    sources = [doc.metadata.get("id", None) for doc, _ in results]
    print(f"Sources: {sources}")
