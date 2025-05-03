from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger
from termcolor import cprint
from rich.pretty import pprint

client = LlamaStackClient(base_url="http://127.0.0.1:8321")

agent = Agent(
    client, 
    model="llama3.2:3b",
    instructions="You are a helpful assistant. Use websearch tool to help answer questions.",
    tools=["builtin::websearch"],
)
user_prompts = [
    "oi",
    "qual foi o ultimo jogo do bahia no campeonato brasileiro de 2025?",
]

session_id = agent.create_session("test-session")
for prompt in user_prompts:
    cprint(f"User> {prompt}", "green")
    response = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        session_id=session_id,
        stream=False,
    )
    
    pprint(response.steps)
    
    print(f"Assistant> {response.output_message.content}")