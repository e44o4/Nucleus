from sqlalchemy import Column, Integer, String
from database.base import Base


class DeviceStatus(Base):

    __tablename__ = "device_status"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(Integer)

    cpu_usage = Column(String)

    uptime = Column(String)

    status = Column(String)