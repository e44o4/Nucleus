from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.device import Device
from models.alert import Alert

router = APIRouter()


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard/summary")
def get_dashboard_summary(tenant_id: int, db: Session = Depends(get_db)):

    # Total devices for tenant
    total_devices = db.query(Device).filter(
        Device.tenant_id == tenant_id
    ).count()

    # Online devices
    online_devices = db.query(Device).filter(
        Device.tenant_id == tenant_id,
        Device.status == "online"
    ).count()

    # Offline devices
    offline_devices = db.query(Device).filter(
        Device.tenant_id == tenant_id,
        Device.status == "offline"
    ).count()

    # Alerts (alerts table currently not tenant based)
    alerts = db.query(Alert).count()

    return {
        "total_devices": total_devices,
        "online_devices": online_devices,
        "offline_devices": offline_devices,
        "alerts": alerts
    }


@router.get("/dashboard/devices")
def get_device_health(tenant_id: int, db: Session = Depends(get_db)):

    devices = db.query(Device).filter(
        Device.tenant_id == tenant_id
    ).all()

    result = []

    for device in devices:
        result.append({
            "id": device.id,
            "name": device.name,
            "ip_address": device.ip_address,
            "status": device.status,
            "location": device.location
        })

    return result


@router.get("/dashboard/alerts")
def get_active_alerts(db: Session = Depends(get_db)):

    alerts = db.query(Alert).all()

    result = []

    for alert in alerts:
        result.append({
            "id": alert.id,
            "device_id": alert.device_id,
            "message": alert.message,
            "severity": alert.severity,
            "created_at": alert.created_at
        })

    return result