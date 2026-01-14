import os
import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

DATASET = "Dataset/clean_emails.csv"        # ganti sesuai nama file
PERSIST_DIR = "vector_db"

df = pd.read_csv(DATASET)

docs = []

for _, row in df.iterrows():
    text = f"""
Error Type: {row['error_type']}

Subject:
{row['subject_clean']}

Body:
{row['body_clean']}

Source: {row['source']}
"""

    if text.strip():
        docs.append(
            Document(
                page_content=text,
                metadata={
                    "error_type": row["error_type"],
                    "source": row["source"]
                }
            )
        )

print(f"📧 Email masuk: {len(docs)}")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

db = Chroma.from_documents(
    docs,
    embedding=embeddings,
    persist_directory=PERSIST_DIR
)

print("✅ Vector DB berhasil dibuat")
