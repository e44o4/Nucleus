from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database.base import Base


class Alert(Base):

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(Integer, index=True)

    message = Column(String)

    severity = Column(String)                          # "critical" / "warning" / "info"

    resolved = Column(Boolean, default=False)          # False = active, True = resolved

    created_at = Column(DateTime, server_default=func.now())   # when alert was created

    resolved_at = Column(DateTime, nullable=True)      # when alert was resolved