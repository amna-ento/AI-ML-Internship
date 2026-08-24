from app.services.weather_service import WeatherError, get_weather


def get_weather_tool(city: str):
    try:
        return get_weather(city)
    except (ValueError, WeatherError) as error:
        return {"error": str(error)}