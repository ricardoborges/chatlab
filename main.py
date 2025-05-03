import uuid
import gradio as gr
from tools.sample import get_temperature
from rich.pretty import pprint
from services.agentbuilder import AgentBuilder
from tools.toolsrepo import ToolsRepository

LLAMA_STACK_BASE_URL = "http://127.0.0.1:8321"

tools_repo = ToolsRepository()
tools_repo.add_tool("get_temperature", get_temperature)

tools = tools_repo.all_tools()

agent = AgentBuilder(LLAMA_STACK_BASE_URL).build_agent(
    tools=tools
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

def new_session():
    global session_id
    new_uuid = str(uuid.uuid4())
    session_id = agent.create_session(session_name=new_uuid)
    return "new session created {new_uuid}"

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Chat"):
            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            clear = gr.Button("Clear")

            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            clear.click(lambda: None, None, chatbot, queue=False)

        with gr.Tab("LLM Settings"):
            api_url = gr.Textbox(label="LLAMA Stack Base URL", value=LLAMA_STACK_BASE_URL)
            
            def update_model(selected_model):
                global agent, session_id
                agent = AgentBuilder(LLAMA_STACK_BASE_URL).build_agent(
                    tools=[get_temperature],
                    model=selected_model
                )
                new_session()
                return f"Modelo alterado para: {selected_model}"

            model_selector = gr.Dropdown(
                choices=[m.identifier for m in agent.client.models.list()] if agent.client.models.list() else ["No models available"],
                label="Model",
                value=next((m.identifier for m in agent.client.models.list() if m.identifier.startswith("llama")), None) if agent.client.models.list() else None,
                interactive=True,
                multiselect=False,
            )

            model_selector.change(update_model, [model_selector], None)

            save_button = gr.Button("Salvar")

            def save_settings(new_url):
                global LLAMA_STACK_BASE_URL, session_id, agent
                LLAMA_STACK_BASE_URL = new_url
                agent = AgentBuilder(LLAMA_STACK_BASE_URL).build_agent(
                    tools=[get_temperature]
                )
                return "Configurações salvas com sucesso!"

            save_button.click(save_settings, [api_url], None)

        #with gr.Tab("Tools"):
            #gr.Markdown("### Active Tools")

            #tools_selector = gr.CheckboxGroup(
            #    choices=[tool for tool in tools_repo.list_tools_names()],
            #    label="Tools",
            #    value=[],
            #    interactive=True,
            #)


demo.launch()