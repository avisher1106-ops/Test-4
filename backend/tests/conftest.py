import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import app as app_module
import routes as routes_module

SAMPLE_FRUITS = [
    {
        "name": "Apple",
        "id": 6,
        "family": "Rosaceae",
        "order": "Rosales",
        "genus": "Malus",
        "nutritions": {
            "calories": 52,
            "fat": 0.2,
            "sugar": 10.3,
            "carbohydrates": 11.4,
            "protein": 0.3,
        },
    },
    {
        "name": "Pineapple",
        "id": 20,
        "family": "Bromeliaceae",
        "order": "Poales",
        "genus": "Ananas",
        "nutritions": {
            "calories": 50,
            "fat": 0.1,
            "sugar": 9.9,
            "carbohydrates": 13.1,
            "protein": 0.5,
        },
    },
    {
        "name": "Banana",
        "id": 1,
        "family": "Musaceae",
        "order": "Zingiberales",
        "genus": "Musa",
        "nutritions": {
            "calories": 96,
            "fat": 0.3,
            "sugar": 12.2,
            "carbohydrates": 22.8,
            "protein": 1.1,
        },
    },
    {
        "name": "Watermelon",
        "id": 25,
        "family": "Cucurbitaceae",
        "order": "Cucurbitales",
        "genus": "Citrullus",
        "nutritions": {
            "calories": 30,
            "fat": 0.2,
            "sugar": 6.2,
            "carbohydrates": 7.6,
            "protein": 0.6,
        },
    },
]


class FakeFruityvice:
    def __init__(self, fruits):
        self.fruits = fruits
        self.call_count = 0

    def __call__(self):
        self.call_count += 1
        return copy.deepcopy(self.fruits)


@pytest.fixture
def sample_fruits():
    return copy.deepcopy(SAMPLE_FRUITS)


@pytest.fixture
def fruityvice(monkeypatch):
    fake = FakeFruityvice(SAMPLE_FRUITS)
    monkeypatch.setattr(routes_module, "get_all_fruits", fake)
    return fake


@pytest.fixture
def log_calls(monkeypatch):
    calls = []

    def fake_insert_log(method, route, total_results, client_ip):
        calls.append(
            {
                "method": method,
                "route": route,
                "total_results": total_results,
                "client_ip": client_ip,
            }
        )

    monkeypatch.setattr(app_module, "init_db", lambda: None)
    monkeypatch.setattr(app_module, "insert_log", fake_insert_log)
    return calls


@pytest.fixture
def client(fruityvice, log_calls):
    with TestClient(app_module.app) as test_client:
        yield test_client
