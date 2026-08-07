import json
import urllib.parse
import urllib.request
from typing import Optional, Dict, Any
from agent.schemas import Tool, ToolParameter

WMO_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

# Fallback offline dictionary for common cities in case of network issues
FALLBACK_WEATHER = {
    "trivandrum": "31°C, Sunny",
    "thiruvananthapuram": "31°C, Sunny",
    "kochi": "29°C, Cloudy",
    "cochin": "29°C, Cloudy",
    "kerala": "Kochi: 29°C, Cloudy | Trivandrum: 31°C, Sunny",
    "delhi": "38°C, Hot",
    "bangalore": "24°C, Rainy",
    "bengaluru": "24°C, Rainy"
}


def _http_get_json(url: str, timeout: int = 5) -> Dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "WeatherAgent/1.0 (Python)"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        data = response.read().decode("utf-8")
        return json.loads(data)


def weather(location: str, unit: str = "celsius") -> str:
    target = location.strip()
    if not target:
        return "Error: Location cannot be empty."

    unit_clean = unit.lower().strip() if unit else "celsius"
    if unit_clean not in ["celsius", "fahrenheit"]:
        unit_clean = "celsius"

    temp_unit_param = "fahrenheit" if unit_clean == "fahrenheit" else "celsius"
    unit_symbol = "°F" if unit_clean == "fahrenheit" else "°C"

    try:
        # Step 1: Geocoding search for location
        encoded_loc = urllib.parse.quote(target)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_loc}&count=1&language=en&format=json"
        geo_data = _http_get_json(geo_url)

        results = geo_data.get("results", [])
        if not results:
            # Check fallback offline dictionary if available
            loc_key = target.lower()
            if loc_key in FALLBACK_WEATHER:
                return f"Weather in {target}: {FALLBACK_WEATHER[loc_key]} (Offline Fallback)"
            return f"Location '{target}' not found. Please verify the city or country name."

        loc_info = results[0]
        lat = loc_info["latitude"]
        lon = loc_info["longitude"]
        city_name = loc_info.get("name", target)
        admin1 = loc_info.get("admin1", "")
        country = loc_info.get("country", "")

        display_location = city_name
        location_parts = [city_name]
        if admin1 and admin1 != city_name:
            location_parts.append(admin1)
        if country:
            location_parts.append(country)
        display_location = ", ".join(location_parts)

        # Step 2: Weather forecast query
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&"
            f"temperature_unit={temp_unit_param}&wind_speed_unit=kmh"
        )
        weather_data = _http_get_json(weather_url)
        current = weather_data.get("current", {})

        temp = current.get("temperature_2m", "N/A")
        apparent_temp = current.get("apparent_temperature", "N/A")
        humidity = current.get("relative_humidity_2m", "N/A")
        wind_speed = current.get("wind_speed_10m", "N/A")
        precipitation = current.get("precipitation", 0.0)
        weather_code = current.get("weather_code", 0)

        condition = WMO_WEATHER_CODES.get(weather_code, "Unknown condition")

        return (
            f"Weather in {display_location}:\n"
            f"• Condition: {condition}\n"
            f"• Temperature: {temp}{unit_symbol} (Feels like {apparent_temp}{unit_symbol})\n"
            f"• Humidity: {humidity}%\n"
            f"• Wind Speed: {wind_speed} km/h\n"
            f"• Precipitation: {precipitation} mm"
        )

    except Exception as e:
        # Fallback handling
        loc_key = target.lower()
        if loc_key in FALLBACK_WEATHER:
            return f"Weather in {target}: {FALLBACK_WEATHER[loc_key]} (Offline Fallback)"
        return f"Unable to fetch weather for '{target}': {str(e)}"


weather_tool = Tool(
    name="weather",
    description="Get the current real-time weather details for any city, state, or country worldwide.",
    parameters={
        "location": ToolParameter(
            type="string",
            description="The city, state, or country to get weather for (e.g. 'London', 'Tokyo', 'Trivandrum', 'New York')."
        ),
        "unit": ToolParameter(
            type="string",
            description="The unit of measurement for temperature: 'celsius' or 'fahrenheit'. Defaults to 'celsius'.",
            enum=["celsius", "fahrenheit"]
        )
    },
    required=[
        "location"
    ],
    function=weather
)

