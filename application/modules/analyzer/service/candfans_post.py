from collections import defaultdict
from datetime import timedelta, datetime
from candfans_client.models.timeline import Post, PostType, ShortPlan

from ..domain_models import (
    CandfansUserModel,
    Stat,
    MonthlyStats,
    DataSet, PostTypeStat,
)
from .candfans_plan import get_candfans_plans_by_user
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


async def get_monthly_post_stats(user: CandfansUserModel) -> MonthlyStats:
    posts = await CandfansPost.get_list_by_user_id(user_id=user.user_id)
    plans = await get_candfans_plans_by_user(user=user)
    plan_id_map = {p.plan_id: p for p in plans}
    rels = await CandFansPostPlanRelation.get_list_by_post_ids(candfans_post_ids=[p.post_id for p in posts])
    post_rel_map = defaultdict(list)
    for rel in rels:
        post_rel_map[rel.candfans_post_id].append(plan_id_map.get(int(rel.candfans_plan_id)))
    posts = [convert_from_candfans_post_to_post(p, post_rel_map.get(p.post_id, [])) for p in posts]
    monthly_aggregated = _aggregate_monthly(posts)
    return MonthlyStats(
        total_post_type_stats=PostTypeStat(
            public_item=len([p for p in posts if p.post_type == PostType.PUBLIC_ITEM.value]),
            limited_access_item=len([p for p in posts if p.post_type == PostType.LIMITED_ACCESS_ITEM.value]),
            individual_item=len([p for p in posts if p.post_type == PostType.INDIVIDUAL_ITEM.value]),
            back_number_item=len([p for p in posts if p.post_type == PostType.BACK_NUMBER_ITEM.value]),
        ),
        monthly_post_type_stats=_create_post_type_stats(monthly_aggregated),
        monthly_content_type_stats=_create_content_type_stats(monthly_aggregated),
        monthly_limited_item_stats=_create_limited_item_stats(monthly_aggregated),
        movie_stats=_create_movie_stats(monthly_aggregated),
        photo_stats=_create_photo_stats(monthly_aggregated),
    )


def _aggregate_monthly(posts: list[Post]) -> dict[str, list[Post]]:
    posts = sorted(posts, key=lambda p: p.month)
    if not posts:
        return {}
    # 1ヶ月投稿がない月が発生するとそこがグラフから消えるので範囲内の月を列挙する
    min_month = datetime.strptime(posts[0].month, '%Y-%m')
    max_month = datetime.strptime(posts[-1].month, '%Y-%m')
    months = set()
    for d in range((max_month - min_month).days):
        months.add(
            (min_month + timedelta(days=d+1)).strftime('%Y-%m')
        )
    monthly_data = {m: [] for m in sorted(months)}
    for post in posts:
        monthly_data[post.month].append(post)

    return monthly_data


def _is_free(post: Post) -> bool:
    plans = post.plans
    if post.post_type == PostType.PUBLIC_ITEM.value:
        return True
    if any([p.support_price == 0 for p in plans]):
        return True
    return False


def _create_post_type_stats(aggregated_posts: dict[str, list[Post]]):
    return Stat(
        labels=aggregated_posts.keys(),
        datasets=[
            DataSet(
                label='公開投稿',
                data=[
                    len([p for p in posts if p.post_type == PostType.PUBLIC_ITEM.value])
                    for posts in aggregated_posts.values()
                ]
            ),
            DataSet(
                label='プラン限定投稿',
                data=[
                    len(
                        [
                            p for p in posts if p.post_type in [
                                PostType.LIMITED_ACCESS_ITEM.value, PostType.BACK_NUMBER_ITEM.value
                            ]
                        ]
                    )
                    for posts in aggregated_posts.values()
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
                    for posts in aggregated_posts.values()
                ]
            ),
        ],
    )


def _create_content_type_stats(aggregated_posts: dict[str, list[Post]]):
    return Stat(
        labels=aggregated_posts.keys(),
        datasets=[
            DataSet(
                label='動画',
                data=[
                    len([p for p in posts if p.contents_type == 2])
                    for posts in aggregated_posts.values()
                ]
            ),
            DataSet(
                label='写真',
                data=[
                    len([p for p in posts if p.contents_type == 1])
                    for posts in aggregated_posts.values()
                ]
            ),
        ],
    )


def _create_movie_stats(aggregated_posts: dict[str, list[Post]]):
    return Stat(
        labels=aggregated_posts.keys(),
        datasets=[
            DataSet(
                label='無料動画時間(分)',
                data=[
                    sum([p.movie_time / 60 for p in posts if (
                        p.contents_type == 2
                        and _is_free(p)
                        and p.post_type != PostType.INDIVIDUAL_ITEM
                    )])
                    for posts in aggregated_posts.values()
                ]
            ),
            DataSet(
                label='有料動画時間(分)',
                data=[
                    sum([p.movie_time / 60 for p in posts if (
                        p.contents_type == 2
                        and not _is_free(p)
                        and p.post_type != PostType.INDIVIDUAL_ITEM
                    )])
                    for posts in aggregated_posts.values()
                ]
            ),
        ]
    )


def _create_photo_stats(aggregated_posts: dict[str, list[Post]]):
    return Stat(
        labels=aggregated_posts.keys(),
        datasets=[
            DataSet(
                label='無料写真枚数',
                data=[
                    sum([p.image_count for p in posts if (
                        p.contents_type == 1
                        and _is_free(p)
                        and p.post_type != PostType.INDIVIDUAL_ITEM
                    )])
                    for posts in aggregated_posts.values()
                ]
            ),
            DataSet(
                label='有料写真枚数',
                data=[
                    sum([p.image_count for p in posts if (
                        p.contents_type == 1
                        and not _is_free(p)
                        and p.post_type != PostType.INDIVIDUAL_ITEM
                    )])
                    for posts in aggregated_posts.values()
                ]
            ),
        ]
    )


def _create_limited_item_stats(
    aggregated_posts: dict[str, list[Post]]
):

    return Stat(
        labels=aggregated_posts.keys(),
        datasets=[
            DataSet(
                label='無料プラン',
                data=[
                    len([
                        p for p in posts
                        if p.post_type in [
                            PostType.LIMITED_ACCESS_ITEM.value, PostType.BACK_NUMBER_ITEM.value
                        ]
                        and _is_free(p)
                    ])
                    for posts in aggregated_posts.values()
                ]
            ),
            DataSet(
                label='有料プラン',
                data=[
                    len([
                        p for p in posts
                        if p.post_type in [
                            PostType.LIMITED_ACCESS_ITEM.value, PostType.BACK_NUMBER_ITEM.value
                        ]
                        and not _is_free(p)
                    ])
                    for posts in aggregated_posts.values()
                ]
            ),
        ],
    )
