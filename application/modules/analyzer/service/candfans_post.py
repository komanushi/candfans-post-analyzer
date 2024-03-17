from collections import defaultdict
from candfans_client.models.timeline import Post, PostType

from ..domain_models import (
    CandfansUserModel,
    Stat,
    Stats,
    DataSet, PostTypeStat,
)
from ..models import CandfansPost, CandFansPostPlanRelation, CandfansPlan
from ..converter import (
    convert_from_post_to_candfans_post,
    convert_from_candfans_post_to_post
)


async def update_or_create_candfans_post(
        posts: list[Post]
) -> int:
    plan_ids = []
    for post in posts:
        plan_ids.extend([plan.plan_id for plan in post.plans])
    # to uniq
    plan_ids = list(set(plan_ids))
    related_plan_map = {p.plan_id: p for p in await CandfansPlan.get_list_by_plan_ids(plan_ids)}
    target_candfans_posts = [
        convert_from_post_to_candfans_post(p)
        for p in posts
    ]
    new_post_map = {
        new_post.post_id: new_post
        for new_post in await CandfansPost.bulk_update_or_create(
            target_candfans_posts,
        )
    }
    rels = []
    for post in posts:
        for plan in post.plans:
            rels.append(CandFansPostPlanRelation(
                candfans_plan=related_plan_map[plan.plan_id],
                candfans_post=new_post_map[post.post_id]
            ))
    await CandFansPostPlanRelation.bulk_create(rels)

    return len(new_post_map.items())


async def get_post_stats(user: CandfansUserModel) -> Stats:
    posts = await CandfansPost.get_list_by_user_id(user_id=user.user_id)
    monthly_aggregated = _aggregate_monthly(posts)
    return Stats(
        total_post_type_stats=PostTypeStat(
            public_item=len([p for p in posts if p.post_type == PostType.PUBLIC_ITEM.value]),
            limited_access_item=len([p for p in posts if p.post_type == PostType.LIMITED_ACCESS_ITEM.value]),
            individual_item=len([p for p in posts if p.post_type == PostType.INDIVIDUAL_ITEM.value]),
            back_number_item=len([p for p in posts if p.post_type == PostType.BACK_NUMBER_ITEM.value]),
        ),
        monthly_post_type_stats=_create_post_type_stats(monthly_aggregated),
        monthly_content_type_stats=_create_content_type_stats(monthly_aggregated),
        movie_stats=_create_movie_stats(monthly_aggregated),
        photo_stats=_create_photo_stats(monthly_aggregated),
    )


def _aggregate_monthly(posts: list[CandfansPost]) -> dict[str, list[CandfansPost]]:
    monthly_data = defaultdict(list)
    for post in posts:
        monthly_data[post.month].append(post)
    return monthly_data


def _create_post_type_stats(monthly_aggregated_posts: dict[str, list[CandfansPost]]):
    return Stat(
        labels=monthly_aggregated_posts.keys(),
        datasets=[
            DataSet(
                label='公開投稿',
                data=[
                    len([p for p in posts if p.post_type == PostType.PUBLIC_ITEM.value])
                    for posts in monthly_aggregated_posts.values()
                ]
            ),
            DataSet(
                label='限定投稿',
                data=[
                    len(
                        [
                            p for p in posts if p.post_type in [
                                PostType.LIMITED_ACCESS_ITEM.value, PostType.BACK_NUMBER_ITEM.value
                            ]
                        ]
                    )
                    for posts in monthly_aggregated_posts.values()
                ]
            ),
            DataSet(
                label='単品販売',
                data=[
                    len(
                        [
                            p for p in posts if p.post_type in [
                                PostType.INDIVIDUAL_ITEM.value
                            ]
                        ]
                    )
                    for posts in monthly_aggregated_posts.values()
                ]
            ),
        ],
    )


def _create_content_type_stats(monthly_aggregated_posts: dict[str, list[CandfansPost]]):
    return Stat(
        labels=monthly_aggregated_posts.keys(),
        datasets=[
            DataSet(
                label='動画',
                data=[
                    len([p for p in posts if p.contents_type == 2])
                    for posts in monthly_aggregated_posts.values()
                ]
            ),
            DataSet(
                label='写真',
                data=[
                    len([p for p in posts if p.contents_type == 1])
                    for posts in monthly_aggregated_posts.values()
                ]
            ),
        ],
    )


def _create_movie_stats(monthly_aggregated_posts: dict[str, list[CandfansPost]]):
    return Stat(
        labels=monthly_aggregated_posts.keys(),
        datasets=[
            DataSet(
                label='動画時間(分)',
                data=[
                    sum([p.movie_time / 60 for p in posts if p.contents_type == 2])
                    for posts in monthly_aggregated_posts.values()
                ]
            ),
        ]
    )


def _create_photo_stats(monthly_aggregated_posts: dict[str, list[CandfansPost]]):
    return Stat(
        labels=monthly_aggregated_posts.keys(),
        datasets=[
            DataSet(
                label='写真枚数',
                data=[
                    sum([p.image_count for p in posts if p.contents_type == 1])
                    for posts in monthly_aggregated_posts.values()
                ]
            ),
        ]
    )
