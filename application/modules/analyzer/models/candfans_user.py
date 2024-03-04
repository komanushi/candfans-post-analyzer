import datetime
from typing import Optional

from django.db import models


class CandfansUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_code = models.CharField(max_length=255)
    username = models.TextField()
    last_synced_at = models.DateTimeField(null=True, default=None)
    detail = models.OneToOneField('CandfansUserDetail', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    async def create(
            cls,
            user_id: int,
            user_code: str,
            username: str,
            last_synced_at: Optional[datetime.datetime],
    ) -> 'CandfansUser':
        return await cls.objects.acreate(
            user_id=user_id,
            user_code=user_code,
            username=username,
            last_synced_at=last_synced_at
        )

    @classmethod
    async def get_by_user_code(cls, user_code: str) -> Optional['CandfansUser']:
        return await cls.objects.filter(user_code=user_code).order_by('-updated_at').afirst()

    @classmethod
    async def get_by_user_id(cls, user_id: int) -> Optional['CandfansUser']:
        return await cls.objects.filter(user_id=user_id).afirst()
