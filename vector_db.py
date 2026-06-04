import os
from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from pinecone import Pinecone, ServerlessSpec

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

def build_vector_store(documents: list, index_name: str = "mutual-fund-facts"):
    """
    Initializes a Pinecone vector store and ingests the chunked documents.
    Uses Pinecone Inference API for embeddings to save local memory.
    """
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY environment variable is not set.")
        
    pc = Pinecone(api_key=api_key)
    
    model_name = "multilingual-e5-large"
    dimension = 1024
    
    if index_name not in pc.list_indexes().names():
        print(f"Creating Pinecone index '{index_name}'...")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        
    embeddings = PineconeEmbeddings(model=model_name, pinecone_api_key=api_key)
    
    texts = [doc["page_content"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]
    
    vectorstore = PineconeVectorStore.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        index_name=index_name
    )
    
    print(f"Successfully ingested {len(texts)} chunks into Pinecone index '{index_name}'")
    return vectorstore

if __name__ == "__main__":
    # Example integration:
    # 1. from ingestion import scrape_groww_url
    # 2. text = scrape_groww_url("https://groww.in/mutual-funds/tata-digital-india-fund-direct-growth")
    # 3. chunks = chunk_text(text, source_url="https://groww.in/mutual-funds/tata-digital-india-fund-direct-growth")
    # 4. build_vector_store(chunks)
    pass
