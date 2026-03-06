import json
from database.db import SessionLocal
from models.job import Job
from models.device import Device
from services.device_connection import run_command_on_device


def run_job(job_id, device_ids, command):

    db = SessionLocal()

    devices = db.query(Device).filter(Device.id.in_(device_ids)).all()

    results = []

    for device in devices:

        try:

            output = run_command_on_device(
                device.ip_address,
                device.username,
                device.password,
                command
            )

            results.append({
                "device": device.name,
                "output": output
            })

        except Exception as e:

            results.append({
                "device": device.name,
                "error": str(e)
            })

    job = db.query(Job).filter(Job.id == job_id).first()

    job.status = "completed"

    job.results = json.dumps(results)

    db.commit()

    db.close()