import factory
from django.utils import timezone

from modules.analyzer.models import CandfansUserDetail

from .base import AsyncMixin


class CandfansUserDetailFactory(AsyncMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = CandfansUserDetail

    user_id = factory.Sequence(lambda n: n)
    user_code = factory.Sequence(lambda n: f"user{n}")
    username = factory.Faker('user_name')
    profile_cover_img = factory.Faker('image_url')
    profile_text = factory.Faker('text')
    profile_img = factory.Faker('image_url')
    creater_genre = factory.Sequence(lambda n: n)
    link_twitter = factory.Faker('url')
    link_instagram = factory.Faker('url')
    link_tiktok = factory.Faker('url')
    link_youtube = factory.Faker('url')
    link_amazon = factory.Faker('url')
    link_facebook = factory.Faker('url')
    link_website = factory.Faker('url')
    apeal_img1 = factory.Faker('image_url')
    apeal_img2 = factory.Faker('image_url')
    apeal_img3 = factory.Faker('image_url')
    follower_cnt = factory.Sequence(lambda n: n)
    follow_cnt = factory.Sequence(lambda n: n)
    like_cnt = factory.Sequence(lambda n: n)
    fans_cnt = factory.Sequence(lambda n: n)
    post_cnt = factory.Sequence(lambda n: n)
    image_cnt = factory.Sequence(lambda n: n)
    movie_cnt = factory.Sequence(lambda n: n)
    is_follow = factory.Faker('boolean')
    is_followed = factory.Faker('boolean')
    is_fansed = factory.Faker('boolean')
    is_block = factory.Faker('boolean')
    is_blocked = factory.Faker('boolean')
    is_ban = factory.Faker('boolean')
    can_send_dm = factory.Faker('boolean')
    delete_at = factory.Faker('date_time')
    is_accept_comment = factory.Faker('boolean')
    is_official_creator = factory.Faker('boolean')
    is_on_air = factory.Faker('boolean')
    live_url = factory.Faker('url')

    created_at = timezone.now()
