from .. import converter
from ..models import CandfansPlan, CandfansPlanFansHistory
from ..domain_models import (
    CandfansPlanModel,
    CandfansUserModel,
)


async def create_candfans_plan(plan: CandfansPlanModel) -> CandfansPlanModel:
    params = plan.model_dump(exclude={'user'})
    params['user_id'] = plan.user.user_id
    candfans_plan = await CandfansPlan.create(
        **params
    )
    candfans_plan = await CandfansPlan.get_by_plan_id(candfans_plan.plan_id)
    await CandfansPlanFansHistory.create(candfans_plan)
    return converter.convert_to_candfans_plan_model(candfans_plan)


async def sync_candfans_plan(plans: list[CandfansPlanModel], user: CandfansUserModel) -> list[CandfansPlanModel]:
    new_plans = []
    for plan in plans:
        params = plan.model_dump(exclude={'user'})
        params['user_id'] = plan.user.user_id
        new_plan = await CandfansPlan.update_or_create(**params)
        new_plan = await CandfansPlan.get_by_plan_id(new_plan.plan_id)
        await CandfansPlanFansHistory.create(new_plan)
        new_plans.append(new_plan)
    await CandfansPlan.delete_by_user_id_and_exclude_plan_ids(
        user_id=user.user_id,
        exclude_plan_ids=[p.plan_id for p in plans]
    )
    return [converter.convert_to_candfans_plan_model(p) for p in new_plans]
