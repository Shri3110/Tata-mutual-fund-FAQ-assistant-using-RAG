from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import MutualFundRAGPipeline
from guardrails import GuardrailSystem

app = FastAPI(title="Mutual Fund FAQ API")

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize backend logic
try:
    pipeline = MutualFundRAGPipeline()
    guard = GuardrailSystem()
except Exception as e:
    print(f"Error initializing systems: {e}")

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    is_refusal: bool = False

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    query = request.query
    
    if query.strip().lower() == "hi":
        return ChatResponse(answer="hi", is_refusal=False)
    
    # 1. Intent Router
    if guard.is_advisory_query(query):
        return ChatResponse(answer=guard.get_refusal_response(), is_refusal=True)
        
    # 2. Generate
    generated_answer = pipeline.generate_answer(query)
    
    # 3. Validate
    if "sorry i dont know" in generated_answer.lower():
        return ChatResponse(answer="sorry i dont know", is_refusal=False)
        
    is_valid, error_msg = guard.validate_llm_response(generated_answer)
    if is_valid:
        return ChatResponse(answer=generated_answer, is_refusal=False)
    else:
        # Failsafe if the LLM output is non-compliant
        return ChatResponse(answer=f"An error occurred during response validation: {error_msg}. Please try asking your question differently.", is_refusal=True)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Mutual Fund FAQ API is running"}
