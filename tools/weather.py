from agent.schemas import Tool, ToolParameter


def weather(location: str = None, city: str = None) -> str:
    target = location or city or "Unknown"
    loc = target.strip().lower()

    weather_data = {
        "trivandrum": "31°C, Sunny",
        "thiruvananthapuram": "31°C, Sunny",
        "kochi": "29°C, Cloudy",
        "cochin": "29°C, Cloudy",
        "kerala": "Kochi: 29°C, Cloudy | Trivandrum: 31°C, Sunny",
        "delhi": "38°C, Hot",
        "bangalore": "24°C, Rainy",
        "bengaluru": "24°C, Rainy"
    }

    if loc in weather_data:
        return f"Weather in {target}: {weather_data[loc]}"

    return weather_data.get(
        target,
        f"The weather in {target} is currently 28°C, Partly Cloudy."
    )


weather_tool = Tool(
    name="weather",
    description="Get the current weather for a location (city, state, or country).",
    parameters={
        "location": ToolParameter(
            type="string",
            description="The location (city, state, or country) to get weather for."
        )
    },
    required=[
        "location"
    ],
    function=weather
)