from candfans_client.models.timeline import Post, ShortPlan

from .models import (
    CandfansUser,
    CandfansUserDetail,
    CandfansPlan,
    CandfansPost,
)
from .domain_models import (
    CandfansUserModel,
    CandfansUserDetailModel,
    CandfansPlanModel,
    SyncStatus,
    PlanSummaryModel
)


def convert_to_candfans_user_model(user: CandfansUser) -> CandfansUserModel:
    return CandfansUserModel(
        user_id=user.user_id,
        user_code=user.user_code,
        username=user.username,
        sync_status=SyncStatus(user.sync_status) if user.sync_status else None,
        sync_requested_at=user.sync_requested_at,
        last_synced_at=user.last_synced_at,
        detail=convert_to_candfans_user_detail_model(user.detail) if user.detail else None
    )


def convert_to_candfans_user_detail_model(detail: CandfansUserDetail) -> CandfansUserDetailModel:
    return CandfansUserDetailModel(
        id=detail.id,
        user_id=detail.user_id,
        user_code=detail.user_code,
        username=detail.username,
        profile_cover_img=detail.profile_cover_img,
        profile_text=detail.profile_text,
        profile_img=detail.profile_img,
        creater_genre=detail.creater_genre,
        link_twitter=detail.link_twitter,
        link_instagram=detail.link_instagram,
        link_tiktok=detail.link_tiktok,
        link_youtube=detail.link_youtube,
        link_amazon=detail.link_amazon,
        link_facebook=detail.link_facebook,
        link_website=detail.link_website,
        apeal_img1=detail.apeal_img1,
        apeal_img2=detail.apeal_img2,
        apeal_img3=detail.apeal_img3,
        follower_cnt=detail.follower_cnt,
        follow_cnt=detail.follow_cnt,
        like_cnt=detail.like_cnt,
        fans_cnt=detail.fans_cnt,
        post_cnt=detail.post_cnt,
        image_cnt=detail.image_cnt,
        movie_cnt=detail.movie_cnt,
        is_follow=detail.is_follow,
        is_followed=detail.is_followed,
        is_fansed=detail.is_fansed,
        is_block=detail.is_block,
        is_blocked=detail.is_blocked,
        is_ban=detail.is_ban,
        can_send_dm=detail.can_send_dm,
        delete_at=detail.delete_at,
        is_accept_comment=detail.is_accept_comment,
        is_official_creator=detail.is_official_creator,
        is_on_air=detail.is_on_air,
        live_url=detail.live_url,
        created_at=detail.created_at,
    )


def convert_to_candfans_plan_model(plan: CandfansPlan) -> CandfansPlanModel:
    return CandfansPlanModel(
        plan_id=plan.plan_id,
        user=convert_to_candfans_user_model(plan.user),
        thanks_message_template_id=plan.thanks_message_template_id,
        plan_name=plan.plan_name,
        support_price=plan.support_price,
        total_support_price=plan.total_support_price,
        plan_detail=plan.plan_detail,
        status=plan.status,
        fans_cnt=plan.fans_cnt,
        is_fans=plan.is_fans,
        is_price_update=plan.is_price_update,
        change_support_price=plan.change_support_price,
        content_length=plan.content_length,
        delete_at=plan.delete_at,
        backnumber_price=plan.backnumber_price,
        limit_after_backnumber=plan.limit_after_backnumber,
        this_month_after_backnumber=plan.this_month_after_backnumber,
        can_see_backnumber_plan_pay=plan.can_see_backnumber_plan_pay,
        can_buy_backnumber_not_entry_plan=plan.can_buy_backnumber_not_entry_plan,
        done_transfar_backnumber=plan.done_transfar_backnumber,
        done_transfar_limit_backnumber=plan.done_transfar_limit_backnumber,
        entry_disabled=plan.entry_disabled,
        upper_limit_entry_cnt=plan.upper_limit_entry_cnt,
    )


