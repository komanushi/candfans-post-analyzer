from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import CandfansUserModel, CandfansUserDetailModel
from modules.candfans_gateway import service as cg_sv


async def create_new_candfans_user(user_code: str) -> CandfansUserModel:
    user_info = await cg_sv.get_candfans_user_info_by_user_code(user_code)
    user = user_info.user

    detail = CandfansUserDetailModel(**user.model_dump())
    new_detail = await analyzer_sv.create_candfans_user_detail(detail)

    user_model = await analyzer_sv.create_candfans_user(
        CandfansUserModel.from_candfans_user_info(user)
    )



    # TODO create details
    return user_model


async def sync_user_stats(user_id: int):
    candfans_user = await analyzer_sv.get_candfans_user_by_user_id(user_id)
    print(candfans_user)
    # TODO get timeline
    # TODO save timeline
