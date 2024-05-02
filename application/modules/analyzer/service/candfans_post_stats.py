from collections import defaultdict
from datetime import timedelta, datetime
from candfans_client.models.timeline import Post, PostType

from ..domain_models import (
    CandfansUserModel,
    Stat,
    MonthlyStats,
    MonthlyPostStats,
    DataSet,
)
from modules.analyzer.service.candfans_plan import get_candfans_plans_by_user
from modules.analyzer.models import CandfansPost, CandFansPostPlanRelation
from modules.analyzer.converter import (
    convert_from_candfans_post_to_post
)

from submodule.sql import get_query_results_via_model

from .sql_and_models.total_post_type_stats import TotalPostTypeStatsQuery
from .sql_and_models.monthly_stats import MonthlyStatsQuery


async def get_monthly_post_stats(user: CandfansUserModel) -> MonthlyStats:
    total_post_type_stats = await get_query_results_via_model(
        TotalPostTypeStatsQuery,
        params=[user.user_id]
    )
    monthly_post_stats_list: list[MonthlyPostStats] = await get_query_results_via_model(
        MonthlyStatsQuery,
        params=[user.user_id, user.user_id]
    )
    label = [s.month for s in monthly_post_stats_list]
    return MonthlyStats(
        total_post_type_stats=total_post_type_stats[0],
        monthly_post_type_stats=Stat(
            labels=label,
            datasets=[
                DataSet(
                    label='公開投稿',
                    data=[s.public_item for s in monthly_post_stats_list]
                ),
                DataSet(
                    label='プラン限定投稿',
                    data=[s.plan_item for s in monthly_post_stats_list]
                ),
                DataSet(
                    label='単品販売',
                    data=[s.individual_item for s in monthly_post_stats_list]
                ),
            ],
        ),
        monthly_content_type_stats=Stat(
            labels=label,
            datasets=[
                DataSet(
                    label='動画',
                    data=[s.movie_item for s in monthly_post_stats_list]
                ),
                DataSet(
                    label='写真',
                    data=[s.photo_item for s in monthly_post_stats_list]
                ),
            ]
        ),
        monthly_limited_item_stats=Stat(
            labels=label,
            datasets=[
                DataSet(
                    label='無料プラン',
                    data=[s.free_plan_item for s in monthly_post_stats_list]
                ),
                DataSet(
                    label='有料プラン',
                    data=[s.paid_plan_item for s in monthly_post_stats_list]
                ),
            ]
        ),
        movie_stats=Stat(
            labels=label,
            datasets=[
                DataSet(
                    label='無料動画時間(分)',
                    data=[s.free_movie_time for s in monthly_post_stats_list]
                ),
                DataSet(
                    label='有料動画時間(分)',
                    data=[s.paid_movie_time for s in monthly_post_stats_list]
                ),
            ]
        ),
        photo_stats=Stat(
            labels=label,
            datasets=[
                DataSet(
                    label='無料写真枚数',
                    data=[s.free_photo_count for s in monthly_post_stats_list]
                ),
                DataSet(
                    label='有料写真枚数',
                    data=[s.paid_photo_count for s in monthly_post_stats_list]
                ),
            ]
        ),
    )

