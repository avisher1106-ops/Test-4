import asyncio

import pytest
from fastapi.testclient import TestClient

import app as app_module
import fruityvice_client


def test_app_loads(client):
    response = client.get("/api/fruits")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 4


def test_exact_api_paths_are_exposed(client):
    assert client.get("/api/fruits").status_code == 200
    assert client.get("/api/search/apple").status_code == 200
    assert client.get("/api/calories/50").status_code == 200

    assert client.get("/fruits").status_code == 404
    assert client.get("/fruits/search?q=apple").status_code == 404
    assert client.get("/fruits/calories/50").status_code == 404


def test_get_all_fruits_keeps_fruityvice_structure(client, sample_fruits):
    response = client.get("/api/fruits")

    assert response.status_code == 200
    assert response.json() == sample_fruits


def test_fruityvice_is_called_on_every_api_request(client, fruityvice):
    client.get("/api/fruits")
    client.get("/api/search/apple")
    client.get("/api/calories/50")

    assert fruityvice.call_count == 3


def test_search_is_case_insensitive_and_matches_substring(client):
    response = client.get("/api/search/APPLE")

    assert response.status_code == 200
    assert [fruit["name"] for fruit in response.json()] == ["Apple", "Pineapple"]


def test_search_returns_empty_array_when_no_match(client):
    response = client.get("/api/search/dragonfruit")

    assert response.status_code == 200
    assert response.json() == []


def test_calories_filter_includes_equal_and_lower_values(client):
    response = client.get("/api/calories/50")

    assert response.status_code == 200
    fruits = response.json()
    assert [fruit["name"] for fruit in fruits] == ["Pineapple", "Watermelon"]
    assert all(fruit["nutritions"]["calories"] <= 50 for fruit in fruits)


def test_calories_returns_empty_array_when_no_match(client):
    response = client.get("/api/calories/10")

    assert response.status_code == 200
    assert response.json() == []


def test_log_records_full_route_and_total_results(client, log_calls):
    client.get("/api/fruits")
    client.get("/api/search/APPLE")
    client.get("/api/search/nope")
    client.get("/api/calories/50")
    client.get("/api/calories/10")

    assert [(call["route"], call["total_results"]) for call in log_calls] == [
        ("/api/fruits", 4),
        ("/api/search/APPLE", 2),
        ("/api/search/nope", 0),
        ("/api/calories/50", 2),
        ("/api/calories/10", 0),
    ]
    assert all(call["method"] == "GET" for call in log_calls)
    assert all(call["client_ip"] == "testclient" for call in log_calls)


def test_logging_failure_returns_clear_error(client, monkeypatch):
    def failing_insert_log(**kwargs):
        raise RuntimeError("logs table unavailable")

    monkeypatch.setattr(app_module, "insert_log", failing_insert_log)

    response = client.get("/api/fruits")

    assert response.status_code == 500
    body = response.json()
    assert body["error"] == "Failed to save request log"
    assert "logs table unavailable" in body["details"]


def test_database_init_failure_is_reported(monkeypatch):
    def failing_init_db():
        raise RuntimeError("cannot connect to MySQL")

    monkeypatch.setattr(app_module, "init_db", failing_init_db)

    with pytest.raises(RuntimeError, match="Failed to initialise database"):
        asyncio.run(_run_lifespan())


def test_fruityvice_client_calls_api_on_every_call(monkeypatch):
    calls = []

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return [{"name": "Apple"}]

    def fake_get(url, timeout):
        calls.append(url)
        return FakeResponse()

    monkeypatch.setattr(fruityvice_client.requests, "get", fake_get)

    assert fruityvice_client.get_all_fruits() == [{"name": "Apple"}]
    assert fruityvice_client.get_all_fruits() == [{"name": "Apple"}]
    assert len(calls) == 2
    assert calls[0].endswith("/api/fruit/all")


def test_fruityvice_client_rejects_non_list_response(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"not": "a list"}

    monkeypatch.setattr(
        fruityvice_client.requests, "get", lambda *args, **kwargs: FakeResponse()
    )

    with pytest.raises(fruityvice_client.FruityviceError):
        fruityvice_client.get_all_fruits()


async def _run_lifespan():
    async with app_module.lifespan(app_module.app):
        pass
