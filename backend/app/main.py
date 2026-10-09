from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
from .database import init_db, save_document, get_document
from .parser import parse_pdf
from .schemas import GenerateTestRequest
from .generator import generate_mock_test

app = FastAPI(title="Chunkless RAG Mock Test Generator")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

MAX_FILE_SIZE = 5 * 1024 * 1024 # 5 MB

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Read file content and check size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit")
        
    doc_id = str(uuid.uuid4())
    temp_pdf_path = f"/tmp/{doc_id}.pdf"
    
    try:
        with open(temp_pdf_path, "wb") as f:
            f.write(content)
            
        # Parse the PDF using Docling
        markdown_content = parse_pdf(temp_pdf_path, doc_id)
        
        # Save to SQLite
        save_document(doc_id, file.filename, markdown_content)
        
        return {
            "doc_id": doc_id,
            "filename": file.filename,
            "status": "parsed"
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error parsing PDF: {str(e)}")
    finally:
        # Clean up temporary PDF file
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

@app.post("/api/generate-test")
async def generate_test(request: GenerateTestRequest):
    # Lookup document
    doc_data = get_document(request.doc_id)
    if not doc_data:
        raise HTTPException(status_code=404, detail="DOCUMENT_NOT_FOUND: Session expired or invalid doc_id. Please re-upload your syllabus.")
    
    try:
        # Generate the test
        payload = generate_mock_test(
            markdown_content=doc_data["markdown_content"],
            topic_prompt=request.topic_prompt,
            doc_id=request.doc_id,
            chat_history=request.chat_history
        )
        return payload.model_dump()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating test: {str(e)}")
