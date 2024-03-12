import factory

from candfans_client.models.user import UserInfo, QueriedUser, Plan


class CandfansClientPlanFactory(factory.Factory):
    class Meta:
        model = Plan
    plan_id = factory.Sequence(lambda n: n)
    user_id = factory.Sequence(lambda n: n)
    thanks_message_template_id = None
    plan_name = factory.Faker('word')
    support_price = factory.Sequence(lambda n: n)
    total_support_price = factory.Sequence(lambda n: n)
    plan_detail = factory.Faker('text')
    r18 = factory.Sequence(lambda n: n)
    status = factory.Sequence(lambda n: n)
    fans_cnt = 10
    is_fans = factory.Faker('boolean')
    is_price_update = None
    change_support_price = None
    content_length = factory.Sequence(lambda n: n)
    delete_at = None
    backnumber_price = None
    limit_after_backnumber = factory.Sequence(lambda n: n)
    this_month_after_backnumber = factory.Sequence(lambda n: n)
    can_see_backnumber_plan_pay = factory.Faker('boolean')
    can_buy_backnumber_not_entry_plan = factory.Faker('boolean')
    done_transfar_backnumber = factory.Faker('boolean')
    done_transfar_limit_backnumber = factory.Faker('boolean')
    entry_disabled = factory.Faker('boolean')
    upper_limit_entry_cnt = None


class CandfansClientQueriedUserFactory(factory.Factory):
    class Meta:
        model = QueriedUser

    id = factory.Sequence(lambda n: n)
    user_code = factory.Faker('user_name')
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
    delete_at = None
    is_accept_comment = factory.Faker('boolean')
    is_official_creator = factory.Faker('boolean')
    is_on_air = factory.Faker('boolean')
    live_url = factory.Faker('url')


class CandfansClientUserInfoFactory(factory.Factory):
    class Meta:
        model = UserInfo
    user = factory.SubFactory(CandfansClientQueriedUserFactory)
    plans = []
