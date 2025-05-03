import uuid
import gradio as gr
from tools.sample import get_temperature, get_bitcoin_value
from rich.pretty import pprint
from services.agentbuilder import AgentBuilder
from tools.toolsrepo import ToolsRepository

LLAMA_STACK_BASE_URL = "http://127.0.0.1:8321"
DEFAULT_MODEL = "llama3.2:3b"

tools_repo = ToolsRepository()
tools_repo.add_tool("get_temperature", get_temperature)
tools_repo.add_tool("get_bitcoin_value", get_bitcoin_value)

chat_agent = AgentBuilder(LLAMA_STACK_BASE_URL, tools_repo).build_agent(model=DEFAULT_MODEL)

def respond(message, chat_history):
    response = chat_agent.create_turn(
        session_id=session_id,
        messages=[{"role": "user", "content": message}],
        stream=False,
        #toolgroups=["username"] // when using MCP integration
    )

    pprint(response.steps)

    assistant_response = response.output_message.content
    chat_history.append((message, assistant_response))
    
    return "", chat_history

def new_session():
    new_uuid = str(uuid.uuid4())
    return chat_agent.create_session(session_name=new_uuid)

session_id = new_session()

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab(f"Chat"):
            model_selector = gr.Dropdown(
                choices=[m.identifier for m in chat_agent.client.models.list()] if chat_agent.client.models.list() else ["No models available"],
                label="Model",
                value=next((m.identifier for m in chat_agent.client.models.list() if m.identifier.startswith("llama")), None) if chat_agent.client.models.list() else None,
                interactive=True,
                multiselect=False,
            )
            
            chatbot = gr.Chatbot(type="tuples")
            msg = gr.Textbox()
            clear = gr.Button("Clear")

            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            clear.click(lambda: None, None, chatbot, queue=False)
            
              
            def update_model(selected_model):
                global chat_agent, session_id
                chat_agent = AgentBuilder(LLAMA_STACK_BASE_URL, tools_repo).build_agent(model=selected_model)
                session_id = new_session()
                return f"Modelo alterado para: {selected_model}"


            model_selector.change(update_model, [model_selector], None)
            
        with gr.Tab("Tools"):
            gr.Markdown("### Active Tools")

            tools_selector = gr.CheckboxGroup(
                choices=[tool for tool in tools_repo.list_tools_names()],
                label="Tools",
                interactive=True,
            )
            
            savetools_button = gr.Button("Save")

            def update_tools(selected_tools):
                for tool_name in tools_repo.list_tools_names():
                    if tool_name in selected_tools:
                        tools_repo.update_tool_status(tool_name, active=True)
                    else:
                        tools_repo.update_tool_status(tool_name, active=False)
                        
                global chat_agent, session_id
                chat_agent = AgentBuilder(LLAMA_STACK_BASE_URL, tools_repo).build_agent(
                    model=model_selector.value
                    )
                
                session_id = new_session()
                
                return f"Tools updated: {', '.join(selected_tools)}"

            savetools_button.click(update_tools, [tools_selector], None)


demo.launch()