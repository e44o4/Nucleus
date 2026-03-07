from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor

from database.db import SessionLocal

from models.device import Device
from models.device_schema import DeviceCreate
from models.command_schema import CommandRequest
from models.bulk_commnd_schema import BulkCommandRequest
from models.job import Job
from models.job_schema import JobResponse
from models.device_status import DeviceStatus
from models.config_schema import ConfigPushRequest

from services.device_connection import run_command_on_device, push_config_to_device
from services.job_runner import run_job
from services.monitoring_service import check_devices

router = APIRouter()


# Database Dependency
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
        location=device.location,
        status="unknown"
    )

    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return new_device


# LIST DEVICES
@router.get("/devices")
def list_devices(tenant_id: int, db: Session = Depends(get_db)):

    devices = db.query(Device).filter(Device.tenant_id == tenant_id).all()

    return devices


# GET DEVICE
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


# RUN COMMAND ON DEVICE
@router.post("/devices/{device_id}/run-command")
def run_command(device_id: int, request: CommandRequest, db: Session = Depends(get_db)):

    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        return {"error": "Device not found"}

    try:
        output = run_command_on_device(
            device.ip_address,
            device.username,
            device.password,
            request.command
        )

        # Save job record for history
        job = Job(
            status="success",
            command=request.command,
            results=f"Device: {device.name}\n{output}"
        )
        db.add(job)
        db.commit()

        return {
            "device": device.name,
            "command": request.command,
            "output": output
        }

    except Exception as e:

        # Save failed job record for history
        job = Job(
            status="failed",
            command=request.command,
            results=f"Device: {device.name}\nError: {str(e)}"
        )
        db.add(job)
        db.commit()

        return {
            "device": device.name,
            "command": request.command,
            "error": str(e)
        }


# BULK COMMAND EXECUTION
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
                "output": output,
                "status": "success"
            }

        except Exception as e:

            return {
                "device": device.name,
                "error": str(e),
                "status": "failed"
            }

    with ThreadPoolExecutor(max_workers=10) as executor:

        futures = executor.map(execute, devices)

        for result in futures:
            results.append(result)

    # Save bulk job record
    import json
    job = Job(
        status="success",
        command=request.command,
        results=json.dumps(results)
    )
    db.add(job)
    db.commit()

    return {"results": results}


# LIST ALL JOBS (Job History)
@router.get("/jobs")
def list_jobs(db: Session = Depends(get_db)):

    jobs = db.query(Job).order_by(Job.id.desc()).limit(100).all()

    result = []

    for job in jobs:
        result.append({
            "id": job.id,
            "command": job.command,
            "status": job.status,
            "results": job.results,
            "created_at": job.created_at
        })

    return result


# CREATE JOB
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


# GET JOB STATUS
@router.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):

    job = db.query(Job).filter(Job.id == job_id).first()

    return job


# RUN MONITOR MANUALLY
@router.post("/monitor/run")
def run_monitor():

    check_devices()

    return {"status": "monitoring completed"}


# DEVICE STATUS
@router.get("/monitor/status")
def get_status(db: Session = Depends(get_db)):

    data = db.query(DeviceStatus).all()

    return data


# PUSH CONFIG TO DEVICE
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