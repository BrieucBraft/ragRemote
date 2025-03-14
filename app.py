import sys
import asyncio
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from ollama import AsyncClient
from fastapi.templating import Jinja2Templates
from fastapi import UploadFile, File, BackgroundTasks
from fastapi.staticfiles import StaticFiles
import os
import time
from typing import Dict
import threading

from get_embedding_function import get_embedding_function

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

CHROMA_PATH = "chroma"
MODEL = "llama3.2:1b"
DATA_PATH = "data"

# Initialize embedding function once at startup
embedding_function = None
db = None

# Create a lock for thread safety
db_lock = threading.Lock()

# Track active user sessions
active_users: Dict[str, bool] = {}
user_lock = threading.Lock()

PROMPT_TEMPLATE = """
Here is some context that can help you provide information to the question

{context}

---

Knowing that only the context is true, lead the human to the legitimate information about his question considering the above context: {question}
"""

# Dependency to get client IP
def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        client_ip = forwarded.split(",")[0]
    else:
        client_ip = request.client.host
    return client_ip

@app.post("/upload_pdf")
async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Accepts PDF uploads and processes them asynchronously."""
    # Create data directory if it doesn't exist
    os.makedirs(DATA_PATH, exist_ok=True)
    
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
    # Reload the database after population
    global db
    with db_lock:
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

# Wait for Ollama to be ready and initialize resources
@app.on_event("startup")
async def startup_event():
    global embedding_function, db
    
    print("Initializing embedding function...")
    embedding_function = get_embedding_function()
    
    print("Initializing vector database...")
    with db_lock:
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
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

@app.get("/")
async def home(request: Request):
    # Return some basic information or a simple response
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query")
async def query(request: Request, client_ip: str = Depends(get_client_ip)):
    """FastAPI route to accept a POST request with JSON input."""
    # Check if the user is already processing a query
    with user_lock:
        if client_ip in active_users and active_users[client_ip]:
            raise HTTPException(
                status_code=429, 
                detail="You already have an active query. Please wait for it to complete."
            )
        active_users[client_ip] = True
    
    try:
        data = await request.json()
        query_text = data.get("query_text", "")

        if not query_text:
            raise HTTPException(status_code=400, detail="query_text parameter is required")

        # Return a StreamingResponse that uses the async generator
        return StreamingResponse(
            query_rag(query_text, client_ip),
            media_type="text/plain"
        )
    except Exception as e:
        # If there's an error, make sure to release the user lock
        with user_lock:
            active_users[client_ip] = False
        raise

@app.get("/query_status")
async def query_status(client_ip: str = Depends(get_client_ip)):
    """Check if a user has an active query."""
    with user_lock:
        is_active = client_ip in active_users and active_users[client_ip]
    return {"active": is_active}

async def query_rag(query_text: str, client_ip: str):
    """Asynchronous function to process the query using RAG + Ollama."""
    try:
        # Use the global database instance
        global db
        
        # Timer for the embedding phase.
        start_embedding = time.perf_counter()
        
        # Use the global db instance with thread safety
        with db_lock:
            results = await asyncio.to_thread(
                db.similarity_search_with_score, 
                query_text, 
                k=2
            )
            
        embedding_time = time.perf_counter() - start_embedding
        print(f"Embedding phase took: {embedding_time:.2f} seconds\n")

        # Build context from retrieved documents.
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        # Prepare the message list for Ollama.
        messages = [{"role": "user", "content": prompt}]

        # Initialize the async client.
        client = AsyncClient()

        # Timer for the LLM response phase.
        start_llm = time.perf_counter()
        
        # Get the response stream
        response = await client.chat(model=MODEL, messages=messages, stream=True, options={'temperature': 0.0})  # Adjust temperature here)

        
        # Process each chunk
        async for chunk in response:
            content = chunk["message"]["content"]
            print(content, end="", flush=True)
            yield content

        yield "\n\n---\n\nSources:\n"
        for i, (doc, score) in enumerate(results):
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "N/A")
            yield f"[{i+1}] {source} (Page: {page}, Score: {score:.2f})\n"
        
        llm_time = time.perf_counter() - start_llm
        print(f"\nLLM response took: {llm_time:.2f} seconds\n")

        yield f"\nResponse time: {llm_time:.2f} seconds\n"

        # Print out source IDs.
        sources = [doc.metadata.get("id", None) for doc, _ in results]
        print(f"Sources: {sources}")
    except Exception as e:
        print(f"Error in query_rag: {e}")
        yield f"An error occurred: {str(e)}"
    finally:
        # Always release the user lock when done
        with user_lock:
            active_users[client_ip] = False