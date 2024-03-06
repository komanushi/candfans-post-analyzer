from candfans_client.async_client import AsyncAnonymousCandFansClient
from candfans_client.models.timeline import PostType, Post
from .domain_models import TimelinePosts, PostMap


async def get_candfans_user_info_by_user_code(user_code: str):
    client = AsyncAnonymousCandFansClient()
    candfans_user_info = await client.get_users(user_code=user_code)
    return candfans_user_info


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
    timeline_months = await client.get_timeline_month(user_id)
    # 直近6ヶ月分までしか見ない(%Y-%m)
    timelines = []
    for timeline_month in timeline_months[:max_months]:
        # (%Y-%m)
        yyyy_mm = timeline_month.formatted_month_str
        timelines.append(TimelinePosts(
            month=yyyy_mm,
            post_map=PostMap(
                public_item=await _get_timeline(client, user_id, yyyy_mm, PostType.PUBLIC_ITEM),
                limited_access_item=await _get_timeline(client, user_id, yyyy_mm, PostType.LIMITED_ACCESS_ITEM),
                individual_access_item=await _get_timeline(client, user_id, yyyy_mm, PostType.INDIVIDUAL_ITEM),
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
