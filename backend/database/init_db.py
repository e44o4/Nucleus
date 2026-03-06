from database.db import engine
from database.base import Base

from models.device import Device


def init_db():
    Base.metadata.create_all(bind=engine)