from datetime import datetime
from agent.schemas import Tool


def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


time_tool = Tool(
    name="get_current_time",
    description="Get the current local date and time.",
    parameters={},
    required=[],
    function=get_current_time
)
