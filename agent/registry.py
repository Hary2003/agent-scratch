from agent.schemas import Tool


class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, tool: Tool, function):
        if tool.name in self.tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")
        if not callable(function):
            raise ValueError(f"Tool '{tool.name}' function must be callable.")

        self.tools[tool.name] = {
            "tool": tool,
            "function": function
        }

    def get(self, name):
        return self.tools.get(name)

    def exists(self, name):
        return name in self.tools

    def list_tools(self):
        return [
            tool["tool"].to_openai_tool()
            for tool in self.tools.values()
        ]
