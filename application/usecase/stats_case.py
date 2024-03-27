from pydantic import BaseModel, json

from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import (
    CandfansPlanModel,
    CandfansUserModel,
    Stats,
    PlanSummaryModel
)


class UserStats(BaseModel):
    stats: Stats
    summary_stats_json: str
    plan_summaries: list[PlanSummaryModel]


async def generate_stats(candfans_user: CandfansUserModel):
    post_stats = await analyzer_sv.get_post_stats(user=candfans_user)
    plan_summaries = await analyzer_sv.get_candfans_plan_summaries_by_user(candfans_user)

    return UserStats(
        stats=post_stats,
        summary_stats_json=post_stats.model_dump_json(indent=4),
        plan_summaries=plan_summaries,
    )
