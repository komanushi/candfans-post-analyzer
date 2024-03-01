from typing import Optional

from django.db import models

from ..domain_models import CandfansUserModel


class CandfansUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_code = models.CharField(max_length=255, unique=True)
    user_name = models.TextField()
    last_synced_at = models.DateTimeField(null=True, default=None)

    @classmethod
    async def create(cls, model: CandfansUserModel) -> 'CandfansUser':
        return await cls.objects.acreate(
            user_id=model.user_id,
            user_code=model.user_code,
            user_name=model.user_name,
        )

    @classmethod
    async def get_by_user_id(cls, user_id: int) -> Optional['CandfansUser']:
        return await cls.objects.afilter(user_id=user_id).first()

    @classmethod
    async def get_by_user_code(cls, user_code: str) -> Optional['CandfansUser']:
        return await cls.objects.afilter(user_code=user_code).first()
