import json
from typing import Any, Dict, List, Optional


class Planner:
    def __init__(self, llm):
        self.llm = llm

    def create_plan(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        planning_messages = [
            {
                "role": "system",
                "content": (
                    "You are the planning stage of an AI agent. "
                    "Create a short internal plan for answering the latest user request. "
                    "Mention which tools, if any, should be used. "
                    "Do not answer the user directly."
                )
            },
            *messages,
        ]

        if tools:
            planning_messages.append(
                {
                    "role": "system",
                    "content": (
                        "Available tools:\n"
                        f"{json.dumps(tools, indent=2)}"
                    )
                }
            )

        response = self.llm.chat(planning_messages)
        plan = response.choices[0].message.content

        return plan or "No explicit plan was generated."
