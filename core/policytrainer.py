from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# I know this is not the best way to handle this, I am doing this because of a time crunch.

def generate_vectordb():
    hf_embedding = HuggingFaceInstructEmbeddings()

    loader = PyPDFLoader("ISM_DA.pdf")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    db = FAISS.from_documents(docs, hf_embedding)
    db.save_local("faiss")
    db = FAISS.load_local("faiss/", embeddings=hf_embedding)
    return db

#as of now this is hardcoded

def search_similar_documents(db, query):
    search = db.similarity_search(query, k=2)
    return search

def load_policy_db():
    #ensure that the db exists
    if not os.path.exists("faiss"):
        generate_vectordb()
    db = FAISS.load_local("faiss/", embeddings=HuggingFaceInstructEmbeddings())
    return db