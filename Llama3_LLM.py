from dotenv import load_dotenv
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

load_dotenv()

repo_id = "meta-llama/Meta-Llama-3-8B-Instruct"

llama3 = HuggingFaceEndpoint(
    repo_id=repo_id,
    temperature=0.01
    )
