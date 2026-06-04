import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Configuration
CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5" # Defaulting to small for demonstration
RERANKER_MODEL_NAME = "BAAI/bge-reranker-base"
LLM_MODEL = "llama-3.1-8b-instant" # Using Groq's supported Llama 3.1 model
COLLECTION_NAME = "mutual_fund_facts"

class MutualFundRAGPipeline:
    def __init__(self):
        # 1. Initialize Dense Retrieval
        print("Loading dense embeddings...")
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        self.vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=CHROMA_DB_DIR
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 15}) # Fetch Top-15
        
        # 2. Initialize Cross-Encoder for Re-ranking
        print("Loading cross-encoder re-ranker...")
        self.reranker = CrossEncoder(RERANKER_MODEL_NAME)
        
        # 3. Initialize LLM (Temperature 0.0 for deterministic factual answers via Groq)
        self.llm = ChatGroq(model_name=LLM_MODEL, temperature=0.0)
        
        # 4. Strict System Prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a strict, facts-only mutual fund assistant. 
You must answer the user's question using ONLY the provided context.
If the context does not contain the answer, or if the question is non-technical, you MUST say exactly "sorry i dont know".

CONSTRAINTS:
1. Maximum 3 sentences.
2. Do not offer opinions, financial advice, or calculations.

CONTEXT: 
{context}"""),
            ("human", "{question}")
        ])

    def two_stage_retrieve(self, query: str):
        """
        Executes Dense Retrieval (Top 15) followed by Cross-Encoder Re-ranking (Top 3).
        """
        # Stage 1: Dense Retrieval
        initial_docs = self.retriever.invoke(query)
        
        if not initial_docs:
            return []
            
        # Stage 2: Cross-Encoder Re-ranking
        # Create pairs of (query, document_text) for the cross-encoder
        pairs = [[query, doc.page_content] for doc in initial_docs]
        scores = self.reranker.predict(pairs)
        
        # Sort documents by their cross-encoder scores in descending order
        scored_docs = list(zip(initial_docs, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        # Return the top 10 chunks to allow answering queries about multiple funds
        top_10_docs = [doc for doc, score in scored_docs[:10]]
        return top_10_docs

    def generate_answer(self, query: str) -> str:
        """
        Main pipeline execution.
        """
        # Step 1: Retrieve context
        top_docs = self.two_stage_retrieve(query)
        
        if not top_docs:
            return "sorry i dont know"
            
        # Format context and metadata for the prompt
        context_str = "\n\n".join([doc.page_content for doc in top_docs])
        
        # Step 2: Generate Response
        chain = self.prompt | self.llm
        response = chain.invoke({
            "context": context_str,
            "question": query
        })
        
        answer = response.content.strip()
        
        if "sorry i dont know" in answer.lower():
            return "sorry i dont know"
            
        source_url = top_docs[0].metadata.get('source_url', 'Unknown')
        last_updated = top_docs[0].metadata.get('last_updated_date', 'Unknown')
        
        formatted_answer = f"{answer}\n\nLast updated from sources: {last_updated}\nSource URL: {source_url}"
        
        return formatted_answer

if __name__ == "__main__":
    # Example usage (Requires GROQ_API_KEY in .env):
    # pipeline = MutualFundRAGPipeline()
    # answer = pipeline.generate_answer("What is the exit load for the Tata Digital India Fund?")
    # print(answer)
    pass
