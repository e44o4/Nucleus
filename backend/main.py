from fastapi import FastAPI

from database.init_db import init_db
from api.devices import router as device_router

app = FastAPI(title="Nucleus Network Automation Platform")

init_db()

app.include_router(device_router)

@app.get("/")
def home():
    return {"status": "API Running"}