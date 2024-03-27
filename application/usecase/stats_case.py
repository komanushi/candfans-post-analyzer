from pydantic import BaseModel, json

from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import (
    CandfansPlanModel,
    CandfansUserModel,
    MonthlyStats,
    PlanSummaryModel
)


class UserStats(BaseModel):
    monthly_stats: MonthlyStats
    summary_monthly_stats_json: str
    plan_summaries: list[PlanSummaryModel]


async def generate_stats(candfans_user: CandfansUserModel) -> UserStats:
    monthly_stats = await analyzer_sv.get_monthly_post_stats(user=candfans_user)
    plan_summaries = await analyzer_sv.get_candfans_plan_summaries_by_user(candfans_user)

    return UserStats(
        monthly_stats=monthly_stats,
        summary_monthly_stats_json=monthly_stats.model_dump_json(indent=4),
        plan_summaries=plan_summaries,
    )
