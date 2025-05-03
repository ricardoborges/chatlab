class ToolItem:
    def __init__(self, name, function, builtin=False):
        self.name = name
        self.function = function
        self.active = False
        self.builtin = builtin

    def __repr__(self):
        return f"ToolItem(name={self.name}, active={self.active}, builtin={self.builtin})"

class ToolsRepository:
    def __init__(self):
        self.tools = {}

    def add_tool(self, tool_name, tool_function, builtin=False):
        if not builtin and not callable(tool_function):
            raise ValueError("The provided tool_function is not callable")

        self.tools[tool_name] = ToolItem(name=tool_name, function=tool_function, builtin=builtin)

    def get_tool(self, tool_name):
        return self.tools.get(tool_name)

    def list_tools_names(self):
        return [tool.name for tool in self.tools.values() if not tool.builtin]

    def list_builtin_tools_names(self):
        return [tool.name for tool in self.tools.values() if tool.builtin]

    def active_all(self):
        return [
            tool.function if not tool.builtin else tool.name
            for tool in self.tools.values() if tool.active
        ]
    
    def builtin_tools(self):
        return [tool.name for tool in self.tools.values() if tool.active and tool.builtin]

    def update_tool_status(self, tool_name, active):
        if tool_name in self.tools:
            self.tools[tool_name].active = active
        else:
            raise ValueError(f"Tool '{tool_name}' not found in the repository.")