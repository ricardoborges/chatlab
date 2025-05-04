import uuid
import os
import gradio as gr
from tools.sample import get_temperature, get_bitcoin_value
from rich.pretty import pprint
from services.agentbuilder import AgentBuilder
from tools.toolsrepo import ToolsRepository
from dotenv import load_dotenv
load_dotenv()

DEFAULT_STACK = "Together"

def default_model():
    if DEFAULT_STACK == "Together":
        return "meta-llama/Llama-3.3-70B-Instruct"
    else:
        return "llama3.2:3b"

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
TAVILY_SEARCH_API_KEY = os.environ['TAVILY_SEARCH_API_KEY']
LLAMA_STACK_BASE_URL = "http://127.0.0.1:8321"
DEFAULT_MODEL = default_model()


tools_repo = ToolsRepository()
tools_repo.add_tool("get_temperature", get_temperature)
tools_repo.add_tool("get_bitcoin_value", get_bitcoin_value)

agent_builder = AgentBuilder(LLAMA_STACK_BASE_URL, tools_repo)

list = [item.identifier for item in agent_builder.client.toolgroups.list()]

for identifier in list:
    tools_repo.add_tool(identifier, None, builtin=True)

chat_agent = agent_builder.build_agent(model=DEFAULT_MODEL)

def respond(message, chat_history):
    response = chat_agent.create_turn(
        session_id=session_id,
        messages=[{"role": "user", "content": message}],
        stream=False,
        #toolgroups=["username"] // when using MCP integration
    )

    print(f"system_prompt: {agent_builder.system_prompt}")
    print(f"model: {agent_builder.model}")
    print(f"prompt: {message}")
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
            with gr.Row():

                model_selector = gr.Dropdown(
                    choices=[m.identifier for m in chat_agent.client.models.list()] if chat_agent.client.models.list() else ["No models available"],
                    label="Model",
                    value=DEFAULT_MODEL,
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
                return f"Model: {selected_model}"

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

            
        with gr.Tab("Registered Tools"):
            gr.Markdown("### Builtin tools available in llama-stack server")

            builtin_tools_selector = gr.CheckboxGroup(
                choices=[tool for tool in tools_repo.list_builtin_tools_names()],
                label="Tools",
                interactive=True,
            )
            
            savebuiltin_button = gr.Button("Save")
            remove_tool_button = gr.Button("Remove Selected Tool")  # Botão para remover a ferramenta
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

            #TODO: update tool list
            def remove_tool(selected_tool):
                if selected_tool:
                    chat_agent.client.toolgroups.unregister(selected_tool[0])
                    return f"Tool '{selected_tool[0]}' removed successfully."
                return "No tool selected to remove."

            savebuiltin_button.click(update_builtin_tools, [builtin_tools_selector], builtin_confirmation_message)
            remove_tool_button.click(remove_tool, [builtin_tools_selector], builtin_confirmation_message)

        with gr.Tab("MCP"):
            gr.Markdown("### MCP Integration")
            
            # List all tools
            #all_tools = chat_agent.client.tools.list


           # pprint(all_tools())
            
         #   mcp_tools_list = gr.Label(value=", ".join(mcp_list), label="Available MCP Tools")

            with gr.Row():
                mcp_name = gr.Textbox(label="MCP Name", value="mcp::", placeholder="Enter MCP Toolgroup Name")
                mcp_url = gr.Textbox(label="MCP URL", value="http://127.0.0.1:8282/sse", placeholder="Enter MCP Endpoint URL")
                process_mcp_button = gr.Button("Process MCP")   
      
            mcp_output = gr.Label(value="", label="MCP Output")

            #TODO: update tool list
            def process_mcp(mcp_name, mcp_url):
                chat_agent.client.toolgroups.register(
                    toolgroup_id=mcp_name,
                    provider_id="model-context-protocol",
                    mcp_endpoint={"uri":mcp_url}
                )

                # Add logic to process MCP data
                return f"Processed MCP data: {mcp_name}"

            process_mcp_button.click(process_mcp, [mcp_name, mcp_url], mcp_output)


demo.launch()