from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.device import Device
from models.device_schema import DeviceCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/devices")
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):

    new_device = Device(
        name=device.name,
        ip_address=device.ip_address,
        username=device.username,
        password=device.password,
        device_type=device.device_type,
        location=device.location
    )

    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return new_device