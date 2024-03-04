from django.db import models


class CandfansUserDetail(models.Model):

    user_id = models.IntegerField()
    user_code = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    profile_cover_img = models.CharField(max_length=255)
    profile_text = models.CharField(max_length=255)
    profile_img = models.CharField(max_length=255)
    creater_genre = models.IntegerField()
    link_twitter = models.CharField(max_length=255)
    link_instagram = models.CharField(max_length=255)
    link_tiktok = models.CharField(max_length=255)
    link_youtube = models.CharField(max_length=255)
    link_amazon = models.CharField(max_length=255)
    link_facebook = models.CharField(max_length=255)
    link_website = models.CharField(max_length=255)
    apeal_img1 = models.CharField(max_length=255)
    apeal_img2 = models.CharField(max_length=255)
    apeal_img3 = models.CharField(max_length=255)
    follower_cnt = models.IntegerField(default=0)
    follow_cnt = models.IntegerField(default=0)
    like_cnt = models.IntegerField(default=0)
    fans_cnt = models.IntegerField(null=True)
    post_cnt = models.IntegerField(default=0)
    image_cnt = models.IntegerField(default=0)
    movie_cnt = models.IntegerField(default=0)
    is_follow = models.BooleanField(default=False)
    is_followed = models.BooleanField(default=False)
    is_fansed = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_ban = models.BooleanField(default=False)
    can_send_dm = models.BooleanField(default=False)
    delete_at = models.CharField(max_length=255, null=True)
    is_accept_comment = models.BooleanField(default=False)
    is_official_creator = models.BooleanField(default=False)
    live_url = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    async def create(cls, **params) -> 'CandfansUserDetail':
        return cls.objects.acreate(**params)
