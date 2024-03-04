import datetime
from typing import Optional

from candfans_client.models.user import QueriedUser
from django.utils import timezone
from pydantic import BaseModel


EXPIRED_DAYS = 2


class CandfansUserModel(BaseModel):
    user_id: int
    user_code: str
    username: str
    last_synced_at: Optional[datetime.datetime]

    @property
    def is_expired(self) -> bool:
        if self.last_synced_at is None:
            return True
        if (timezone.now() - self.last_synced_at) > datetime.timedelta(days=EXPIRED_DAYS):
            return True
        return False

    @classmethod
    def from_candfans_user_info(cls, param: QueriedUser) -> 'CandfansUserModel':
        return cls(
            user_id=param.id,
            user_code=param.user_code,
            username=param.username,
            last_synced_at=None,
        )
