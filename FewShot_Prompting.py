from langchain_core.prompts import PromptTemplate
from Article_Scrapping import article

article_title = article.title
article_text = article.text

template = """Write a concise summary of the following text delimited by triple backquotes.Return your response in 
bullet points which covers the key points of the text. 
```{text}``` 
BULLET POINT SUMMARY:"""

prompt = PromptTemplate(template=template, input_variables=["text"])
