from pydantic import BaseModel
from typing import List


class ConfigPushRequest(BaseModel):

    device_ids: List[int]

    commands: List[str]