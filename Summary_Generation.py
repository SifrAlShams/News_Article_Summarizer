from langchain.chains.llm import LLMChain
from Llama3_LLM import llama3
from FewShot_Prompting import prompt, article_text

llm_chain = LLMChain(prompt=prompt, llm=llama3)
print(llm_chain.invoke(article_text)['text'])
