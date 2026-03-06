from sqlalchemy import Column, Integer, String
from database.base import Base


class Alert(Base):

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(Integer)

    message = Column(String)

    severity = Column(String)