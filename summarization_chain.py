from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate

from utils.import_llama3 import llama3



def summarization_chain(docs):
    llm = llama3

    context = docs
    print(type(docs))
    print(f"Context to LLM:\n{context[:500]}")

    template = """Write a concise summary of the following text delimited by triple backquotes.Return your response in 
    bullet points which covers the key points of the text. 
    ```{context}``` 
    BULLET POINT SUMMARY:"""

    prompt = PromptTemplate(template=template, input_variables=["context"])

    chain = create_stuff_documents_chain(llm, prompt)
    print(f"Docs: {docs}")
    result = chain.invoke({"context": context})
    return result