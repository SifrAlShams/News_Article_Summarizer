import streamlit as st
import time
from langchain_community.document_loaders import WebBaseLoader
from Summarization_with_Updated_Langchain import stuff_chain


def summarize(input_url):
    """Summarizes the article at the provided URL"""

    loader = WebBaseLoader(input_url)
    docs = loader.load()
    return stuff_chain.invoke(docs)["output_text"]


def response_generator(chain_response):
    for word in chain_response.split(" "):
        yield word + " "
        time.sleep(0.02)


st.title("AI News Summarizer")
st.write("You can summarize the articles from following news sites:\n\n"
         "[DAWN News, The News International, The Express Tribune, Radio Pakistan, BBC News, CNN News, Medium, "
         "Langchain]")
url = st.text_input("Enter the URL of the article you want to summarize:")

if st.button("Summarize"):
    if url:
        with st.spinner("Summarizing..."):
            summary = summarize(url)
        st.success("Summary:")
        st.write_stream(response_generator(summary))
    else:
        st.warning("Please enter a valid URL.")
