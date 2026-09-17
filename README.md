# 📚 Research Paper Assistant using RAG

A professional **Research Paper Assistant** built with **Python, FastAPI, PyPDF, PDFplumber, and Google Gemini**.

The application allows users to upload one or multiple research papers in PDF format and ask questions about them. The system retrieves relevant content from the uploaded documents before generating an answer using an LLM.

## 🚀 Features

* 📄 Upload one or multiple research papers
* 🔍 Extract text from PDF documents
* 📑 Track document page numbers
* 🧩 Split documents into searchable chunks
* 🔎 Retrieve relevant context using text similarity
* 🤖 Generate answers using Google Gemini
* 💬 Interactive chat interface
* 📚 Display source document name
* 📄 Display source page number
* 🚫 Answers are restricted to uploaded documents
* ⚠️ Handles empty questions
* ⚠️ Handles no uploaded documents
* ⚠️ Handles unsupported file formats

---

## 🧠 How RAG Works

The application follows a Retrieval-Augmented Generation workflow:

```text
Upload Research Papers
        ↓
PDF Text Extraction
(PyPDF / PDFplumber)
        ↓
Text Chunking
        ↓
Relevant Context Retrieval
        ↓
Google Gemini LLM
        ↓
Document-Based Answer
        ↓
Source PDF + Page Number
```

The LLM receives context retrieved from the uploaded papers and is instructed not to use outside knowledge.

If the required information is not available, the application responds:

```text
Information not found in the uploaded research papers.
```

---

## 🛠️ Technologies Used

| Technology          | Purpose                 |
| ------------------- | ----------------------- |
| Python              | Programming language    |
| FastAPI             | Backend web framework   |
| PyPDF               | PDF text extraction     |
| PDFplumber          | PDF extraction fallback |
| Google Gemini       | Large Language Model    |
| HTML/CSS/JavaScript | Frontend                |
| Jinja2              | HTML templates          |
| python-dotenv       | Environment variables   |

---

## 📁 Project Structure

```text
research-paper-assistant/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── uploads/
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── app.js
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

```bash
cd research-paper-assistant
```

## 2. Create virtual environment

### Linux / Ubuntu

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Gemini API Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Replace `YOUR_GEMINI_API_KEY` with your Google Gemini API key.

**Do not upload the `.env` file to GitHub.**

---

# ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

Open your browser and visit:

```text
http://127.0.0.1:8000
```

---

# 💬 Example Questions

After uploading a research paper, users can ask:

### Summary

```text
Summarize this paper.
```

### Problem

```text
What problem does this paper solve?
```

### Methodology

```text
What methodology is used?
```

### Dataset

```text
What datasets are used?
```

### Algorithms

```text
What algorithms are used?
```

### Findings

```text
What are the key findings?
```

### Limitations

```text
What limitations are mentioned?
```

### Future Work

```text
What future work is suggested?
```

---

# 📚 Source Attribution

Each generated answer can include source information such as:

```text
Sources:

📄 research_paper.pdf — Page 5
📄 research_paper.pdf — Page 7
```

This helps users identify where the retrieved information came from.

---

# 🛡️ Document-Only Answering

The assistant is specifically instructed to answer only from the retrieved content of uploaded research papers.

For example, if a user asks a question whose answer is not present in the uploaded documents, the application returns:

```text
Information not found in the uploaded research papers.
```

This prevents the assistant from intentionally relying on external knowledge for unsupported questions.

---

# ⚠️ Error Handling

The application handles several common cases.

### No document uploaded

```text
Please upload at least one research paper first.
```

### Empty question

```text
Please enter a question.
```

### Unsupported file

Only PDF files are accepted.

### Missing API key

```text
Gemini API key is not configured.
```

---

# 🔌 API Endpoints

## Home

```text
GET /
```

Displays the Research Paper Assistant interface.

## Upload Documents

```text
POST /upload
```

Uploads one or multiple PDF research papers.

## Ask Question

```text
POST /chat
```

Retrieves relevant document context and generates an answer.

## Get Documents

```text
GET /documents
```

Returns the currently uploaded documents.

## Clear Documents

```text
DELETE /documents
```

Removes uploaded documents from the current application session.

---

# 🎯 Assignment Requirements

This project implements the required functionality:

* [x] Python
* [x] FastAPI
* [x] PyPDF
* [x] PDFplumber
* [x] Gemini LLM
* [x] Multiple PDF upload
* [x] Chat interface
* [x] Retrieval before generation
* [x] Source document name
* [x] Page number
* [x] Empty question handling
* [x] No-document handling
* [x] Unsupported file handling
* [x] Document-only answering

---

# 👩‍💻 Project Purpose

The purpose of this project is to demonstrate how **Retrieval-Augmented Generation (RAG)** can be used to build a question-answering system over research papers.

Instead of asking the language model to answer from its general knowledge, the application first retrieves relevant information from the uploaded documents and then uses that information to generate the response.

---

## 📌 Future Improvements

Possible future improvements include:

* Vector database integration
* Semantic embeddings
* FAISS/Chroma integration
* Better document chunking
* Conversation history
* User authentication
* Research paper summaries
* Highlighting relevant PDF passages
* Multiple LLM provider support
* Persistent document storage

---

## 📜 License

This project is created for educational and portfolio purposes.

````

**Abhi jaldi se save karein:** `README.md` project ke **root folder** mein hona chahiye, yani `app.py` ke saath.

Phir terminal:

```bash
git add .
git commit -m "Add Research Paper Assistant RAG"
git push
````

**`.env` ko GitHub par bilkul push na karein.**
