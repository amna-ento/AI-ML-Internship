import time

import httpx


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

MAX_RETRIES = 3


class WeatherError(Exception):
    pass


def get_weather(city: str):
    city = city.strip()

    if not city:
        raise ValueError("City cannot be empty")

    location = _get_location(city)

    latitude = location["latitude"]
    longitude = location["longitude"]

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,weather_code",
        "timezone": "auto",
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = httpx.get(
                WEATHER_URL,
                params=params,
                timeout=5.0,
            )

            response.raise_for_status()

            data = response.json()

            current = data.get("current")

            if not current:
                raise WeatherError("Weather API returned an unexpected response")

            return {
                "city": location["name"],
                "country": location.get("country"),
                "temperature": current["temperature_2m"],
                "humidity": current["relative_humidity_2m"],
                "weather_code": current["weather_code"],
            }

        except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError) as error:
            if isinstance(error, httpx.HTTPStatusError):
                status_code = error.response.status_code

                if 400 <= status_code < 500:
                    raise WeatherError("Weather API rejected the request")

            if attempt == MAX_RETRIES:
                raise WeatherError(
                    "Weather service failed after 3 attempts"
                )

            time.sleep(2 ** (attempt - 1))


def _get_location(city: str):
    try:
        response = httpx.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=5.0,
        )

        response.raise_for_status()

        data = response.json()

    except httpx.TimeoutException:
        raise WeatherError("Weather location service timed out")

    except httpx.NetworkError:
        raise WeatherError("Weather location service is unavailable")

    except httpx.HTTPStatusError:
        raise WeatherError("Weather location service returned an error")

    results = data.get("results")

    if not results:
        raise WeatherError(f"City '{city}' was not found")

    return results[0]