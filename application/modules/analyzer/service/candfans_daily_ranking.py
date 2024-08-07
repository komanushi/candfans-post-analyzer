from datetime import timedelta

from django.utils import timezone

from modules.candfans_gateway import service as cg_sv
from ..models import CandfansCreatorDailyRanking
from ..domain_models import DailyRanks, DailyRank


async def save_ranking():
    today = timezone.localtime(timezone.now()).date()
    creators = await cg_sv.get_daily_popular_creator()
    try:
        for i, creator in enumerate(creators):
            await CandfansCreatorDailyRanking.create(
                day=today,
                rank=i + 1,
                user_id=creator.id,
                user_code=creator.user_code,
                username=creator.username,
                profile_img=creator.profile_img,
                profile_text=creator.profile_text,
                follow_cnt=creator.follow_cnt,
                follower_cnt=creator.follower_cnt,
                like_cnt=creator.like_cnt,
                is_official_creator=creator.is_official_creator
            )
    except Exception as e:
        await CandfansCreatorDailyRanking.delete_by_day(today)
        print(f'clean up for {today}')
        raise e


async def get_daily_ranking_list_by_user_id(user_id: int) -> DailyRanks:
    today = timezone.localtime(timezone.now()).date()
    one_month_ago = today - timedelta(days=30)
    date_sets = [one_month_ago + timedelta(days=x) for x in range(30)]
    rank_list = await CandfansCreatorDailyRanking.get_list_by_user_id(user_id)
    date_and_rank_map = {r.day: r.rank for r in rank_list}
    rank_set = [
        DailyRank(
            day=d,
            rank=date_and_rank_map.get(d),
        )
        for d in date_sets
    ]
    return DailyRanks(ranks=rank_set)
