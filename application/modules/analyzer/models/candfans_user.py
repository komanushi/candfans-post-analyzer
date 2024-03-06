import datetime
from typing import Optional

from django.db import models
from ..domain_models import SyncStatus


class CandfansUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_code = models.CharField(max_length=255)
    username = models.TextField()
    sync_status = models.CharField(max_length=100, choices=SyncStatus.choices(), null=True)
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
            sync_status: Optional[SyncStatus] = None,
            last_synced_at: Optional[datetime.datetime] = None,
            detail_id: Optional[int] = None
    ) -> 'CandfansUser':
        return await cls.objects.acreate(
            user_id=user_id,
            user_code=user_code,
            username=username,
            sync_status=sync_status.value if sync_status else None,
            last_synced_at=last_synced_at,
            detail_id=detail_id,
        )

    @classmethod
    async def update(cls, user_id: int, params: dict):
        return await cls.objects.filter(user_id=user_id).aupdate(**params)

    @classmethod
    async def get_by_user_code(cls, user_code: str) -> Optional['CandfansUser']:
        return await (
            cls.objects
            .filter(user_code=user_code)
            .select_related('detail')
            .order_by('-updated_at').afirst()
        )

    @classmethod
    async def get_by_user_id(cls, user_id: int) -> Optional['CandfansUser']:
        return await (
            cls.objects
            .filter(user_id=user_id)
            .select_related('detail').afirst()
        )
