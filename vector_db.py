import os
from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
# Note: In a production environment, use a robust embedding model like OpenAIEmbeddings or HuggingFaceEmbeddings.
# Here we'll configure a placeholder or a lightweight open-source embedding if possible.
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb

# Ensure ChromaDB uses a local directory for persistence
CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")

def chunk_text(text: str, source_url: str) -> list:
    """
    Splits the extracted text into semantic chunks and attaches metadata.
    """
    # The RecursiveCharacterTextSplitter attempts to split on paragraphs, then sentences, etc.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(text)
    
    # Attach metadata to each chunk
    documents = []
    for chunk in chunks:
        # Create a document object or just dicts depending on the interface needed
        # We'll return a dict representation that can be converted to Langchain Document objects
        document = {
            "page_content": chunk,
            "metadata": {
                "source_url": source_url,
                "last_updated_date": datetime.today().strftime('%Y-%m-%d')
            }
        }
        documents.append(document)
        
    return documents

def build_vector_store(documents: list, collection_name: str = "mutual_fund_facts"):
    """
    Initializes a ChromaDB vector store and ingests the chunked documents.
    Dynamically selects BGE embedding model based on the volume of chunks.
    """
    total_chunks = len(documents)
    
    # Select embedding model based on volume. 
    # For a large number of chunks, BGE-large provides better semantic matching.
    # For fewer chunks, BGE-small is faster and sufficient.
    if total_chunks > 1000:
        model_name = "BAAI/bge-large-en-v1.5"
        print(f"Volume is high ({total_chunks} chunks). Using {model_name} for embeddings.")
    else:
        model_name = "BAAI/bge-small-en-v1.5"
        print(f"Volume is moderate ({total_chunks} chunks). Using {model_name} for embeddings.")

    # Using HuggingFace's sentence transformers for BGE embeddings
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    # Format for Langchain's Chroma wrapper
    texts = [doc["page_content"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]
    
    # Initialize the Vector Store
    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        collection_name=collection_name,
        persist_directory=CHROMA_DB_DIR
    )
    
    vectorstore.persist()
    print(f"Successfully ingested {len(texts)} chunks into ChromaDB collection '{collection_name}' at {CHROMA_DB_DIR}")
    return vectorstore

if __name__ == "__main__":
    # Example integration:
    # 1. from ingestion import scrape_groww_url
    # 2. text = scrape_groww_url("https://groww.in/mutual-funds/tata-digital-india-fund-direct-growth")
    # 3. chunks = chunk_text(text, source_url="https://groww.in/mutual-funds/tata-digital-india-fund-direct-growth")
    # 4. build_vector_store(chunks)
    pass
