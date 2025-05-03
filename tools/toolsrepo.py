class ToolItem:
    def __init__(self, name, function):
        self.name = name
        self.function = function
        self.active = False

    def __repr__(self):
        return f"ToolItem(name={self.name}, active={self.active})"

class ToolsRepository:
    def __init__(self):
        self.tools = {}

    def add_tool(self, tool_name, tool_function):
        if callable(tool_function):
            self.tools[tool_name] = ToolItem(name=tool_name, function=tool_function)
        else:
            raise ValueError("The provided tool_function is not callable")

    def get_tool(self, tool_name):
        return self.tools.get(tool_name)

    def list_tools_names(self):
        return list(self.tools.keys())

    def active_tools(self):
        return [tool.function for tool in self.tools.values() if tool.active]

    def update_tool_status(self, tool_name, active):
        if tool_name in self.tools:
            self.tools[tool_name].active = active
        else:
            raise ValueError(f"Tool '{tool_name}' not found in the repository.")