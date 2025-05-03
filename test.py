from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client import LlamaStackClient
import os
from dotenv import load_dotenv
load_dotenv


client = LlamaStackClient(
    base_url=f"http://127.0.0.1:8321",
    provider_data={
        "tavily_search_api_key": os.getenv("TAVILY_SEARCH_API_KEY")
    },  # Set this from the client side. No need to provide it if it has already been configured on the Llama Stack server.
)

agent = Agent(
    client,
    model="llama3.2:3b",
    instructions=(
        "You are a web search assistant, must use websearch tool to look up the most current and precise information available. "
    ),
    tools=["builtin::websearch"],
    
)

session_id = agent.create_session("websearch-session")

response = agent.create_turn(
    messages=[
        {"role": "user", "content": "How did the USA perform in the last Olympics?"}
    ],
    session_id=session_id,
    toolgroups=["builtin::websearch"],
    stream=False,
)
    
print(response.steps)

print(response.output_message.content)