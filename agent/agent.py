import json
from agent.schemas import ToolCall


class Agent:

    def __init__(
        self,
        llm,
        memory,
        registry,
        executor,
        planner=None
    ):

        self.llm = llm
        self.memory = memory
        self.registry = registry
        self.executor = executor
        self.planner = planner

        self.memory.add_system(
            "You are a helpful AI assistant."
        )

    def _messages_with_plan(self, plan: str):
        messages = self.memory.to_openai_messages()
        if plan:
            plan_message = {
                "role": "system",
                "content": (
                    "Use this internal plan to guide the next response. "
                    "Do not mention the plan unless the user asks for it.\n\n"
                    f"{plan}"
                )
            }
            insert_at = 1 if messages and messages[0]["role"] == "system" else 0
            messages.insert(insert_at, plan_message)

        return messages

    def run(self, user_message: str):

        # Step 1
        self.memory.add_user(user_message)

        # Step 2
        messages = self.memory.to_openai_messages()

        # Step 3
        tools = self.registry.list_tools()

        # Step 4
        plan = None
        if self.planner:
            plan = self.planner.create_plan(
                messages,
                tools
            )

        # Step 5
        response = self.llm.chat(
            self._messages_with_plan(plan),
            tools
        )

        message = response.choices[0].message

        # Step 6
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

            for tool_call in message.tool_calls:
                raw_args = tool_call.function.arguments or "{}"
                try:
                    args = json.loads(raw_args)
                except json.JSONDecodeError:
                    args = {
                        "_parse_error": (
                            "Tool arguments must be valid JSON."
                        )
                    }
                if not isinstance(args, dict):
                    args = {
                        "_parse_error": (
                            "Tool arguments must be a JSON object."
                        )
                    }

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
                self._messages_with_plan(plan),
                tools
            )

            message = response.choices[0].message

        # Step 7
        self.memory.add_assistant(
            message.content
        )

        return message.content
