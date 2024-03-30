from django.db import models


class SearchHistory(models.Model):
    user_code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    async def create(cls, user_code) -> 'SearchHistory':
        return await cls.objects.acreate(user_code=user_code)
