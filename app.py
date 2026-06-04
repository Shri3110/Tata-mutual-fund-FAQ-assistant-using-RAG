import streamlit as st
from rag_pipeline import MutualFundRAGPipeline
from guardrails import GuardrailSystem
from dotenv import load_dotenv

# Load env variables (for Groq API Key)
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Tata Mutual Fund FAQ Assistant",
    page_icon="🏦",
    layout="centered"
)

# --- Initializing Backend Systems ---
@st.cache_resource
def load_systems():
    # Cache the pipeline and guardrails so they aren't re-initialized on every UI interaction
    pipeline = MutualFundRAGPipeline()
    guard = GuardrailSystem()
    return pipeline, guard

try:
    pipeline, guard = load_systems()
except Exception as e:
    st.error(f"Error initializing backend systems. Please check your .env file and dependencies. \n{e}")
    st.stop()

# --- UI Header & Disclaimer ---
st.title("🏦 Tata Mutual Fund FAQ Assistant")
st.error("**DISCLAIMER:** Facts-only. No investment advice. This assistant only retrieves factual data from official SIDs, KIMs, and Factsheets. It cannot compare funds or advise you on investments.")

# --- Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Example Prompts ---
st.markdown("### Example Queries:")
col1, col2, col3 = st.columns(3)
if col1.button("What is the exit load?"):
    st.session_state.query_to_run = "What is the exit load for the Tata Digital India Fund?"
if col2.button("Who is the fund manager?"):
    st.session_state.query_to_run = "Who is the fund manager for Tata Digital India Fund?"
if col3.button("Minimum SIP amount?"):
    st.session_state.query_to_run = "What is the minimum SIP amount?"

# --- Chat Input & Processing ---
prompt = st.chat_input("Ask a factual question about Tata Mutual Funds...")

# If a user clicks an example button, override the prompt
if "query_to_run" in st.session_state and st.session_state.query_to_run:
    prompt = st.session_state.query_to_run
    st.session_state.query_to_run = None

if prompt:
    # 1. Add user message to UI
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing official documents..."):
            
            # 2. Guardrail: Intent Router (Intercept Advisory Queries)
            if prompt.strip().lower() == "hi":
                response_text = "hi"
            elif guard.is_advisory_query(prompt):
                response_text = guard.get_refusal_response()
            else:
                # 3. RAG Pipeline: Retrieve and Generate
                generated_answer = pipeline.generate_answer(prompt)
                
                # 4. Guardrail: Post-Processing Filter
                # Note: The fallback "I cannot find this information" from pipeline avoids validation errors usually, 
                # but we validate anyway for safety.
                if "sorry i dont know" in generated_answer.lower():
                    response_text = generated_answer
                else:
                    is_valid, error_msg = guard.validate_llm_response(generated_answer)
                    if is_valid:
                        response_text = generated_answer
                    else:
                        # If the LLM hallucinated, broke the 3-sentence rule, or forgot the link/footer
                        response_text = f"An error occurred during response formatting: {error_msg}. Please try asking your question differently."
            
            st.markdown(response_text)
            
    # 5. Save assistant message to UI state
    st.session_state.messages.append({"role": "assistant", "content": response_text})
