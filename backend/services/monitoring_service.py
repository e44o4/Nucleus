from database.db import SessionLocal
from models.device import Device
from models.device_status import DeviceStatus
from models.alert import Alert
from services.device_connection import run_command_on_device


def check_devices():

    db = SessionLocal()

    devices = db.query(Device).all()

    for device in devices:

        try:

            cpu_output = run_command_on_device(
                device.ip_address,
                device.username,
                device.password,
                "/system resource print"
            )

            status = DeviceStatus(
                device_id=device.id,
                cpu_usage=cpu_output,
                uptime="unknown",
                status="online"
            )

            db.add(status)

        except Exception:

            status = DeviceStatus(
                device_id=device.id,
                cpu_usage="N/A",
                uptime="N/A",
                status="offline"
            )

            db.add(status)

            alert = Alert(
                device_id=device.id,
                message="Device offline",
                severity="critical"
            )

            db.add(alert)

    db.commit()

    db.close()