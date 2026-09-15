from fastapi import FastAPI

from app.config import settings

app = FastAPI(title="support-agent")


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}
