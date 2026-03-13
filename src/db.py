from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

def init_db(pdf_path="content/HR_Policy_2018.pdf", persist_dir="db2"):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
    texts = text_splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma.from_documents(texts, embeddings, persist_directory=persist_dir)
    return db
