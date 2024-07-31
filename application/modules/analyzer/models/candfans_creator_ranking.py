from datetime import datetime

from django.db import models


class CandfansCreatorDailyRanking(models.Model):
    day = models.DateField()
    rank = models.IntegerField()
    user_id = models.IntegerField()
    user_code = models.CharField(max_length=255)
    username = models.TextField()
    profile_img = models.CharField(max_length=500)
    profile_text = models.TextField()
    follow_cnt = models.IntegerField()
    follower_cnt = models.IntegerField()
    like_cnt = models.IntegerField()
    is_official_creator = models.BooleanField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('day', 'user_id'),)

    @classmethod
    async def create(
            cls,
            day: datetime.date,
            rank: int,
            user_id: int,
            user_code: str,
            username: str,
            profile_img: str,
            profile_text: str,
            follow_cnt: int,
            follower_cnt: int,
            like_cnt: int,
            is_official_creator: bool,
    ) -> 'CandfansCreatorDailyRanking':
        return await cls.objects.acreate(
            day=day,
            rank=rank,
            user_id=user_id,
            user_code=user_code,
            username=username,
            profile_img=profile_img,
            profile_text=profile_text,
            follow_cnt=follow_cnt,
            follower_cnt=follower_cnt,
            like_cnt=like_cnt,
            is_official_creator=is_official_creator,
        )

    @classmethod
    async def delete_by_day(cls, day: datetime.date):
        return await cls.objects.filter(day=day).adelete()

    @classmethod
    async def get_list_by_user_id(cls, user_id: int) -> list['CandfansCreatorDailyRanking']:
        ranks = []
        async for rank in cls.objects.filter(user_id=user_id):
            ranks.append(rank)
        return ranks
