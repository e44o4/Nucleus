from sqlalchemy import Column, Integer, String, Text
from database.base import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    status = Column(String)

    command = Column(String)

    results = Column(Text)