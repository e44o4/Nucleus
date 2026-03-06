from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.device import Device
from models.device_status import DeviceStatus
from models.alert import Alert

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):

    total_devices = db.query(Device).count()

    online_devices = db.query(DeviceStatus).filter(DeviceStatus.status == "online").count()

    offline_devices = db.query(DeviceStatus).filter(DeviceStatus.status == "offline").count()

    alerts = db.query(Alert).count()

    return {
        "total_devices": total_devices,
        "online_devices": online_devices,
        "offline_devices": offline_devices,
        "alerts": alerts
    }


@router.get("/dashboard/devices")
def device_health(db: Session = Depends(get_db)):

    data = db.query(DeviceStatus).all()

    return data


@router.get("/dashboard/alerts")
def active_alerts(db: Session = Depends(get_db)):

    alerts = db.query(Alert).all()

    return alerts