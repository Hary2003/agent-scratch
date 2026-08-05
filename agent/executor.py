from agent.schemas import ToolCall, ToolResult


class ToolExecutor:

    def __init__(self, registry):
        self.registry = registry

    def execute(
        self,
        tool_call: ToolCall
    ) -> ToolResult:

        tool_info = self.registry.get(tool_call.name)

        if tool_info is None:

            return ToolResult(
                tool_call_id=tool_call.id,
                tool_name=tool_call.name,
                output=f"Unknown tool '{tool_call.name}'."
            )

        tool_fn = tool_info["function"]

        try:

            result = tool_fn(
                **tool_call.arguments
            )

            return ToolResult(
                tool_call_id=tool_call.id,
                tool_name=tool_call.name,
                output=result
            )

        except Exception as e:

            return ToolResult(
                tool_call_id=tool_call.id,
                tool_name=tool_call.name,
                output=f"Tool execution failed: {e}"
            )