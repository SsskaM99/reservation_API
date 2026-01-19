from __future__ import annotations

from functools import lru_cache

from app.storage.memory import InMemoryReservationStorage


@lru_cache(maxsize=1)
def get_storage() -> InMemoryReservationStorage:
    """
    Returns a singleton in-memory storage instance for the app process.
    """

    return InMemoryReservationStorage()

