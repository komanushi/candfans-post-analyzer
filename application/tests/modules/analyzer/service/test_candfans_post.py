import freezegun
from django.test import TestCase
from django.utils import timezone

from modules.analyzer.service import candfans_post as candfans_post_sv
from tests.factories.models.candfans_user import CandfansUserFactory
from tests.factories.domain_models.candfans_gateway import PostFactory
from tests.factories.domain_models.analyzer import (
    CandfansUserDetailModelFactory,
    CandfansPlanModelFactory,
)


class CandfansPostServiceTest(TestCase):

    async def test__aggregate_monthly(self):
        posts = [
            PostFactory.create(month='2024-01'),
            PostFactory.create(month='2024-02'),
            PostFactory.create(month='2024-02'),
            PostFactory.create(month='2024-03'),
            PostFactory.create(month='2024-03'),
            PostFactory.create(month='2024-03'),
        ]
        aggregated = candfans_post_sv._aggregate_monthly(posts)
        self.assertEqual(len(aggregated.keys()), 3)
        self.assertEqual(sum([len(x) for x in aggregated.values()]), len(posts))

    async def test__aggregate_monthly_with_lack(self):
        # 2024-02が投稿がなかった場合
        posts = [
            PostFactory.create(month='2024-01'),
            PostFactory.create(month='2024-03'),
            PostFactory.create(month='2024-03'),
            PostFactory.create(month='2024-03'),
        ]
        aggregated = candfans_post_sv._aggregate_monthly(posts)
        self.assertEqual(len(aggregated.keys()), 3)
        self.assertEqual(sum([len(x) for x in aggregated.values()]), len(posts))
