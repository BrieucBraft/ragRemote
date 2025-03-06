import argparse
import os
import shutil
import time
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

    # Initialize the Chroma DB and get existing IDs once.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    
    pdf_files = [f for f in os.listdir(DATA_PATH) if f.endswith(".pdf")]
    
    all_new_chunks = []
    
    # Process all PDFs at once
    for pdf_file in pdf_files:
        pdf_path = os.path.join(DATA_PATH, pdf_file)
        print(f"📄 Loading {pdf_file}")
        documents = load_document(pdf_path)
        if not documents:
            print(f"⚠️ No documents found in {pdf_file}, skipping.")
            continue
        chunks = split_documents(documents)
        chunks_with_ids = calculate_chunk_ids(chunks)
        # Filter out chunks that already exist in the DB.
        new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]
        if new_chunks:
            all_new_chunks.extend(new_chunks)
        else:
            print(f"✅ All chunks from {pdf_file} already exist in the DB.")
    
    # Group new chunks by their source PDF file.
    pdf_to_chunks = {}
    for chunk in all_new_chunks:
        source = chunk.metadata.get("source")
        if source not in pdf_to_chunks:
            pdf_to_chunks[source] = []
        pdf_to_chunks[source].append(chunk)
    
    total_new_chunks = sum(len(chunks) for chunks in pdf_to_chunks.values())
    print(f"Total new chunks across all PDFs: {total_new_chunks}")

    # If total exceeds MAX_BATCH_SIZE, remove PDFs starting with the largest.
    if total_new_chunks > MAX_BATCH_SIZE:
        # Create a list of (pdf, count) tuples sorted descending by chunk count.
        pdf_counts = [(pdf, len(chunks)) for pdf, chunks in pdf_to_chunks.items()]
        pdf_counts.sort(key=lambda x: x[1], reverse=True)
        
        removed_pdfs = []
        while total_new_chunks > MAX_BATCH_SIZE and pdf_counts:
            pdf_to_remove, count = pdf_counts.pop(0)
            removed_pdfs.append(pdf_to_remove)
            total_new_chunks -= count
            del pdf_to_chunks[pdf_to_remove]
            print(f"⏩ Skipping {os.path.basename(pdf_to_remove)} with {count} chunks to remain under the limit.")
        
        print(f"After removals, total new chunks: {total_new_chunks}")

    # Flatten the remaining chunks from selected PDFs.
    final_new_chunks = [chunk for chunks in pdf_to_chunks.values() for chunk in chunks]

    if final_new_chunks:
        print(f"👉 Adding {len(final_new_chunks)} new chunks from the selected PDFs.")
        start_time = time.time()
        new_chunk_ids = [chunk.metadata["id"] for chunk in final_new_chunks]
        db.add_documents(final_new_chunks, ids=new_chunk_ids)
        end_time = time.time()
        print(f"⏱️ Time taken to add chunks: {end_time - start_time:.2f} seconds")
    else:
        print("✅ No new chunks to add after filtering.")

def load_document(pdf_path):
    # Load only documents from the given PDF file.
    document_loader = PyPDFDirectoryLoader(os.path.dirname(pdf_path))
    documents = document_loader.load()
    return [doc for doc in documents if doc.metadata.get("source") == pdf_path]

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=550,
        chunk_overlap=200,
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
        
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
        chunk.metadata["id"] = chunk_id
    
    return chunks

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()
