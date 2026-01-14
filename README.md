## 1. Install Ollama (WAJIB PERTAMA)

Ollama digunakan sebagai LLM lokal.

Download dan install:
https://ollama.com

Jalankan Ollama service:
```bash
ollama serve
ollama pull llama3


## 2 Install Depedency
pip install -r requirements.txt


## 3 Run Project
python preprocessing.py
python ingest.py
uvicorn api:app --reload
