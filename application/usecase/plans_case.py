from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import CandfansPlanModel, CandfansUserModel
from modules.candfans_gateway import service as cg_sv


async def resync_candfans_plan(user_code: str) -> list[CandfansPlanModel]:
    user_info = await cg_sv.get_candfans_user_info_by_user_code(user_code=user_code)
    user = user_info.user
    plans = user_info.plans
    user_model = CandfansUserModel.from_candfans_user_info_api(user)
    plan_models = [CandfansPlanModel.from_candfans_plan_api(p, user_model) for p in plans]
    return await analyzer_sv.sync_candfans_plan(plans=plan_models, user=user_model)
