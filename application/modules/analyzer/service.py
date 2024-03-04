from typing import Optional

from .domain_models import CandfansUserModel
from .models import CandfansUser
from . import converter


async def create_candfans_user(candfans_user: CandfansUserModel) -> CandfansUserModel:
    created_user = await CandfansUser.create(**candfans_user.model_dump())
    return converter.convert_to_candfans_user_model(created_user)


async def get_candfans_user_by_user_code(user_code: str) -> Optional[CandfansUserModel]:
    candfans_user = await CandfansUser.get_by_user_code(user_code=user_code)
    if not candfans_user:
        return None
    return converter.convert_to_candfans_user_model(candfans_user)


async def get_candfans_user_by_user_id(user_id: int) -> Optional[CandfansUserModel]:
    candfans_user = await CandfansUser.get_by_user_id(user_id=user_id)
    if not candfans_user:
        return None
    return converter.convert_to_candfans_user_model(candfans_user)
