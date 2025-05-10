from pydantic import BaseModel
from client import build_client 
from rich.pretty import pprint


client = build_client()

#model_id = "llama3.2:3b"
model_id = "meta-llama/Llama-3.3-70B-Instruct"

class Output(BaseModel):
    name: str
    year_born: str
    year_retired: str


user_input = "Michael Jordan was born in 1963. He played basketball for the Chicago Bulls. He retired in 2003. Extract this information into JSON for me. "
response = client.inference.completion(
    model_id=model_id,
    content=user_input,
    stream=False,
    sampling_params={
        "strategy": {
            "type": "greedy",
        },
        "max_tokens": 50,
    },
    response_format={
        "type": "json_schema",
        "json_schema": Output.model_json_schema(),
    },
)

pprint(Output.model_validate_json(response.content))
