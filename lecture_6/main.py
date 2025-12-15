from fastapi import FastAPI

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck() -> dict:
    """Healthcheck endpoint"""
    return {"status": "ok"}
