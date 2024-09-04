import factory
from candfans_client.models.timeline import PostType
from faker import Faker

from modules.analyzer.models import CandfansPost
from .candfans_user import CandfansUserFactory


from .base import AsyncMixin


class CandfansPostFactory(AsyncMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = CandfansPost

    post_id = factory.Sequence(lambda n: n)
    month = factory.Faker('month_name')
    user = factory.SubFactory(CandfansUserFactory)
    user_code = factory.LazyAttribute(lambda o: o.user.user_code)
    username = factory.LazyAttribute(lambda o: o.user.username)
    profile_img = factory.Faker('image_url')
    profile_cover_img = factory.Faker('image_url')
    post_date = Faker().date_time().strftime("%Y-%m-%d %H:%M:%S")
    contents_type = 1
    post_type = PostType.LIMITED_ACCESS_ITEM.value
    contents_text = factory.Faker('text')
    over_contents_50str = 1
    price = 1000
    limit_post_date = factory.Faker('date_time')
    reserve_post_date = factory.Faker('date_time')
    contents_path1 = factory.Faker('file_path')
    contents_path2 = factory.Faker('file_path')
    contents_path3 = factory.Faker('file_path')
    contents_path4 = factory.Faker('file_path')
    image_count = 3
    movie_time = factory.Faker('random_digit')
    secret_file = factory.Faker('file_path')
    thumbnail_file = factory.Faker('file_path')
    like_cnt = factory.Sequence(lambda n: n)
    comments_cnt = factory.Sequence(lambda n: n)
    chip_cnt = factory.Sequence(lambda n: n)
    is_like = factory.Faker('boolean')
    can_browsing = factory.Faker('boolean')
    can_send_chip = factory.Faker('boolean')
    apply_status = factory.Sequence(lambda n: n)
    is_progressed = factory.Faker('boolean')
    is_accept_comment = factory.Faker('boolean')
    can_read_text = factory.Faker('boolean')
    is_official_creator = factory.Faker('boolean')
    has_own_thumbnail = factory.Faker('boolean')
    is_on_air = factory.Faker('boolean')
    live_url = factory.Faker('url')
