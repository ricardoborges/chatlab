from termcolor import cprint
from client import build_client 
from llama_stack_client import Agent, AgentEventLogger


client = build_client()

#model_id = "llama3.2:3b"
model_id = "meta-llama/Llama-3.3-70B-Instruct"


agent = Agent(
    client, 
    model=model_id,
    instructions="You are a helpful assistant. Use websearch tool to help answer questions.",
    tools=["builtin::websearch"],
)
user_prompts = [
    "Hello",
    "Which teams played in the NBA western conference finals of 2024",
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
    )
    for log in AgentEventLogger().log(response):
        log.print()