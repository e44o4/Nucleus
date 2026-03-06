from pydantic import BaseModel
from typing import List


class BulkCommandRequest(BaseModel):
    device_ids: List[int]
    command: str