from pydantic import BaseModel

from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import (
    CandfansUserModel,
    MonthlyStats,
    PlanSummaryModel,
    PlanPostSummary
)


class UserStats(BaseModel):
    monthly_stats: MonthlyStats
    plan_summaries: list[PlanSummaryModel]
    plan_post_summary_map: dict[str, PlanPostSummary]


async def generate_stats(candfans_user: CandfansUserModel) -> UserStats:
    monthly_stats = await analyzer_sv.get_monthly_post_stats(user=candfans_user)
    plan_summaries = await analyzer_sv.get_candfans_plan_summaries_by_user(candfans_user)
    _, plan_post_summary_map = await analyzer_sv.get_plan_based_stats(candfans_user)
    return UserStats(
        monthly_stats=monthly_stats,
        plan_summaries=plan_summaries,
        plan_post_summary_map=plan_post_summary_map,
    )
