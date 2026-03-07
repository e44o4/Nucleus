from sqlalchemy import Column, Integer, String, ForeignKey
from database.base import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    # Tenant reference (for SaaS multi-company support)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)

    # Device basic information
    name = Column(String, nullable=False)
    ip_address = Column(String, unique=True, nullable=False)

    # Login credentials
    username = Column(String)
    password = Column(String)

    # Device details
    device_type = Column(String)
    location = Column(String)

    # Monitoring status
    status = Column(String, default="unknown")  # online / offline / unknown