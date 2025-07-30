import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from langchain_community.document_loaders import WebBaseLoader
from summarization_chain import summarization_chain


app = FastAPI()

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URLRequest(BaseModel):
    url: str


@app.post("/summarize/")
def summarize(request: URLRequest):
    """Summarizes the article at the provided URL"""
    input_url = request.url
    # loader = WebBaseLoader(input_url)
    # docs = loader.load()
    loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
    docs = loader.load()
    
    response = summarization_chain(docs)
    return {"summary": response}
