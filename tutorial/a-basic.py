from client import build_client 
from rich.pretty import pprint
from llama_stack_client import InferenceEventLogger


client = build_client()

#model_id = "llama3.2:3b"
model_id = "meta-llama/Llama-3.3-70B-Instruct"

message = {"role": "user", "content": "Write a paragraph about guitars."}
print(f'User> {message["content"]}')

response = client.inference.chat_completion(
    messages=[message],
    model_id=model_id,
    stream=True,  
)

for log in InferenceEventLogger().log(response):
    log.print()
