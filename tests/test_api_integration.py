from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)
UTC = timezone.utc


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_reservation():
    start = (datetime.now(tz=UTC) + timedelta(hours=1)).isoformat()
    end = (datetime.now(tz=UTC) + timedelta(hours=2)).isoformat()

    payload = {
        "room_id": "room-101",
        "title": "Integration Meeting",
        "start_time": start,
        "end_time": end,
    }
    create_resp = client.post("/rooms/room-101/reservations", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["room_id"] == "room-101"

    list_resp = client.get("/rooms/room-101/reservations")
    assert list_resp.status_code == 200
    reservations = list_resp.json()
    assert len(reservations) >= 1


def test_overlapping_reservations_conflict():
    start = (datetime.now(tz=UTC) + timedelta(hours=3)).isoformat()
    end = (datetime.now(tz=UTC) + timedelta(hours=4)).isoformat()
    payload = {
        "room_id": "room-202",
        "title": "First Meeting",
        "start_time": start,
        "end_time": end,
    }
    client.post("/rooms/room-202/reservations", json=payload)

    # Overlapping interval
    payload2 = {
        "room_id": "room-202",
        "title": "Overlap Meeting",
        "start_time": (datetime.now(tz=UTC) + timedelta(hours=3, minutes=30)).isoformat(),
        "end_time": (datetime.now(tz=UTC) + timedelta(hours=4, minutes=30)).isoformat(),
    }
    resp2 = client.post("/rooms/room-202/reservations", json=payload2)
    assert resp2.status_code == 409


def test_cancel_reservation_and_404_after():
    start = (datetime.now(tz=UTC) + timedelta(hours=5)).isoformat()
    end = (datetime.now(tz=UTC) + timedelta(hours=6)).isoformat()
    payload = {
        "room_id": "room-303",
        "title": "To Be Canceled",
        "start_time": start,
        "end_time": end,
    }
    create_resp = client.post("/rooms/room-303/reservations", json=payload)
    assert create_resp.status_code == 201
    res_id = create_resp.json()["id"]

    del_resp = client.delete(f"/rooms/room-303/reservations/{res_id}")
    assert del_resp.status_code == 204

    # Deleting again should yield 404
    del_resp2 = client.delete(f"/rooms/room-303/reservations/{res_id}")
    assert del_resp2.status_code == 404

def test_list_empty_room_returns_empty_list():
    client = TestClient(app)

    response = client.get("/rooms/empty-room/reservations")

    assert response.status_code == 200
    assert response.json() == []

def test_create_reservation_rejects_naive_datetime():
    client = TestClient(app)

    payload = {
        "start_time": "2026-01-20T10:00:00",  # no timezone info
        "end_time": "2026-01-20T11:00:00"
    }

    response = client.post("/rooms/room-1/reservations", json=payload)

    assert response.status_code == 422
