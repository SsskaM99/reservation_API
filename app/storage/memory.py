from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional

from app.models.schemas import ReservationInStorage


class InMemoryReservationStorage:
    """
    Simple in-memory reservation storage.

    Reservations are stored per room_id, each with an auto-incrementing integer id.
    """

    def __init__(self) -> None:
        self._reservations_by_room: Dict[str, List[ReservationInStorage]] = defaultdict(list)
        self._id_counter: int = 0

    def _next_id(self) -> int:
        self._id_counter += 1
        return self._id_counter

    def create(self, reservation: ReservationInStorage) -> ReservationInStorage:
        self._reservations_by_room[reservation.room_id].append(reservation)
        return reservation

    def create_from_data(
        self,
        room_id: str,
        title: str,
        start_time,
        end_time,
    ) -> ReservationInStorage:
        new = ReservationInStorage(
            id=self._next_id(),
            room_id=room_id,
            title=title,
            start_time=start_time,
            end_time=end_time,
        )
        return self.create(new)

    def list_by_room(self, room_id: str) -> List[ReservationInStorage]:
        return list(self._reservations_by_room.get(room_id, []))

    def get(self, room_id: str, reservation_id: int) -> Optional[ReservationInStorage]:
        for res in self._reservations_by_room.get(room_id, []):
            if res.id == reservation_id:
                return res
        return None

    def delete(self, room_id: str, reservation_id: int) -> bool:
        reservations = self._reservations_by_room.get(room_id)
        if reservations is None:
            return False
        for idx, res in enumerate(reservations):
            if res.id == reservation_id:
                del reservations[idx]
                return True
        return False

