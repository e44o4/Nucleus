from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database.base import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    status = Column(String)        # "running" / "success" / "failed"

    command = Column(String)

    results = Column(Text)         # JSON string of results

    created_at = Column(DateTime, server_default=func.now())   # when job was created