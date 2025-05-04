from llama_stack_client import LlamaStackClient, Agent
from rich.pretty import pprint
from tools.toolsrepo import ToolsRepository
from dotenv import load_dotenv
import os

class AgentBuilder:
    def __init__(self, base_url, tools_repo: ToolsRepository):
        load_dotenv()
        self.client = LlamaStackClient(
            base_url=base_url,
            provider_data={
                "tavily_search_api_key": os.getenv("TAVILY_SEARCH_API_KEY"),
                "together_api_key": os.getenv("TOGETHER_API_KEY"),
            },            
            )
        self.tools_repo = tools_repo
        self.agent = None
        self.model = None
        self.system_prompt = None
        

    def build_agent(self, 
                    model = "llama3.2:3b", 
                    system_prompt="You are a helpful assistant that can use tools to answer questions."
                    ):

        self.model = model
        self.system_prompt = system_prompt

        print("ATUALIZAÇÃO DE TOOLS")
        pprint(self.tools_repo.active_all())
        
        if ("builtin::websearch" in self.tools_repo.active_all()):
            system_prompt += "\nYou can use the websearch tool to find information online."
            
        print("ATUALIZAÇÃO DE SYSTEM PROMPT")
        print(system_prompt)
            
        self.agent = Agent(
            self.client,
            model=model,
            instructions=system_prompt,
            tools=self.tools_repo.active_all()
        )
        
        return self.agent
