import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV=os.getenv("PINECONE_ENV")
PINECONE_INDEX=os.getenv("PINECONE_INDEX")


docs1 = PyPDFLoader("data/lets talk money.pdf").load()
docs2 = PyPDFLoader("data/FAME202426022024.pdf").load()
docs3 = PyPDFLoader("data/lets-talk-mutual-funds.pdf").load()
docs4 = PyPDFLoader("data/The Psychology of Money PDF.pdf").load()
docs5 = PyPDFLoader("data/book.pdf").load()
docs6 = PyPDFLoader("data/cashflow1.pdf").load()



print("Documents Loaded!")



for doc in docs1:
    doc.metadata["source"] = "Lets Talk Money"

for doc in docs2:
    doc.metadata["source"] = "FAME Government Policy"

for doc in docs3:
    doc.metadata["source"] = "Lets Talk Mutual Funds"

for doc in docs4:
    doc.metadata["source"] = "The Psychology of Moneyr"

for doc in docs5:
    doc.metadata["source"] = "book"

for doc in docs6:
    doc.metadata["source"] = "cash flow"





final_doc = docs1 + docs2 + docs3 + docs4 + docs5 + docs6

print("Total pages loaded:", len(final_doc))


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = splitter.split_documents(final_doc)

print("Total chunks created:", len(chunks))


embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

print("Embedding model ready!")


pc = Pinecone(api_key=PINECONE_API_KEY)


vectorstore = PineconeVectorStore.from_documents(
    chunks,
    embeddings,
    index_name=PINECONE_INDEX
)


print("Data Ingestion Over ")




