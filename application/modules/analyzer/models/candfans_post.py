from django.db import models
from django.db.models.fields import Field


class CandfansPost(models.Model):
    post_id = models.BigIntegerField(primary_key=True)
    month = models.CharField(max_length=50)
    user = models.ForeignKey('CandfansUser', on_delete=models.CASCADE)
    user_code = models.CharField(max_length=50)
    username = models.CharField(max_length=200)
    profile_img = models.CharField(max_length=500)
    profile_cover_img = models.CharField(max_length=500)
    post_date = models.CharField(max_length=50)
    contents_type = models.IntegerField()
    post_type = models.IntegerField()
    contents_text = models.TextField()
    over_contents_50str = models.IntegerField()
    price = models.IntegerField()
    limit_post_date = models.CharField(max_length=50)
    reserve_post_date = models.CharField(max_length=50)
    contents_path1 = models.CharField(max_length=500, null=True)
    contents_path2 = models.CharField(max_length=500, null=True)
    contents_path3 = models.CharField(max_length=500, null=True)
    contents_path4 = models.CharField(max_length=500, null=True)
    image_count = models.IntegerField()
    movie_time = models.FloatField(null=True)
    secret_file = models.CharField(max_length=500, null=True)
    thumbnail_file = models.CharField(max_length=500)
    like_cnt = models.IntegerField()
    comments_cnt = models.IntegerField()
    chip_cnt = models.IntegerField()
    is_like = models.BooleanField()
    can_browsing = models.BooleanField()
    can_send_chip = models.BooleanField()
    r18 = models.IntegerField()
    apply_status = models.IntegerField()
    is_progressed = models.BooleanField()
    is_accept_comment = models.BooleanField()
    can_read_text = models.BooleanField()
    is_official_creator = models.BooleanField()
    has_own_thumbnail = models.BooleanField()
    is_on_air = models.BooleanField()
    live_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.user_id=}, {self.post_id=}'

    @classmethod
    async def update_or_create(cls, post_id, **params) -> 'CandfansPost':
        post, is_new = await cls.objects.aupdate_or_create(
            post_id=post_id,
            defaults=params,
        )
        return post

    @classmethod
    async def bulk_update_or_create(cls, posts: list['CandfansPost']) -> list['CandfansPost']:
        field_names = [
            f.name for f in cls._meta.get_fields()
            if isinstance(f, Field) and f.name != 'post_id'
        ]
        return await cls.objects.abulk_create(
            posts,
            update_conflicts=True,
            unique_fields=['post_id'],
            update_fields=field_names,
        )

    @classmethod
    async def get_list_by_user_id(cls, user_id: int) -> list['CandfansPost']:
        posts = []
        async for post in cls.objects.filter(user_id=user_id).order_by('post_date'):
            posts.append(post)
        return posts
