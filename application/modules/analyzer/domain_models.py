import datetime
import enum
import json
from typing import Optional

from candfans_client.models.user import QueriedUser, Plan
from django.conf import settings
from django.utils import timezone
from pydantic import BaseModel, conint, conlist


EXPIRED_DAYS = settings.SYNC_EXPIRED_DAYS
SYNC_MUST_BE_FINISH_HOUR = 1


class SyncStatus(enum.Enum):
    SYNCING = "SYNCING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"

    @property
    def label(self):
        return {
            self.SYNCING: '同期中',
            self.FINISHED: '同期完了',
            self.ERROR: '同期失敗',
        }[self]

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
    sync_requested_at: Optional[datetime.datetime] = None
    last_synced_at: Optional[datetime.datetime] = None
    detail: Optional[CandfansUserDetailModel] = None

    def __hash__(self) -> int:
        return self.user_id.__hash__()

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
        # 同期が1時間終わらないのはおかしい
        if self.sync_status is SyncStatus.SYNCING:
            return (timezone.now() - self.sync_requested_at) > datetime.timedelta(hours=SYNC_MUST_BE_FINISH_HOUR)
        # 同期が完了しているなら期限切れまでは保持する
        if self.is_expire:
            return True
        return False

    @classmethod
    def from_candfans_user_info_api(cls, param: QueriedUser) -> 'CandfansUserModel':
        return cls(
            user_id=param.id,
            user_code=param.user_code,
            username=param.username,
            sync_status=None,
            sync_requested_at=None,
            last_synced_at=None,
            detail=None,
        )


class CandfansPlanModel(BaseModel):
    plan_id: int
    user: CandfansUserModel
    thanks_message_template_id: Optional[int]
    plan_name: str
    support_price: int
    total_support_price: int
    plan_detail: str
    status: int
    fans_cnt: Optional[int]
    is_fans: bool
    is_price_update: Optional[int]
    change_support_price: Optional[int]
    content_length: int
    delete_at: Optional[datetime.datetime]
    backnumber_price: Optional[int]
    limit_after_backnumber: int
    this_month_after_backnumber: int
    can_see_backnumber_plan_pay: bool
    can_buy_backnumber_not_entry_plan: bool
    done_transfar_backnumber: bool
    done_transfar_limit_backnumber: bool
    entry_disabled: bool
    upper_limit_entry_cnt: Optional[int]

    @classmethod
    def from_candfans_plan_api(cls, param: Plan, user: CandfansUserModel):
        return cls(
            plan_id=param.plan_id,
            user=user,
            thanks_message_template_id=param.thanks_message_template_id,
            plan_name=param.plan_name,
            support_price=param.support_price,
            total_support_price=param.total_support_price,
            plan_detail=param.plan_detail,
            status=param.status,
            fans_cnt=param.fans_cnt,
            is_fans=param.is_fans,
            is_price_update=param.is_price_update,
            change_support_price=param.change_support_price,
            content_length=param.content_length,
            delete_at=param.delete_at,
            backnumber_price=param.backnumber_price,
            limit_after_backnumber=param.limit_after_backnumber,
            this_month_after_backnumber=param.this_month_after_backnumber,
            can_see_backnumber_plan_pay=param.can_see_backnumber_plan_pay,
            can_buy_backnumber_not_entry_plan=param.can_buy_backnumber_not_entry_plan,
            done_transfar_backnumber=param.done_transfar_backnumber,
            done_transfar_limit_backnumber=param.done_transfar_limit_backnumber,
            entry_disabled=param.entry_disabled,
            upper_limit_entry_cnt=param.upper_limit_entry_cnt,
        )


class DataSet(BaseModel):
    label: str
    data: list[int | float]
    stack: Optional[str] = None
    backgroundColor: Optional[str] = None


class Stat(BaseModel):
    labels: list[str]
    datasets: list[DataSet]


class MonthlyPostStats(BaseModel):
    month: str
    public_item: int
    plan_item: int
    individual_item: int
    photo_item: int
    movie_item: int
    free_plan_item: int
    paid_plan_item: int
    free_movie_time_sec: float
    paid_movie_time_sec: float
    free_photo_count: int
    paid_photo_count: int

    @property
    def free_movie_time(self):
        return self.free_movie_time_sec / 60

    @property
    def paid_movie_time(self):
        return self.paid_movie_time_sec / 60


class PostTypeStat(BaseModel):
    public_item: int
    limited_access_item: int
    individual_item: int
    back_number_item: int

    @property
    def total_item(self):
        return (
            self.public_item
            + self.limited_access_item
            + self.individual_item
            + self.back_number_item
        )


class MonthlyStats(BaseModel):
    total_post_type_stats: PostTypeStat
    monthly_post_type_stats: Stat
    monthly_content_type_stats: Stat
    monthly_limited_item_stats: Stat
    movie_stats: Stat
    photo_stats: Stat


class PlanSummaryModel(BaseModel):
    plan_id: int
    plan_name: str
    support_price: int
    plan_detail: str
    backnumber_price: Optional[int]


class PlanStats(BaseModel):
    month: str
    plan_name: str
    plan_id: int
    support_price: int
    backnumber_price: Optional[int]
    total_post_count: int
    plan_post_count: int
    backnumber_post_count: int
    plan_movie_post_count: int
    backnumber_movie_post_count: int
    plan_movie_time_sec: float
    backnumber_movie_time_sec: float
    plan_photo_post_count: int
    backnumber_photo_post_count: int
    plan_photo_count: int
    backnumber_photo_count: int

    @property
    def plan_movie_time(self):
        return self.plan_movie_time_sec / 60

    @property
    def backnumber_movie_time(self):
        return self.backnumber_movie_time_sec / 60


class PlanPostSummary(BaseModel):
    plan_name: str
    support_price: int
    backnumber_price: Optional[int]
    first_month: str
    total_plan_post_count: int
    total_backnumber_post_count: int
    total_plan_photo_post_count: int
    total_backnumber_photo_post_count: int
    total_plan_movie_post_count: int
    total_backnumber_movie_post_count: int
    total_plan_photo_count: int
    total_backnumber_photo_count: int
    total_plan_movie_time_sec: float
    total_backnumber_movie_time_sec: float

    @property
    def total_plan_movie_time(self):
        return self.total_plan_movie_time_sec / 60

    @property
    def total_plan_movie_hour(self):
        return self.total_plan_movie_time_sec / 60 / 60

    @property
    def total_backnumber_movie_time(self):
        return self.total_backnumber_movie_time_sec / 60

    @property
    def total_backnumber_movie_hour(self):
        return self.total_backnumber_movie_time_sec / 60 / 60


class MonthlyPlanStats(BaseModel):
    plan_post_stats: Stat
    plan_photo_post_count_stats: Stat
    plan_photo_count_stats: Stat
    plan_movie_post_count_stats: Stat
    plan_movie_time_stats: Stat


class DailyRank(BaseModel):
    day: datetime.date
    rank: Optional[int]


class DailyRanks(BaseModel):
    ranks: conlist(DailyRank, min_length=30, max_length=30)

    @property
    def valid_ranks(self):
        return [r for r in self.ranks if r.rank is not None]

    @property
    def formated_ranks(self):
        return [
            r.rank if r.rank is not None else 101
            for r in self.ranks
        ]

    @property
    def rank_json(self):
        return json.dumps({
            'labels': [r.day.isoformat() for r in self.ranks],
            'datasets': [{
                'label': 'デイリー順位',
                'data': self.formated_ranks,
            }],
        }, indent=4)
