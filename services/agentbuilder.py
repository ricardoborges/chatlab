from llama_stack_client import LlamaStackClient, Agent

class AgentBuilder:
    def __init__(self, base_url):
        self.client = LlamaStackClient(base_url=base_url)

    def build_agent(self, 
                    model="llama3.2:3b", 
                    system_prompt="You are a helpful assistant that can use tools to answer questions.",
                    tools=None):

        self.agent = Agent(
            self.client,
            model=model,
            instructions=system_prompt,
            tools=tools
        )
        
        return self.agent
