import os
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Configuration
EMBEDDING_MODEL_NAME = "multilingual-e5-large"
LLM_MODEL = "llama-3.1-8b-instant" # Using Groq's supported Llama 3.1 model
INDEX_NAME = "mutual-fund-facts"

class MutualFundRAGPipeline:
    def __init__(self):
        # 1. Initialize Dense Retrieval via Pinecone Serverless API
        print("Connecting to Pinecone Inference API...")
        api_key = os.getenv("PINECONE_API_KEY")
        self.embeddings = PineconeEmbeddings(model=EMBEDDING_MODEL_NAME, pinecone_api_key=api_key)
        self.vectorstore = PineconeVectorStore(
            index_name=INDEX_NAME,
            embedding=self.embeddings
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5}) # Fetch Top-5 for dense
        
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
        Executes Dense Retrieval (Top 5). Re-ranking removed to save memory.
        """
        return self.retriever.invoke(query)

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
