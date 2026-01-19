## Meeting Room Reservation API

Simple in-memory Meeting Room Reservation API built with **FastAPI** and **Python**.

### Project Goal

Provide a minimal but working baseline API to manage meeting room reservations, enforcing:

- **No overlapping reservations in the same room**
- **No reservations in the past**
- **Start time must be strictly before end time**

All timestamps are **timezone-aware UTC** ISO 8601 strings.

---

## Setup

### 1. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv .venv
.\.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the API

From the project root:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

- **Interactive docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **ReDoc docs**: `http://127.0.0.1:8000/redoc`

---

## Endpoints

- **`GET /health`**
  - Health check.

- **`POST /rooms/{room_id}/reservations`**
  - Create a reservation for a given room.

- **`GET /rooms/{room_id}/reservations`**
  - List all reservations for a given room.

- **`DELETE /rooms/{room_id}/reservations/{reservation_id}`**
  - Cancel (delete) an existing reservation.

### Business Rules (enforced)

- **No overlapping reservations in the same room** (409 Conflict).
- **Reservations cannot be created in the past** (400 Bad Request).
- **Start time must be strictly before end time** (400 Bad Request).
- **Timezone-aware UTC datetimes only.**

---

## Example Payloads and `curl` Commands

### Create a reservation

```bash
curl -X POST "http://127.0.0.1:8000/rooms/room-101/reservations" ^
  -H "Content-Type: application/json" ^
  -d "{
    \"room_id\": \"room-101\",
    \"title\": \"Planning Meeting\",
    \"start_time\": \"2026-01-20T09:00:00+00:00\",
    \"end_time\": \"2026-01-20T10:00:00+00:00\"
  }"
```

### List reservations for a room

```bash
curl "http://127.0.0.1:8000/rooms/room-101/reservations"
```

### Cancel a reservation

```bash
curl -X DELETE "http://127.0.0.1:8000/rooms/room-101/reservations/1"
```

### Health check

```bash
curl "http://127.0.0.1:8000/health"
```

---

## Testing

Run unit and integration tests with:

```bash
pytest
```

Tests cover:

- **Overlap detection logic**
- **Time validation rules (past, start < end)**
- **Basic API integration using FastAPI `TestClient`**

