# 📄 PDF Q&A — Document Intelligence

Upload a PDF and ask questions about it. Powered by Cohere's Command model.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-Deployed-9B4DCA?style=for-the-badge&logo=railway)
![Cohere](https://img.shields.io/badge/Cohere-Command%20A-FF7A59?style=for-the-badge)

---
**🚀 Live Demo:** [https://pdf-qa-production.up.railway.app/](https://pdf-qa-production.up.railway.app/)

Upload a PDF and ask questions about it. Powered by Cohere's Command model.

## ✨ Features

- Upload any PDF and extract its text
- Ask natural language questions about the document
- AI-generated answers rendered as formatted markdown
- Session-based document memory — no login required

## 🛠️ Tech Stack

- **Backend:** FastAPI, Uvicorn
- **AI:** Cohere API (`command-a-03-2025`)
- **PDF Parsing:** PyPDF
- **Templating:** Jinja2
- **Sessions:** Starlette session middleware
- **Hosting:** Railway

## ⚙️ How It Works

1. User uploads a PDF — text is extracted page by page using PyPDF.
2. A session ID is assigned and the document text is stored in memory.
3. User submits a question — it's sent to Cohere along with the document as context.
4. The response is rendered as formatted markdown in the browser.

---

## Getting Started Locally

### 1. Clone the repo

```bash
git clone https://github.com/arafeytanwir-cloud/pdf-qa.git
cd pdf-qa
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a `.env` file in the root directory:

```
API_KEY=your_cohere_api_key_here
```

Get a free API key at [cohere.com](https://cohere.com)

### 5. Run the app

```bash
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## How It Works

1. User uploads a PDF — text is extracted page by page using PyPDF
2. A session ID is assigned and the document text is stored in memory
3. User submits a question — it's sent to Cohere along with the document as context
4. The response is rendered as formatted markdown in the browser
