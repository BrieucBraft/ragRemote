import sys
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from ollama import AsyncClient
from get_embedding_function import get_embedding_function
import time

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()
templates = Jinja2Templates(directory="templates")

CHROMA_PATH = "chroma"
MODEL = "gemma3"  # Use the registered model name

PROMPT_TEMPLATE = """
Here is some context that can help you provide information to the question

{context}

---

Knowing that only the context is true, lead the human to the legitimate information about his question considering the above context: {question}
"""


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    query_text = data.get("query_text", "")

    if not query_text:
        raise HTTPException(status_code=400, detail="query_text parameter is required")

    return StreamingResponse(query_rag(query_text), media_type="text/plain")

async def query_rag(query_text: str):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    start_embedding = time.perf_counter()
    results = await asyncio.to_thread(db.similarity_search_with_score, query_text, k=3)
    embedding_time = time.perf_counter() - start_embedding
    print(f"Embedding phase took: {embedding_time:.2f} seconds\n")

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    messages = [{"role": "user", "content": prompt}]
    print(prompt)

    start_llm = time.perf_counter()
    client = AsyncClient(host="http://localhost:11434")
    response = await client.chat(
        model=MODEL,
        messages=messages,
        stream=True
    )

    async for chunk in response:
        content = chunk["message"]["content"]
        print(content, end="", flush=True)
        yield content

    llm_time = time.perf_counter() - start_llm
    print(f"\nLLM response took: {llm_time:.2f} seconds\n")

    sources = [doc.metadata.get("id", None) for doc, _ in results]
    print(f"Sources: {sources}")
