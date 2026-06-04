# Implementation Plan: Mutual Fund FAQ Assistant

This document outlines the phase-wise implementation strategy to build the facts-only FAQ assistant for the selected Tata Mutual Fund schemes.

## User Review Required
> [!IMPORTANT]
> The UI framework in Phase 4 has been pivoted from a basic Streamlit app to a **React + FastAPI** stack to strictly adhere to the `DESIGN.md` visual specifications. Please review this architectural shift.

## Open Questions
> [!WARNING]
> 1. **Vite/React Setup:** I will initialize the React app in a `frontend` subfolder using Vite, and convert the Python backend to a FastAPI service. Does this folder structure work for you?

---

## Proposed Changes

### Phase 1: Setup & Offline Data Ingestion Pipeline (Pinecone Migration)
**Goal:** Establish the foundational knowledge base using the 5 selected Groww URLs and official documents.
*   **Initialize Project:** Set up the Python virtual environment and core dependencies.
*   **Web Scraper & PDF Parser:** Implement scripts to fetch the Groww URLs, KIM, SID, and Factsheets.
*   **Semantic Chunking:** Implement a text splitter that divides documents logically and attaches metadata (`source_url`, `last_updated_date`, etc.).
*   **Vector Database:** Configure Pinecone Serverless as the vector database, replacing local ChromaDB to avoid OOM memory crashes on Railway. Use `multilingual-e5-large` via Pinecone Inference API for embeddings instead of local HuggingFace models.
*   *Output:* A populated vector database ready for queries.

---

### Phase 2: Core RAG & Generation Pipeline (Serverless Update)
**Goal:** Connect the vector database to the LLM and enforce the strict response constraints.
*   **Retrieval Logic:** Implement Dense search using Pinecone Vector DB (Top-5). Drop the local Cross-Encoder re-ranker to further prevent memory issues on the 500MB Railway free tier container.
*   **Strict Prompt Builder:** Create the system prompt enforcing the 3-sentence limit, single citation requirement, and the "Last updated from sources: <date>" footer.
*   **LLM Integration:** Connect to Groq's high-speed inference engine (e.g., Llama-3-70B) with temperature set to `0.0`.
*   *Output:* A functional backend script that can accurately answer factual queries based *only* on the ingested corpus.

---

### Phase 3: Guardrails & Compliance Layer
**Goal:** Implement the "gatekeeper" to refuse advisory and comparative queries.
*   **Intent Router:** Build a lightweight classifier or regex-based filter to detect trigger words ("Should I", "better", "recommend").
*   **Refusal Handler:** Implement predefined, polite refusal templates directing users to AMFI/SEBI for educational purposes.
*   **Post-Processing Filter:** Add a validation step *after* the LLM generates a response to guarantee the footer and citation are present before returning the answer.
*   *Output:* A secure, compliant backend that gracefully rejects non-factual questions.

---

### Phase 4: Full-Stack UI (React + FastAPI)
**Goal:** Expose the RAG pipeline via a REST API and build a premium React interface following the `DESIGN.md` specifications.

*   **API Layer (FastAPI):** Convert the backend into a FastAPI service (`api.py`) exposing a `/chat` endpoint that integrates the RAG pipeline and guardrails.
*   **React Frontend Setup:** Initialize a modern React application using Vite in a `frontend` directory.
*   **Design Implementation:** Implement the "Modern Corporate Minimalism" aesthetic using Vanilla CSS (Deep Navy, Emerald Green, Inter font, specific elevations and border-radii) as specified in the reference folder.
*   **UI Components:** Build the Chat Interface, including User/Assistant message bubbles, quick-start query chips, and a sticky input field.
*   *Output:* A fully functional, production-like web application where users can interact with the factual assistant.

---

### Phase 5: Automated Scheduler
**Goal:** Implement a scheduling mechanism to automatically update the knowledge base.
*   **Daily Sync:** Configure a task scheduler (like APScheduler, Celery, or cron) to run the data ingestion pipeline.
*   **Vector DB Updates:** Ensure the scheduler updates the vector database without interrupting ongoing queries.
*   *Output:* An automated system that keeps the vector database fresh with the latest Groww URLs and official documents.

---

## Verification Plan

### Automated Tests
*   **Retrieval Tests:** Verify that queries for specific scheme metrics (e.g., exit load) retrieve the correct chunk from the correct document.
*   **Guardrail Tests:** Assert that inputting "Which fund is best?" immediately triggers the Refusal Handler without calling the main LLM.
*   **Constraint Tests:** Programmatically check LLM outputs to ensure they never exceed 3 sentences and always contain exactly one HTTP link.

### Manual Verification
*   Launch the UI and interact with the assistant to evaluate response quality, response time, and refusal gracefulness.
*   Verify the daily scheduler updates the Vector DB when a new document is introduced.
