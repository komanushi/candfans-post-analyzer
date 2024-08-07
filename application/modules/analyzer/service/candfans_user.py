import random
from typing import Optional

from django.utils import timezone

from ..domain_models import CandfansUserModel, CandfansUserDetailModel, SyncStatus
from ..models import CandfansUser, CandfansUserDetail
from .. import converter


async def create_candfans_user(
        candfans_user: CandfansUserModel,
        candfans_detail: Optional[CandfansUserDetailModel] = None
) -> CandfansUserModel:
    param = candfans_user.model_dump(exclude={'detail'})
    if candfans_detail and candfans_detail.id is not None:
        param['detail_id'] = candfans_detail.id

    # detailインスタンス再取得
    created_user = await CandfansUser.create(**param)
    created_user = await CandfansUser.get_by_user_id(created_user.user_id)
    return converter.convert_to_candfans_user_model(created_user)


async def create_candfans_user_detail(candfans_user_detail: CandfansUserDetailModel) -> CandfansUserDetailModel:
    dumped = candfans_user_detail.model_dump()
    dumped['user_id'] = dumped['id']
    del dumped['id']
    created_detail = await CandfansUserDetail.create(**candfans_user_detail.model_dump())
    return converter.convert_to_candfans_user_detail_model(created_detail)


async def associate_user_detail(candfans_user: CandfansUserModel, candfans_user_detail: CandfansUserDetailModel):
    user = await CandfansUser.get_by_user_id(candfans_user.user_id)
    assert candfans_user_detail.id is not None
    user.detail_id = candfans_user_detail.id
    await user.asave()
    return converter.convert_to_candfans_user_model(
        await CandfansUser.get_by_user_id(user.user_id)
    )


async def update_user_code(candfans_user: CandfansUserModel):
    await CandfansUser.update(
        user_id=candfans_user.user_id,
        params={
            'user_code': candfans_user.user_code,
        }
    )


async def mark_user_deleted(candfans_user: CandfansUserModel):
    await CandfansUser.update(
        user_id=candfans_user.user_id,
        params={
            'is_deleted': True,
        }
    )


async def set_sync_status(candfans_user: CandfansUserModel, status: SyncStatus) -> CandfansUserModel:
    user = await CandfansUser.get_by_user_id(candfans_user.user_id)
    user.sync_status = status.value
    if status is SyncStatus.FINISHED:
        user.last_synced_at = timezone.now()
    elif status is SyncStatus.SYNCING:
        user.sync_requested_at = timezone.now()
    await user.asave()
    return converter.convert_to_candfans_user_model(user)


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


async def get_recently_synced_candfans_user_list_order_by_last_synced_at(limit: int) -> list[CandfansUserModel]:
    candfans_user_list = await CandfansUser.get_list_order_by_last_synced_at_desc(
        limit=limit + 1
    )
    candidates = [converter.convert_to_candfans_user_model(u)for u in candfans_user_list]
    komachi = await get_candfans_user_by_user_code('koma_showcase')
    candidates = list(set(candidates + [komachi]))
    random.shuffle(candidates)
    return candidates[:limit]


async def get_candfans_user_list_order_by_last_synced_at_asc(limit: int) -> list[CandfansUserModel]:
    candfans_user_list = await CandfansUser.get_list_order_by_last_synced_at_asc(
        limit=limit + 1
    )
    users = [converter.convert_to_candfans_user_model(u)for u in candfans_user_list]
    return users
