from llama_stack_client import LlamaStackClient
from dotenv import load_dotenv
import os

load_dotenv()

def build_client():
    client = LlamaStackClient(
        base_url="http://localhost:8321",
        provider_data={
            "tavily_search_api_key": os.getenv("TAVILY_SEARCH_API_KEY"),
            "together_api_key": os.getenv("TOGETHER_API_KEY"),
        },           
        )
    return client
