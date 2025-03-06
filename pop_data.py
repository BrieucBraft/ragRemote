import argparse
import os
import shutil
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma

CHROMA_PATH = "chroma"
DATA_PATH = "data"
MAX_BATCH_SIZE = 5461

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Initialize the Chroma database and retrieve existing IDs and source paths.
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    existing_items = db.get(include=["metadatas"])  # use "metadatas" here
    existing_ids = set(existing_items["ids"])
    existing_sources = {meta["source"] for meta in existing_items["metadatas"] if "source" in meta}

    pdf_files = [f for f in os.listdir(DATA_PATH) if f.endswith(".pdf")]

    results = {}  # Maps each pdf file to its list of new chunks.
    start_total = time.time()

    with ProcessPoolExecutor() as executor:
        # Pass existing_ids and existing_sources to each worker.
        future_to_pdf = {
            executor.submit(process_pdf, pdf_file, existing_ids, existing_sources): pdf_file
            for pdf_file in pdf_files
        }
        for future in as_completed(future_to_pdf):
            pdf_file = future_to_pdf[future]
            try:
                processed_pdf, new_chunks = future.result()
                results[processed_pdf] = new_chunks
            except Exception as e:
                print(f"Error processing {pdf_file}: {e}")

    total_new_chunks = sum(len(chunks) for chunks in results.values())
    print(f"Total new chunks across all PDFs: {total_new_chunks}")

    # If total exceeds MAX_BATCH_SIZE, remove PDFs with the largest chunk counts until under the limit.
    if total_new_chunks > MAX_BATCH_SIZE:
        pdf_counts = [(pdf, len(chunks)) for pdf, chunks in results.items()]
        pdf_counts.sort(key=lambda x: x[1], reverse=True)
        removed_pdfs = []
        while total_new_chunks > MAX_BATCH_SIZE and pdf_counts:
            pdf_to_remove, count = pdf_counts.pop(0)
            removed_pdfs.append(pdf_to_remove)
            total_new_chunks -= count
            del results[pdf_to_remove]
            print(f"⏩ Skipping {os.path.basename(pdf_to_remove)} with {count} chunks to remain under the limit.")
        print(f"After removals, total new chunks: {total_new_chunks}")

    final_new_chunks = [chunk for chunks in results.values() for chunk in chunks]

    if final_new_chunks:
        print(f"👉 Adding {len(final_new_chunks)} new chunks from the selected PDFs.")
        start_add = time.time()
        new_chunk_ids = [chunk.metadata["id"] for chunk in final_new_chunks]
        db.add_documents(final_new_chunks, ids=new_chunk_ids)
        end_add = time.time()
        print(f"⏱️ Time taken to add chunks: {end_add - start_add:.2f} seconds")
    else:
        print("✅ No new chunks to add after filtering.")

    end_total = time.time()
    print(f"Total processing time: {end_total - start_total:.2f} seconds")

def process_pdf(pdf_file, existing_ids, existing_sources):
    """
    Process a single PDF:
      - If the PDF's path is already in existing_sources, skip processing.
      - Otherwise, load the PDF, split it into chunks, calculate unique chunk IDs,
        and filter out chunks that already exist in the database.
    Returns a tuple (pdf_file, list_of_new_chunks).
    """
    pdf_path = os.path.join(DATA_PATH, pdf_file)
    if pdf_path in existing_sources:
        print(f"📄 Skipping {pdf_file} as it is already in the database.")
        return pdf_file, []

    print(f"📄 Processing {pdf_file}")
    documents = load_document(pdf_path)
    if not documents:
        print(f"⚠️ No documents found in {pdf_file}, skipping.")
        return pdf_file, []
    chunks = split_documents(documents)
    chunks_with_ids = calculate_chunk_ids(chunks)
    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]
    return pdf_file, new_chunks

def load_document(pdf_path):
    # Load only documents from the specified PDF file.
    document_loader = PyPDFDirectoryLoader(os.path.dirname(pdf_path))
    documents = document_loader.load()
    return [doc for doc in documents if doc.metadata.get("source") == pdf_path]

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0
        chunk.metadata["id"] = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
    return chunks

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()
