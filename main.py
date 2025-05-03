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


list = [item.identifier for item in chat_agent.client.toolgroups.list()]

for identifier in list:
    tools_repo.add_tool(identifier, None, builtin=True)

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
            
        with gr.Tab("Custom Tools"):
            gr.Markdown("### Custom tools available")

            list = [item.identifier for item in chat_agent.client.toolgroups.list()]

            tools_selector = gr.CheckboxGroup(
                choices=[tool for tool in tools_repo.list_tools_names()],
                label="Tools",
                interactive=True,
            )
            
            savetools_button = gr.Button("Save")
            confirmation_message = gr.Label(value="", label="")  # Componente para exibir a mensagem

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
                
                return f"Tools activated: {', '.join(selected_tools)}"

            savetools_button.click(update_tools, [tools_selector], confirmation_message)  # Atualiza a mensagem

            
        with gr.Tab("Builtin Tools"):
            gr.Markdown("### Builtin tools available in llama-stack server")

            builtin_tools_selector = gr.CheckboxGroup(
                choices=[tool for tool in tools_repo.list_builtin_tools_names()],
                label="Tools",
                interactive=True,
            )
            
            savebuiltin_button = gr.Button("Save")
            builtin_confirmation_message = gr.Label(value="", label="")  # Componente para exibir a mensagem

            def update_builtin_tools(selected_tools):
                for tool_name in tools_repo.list_builtin_tools_names():
                    if tool_name in selected_tools:
                        tools_repo.update_tool_status(tool_name, active=True)
                    else:
                        tools_repo.update_tool_status(tool_name, active=False)
                        
                global chat_agent, session_id
                chat_agent = AgentBuilder(LLAMA_STACK_BASE_URL, tools_repo).build_agent(
                    model=model_selector.value
                )
            
                session_id = new_session()
                
                return f"Builtin Tools activated: {', '.join(selected_tools)}"
                
            savebuiltin_button.click(update_builtin_tools, [builtin_tools_selector], builtin_confirmation_message)  # Atualiza a mensagem


demo.launch()