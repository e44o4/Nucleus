from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.command_schema import CommandRequest
from services.device_connection import run_command_on_device
from models.bulk_commnd_schema import BulkCommandRequest
from concurrent.futures import ThreadPoolExecutor
from fastapi import BackgroundTasks
from models.job import Job
from models.job_schema import JobResponse
from services.job_runner import run_job


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

# Automation API
@router.post("/devices/{device_id}/run-command")
def run_command(device_id: int, request: CommandRequest, db: Session = Depends(get_db)):

    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        return {"error": "Device not found"}

    output = run_command_on_device(
        device.ip_address,
        device.username,
        device.password,
        request.command
    )

    return {
        "device": device.name,
        "command": request.command,
        "output": output
    }

# Bulk Command Run

@router.post("/bulk/run-command")
def run_bulk_command(request: BulkCommandRequest, db: Session = Depends(get_db)):

    devices = db.query(Device).filter(Device.id.in_(request.device_ids)).all()

    results = []

    def execute(device):

        try:
            output = run_command_on_device(
                device.ip_address,
                device.username,
                device.password,
                request.command
            )

            return {
                "device": device.name,
                "output": output
            }

        except Exception as e:

            return {
                "device": device.name,
                "error": str(e)
            }

    with ThreadPoolExecutor(max_workers=10) as executor:

        futures = executor.map(execute, devices)

        for result in futures:
            results.append(result)

    return {"results": results}

# Run-Jobs

@router.post("/jobs/run-command")
def create_job(request: BulkCommandRequest,
               background_tasks: BackgroundTasks,
               db: Session = Depends(get_db)):

    job = Job(
        status="running",
        command=request.command
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(
        run_job,
        job.id,
        request.device_ids,
        request.command
    )

    return {
        "job_id": job.id,
        "status": "running"
    }

@router.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):

    job = db.query(Job).filter(Job.id == job_id).first()

    return job