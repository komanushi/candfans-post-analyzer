import datetime
import enum
from typing import Optional

from candfans_client.models.user import QueriedUser
from django.utils import timezone
from pydantic import BaseModel, conint


EXPIRED_DAYS = 2


class SyncStatus(enum.Enum):
    SYNCING = "SYNCING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"

    @classmethod
    def choices(cls):
        return [(c.value, c.name) for c in cls]


class CandfansUserDetailModel(BaseModel):
    id: Optional[int] = None
    user_id: int
    user_code: str
    username: str
    profile_cover_img: str
    profile_text: str
    profile_img: str
    creater_genre: int
    link_twitter: str
    link_instagram: str
    link_tiktok: str
    link_youtube: str
    link_amazon: str
    link_facebook: str
    link_website: str
    apeal_img1: str
    apeal_img2: str
    apeal_img3: str
    follower_cnt: conint(ge=0)
    follow_cnt: conint(ge=0)
    like_cnt: conint(ge=0)
    fans_cnt: Optional[int]
    post_cnt: conint(ge=0)
    image_cnt: conint(ge=0)
    movie_cnt: conint(ge=0)
    is_follow: bool
    is_followed: bool
    is_fansed: bool
    is_block: bool
    is_blocked: bool
    is_ban: bool
    can_send_dm: bool
    delete_at: Optional[str]
    is_accept_comment: bool
    is_official_creator: bool
    is_on_air: bool
    live_url: str
    created_at: Optional[datetime.datetime] = None

    @classmethod
    def from_candfans_user_info(cls, param: QueriedUser) -> 'CandfansUserDetailModel':
        param_dict = param.model_dump()
        param_dict['user_id'] = param_dict['id']
        del param_dict['id']
        return cls(**param_dict)


class CandfansUserModel(BaseModel):
    user_id: int
    user_code: str
    username: str
    sync_status: Optional[SyncStatus] = None
    last_synced_at: Optional[datetime.datetime] = None
    detail: Optional[CandfansUserDetailModel] = None

    @property
    def is_expire(self) -> bool:
        if self.last_synced_at is None:
            return True
        if (timezone.now() - self.last_synced_at) > datetime.timedelta(days=EXPIRED_DAYS):
            return True
        return False

    @property
    def is_necessary_to_refresh(self) -> bool:
        if self.sync_status is None:
            return True
        if self.is_expire:
            return True
        return False

    @classmethod
    def from_candfans_user_info(cls, param: QueriedUser) -> 'CandfansUserModel':
        return cls(
            user_id=param.id,
            user_code=param.user_code,
            username=param.username,
            sync_status=None,
            last_synced_at=None,
            detail=None,
        )
