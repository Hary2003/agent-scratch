# main.py

from agent.memory import Memory
from agent.registry import ToolRegistry
from agent.executor import ToolExecutor
from agent.llm import LLMClient
from agent.agent import Agent

from tools.calculator import calculator, calculator_tool
from tools.current_time import get_current_time, time_tool


def main():
    # Initialize components
    memory = Memory()

    registry = ToolRegistry()
    registry.register(calculator_tool, calculator)
    registry.register(time_tool, get_current_time)

    llm = LLMClient()

    executor = ToolExecutor(registry)

    agent = Agent(
        llm=llm,
        memory=memory,
        registry=registry,
        executor=executor,
    )

    print("=" * 50)
    print("Simple AI Agent")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            response = agent.run(user_input)
            print(f"\nAssistant: {response}")

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()