class ToolsRepository:
    def __init__(self):
        self.tools = {}

    def add_tool(self, tool_name, tool_function):
        if callable(tool_function):
            self.tools[tool_name] = tool_function
        else:
            raise ValueError("not a python function")

    def get_tool(self, tool_name):
        return self.tools.get(tool_name)

    def list_tools_names(self):
        return list(self.tools.keys())

    def all_tools(self):
        return list(self.tools.values())  