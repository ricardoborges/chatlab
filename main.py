import gradio as gr
from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger
from tools.sample import get_temperature
from rich.pretty import pprint

LLAMA_STACK_BASE_URL = "http://127.0.0.1:8321"

client = LlamaStackClient(base_url=LLAMA_STACK_BASE_URL)

#client.toolgroups.unregister("usr::username")

agent = Agent(
    client,
    model="llama3.2:3b",
    instructions="You are a helpful assistant that can use tools to answer questions.",
    tools=[get_temperature]
)

session_id = agent.create_session(session_name="My conversation")

def respond(message, chat_history):
    response = agent.create_turn(
        session_id=session_id,
        messages=[{"role": "user", "content": message}],
        stream=False,
        #toolgroups=["username"] // when using MCP integration
    )

    pprint(response.steps)

    assistant_response = response.output_message.content
    chat_history.append((message, assistant_response))
    
    return "", chat_history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()