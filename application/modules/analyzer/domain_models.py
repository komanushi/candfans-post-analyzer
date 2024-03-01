import datetime
from typing import Optional

from pydantic import BaseModel


class CandfansUserModel(BaseModel):
    user_id: int
    user_code: str
    user_name: str
    last_synced_at: Optional[datetime.datetime]
