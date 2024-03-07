from .. import converter
from ..models import CandfansPlan
from ..domain_models import CandfansPlanModel


async def create_candfans_plan(plan: CandfansPlanModel) -> CandfansPlanModel:
    params = plan.model_dump(exclude={'user'})
    params['user_id'] = plan.user.user_id
    candfans_plan = await CandfansPlan.create(
        **params
    )
    candfans_plan = await CandfansPlan.get_by_plan_id(candfans_plan.plan_id)
    return converter.convert_to_candfans_plan_model(candfans_plan)
