from agent.schemas import Tool, ToolParameter


def calculator(operation: str, a: float, b: float) -> float:
    op = operation.lower().strip()
    if op in ["add", "addition", "+"]:
        return a + b
    elif op in ["subtract", "subtraction", "-"]:
        return a - b
    elif op in ["multiply", "multiplication", "*", "x"]:
        return a * b
    elif op in ["divide", "division", "/"]:
        if b == 0:
            raise ValueError("Division by zero.")
        return a / b

    raise ValueError(f"Unknown operation: {operation}")


calculator_tool = Tool(
    name="calculator",
    description="Perform basic arithmetic operations.",
    parameters={
        "operation": ToolParameter(
            type="string",
            description="Operation to perform.",
            enum=["add", "subtract", "multiply", "divide"]
        ),
        "a": ToolParameter(
            type="number",
            description="First number."
        ),
        "b": ToolParameter(
            type="number",
            description="Second number."
        )
    },
    required=[
        "operation",
        "a",
        "b"
    ],
    function=calculator
)
