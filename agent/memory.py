from agent.schemas import Message


class Memory:
    def __init__(self):
        self.messages: list[Message] = []

    def add_system(self, content: str) -> None:
        self.messages.append(
            Message(
                role="system",
                content=content
            )
        )

    def add_user(self, content: str) -> None:
        self.messages.append(
            Message(
                role="user",
                content=content
            )
        )

    def add_assistant(self, content: str = None, tool_calls: list = None) -> None:
        self.messages.append(
            Message(
                role="assistant",
                content=content,
                tool_calls=tool_calls
            )
        )

    def add_tool(self, tool_call_id: str, result: str) -> None:
        self.messages.append(
            Message(
                role="tool",
                content=str(result),
                tool_call_id=tool_call_id
            )
        )

    def get_messages(self) -> list[Message]:
        return self.messages.copy()

    def clear(self) -> None:
        self.messages.clear()

    def to_openai_messages(self):

        return [
            message.model_dump(exclude_none=True)
            for message in self.messages
        ]