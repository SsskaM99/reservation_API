from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from app.services.reservations import create_reservation
from app.models.schemas import ReservationCreate
from app.storage.memory import InMemoryReservationStorage


UTC = timezone.utc


def future_time(hours: int) -> datetime:
    return datetime.now(tz=UTC) + timedelta(hours=hours)


def make_payload(start: datetime, end: datetime) -> ReservationCreate:
    return ReservationCreate(
        room_id="room-1",
        title="Test",
        start_time=start,
        end_time=end,
    )


def test_overlapping_reservations_raise_conflict():
    storage = InMemoryReservationStorage()
    start1 = future_time(1)
    end1 = future_time(2)
    payload1 = make_payload(start1, end1)
    create_reservation(storage, payload1)

    # Overlapping interval
    start2 = future_time(1, )
    end2 = future_time(3)
    payload2 = make_payload(start2, end2)

    with pytest.raises(HTTPException) as exc:
        create_reservation(storage, payload2)

    assert exc.value.status_code == 409


def test_start_must_be_before_end():
    storage = InMemoryReservationStorage()
    start = future_time(2)
    end = future_time(1)
    payload = make_payload(start, end)

    with pytest.raises(HTTPException) as exc:
        create_reservation(storage, payload)

    assert exc.value.status_code == 400


def test_cannot_create_in_past():
    storage = InMemoryReservationStorage()
    now = datetime.now(tz=UTC)
    start = now - timedelta(minutes=10)
    end = now + timedelta(minutes=10)
    payload = make_payload(start, end)

    with pytest.raises(HTTPException) as exc:
        create_reservation(storage, payload)

    assert exc.value.status_code == 400

