import factory
from faker import Faker
from candfans_client.models.timeline import ShortPlan, PostType
from modules.candfans_gateway.domain_models import (
    TimelinePosts,
    PostMap,
    Post
)


class ShortPlanFactory(factory.Factory):
    class Meta:
        model = ShortPlan

    plan_id = factory.Sequence(lambda n: n)
    support_price = factory.Sequence(lambda n: n)
    total_support_price = factory.Sequence(lambda n: n)
    plan_name = factory.Faker('word')
    plan_detail = factory.Faker('text')
    backnumber_id = None
    backnumber_price = None
    total_backnumber_price = None
    can_see_backnumber_plan_pay = factory.Faker('boolean')
    can_buy_backnumber_not_entry_plan = factory.Faker('boolean')
    add_backnumber_date = Faker().date_time().strftime("%Y-%m")
    is_joined_plan = factory.Faker('boolean')


class PostFactory(factory.Factory):
    class Meta:
        model = Post
    month = '2024-01'
    post_id = factory.Sequence(lambda n: n)
    user_id = factory.Sequence(lambda n: n)
    user_code = factory.Faker('user_name')
    username = factory.Faker('user_name')
    profile_img = factory.Faker('image_url')
    profile_cover_img = factory.Faker('image_url')
    post_date = Faker().date_time().strftime("%Y-%m-%d %H:%M:%S")
    contents_type = 1
    post_type = PostType.LIMITED_ACCESS_ITEM.value
    contents_text = factory.Faker('text')
    over_contents_50str = factory.Sequence(lambda n: n)
    price = factory.Sequence(lambda n: n)
    limit_post_date = Faker().date_time().strftime("%Y-%m-%d %H:%M:%S")
    reserve_post_date = Faker().date_time().strftime("%Y-%m-%d %H:%M:%S")
    contents_path1 = factory.Faker('file_path')
    contents_path2 = factory.Faker('file_path')
    contents_path3 = factory.Faker('file_path')
    contents_path4 = factory.Faker('file_path')
    image_count = factory.Sequence(lambda n: n)
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
    plans = []


class PostMapFactory(factory.Factory):
    class Meta:
        model = PostMap

    public_item = factory.List([factory.SubFactory(PostFactory) for _ in range(1)])
    limited_access_item = factory.List([factory.SubFactory(PostFactory) for _ in range(2)])
    individual_access_item = factory.List([factory.SubFactory(PostFactory) for _ in range(3)])
    back_number_item = factory.List([factory.SubFactory(PostFactory) for _ in range(2)])


class TimelinePostsModelFactory(factory.Factory):
    class Meta:
        model = TimelinePosts

    month = '2024-03'
    post_map = factory.SubFactory(PostMapFactory)
