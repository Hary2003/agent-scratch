from typing import Any, Callable, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


# --------------------------------------------------
# Chat Messages
# --------------------------------------------------

class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None


# --------------------------------------------------
# Tool Parameters
# --------------------------------------------------

class ToolParameter(BaseModel):
    type: str
    description: str


# --------------------------------------------------
# Tool Definition
# --------------------------------------------------

class Tool(BaseModel):
    name: str
    description: str

    parameters: Dict[str, ToolParameter]

    required: List[str] = Field(default_factory=list)

    function: Callable[..., Any]

    class Config:
        arbitrary_types_allowed = True

    def to_openai_tool(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        name: {
                            "type": param.type,
                            "description": param.description
                        }
                        for name, param in self.parameters.items()
                    },
                    "required": self.required
                }
            }
        }


# --------------------------------------------------
# Tool Call requested by the LLM
# --------------------------------------------------

class ToolCall(BaseModel):
    id: str
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


# --------------------------------------------------
# Tool Execution Result
# --------------------------------------------------

class ToolResult(BaseModel):
    tool_call_id: str
    tool_name: str
    output: Any


# --------------------------------------------------
# Chat Request
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str


# --------------------------------------------------
# Chat Response
# --------------------------------------------------

class ChatResponse(BaseModel):
    answer: str