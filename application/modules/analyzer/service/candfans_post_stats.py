import itertools
from collections import defaultdict
from submodule.sql import get_query_results_via_model

from ..domain_models import (
    CandfansUserModel,
    Stat,
    MonthlyStats,
    MonthlyPostStats,
    MonthlyPlanStats,
    PlanStats,
    DataSet,
)
from .sql_and_models import (
    TotalPostTypeStatsQuery,
    MonthlyStatsQuery,
    PlanBasedStatsQuery
)

CHART_COLORS = {
  'red': 'rgb(255 99 132)',
  'green': 'rgb(75 192 192)',
  'blue': 'rgb(54 162 235)',
  'orange': 'rgb(255 159 64)',
  'yellow': 'rgb(255 205 86)',
  'purple': 'rgb(153 102 255)',
  'grey': 'rgb(201 203 207)'
}
LIGHT_COLORS = {
  'red': 'rgb(255 99 132 / 50%)',
  'green': 'rgb(75 192 192 / 50%)',
  'blue': 'rgb(54 162 235 / 50%)',
  'orange': 'rgb(255 159 64 / 50%)',
  'yellow': 'rgb(255 205 86 / 50%)',
  'purple': 'rgb(153 102 255 / 50%)',
  'grey': 'rgb(201 203 207 / 50%)'
}

COLOR_KEYS = list(CHART_COLORS.keys())
COLOR_LENGTH = len(CHART_COLORS)


async def get_plan_based_stats(user: CandfansUserModel) -> MonthlyPlanStats:
    plan_based_stats_list: list[PlanStats] = await get_query_results_via_model(
        PlanBasedStatsQuery,
        params=[user.user_id, user.user_id]
    )
    labels = sorted(set([s.month for s in plan_based_stats_list]))
    paid_plan_aggregated_stats: dict[tuple[str, int], list[PlanStats]] = defaultdict(list)
    free_plan_aggregated_stats: list[PlanStats] = []
    free_plan_name = ''
    for stats in plan_based_stats_list:
        if stats.support_price > 0:
            paid_plan_aggregated_stats[(stats.plan_name, stats.support_price)].append(stats)
        else:
            free_plan_name = stats.plan_name
            free_plan_aggregated_stats.append(stats)

    return MonthlyPlanStats(
        plan_post_stats=Stat(
            labels=labels,
            datasets=[
                DataSet(
                    label=f'{plan_name}({support_price}円)',
                    data=[s.total_post_count for s in stats],
                    stack=plan_name,
                    backgroundColor=CHART_COLORS[COLOR_KEYS[i % COLOR_LENGTH]]
                ) for i, ((plan_name, support_price), stats) in enumerate(paid_plan_aggregated_stats.items())
            ] + ([
                DataSet(
                    label=f'{free_plan_name}(0円)',
                    data=[s.total_post_count for s in free_plan_aggregated_stats],
                    stack=free_plan_name,
                    backgroundColor=CHART_COLORS[COLOR_KEYS[len(paid_plan_aggregated_stats) % COLOR_LENGTH]]
                )
            ] if free_plan_name else [])
        ),
        only_paid_plan_post_stats=Stat(
            labels=labels,
            datasets=list(itertools.chain(*[
                [

                    DataSet(
                        label=f'{plan_name}(非バックナンバー)',
                        data=[s.plan_post_count for s in stats],
                        stack=plan_name,
                        backgroundColor=CHART_COLORS[COLOR_KEYS[i % COLOR_LENGTH]]
                    ),
                    DataSet(
                        label=f'{plan_name}(バックナンバー)',
                        data=[s.backnumber_post_count for s in stats],
                        stack=plan_name,
                        backgroundColor=LIGHT_COLORS[COLOR_KEYS[i % COLOR_LENGTH]]
                    )
                ]
                for i, ((plan_name, support_price), stats) in enumerate(paid_plan_aggregated_stats.items())
            ]))
        ),
        # plan_post_summary=PlanPostSummary(
        #     total_current_post_count=sum([s.total_current_post_count for s in plan_based_stats_list]),
        #     total_backnumber_post_count=sum([s.total_backnumber_post_count for s in plan_based_stats_list]),
        #     total_current_photo_post_count=sum([s.total_current_photo_post_count for s in plan_based_stats_list]),
        #     total_backnumber_photo_post_count=sum([s.total_backnumber_photo_post_count for s in plan_based_stats_list]),
        #     total_current_movie_post_count=sum([s.total_current_movie_post_count for s in plan_based_stats_list]),
        #     total_backnumber_movie_post_count=sum([s.total_backnumber_movie_post_count for s in plan_based_stats_list]),
        #     total_current_photo_count=sum([s.total_current_photo_count for s in plan_based_stats_list]),
        #     total_backnumber_photo_count=sum([s.total_backnumber_photo_count for s in plan_based_stats_list]),
        #     total_current_movie_time_sec=sum([s.total_current_movie_time_sec for s in plan_based_stats_list]),
        #     total_backnumber_movie_time_sec=sum([s.total_backnumber_movie_time_sec for s in plan_based_stats_list]),
        # ),
    )


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

