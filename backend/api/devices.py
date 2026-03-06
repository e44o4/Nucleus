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


# CREATE DEVICE
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


# LIST ALL DEVICES
@router.get("/devices")
def list_devices(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return devices


# GET DEVICE BY ID
@router.get("/devices/{device_id}")
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    return device


# DELETE DEVICE
@router.delete("/devices/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):

    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        return {"error": "Device not found"}

    db.delete(device)
    db.commit()

    return {"message": "Device deleted successfully"}