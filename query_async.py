import sys
if sys.platform.startswith('win'):
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from flask import Flask
import argparse
import asyncio
import time
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from ollama import AsyncClient  # Import the async client from Ollama

from get_embedding_function import get_embedding_function

app = Flask(__name__)

# @app.route("/")
# def run_script():
#     return "Hello from Cloud Run!"



CHROMA_PATH = "chroma"
MODEL = "gemma3"

PROMPT_TEMPLATE = """
Here is some context that can help you provide information to the question

{context}

---

Knowing that only the context is true, lead the human to the legitimate information about his question considering the above context. : {question}
"""

@app.route("/")
async def main():
    # Parse CLI arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    await query_rag(query_text)

async def query_rag(query_text: str):
    # Prepare the vector database.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

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

    response_text = ""
    print("Response: ", end="", flush=True)

    # Timer for the LLM response phase.
    start_llm = time.perf_counter()
    async for chunk in await client.chat(model=MODEL, messages=messages, stream=True):
        content = chunk["message"]["content"]
        print(content, end="", flush=True)
        response_text += content
    llm_time = time.perf_counter() - start_llm
    print()  # Newline after streaming is complete.

    print(f"\nLLM response took: {llm_time:.2f} seconds\n")

    # Print out source IDs.
    sources = [doc.metadata.get("id", None) for doc, _ in results]
    print(f"Sources: {sources}")

    return response_text

# if __name__ == "__main__":
#     asyncio.run(main())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)