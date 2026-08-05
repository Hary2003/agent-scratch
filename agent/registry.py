from agent.schemas import Tool


class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, tool: Tool, function):
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