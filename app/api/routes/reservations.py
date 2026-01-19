from __future__ import annotations

from typing import List

from fastapi import APIRouter, Body, Depends, Response, status

from app.api.deps import get_storage
from app.models.schemas import (
    ErrorResponse,
    ReservationCreate,
    ReservationResponse,
)
from app.services import reservations as reservation_service
from app.storage.memory import InMemoryReservationStorage

router = APIRouter()


@router.post(
    "/{room_id}/reservations",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Validation error (e.g. start >= end or reservation in the past)",
        },
        409: {
            "model": ErrorResponse,
            "description": "Reservation overlaps with existing reservation in the same room",
        },
    },
)
def create_reservation(
    room_id: str,
    payload: ReservationCreate = Body(
        ...,
        examples={
            "valid": {
                "summary": "Valid reservation",
                "description": "A simple 1-hour meeting in UTC.",
                "value": {
                    "room_id": "room-101",
                    "title": "Planning Meeting",
                    "start_time": "2026-01-20T09:00:00+00:00",
                    "end_time": "2026-01-20T10:00:00+00:00",
                },
            },
            "past": {
                "summary": "Reservation in the past",
                "description": "This will be rejected with HTTP 400.",
                "value": {
                    "room_id": "room-101",
                    "title": "Past Meeting",
                    "start_time": "2025-01-20T09:00:00+00:00",
                    "end_time": "2025-01-20T10:00:00+00:00",
                },
            },
        },
    ),
    storage: InMemoryReservationStorage = Depends(get_storage),
) -> ReservationResponse:
    """
    Create a new reservation for a room.
    """
    # Ensure payload room_id matches path
    payload.room_id = room_id
    reservation = reservation_service.create_reservation(storage, payload)
    return ReservationResponse(**reservation.model_dump())


@router.get(
    "/{room_id}/reservations",
    response_model=List[ReservationResponse],
)
def list_reservations(
    room_id: str,
    storage: InMemoryReservationStorage = Depends(get_storage),
) -> List[ReservationResponse]:
    """
    List all reservations for a specific room.
    """
    reservations = reservation_service.list_reservations(storage, room_id)
    return [ReservationResponse(**r.model_dump()) for r in reservations]


@router.delete(
    "/{room_id}/reservations/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse},
    },
)
def cancel_reservation(
    room_id: str,
    reservation_id: int,
    storage: InMemoryReservationStorage = Depends(get_storage),
) -> Response:
    """
    Cancel (delete) a reservation by id.
    """
    reservation_service.cancel_reservation(storage, room_id, reservation_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

