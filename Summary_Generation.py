from langchain.chains.llm import LLMChain
from utils.import_llama3 import llama3
from summarization_prompt import prompt, article_text

llm_chain = LLMChain(prompt=prompt, llm=llama3)
print(llm_chain.invoke(article_text)['text'])
