from agent.schemas import Tool, ToolParameter


def weather(location: str) -> str:
    target = location.strip()
    loc = target.lower()

    weather_data = {
        "trivandrum": "31 degrees C, Sunny",
        "thiruvananthapuram": "31 degrees C, Sunny",
        "kochi": "29 degrees C, Cloudy",
        "cochin": "29 degrees C, Cloudy",
        "kerala": (
            "Kochi: 29 degrees C, Cloudy | "
            "Trivandrum: 31 degrees C, Sunny"
        ),
        "delhi": "38 degrees C, Hot",
        "bangalore": "24 degrees C, Rainy",
        "bengaluru": "24 degrees C, Rainy"
    }

    if loc in weather_data:
        return f"Weather in {target}: {weather_data[loc]}"

    return f"The weather in {target} is currently 28 degrees C, Partly Cloudy."


weather_tool = Tool(
    name="weather",
    description="Get the current weather for a city, state, or country.",
    parameters={
        "location": ToolParameter(
            type="string",
            description="The city, state, or country to get weather for."
        )
    },
    required=[
        "location"
    ],
    function=weather
)
