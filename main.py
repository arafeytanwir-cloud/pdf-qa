from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import cohere
import tempfile
from pypdf import PdfReader 
from starlette.middleware.sessions import SessionMiddleware 
import uuid 
import markdown 

load_dotenv()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "supersecretkey"))

templates = Jinja2Templates(directory="templates") 

model = cohere.ClientV2(os.getenv("API_KEY")) 

pdf_store: dict[str, str] = {} 

def extract_text(pdf: UploadFile) -> str: 
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp: 
        temp.write(pdf.file.read()) 
        temp_path = temp.name 

    reader = PdfReader(temp_path) 
    text = ""

    for page in reader.pages: 
        if page.extract_text(): 
            text += page.extract_text() + "\n" 

    os.remove(temp_path)
    return text 

def ask_ai(doc_text: str, question: str) -> str: 
    prompt = f"""
    ---SYSTEM PROMPT STARTS---
    You are an AI assistant. Answer the user question based on the following document text.
    
    Document:
    {doc_text}
    
    Question:
    {question}
    
    Provide a clear and concise answer.
    Never return an empty (null) response. 
    ---SYSTEM PROMPT ENDS---
    """
    response = model.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": prompt}],
    ) 
    return response.message.content[0].text.strip()


@app.api_route("/", methods=["GET", "POST"], response_class=HTMLResponse)
async def home(
    request: Request,
    pdf_file: UploadFile = File(None),
    question: str = Form(None),
    discard: str = Form(None),
):

    answer = None
    error = None

    session_id = request.cookies.get("session_id")

    # -------- Discard --------
    if discard:
        if session_id and session_id in pdf_store:
            del pdf_store[session_id]

    # -------- Upload PDF --------
    elif pdf_file and pdf_file.filename:
        text = extract_text(pdf_file)
        if not text:
            error = "Could not extract text from PDF."
        else:
            session_id = str(uuid.uuid4())  # Generate new session ID
            pdf_store[session_id] = text

    # -------- Ask Question --------
    elif question:
        if not session_id or session_id not in pdf_store:
            error = "Upload a PDF first."
        else:
            answer = ask_ai(pdf_store[session_id], question)
            answer = markdown.markdown(answer) 

    pdf_uploaded = bool(session_id and session_id in pdf_store)

    response = templates.TemplateResponse("index.html", {
        "request": request,
        "pdf_uploaded": pdf_uploaded,
        "answer": answer,
        "error": error,
        "question": question,
    })

    # Set the lightweight session ID cookie
    if session_id:
        response.set_cookie("session_id", session_id, httponly=True)

    return response 