from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.core.config import UTC


class ReservationBase(BaseModel):
    room_id: str = Field(..., example="room-101")
    title: str = Field(..., example="Weekly Sync")
    start_time: datetime = Field(
        ...,
        description="Start time in ISO 8601, UTC",
        example="2026-01-20T09:00:00+00:00",
    )
    end_time: datetime = Field(
        ...,
        description="End time in ISO 8601, UTC",
        example="2026-01-20T10:00:00+00:00",
    )

    @validator("start_time", "end_time")
    def ensure_timezone_aware_utc(cls, value: datetime) -> datetime:  # type: ignore[override]
        if value.tzinfo is None:
            raise ValueError("Datetime must be timezone-aware and in UTC")
        # Normalize to UTC
        value_utc = value.astimezone(UTC)
        if value_utc.utcoffset() != UTC.utcoffset(value_utc):
            raise ValueError("Datetime must be in UTC")
        return value_utc


class ReservationCreate(ReservationBase):
    pass


class ReservationInStorage(ReservationBase):
    id: int
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=UTC),
        description="Timestamp when the reservation was created",
    )


class ReservationResponse(ReservationInStorage):
    class Config:
        orm_mode = True


class ErrorResponse(BaseModel):
    detail: str = Field(..., example="Reservation overlaps with existing reservation")

