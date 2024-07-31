import datetime

from freezegun import freeze_time
from django.test import TransactionTestCase

from modules.analyzer import service as analyzer_sv
from tests.factories.models.candfans_daily_ranking import CandfansCreatorDailyRankingFactory


class CandfansPostServiceTest(TransactionTestCase):

    async def test_get_monthly_post_stats(self):
        user_id = 100
        base_date = datetime.date(2024, 7, 31)
        await CandfansCreatorDailyRankingFactory.create(
            day=datetime.date(2024, 7, 1),
            rank=1,
            user_id=user_id
        )
        await CandfansCreatorDailyRankingFactory.create(
            day=datetime.date(2024, 7, 2),
            rank=2,
            user_id=user_id
        )

        with freeze_time(base_date):
            daily_ranks = await analyzer_sv.get_daily_ranking_list_by_user_id(user_id)
            self.assertEqual(daily_ranks.ranks[0].day, datetime.date(2024, 7, 1))
            self.assertEqual(daily_ranks.ranks[-1].day, datetime.date(2024, 7, 30))
            self.assertEqual(len(daily_ranks.ranks), 30)
            self.assertEqual(len(daily_ranks.valid_ranks), 2)
