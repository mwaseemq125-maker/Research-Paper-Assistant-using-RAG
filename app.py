import os
import shutil
import math
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pypdf import PdfReader
import pdfplumber
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

app = FastAPI(title="Research Paper Assistant")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

documents = []


def extract_pdf(path):
    pages = []

    try:
        reader = PdfReader(str(path))

        for number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if text.strip():
                pages.append({
                    "text": text,
                    "page": number,
                    "source": path.name
                })

    except Exception:
        pass

    # PDFplumber fallback / additional extraction
    if not pages:
        try:
            with pdfplumber.open(path) as pdf:
                for number, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text() or ""

                    if text.strip():
                        pages.append({
                            "text": text,
                            "page": number,
                            "source": path.name
                        })
        except Exception:
            pass

    return pages


def chunk_text(text, size=1200):
    words = text.split()
    chunks = []

    for i in range(0, len(words), size // 5):
        chunk = " ".join(words[i:i + size // 5])

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def similarity(question, text):
    q_words = set(question.lower().split())
    t_words = set(text.lower().split())

    if not q_words:
        return 0

    common = q_words.intersection(t_words)

    return len(common) / math.sqrt(len(q_words) * max(len(t_words), 1))


def retrieve(question, top_k=5):
    results = []

    for doc in documents:
        for page in doc["pages"]:
            for chunk in chunk_text(page["text"]):
                score = similarity(question, chunk)

                results.append({
                    "score": score,
                    "text": chunk,
                    "source": page["source"],
                    "page": page["page"]
                })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]


def generate_answer(question, contexts):
    if not contexts or contexts[0]["score"] == 0:
        return (
            "Information not found in the uploaded research papers.",
            []
        )

    context_text = "\n\n".join(
        f"[Source: {c['source']}, Page: {c['page']}]\n{c['text']}"
        for c in contexts
    )

    prompt = f"""
You are a Research Paper Assistant.

IMPORTANT RULES:
1. Answer ONLY using the provided research paper context.
2. Do not use outside knowledge.
3. Do not invent facts.
4. If the answer is not available in the context, say exactly:
"Information not found in the uploaded research papers."
5. Give a clear and concise answer.

RESEARCH PAPER CONTEXT:
{context_text}

USER QUESTION:
{question}
"""

    if not API_KEY:
        return (
            "Gemini API key is not configured. Please add GEMINI_API_KEY to .env.",
            contexts
        )

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        return response.text, contexts

    except Exception as e:
        return f"AI error: {str(e)}", contexts


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html"
    )

@app.post("/upload")
async def upload(files: list[UploadFile] = File(...)):
    uploaded = []

    for file in files:

        if not file.filename.lower().endswith(".pdf"):
            continue

        safe_name = Path(file.filename).name
        path = UPLOAD_DIR / safe_name

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        pages = extract_pdf(path)

        if pages:
            documents.append({
                "name": safe_name,
                "pages": pages
            })

            uploaded.append(safe_name)

    return {
        "success": True,
        "uploaded": uploaded,
        "total_documents": len(documents)
    }


@app.post("/chat")
async def chat(question: str = Form(...)):
    question = question.strip()

    if not question:
        return JSONResponse(
            {"answer": "Please enter a question.", "sources": []},
            status_code=400
        )

    if not documents:
        return {
            "answer": "Please upload at least one research paper first.",
            "sources": []
        }

    contexts = retrieve(question)
    answer, sources = generate_answer(question, contexts)

    unique_sources = []
    seen = set()

    for source in sources:
        key = (source["source"], source["page"])

        if key not in seen:
            seen.add(key)

            unique_sources.append({
                "source": source["source"],
                "page": source["page"]
            })

    return {
        "answer": answer,
        "sources": unique_sources
    }


@app.get("/documents")
async def get_documents():
    return {
        "documents": [doc["name"] for doc in documents]
    }


@app.delete("/documents")
async def clear_documents():
    documents.clear()

    for file in UPLOAD_DIR.glob("*.pdf"):
        file.unlink(missing_ok=True)

    return {"success": True}