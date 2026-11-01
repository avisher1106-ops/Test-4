import requests

from config import Config


class FruityviceError(Exception):
    """Raised when the Fruityvice API cannot be reached or returns bad data."""


def get_all_fruits():
    url = f"{Config.FRUITYVICE_BASE_URL.rstrip('/')}/api/fruit/all"
    try:
        response = requests.get(url, timeout=Config.FRUITYVICE_TIMEOUT)
        response.raise_for_status()
        fruits = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise FruityviceError(str(exc)) from exc

    if not isinstance(fruits, list):
        raise FruityviceError("Unexpected response format from Fruityvice API")

    return fruits
