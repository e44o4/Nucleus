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
from services.monitoring_service import check_devices
from models.device_status import DeviceStatus
from models.config_schema import ConfigPushRequest
from services.device_connection import push_config_to_device


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
        tenant_id=device.tenant_id,
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
def list_devices(tenant_id: int, db: Session = Depends(get_db)):

    devices = db.query(Device).filter(Device.tenant_id == tenant_id).all()

    return devices


# GET DEVICE BY ID
@router.get("/devices/{device_id}")
def get_device(device_id: int, tenant_id: int, db: Session = Depends(get_db)):

    device = db.query(Device).filter(
        Device.id == device_id,
        Device.tenant_id == tenant_id
    ).first()

    return device


# DELETE DEVICE
@router.delete("/devices/{device_id}")
def delete_device(device_id: int, tenant_id: int, db: Session = Depends(get_db)):

    device = db.query(Device).filter(
        Device.id == device_id,
        Device.tenant_id == tenant_id
    ).first()

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

# Job-ID

@router.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):

    job = db.query(Job).filter(Job.id == job_id).first()

    return job

# Device Monitor

@router.post("/monitor/run")
def run_monitor():

    check_devices()

    return {"status": "monitoring completed"}

# Device Status

@router.get("/monitor/status")
def get_status(db: Session = Depends(get_db)):

    data = db.query(DeviceStatus).all()

    return data

# Push Config

@router.post("/config/push")
def push_config(request: ConfigPushRequest, db: Session = Depends(get_db)):

    devices = db.query(Device).filter(Device.id.in_(request.device_ids)).all()

    results = []

    for device in devices:

        try:

            output = push_config_to_device(
                device.ip_address,
                device.username,
                device.password,
                request.commands
            )

            results.append({
                "device": device.name,
                "status": "success",
                "output": output
            })

        except Exception as e:

            results.append({
                "device": device.name,
                "status": "failed",
                "error": str(e)
            })

    return {"results": results}