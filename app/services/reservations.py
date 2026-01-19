from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from app.core.config import UTC
from app.models.schemas import ReservationCreate, ReservationInStorage
from app.storage.memory import InMemoryReservationStorage


def _validate_times(start: datetime, end: datetime) -> None:
    now = datetime.now(tz=UTC)
    if start >= end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be strictly before end time",
        )
    if start <= now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reservations cannot be created in the past",
        )


def _overlaps(
    existing_start: datetime,
    existing_end: datetime,
    new_start: datetime,
    new_end: datetime,
) -> bool:
    # Overlap if intervals intersect with positive duration
    return new_start < existing_end and existing_start < new_end


def _ensure_no_overlap(
    storage: InMemoryReservationStorage,
    room_id: str,
    start: datetime,
    end: datetime,
) -> None:
    for res in storage.list_by_room(room_id):
        if _overlaps(res.start_time, res.end_time, start, end):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Reservation overlaps with an existing reservation",
            )


def create_reservation(
    storage: InMemoryReservationStorage,
    payload: ReservationCreate,
) -> ReservationInStorage:
    _validate_times(payload.start_time, payload.end_time)
    _ensure_no_overlap(storage, payload.room_id, payload.start_time, payload.end_time)

    return storage.create_from_data(
        room_id=payload.room_id,
        title=payload.title,
        start_time=payload.start_time,
        end_time=payload.end_time,
    )


def list_reservations(
    storage: InMemoryReservationStorage,
    room_id: str,
) -> List[ReservationInStorage]:
    return storage.list_by_room(room_id)


def cancel_reservation(
    storage: InMemoryReservationStorage,
    room_id: str,
    reservation_id: int,
) -> None:
    deleted = storage.delete(room_id, reservation_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found",
        )

