from fastapi import FastAPI
from services.scheduler import start_scheduler
from database.init_db import init_db
from api.devices import router as device_router
from api.dashboard import router as dashboard_router
from api.tenants import router as tenant_router
from api.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Nucleus")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

start_scheduler()

app.include_router(device_router)
app.include_router(dashboard_router)
app.include_router(tenant_router)   
app.include_router(auth_router)

@app.get("/")
def home():
    return {"status": "API Running"}