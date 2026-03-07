from database.db import engine
from database.base import Base
from models.device_status import DeviceStatus
from models.device import Device
from models.alert import Alert
from models.tenant import Tenant
from models.job import Job
from models.user import User


def init_db():
    Base.metadata.create_all(bind=engine)