import subprocess

from database.db import SessionLocal
from models.device import Device
from models.device_status import DeviceStatus
from models.alert import Alert
from services.device_connection import run_command_on_device


def ping_device(ip):

    try:

        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return result.returncode == 0

    except Exception:

        return False


def check_devices():

    db = SessionLocal()

    devices = db.query(Device).all()

    for device in devices:

        # Step 1 — Ping check

        reachable = ping_device(device.ip_address)

        if not reachable:

            device.status = "offline"

            status = DeviceStatus(
                device_id=device.id,
                cpu_usage="N/A",
                uptime="N/A",
                status="offline"
            )

            db.add(status)

            alert = Alert(
                device_id=device.id,
                message="Device unreachable (Ping failed)",
                severity="critical"
            )

            db.add(alert)

            continue

        # Step 2 — Try SSH command

        try:

            cpu_output = run_command_on_device(
                device.ip_address,
                device.username,
                device.password,
                "/system resource print"
            )

            device.status = "online"

            status = DeviceStatus(
                device_id=device.id,
                cpu_usage=cpu_output,
                uptime="unknown",
                status="online"
            )

            db.add(status)

        except Exception:

            device.status = "offline"

            status = DeviceStatus(
                device_id=device.id,
                cpu_usage="N/A",
                uptime="N/A",
                status="offline"
            )

            db.add(status)

            alert = Alert(
                device_id=device.id,
                message="SSH login failed",
                severity="warning"
            )

            db.add(alert)

    db.commit()

    db.close()