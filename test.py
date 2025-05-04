from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client import LlamaStackClient
import os
from dotenv import load_dotenv

load_dotenv()

# Certifique-se de que as chaves estão configuradas corretamente
together_api_key = os.getenv("TOGETHER_API_KEY")
if not together_api_key:
    raise ValueError("TOGETHER_API_KEY is not set in the environment variables.")

client = LlamaStackClient(
    base_url=f"http://127.0.0.1:8321",
    provider_data={
        "tavily_search_api_key": os.getenv("TAVILY_SEARCH_API_KEY"),
        "together_api_key": together_api_key,  # Certifique-se de que a chave está sendo passada
    },
)

#default_model = "llama3.2:3b-instruct-fp16"
default_model = "meta-llama/Llama-3.3-70B-Instruct"

agent = Agent(
    client,
    model=default_model,
    instructions=(
        "You are a web search assistant, must use websearch tool to look up the most current and precise information available. "
    ),
    tools=["builtin::websearch"],
)

session_id = agent.create_session("websearch-session")

response = agent.create_turn(
    messages=[
        {"role": "user", "content": "what was the last game of Bahia team from Brazil in 2025?"}
    ],
    session_id=session_id,
    stream=False,
)

#print(response.steps)
print(response.output_message.content)