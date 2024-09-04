from typing import Optional

from candfans_client.async_client import AsyncAnonymousCandFansClient, AsyncCandFansClient
from candfans_client.exceptions import CandFansException
from candfans_client.models.timeline import PostType, Post
from candfans_client.models.search import Creator, RankingCreator
from candfans_client.models.user import UserInfo
from dateutil import relativedelta
from django.conf import settings
from django.utils import timezone

from modules.exceptions import NotFoundUser
from .domain_models import TimelinePosts, PostMap


async def get_candfans_user_info_by_user_code(user_code: str) -> Optional[UserInfo]:
    client = AsyncAnonymousCandFansClient()
    try:
        candfans_user_info = await client.get_users(user_code=user_code)
        return candfans_user_info
    except CandFansException as e:
        if 'アカウントが見つかりませんでした。' in str(e):
            raise NotFoundUser(f'{user_code} is not found')
        raise e


async def get_timelines(user_id: int, max_months: int = 6) -> list[TimelinePosts]:
    """
    {
        'YYYY-MM': {
            'public_item: [Post, Post],
            'limited_access_item': [],
            'individual_access_item': [],
        },
    }
    """
    client = AsyncAnonymousCandFansClient()
    # 直近6ヶ月分までしか見ない(%Y-%m)
    today = timezone.now().date()
    timeline_months = sorted([
        (today - relativedelta.relativedelta(months=i)).strftime('%Y-%m')
        for i in range(max_months)
    ])
    timelines = []
    for timeline_month in timeline_months:
        # (%Y-%m)
        timelines.append(TimelinePosts(
            month=timeline_month,
            post_map=PostMap(
                public_item=await _get_timeline(client, user_id, timeline_month, PostType.PUBLIC_ITEM),
                limited_access_item=await _get_timeline(client, user_id, timeline_month, PostType.LIMITED_ACCESS_ITEM),
                individual_access_item=await _get_timeline(client, user_id, timeline_month, PostType.INDIVIDUAL_ITEM),
                back_number_item=await _get_timeline(client, user_id, timeline_month, PostType.BACK_NUMBER_ITEM),
            )
        ))
    return timelines


async def _get_timeline(
        client: AsyncAnonymousCandFansClient, user_id: int, month: str, post_type: PostType
) -> list[Post]:
    posts = client.get_timeline(
        user_id=user_id,
        month=month,
        post_types=[post_type],
        max_page=100
    )
    result = []
    async for post in posts:
        result.append(post)
    return result


async def get_daily_popular_creator(max_ranking=50) -> list[Creator]:
    client = AsyncCandFansClient(
        email=settings.CANDFANS_EMAIL,
        password=settings.CANDFANS_PASSWORD
    )
    await client.login()
    creators = []
    # ページングで同じユーザーが戻される可能性があるので少し余剰をもたせる
    max_page = (max_ranking // 5) + 2
    async for creator in client.get_popular_creators(between=BetweenType.DAY, max_page=max_page):
        if creator not in creators:
            creators.append(creator)
    return creators[:max_ranking]


async def get_creator_ranking(max_ranking: int = 100) -> list[RankingCreator]:
    client = AsyncAnonymousCandFansClient()
    ranking_creators = []
    async for rank in client.get_creator_ranking(
        start_page=1,
        max_page=1,
        per_page=max_ranking
    ):
        ranking_creators.append(rank)
    return ranking_creators