def convert_to_plan_summary(plan: CandfansPlan) -> PlanSummaryModel:
    return PlanSummaryModel(
        plan_id=plan.plan_id,
        plan_name=plan.plan_name,
        support_price=plan.support_price,
        plan_detail=plan.plan_detail,
        backnumber_price=plan.backnumber_price,
    )


def convert_from_post_to_candfans_post(post: Post) -> CandfansPost:
    return CandfansPost(
        month=post.month,
        post_id=post.post_id,
        user_id=post.user_id,
        user_code=post.user_code,
        username=post.username,
        profile_img=post.profile_img,
        profile_cover_img=post.profile_cover_img,
        post_date=post.post_date,
        contents_type=post.contents_type,
        post_type=post.post_type,
        contents_text=post.contents_text,
        over_contents_50str=post.over_contents_50str,
        price=post.price,
        limit_post_date=post.limit_post_date,
        reserve_post_date=post.reserve_post_date,
        contents_path1=post.contents_path1,
        contents_path2=post.contents_path2,
        contents_path3=post.contents_path3,
        contents_path4=post.contents_path4,
        image_count=post.attachment_length if post.contents_type == 1 else 0,
        movie_time=post.movie_time,
        secret_file=post.secret_file,
        thumbnail_file=post.thumbnail_file,
        like_cnt=post.like_cnt,
        comments_cnt=post.comments_cnt,
        chip_cnt=0,
        is_like=post.is_like,
        can_browsing=post.can_browsing,
        can_send_chip=post.can_send_chip,
        apply_status=post.apply_status,
        is_progressed=post.is_progressed,
        is_accept_comment=post.is_accept_comment,
        can_read_text=post.can_read_text,
        is_official_creator=post.is_official_creator,
        has_own_thumbnail=post.has_own_thumbnail,
        is_on_air=post.is_on_air,
        live_url=post.live_url,
    )


def convert_from_candfans_post_to_post(post: CandfansPost, plans: list[CandfansPlan]) -> Post:
    return Post(
        month=post.month,
        post_id=post.post_id,
        user_id=post.user_id,
        user_code=post.user_code,
        username=post.username,
        profile_img=post.profile_img,
        profile_cover_img=post.profile_cover_img,
        post_date=post.post_date,
        contents_type=post.contents_type,
        post_type=post.post_type,
        contents_text=post.contents_text,
        over_contents_50str=post.over_contents_50str,
        price=post.price,
        limit_post_date=post.limit_post_date,
        reserve_post_date=post.reserve_post_date,
        contents_path1=post.contents_path1,
        contents_path2=post.contents_path2,
        contents_path3=post.contents_path3,
        contents_path4=post.contents_path4,
        image_count=post.image_count,
        movie_time=post.movie_time,
        secret_file=post.secret_file,
        thumbnail_file=post.thumbnail_file,
        like_cnt=post.like_cnt,
        comments_cnt=post.comments_cnt,
        is_like=post.is_like,
        can_browsing=post.can_browsing,
        can_send_chip=post.can_send_chip,
        apply_status=post.apply_status,
        is_progressed=post.is_progressed,
        is_accept_comment=post.is_accept_comment,
        can_read_text=post.can_read_text,
        is_official_creator=post.is_official_creator,
        has_own_thumbnail=post.has_own_thumbnail,
        is_on_air=post.is_on_air,
        live_url=post.live_url,
        plans=[
            ShortPlan(
                plan_id=p.plan_id,
                support_price=p.support_price,
                total_support_price=p.total_support_price,
                plan_name=p.plan_name,
                plan_detail=p.plan_detail,
                backnumber_id=None,
                backnumber_price=p.backnumber_price,
                total_backnumber_price=None,
                can_see_backnumber_plan_pay=p.can_see_backnumber_plan_pay,
                can_buy_backnumber_not_entry_plan=p.can_buy_backnumber_not_entry_plan,
                add_backnumber_date=None,
                is_joined_plan=False
            )
            for p in plans
        ],
    )
