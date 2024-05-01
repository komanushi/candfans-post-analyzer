from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import (
    CandfansUserModel,
    CandfansUserDetailModel,
    CandfansPlanModel,
    SyncStatus
)
from modules.candfans_gateway import service as cg_sv
from .plans_case import resync_candfans_plan


async def create_new_candfans_user(user_code: str) -> tuple[CandfansUserModel, list[CandfansPlanModel]]:
    user_info = await cg_sv.get_candfans_user_info_by_user_code(user_code)
    user = user_info.user
    plans = user_info.plans

    new_detail = await analyzer_sv.create_candfans_user_detail(
        CandfansUserDetailModel.from_candfans_user_info(user)
    )

    # user_codeは変化し得るのでuser_idで引き直す
    user_model = await analyzer_sv.get_candfans_user_by_user_id(user.id)
    if user_model:
        user_model.user_code = user_code
        await analyzer_sv.update_user_code(candfans_user=user_model)
        user_model = await analyzer_sv.associate_user_detail(
            candfans_user=user_model,
            candfans_user_detail=new_detail,
        )
    else:
        user_model = await analyzer_sv.create_candfans_user(
            CandfansUserModel.from_candfans_user_info_api(user),
            candfans_detail=new_detail,
        )

    created_plans = []
    for plan in plans:
        created_plan = await analyzer_sv.create_candfans_plan(CandfansPlanModel.from_candfans_plan_api(
            param=plan,
            user=user_model
        ))
        created_plans.append(created_plan)

    return user_model, created_plans


async def sync_user_stats(user_id: int):
    print(f'start sync_user_stats for {user_id=}')
    candfans_user = await analyzer_sv.get_candfans_user_by_user_id(user_id)
    print(f'target user_code={candfans_user.user_code}')

    # if not candfans_user.is_necessary_to_refresh:
    #     print(f'SKIP {candfans_user.is_necessary_to_refresh=}')
    #     return

    await resync_candfans_plan(candfans_user.user_code)
    timeline_map = await cg_sv.get_timelines(user_id=user_id)
    target_posts = []
    for t_post in timeline_map:
        target_posts.extend(t_post.post_map.all_posts)

    new_post_count = await analyzer_sv.update_or_create_candfans_post(target_posts)
    await analyzer_sv.set_sync_status(candfans_user, status=SyncStatus.FINISHED)
    print(f'end sync_user_stats for {user_id=}, {new_post_count=}')
