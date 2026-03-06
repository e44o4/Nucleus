from sqlalchemy import Column, Integer, String
from database.base import Base

class Device(Base):

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ip_address = Column(String, unique=True, nullable=False)
    username = Column(String)
    password = Column(String)
    device_type = Column(String)
    location = Column(String)