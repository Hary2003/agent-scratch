import json
from agent.schemas import ToolCall


class Agent:

    def __init__(
        self,
        llm,
        memory,
        registry,
        executor
    ):

        self.llm = llm
        self.memory = memory
        self.registry = registry
        self.executor = executor

        self.memory.add_system(
            "You are a helpful AI assistant."
        )

    def run(self, user_message: str):

        # Step 1
        self.memory.add_user(user_message)

        # Step 2
        messages = self.memory.to_openai_messages()

        # Step 3
        tools = self.registry.list_tools()

        # Step 4
        response = self.llm.chat(
            messages,
            tools
        )

        message = response.choices[0].message

        # Step 5
        while message.tool_calls:
            tool_calls_data = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
            self.memory.add_assistant(content=message.content, tool_calls=tool_calls_data)

            tool_call = message.tool_calls[0]

            raw_args = tool_call.function.arguments or "{}"
            try:
                args = json.loads(raw_args)
            except Exception:
                try:
                    args = eval(raw_args)
                except Exception:
                    args = {}
            if not isinstance(args, dict):
                args = {}

            tool_request = ToolCall(
                id=tool_call.id,
                name=tool_call.function.name,
                arguments=args
            )

            tool_result = self.executor.execute(
                tool_request
            )

            self.memory.add_tool(
                tool_result.tool_call_id,
                str(tool_result.output)
            )

            response = self.llm.chat(
                self.memory.to_openai_messages(),
                tools
            )

            message = response.choices[0].message

        # Step 6
        self.memory.add_assistant(
            message.content
        )

        return message.content