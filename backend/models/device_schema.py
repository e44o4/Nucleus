from pydantic import BaseModel


class DeviceCreate(BaseModel):

    tenant_id: int
    name: str
    ip_address: str
    username: str
    password: str
    device_type: str
    location: str