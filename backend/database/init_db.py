from database.db import engine
from database.base import Base
from models.device_status import DeviceStatus
from models.device import Device
from models.alert import Alert


def init_db():
    Base.metadata.create_all(bind=engine)