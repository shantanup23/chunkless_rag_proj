# chunkless_rag_proj

An experimental RAG (Retrieval-Augmented Generation) setup that skips explicit text chunking. It relies on Gemini's multimodal context window for processing documents and extracting answers.

## Project Structure
- `backend/`: FastAPI server for document processing (uses `docling` and `google-genai`)
- `frontend/`: React + Vite app for the UI

## Getting Started

### Backend
1. `cd backend`
2. `python3 -m venv venv`
3. `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. `cp .env.example .env` and add your Gemini API key
6. `uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Notes
Old experimental scripts and vector DB attempts were removed from the root directory to keep things clean.
