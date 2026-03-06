from pydantic import BaseModel

class DeviceCreate(BaseModel):
    name: str
    ip_address: str
    username: str
    password: str
    device_type: str
    location: str