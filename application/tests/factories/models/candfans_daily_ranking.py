import factory
from django.utils import timezone

from modules.analyzer.models import CandfansCreatorDailyRanking
from faker import Faker

from .base import AsyncMixin

faker = Faker()


class CandfansRankingCreatorFactory(AsyncMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = CandfansCreatorDailyRanking

    day = timezone.now().date()
    rank = 1
    user_id = factory.Sequence(lambda x: x)
    user_code = factory.Sequence(lambda x: f'user_code_{x}')
    username = factory.Sequence(lambda x: f'username_{x}')
    follow_cnt = 1
    follower_cnt = 2
    like_cnt = 3
    is_official_creator = True
    plans = {}
