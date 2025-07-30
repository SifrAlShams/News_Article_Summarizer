from dotenv import load_dotenv
load_dotenv()

from langchain_nebius import ChatNebius



llama3 = ChatNebius(
    model="meta-llama/Llama-3.3-70B-Instruct-fast"
)

