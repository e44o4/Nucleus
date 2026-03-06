from fastapi import FastAPI
from services.scheduler import start_scheduler
from database.init_db import init_db
from api.devices import router as device_router
from api.dashboard import router as dashboard_router

app = FastAPI(title="Nucleus Network Automation Platform")

init_db()

start_scheduler()

app.include_router(device_router)
app.include_router(dashboard_router)

@app.get("/")
def home():
    return {"status": "API Running"}