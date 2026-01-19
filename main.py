from fastapi import FastAPI

from app.api.routes import reservations, health


app = FastAPI(
    title="Meeting Room Reservation API",
    version="0.1.0",
    description="Simple in-memory meeting room reservation API.",
)


app.include_router(health.router)
app.include_router(reservations.router, prefix="/rooms", tags=["reservations"])


@app.get("/")
def read_root() -> dict:
    return {"message": "Meeting Room Reservation API"}

