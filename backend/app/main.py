from fastapi import FastAPI
from app.api.v1.router import api_router
from app.db.init_db import init_db

app = FastAPI(title="School Management System")

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()
