from django.utils import timezone

from modules.candfans_gateway import service as cg_sv
from ..models import CandfansCreatorDailyRanking


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
