import subprocess
import logging

from database.db import SessionLocal
from models.device import Device
from models.device_status import DeviceStatus
from models.alert import Alert
from services.device_connection import run_command_on_device

# Set up logging so you can trace what the monitor is doing
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ping_device(ip):
    """Quick ICMP ping check before attempting SSH."""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0

    except Exception:
        return False


def has_active_alert(db, device_id, message):
    """
    Check if an unresolved alert already exists for this device with the same message.
    This prevents duplicate alerts from being created every 10 seconds.
    """
    existing = db.query(Alert).filter(
        Alert.device_id == device_id,
        Alert.message == message,
        Alert.resolved == False
    ).first()

    return existing is not None


def resolve_alerts_for_device(db, device_id):
    """
    When a device comes back online, automatically resolve all its active alerts.
    """
    db.query(Alert).filter(
        Alert.device_id == device_id,
        Alert.resolved == False
    ).update({
        "resolved": True
    })


def create_alert_if_not_exists(db, device_id, message, severity):
    """
    Only create a new alert if no active alert with the same message exists.
    This is the core deduplication logic.
    """
    if not has_active_alert(db, device_id, message):
        alert = Alert(
            device_id=device_id,
            message=message,
            severity=severity,
            resolved=False
        )
        db.add(alert)
        logger.warning(f"[ALERT] Device {device_id} — {message}")
    else:
        logger.info(f"[SKIP] Duplicate alert suppressed for device {device_id}: {message}")


def check_devices():
    """
    Main monitoring loop — runs every 10 seconds via APScheduler.
    For each device:
      1. Ping check
      2. SSH health check
      3. Store device status
      4. Create alerts (deduplicated)
      5. Auto-resolve alerts when device comes back online
    """
    db = SessionLocal()

    try:
        devices = db.query(Device).all()
        logger.info(f"[MONITOR] Checking {len(devices)} devices...")

        for device in devices:

            # ── Step 1: Ping Check ──────────────────────────────────────────
            reachable = ping_device(device.ip_address)

            if not reachable:
                logger.warning(f"[OFFLINE] Device {device.name} ({device.ip_address}) is unreachable")

                device.status = "offline"

                status = DeviceStatus(
                    device_id=device.id,
                    cpu_usage="N/A",
                    uptime="N/A",
                    status="offline"
                )
                db.add(status)

                # Only create alert if no active ping alert exists for this device
                create_alert_if_not_exists(
                    db,
                    device_id=device.id,
                    message="Device unreachable (Ping failed)",
                    severity="critical"
                )

                continue

            # ── Step 2: SSH Health Check ────────────────────────────────────
            try:
                cpu_output = run_command_on_device(
                    device.ip_address,
                    device.username,
                    device.password,
                    "/system resource print"
                )

                # Device is healthy — mark online and resolve any active alerts
                device.status = "online"

                status = DeviceStatus(
                    device_id=device.id,
                    cpu_usage=cpu_output,
                    uptime="unknown",
                    status="online"
                )
                db.add(status)

                # Auto-resolve any alerts that were previously open for this device
                resolve_alerts_for_device(db, device.id)
                logger.info(f"[ONLINE] Device {device.name} ({device.ip_address}) is healthy")

            except Exception as e:
                error_message = str(e)
                logger.error(f"[SSH FAIL] Device {device.name} ({device.ip_address}): {error_message}")

                device.status = "offline"

                status = DeviceStatus(
                    device_id=device.id,
                    cpu_usage="N/A",
                    uptime="N/A",
                    status="offline"
                )
                db.add(status)

                # Deduplicated SSH alert
                create_alert_if_not_exists(
                    db,
                    device_id=device.id,
                    message="SSH login failed",
                    severity="warning"
                )

        db.commit()
        logger.info("[MONITOR] Check cycle complete.")

    except Exception as e:
        logger.error(f"[MONITOR ERROR] Unexpected error during check_devices: {str(e)}")
        db.rollback()

    finally:
        db.close()