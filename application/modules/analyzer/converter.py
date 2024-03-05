from .models import CandfansUser, CandfansUserDetail
from .domain_models import CandfansUserModel, CandfansUserDetailModel


def convert_to_candfans_user_model(user: CandfansUser) -> CandfansUserModel:
    return CandfansUserModel(
        user_id=user.user_id,
        user_code=user.user_code,
        username=user.username,
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
