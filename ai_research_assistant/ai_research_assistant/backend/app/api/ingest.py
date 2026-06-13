# backend/app/api/ingest.py
"""API route for document ingestion."""
from fastapi import APIRouter, HTTPException, UploadFile, File
import io
from pypdf import PdfReader
from app.models.schemas import DocumentIngest
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

@router.post("/document")
async def ingest_doc(request: DocumentIngest):
    """Ingest a document into the RAG store."""
    try:
        await rag_service.ingest_document(request.text, request.metadata)
        return {"status": "success", "message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and ingest a PDF document."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        content = await file.read()
        pdf_reader = PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
        if not text.strip():
            raise ValueError("No extractable text found in the PDF.")
            
        metadata = {"title": file.filename, "source_type": "upload"}
        await rag_service.ingest_document(text, metadata)
        return {"status": "success", "message": f"Successfully processed {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
