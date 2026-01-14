from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import PromptTemplate

PERSIST_DIR = "vector_db"

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.2
)

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

db = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=embeddings
)

retriever = db.as_retriever(search_kwargs={"k": 4})

PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Kamu adalah IT Support internal perusahaan.

Tugas kamu:
- Jawab pertanyaan user secara LANGSUNG dan JELAS berdasarkan email internal.
- Jangan menyebut "email", "dokumen", atau "dataset".
- Jangan memberi opsi pilihan email.

Context:
{context}

Pertanyaan:
{question}

Jawaban:
"""
)

def ask(question: str) -> str:
    docs = retriever.invoke(question)

    if not docs:
        return "Maaf, saya tidak menemukan informasi yang relevan."

    context = "\n\n".join([d.page_content for d in docs])

    prompt = PROMPT.format(
        context=context,
        question=question
    )

    return llm.invoke(prompt)
