from sqlalchemy import Column, Integer, String, ForeignKey
from database.base import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(Integer, ForeignKey("tenants.id"))

    email = Column(String, unique=True)
    password = Column(String)

    role = Column(String, default="admin")