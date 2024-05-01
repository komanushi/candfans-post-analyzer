from django.test import TransactionTestCase

from candfans_client.models.timeline import PostType

from modules.analyzer.domain_models import PostTypeStat, DataSet
from modules.analyzer.service import candfans_post_stats as candfans_post_stats_sv
from tests.factories.models.candfans_user import CandfansUserFactory
from tests.factories.models.candfans_plan import CandfansPlanFactory
from tests.factories.models.candfans_post import CandfansPostFactory
from tests.factories.models.candfans_post_plan_relation import CandFansPostPlanRelationFactory
from tests.factories.domain_models.candfans_gateway import PostFactory


class CandfansPostServiceTest(TransactionTestCase):

    async def test__aggregate_monthly(self):
        posts = [
            PostFactory.create(month='2024-01'),
            PostFactory.create(month='2024-02'),
            PostFactory.create(month='2024-02'),
            PostFactory.create(month='2024-03'),
            PostFactory.create(month='2024-03'),
            PostFactory.create(month='2024-03'),
        ]
        aggregated = candfans_post_stats_sv._aggregate_monthly(posts)
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
        aggregated = candfans_post_stats_sv._aggregate_monthly(posts)
        self.assertEqual(len(aggregated.keys()), 3)
        self.assertEqual(sum([len(x) for x in aggregated.values()]), len(posts))

    async def test_get_monthly_post_stats(self):
        user = await CandfansUserFactory.create()
        free = await CandfansPlanFactory.create(user=user, support_price=0)
        non_free = await CandfansPlanFactory.create(user=user, support_price=1000)
        PHOTO = 1
        MOVIE = 2
        post_attrs = [
            {'month': '2024-01', 'post_type': PostType.LIMITED_ACCESS_ITEM.value, 'contents_type': PHOTO, 'is_free': True},
            {'month': '2024-01', 'post_type': PostType.PUBLIC_ITEM.value, 'contents_type': PHOTO},
            {'month': '2024-01', 'post_type': PostType.LIMITED_ACCESS_ITEM.value, 'contents_type': MOVIE},
            {'month': '2024-01', 'post_type': PostType.PUBLIC_ITEM.value, 'contents_type': MOVIE},
            {'month': '2024-01', 'post_type': PostType.INDIVIDUAL_ITEM.value, 'contents_type': MOVIE},
            {'month': '2024-02', 'post_type': PostType.LIMITED_ACCESS_ITEM.value, 'contents_type': PHOTO, 'is_free': True},
            {'month': '2024-02', 'post_type': PostType.LIMITED_ACCESS_ITEM.value, 'contents_type': MOVIE},
        ]
        for attr in post_attrs:
            is_free = attr.get('is_free', False)
            if 'is_free' in attr:
                del attr['is_free']

            post = await CandfansPostFactory.create(user=user, **attr)
            if is_free:
                await CandFansPostPlanRelationFactory.create(candfans_post=post, candfans_plan=free)
            else:
                await CandFansPostPlanRelationFactory.create(candfans_post=post, candfans_plan=non_free)

        stats = await candfans_post_stats_sv.get_monthly_post_stats(user)
        self.assertEqual(
            stats.total_post_type_stats,
            PostTypeStat(
                public_item=len([a for a in post_attrs if a['post_type'] == PostType.PUBLIC_ITEM.value]),
                limited_access_item=len([a for a in post_attrs if a['post_type'] == PostType.LIMITED_ACCESS_ITEM.value]),
                individual_item=len([a for a in post_attrs if a['post_type'] == PostType.INDIVIDUAL_ITEM.value]),
                back_number_item=len([a for a in post_attrs if a['post_type'] == PostType.BACK_NUMBER_ITEM.value]),
            )
        )
        self.assertEqual(
            stats.monthly_post_type_stats.datasets,
            [
                DataSet(
                    label='公開投稿',
                    data=[2, 0]
                ),
                DataSet(
                    label='プラン限定投稿',
                    data=[2, 2]
                ),
                DataSet(
                    label='単品販売',
                    data=[1, 0]
                ),
            ]
        )
        self.assertEqual(
            stats.monthly_content_type_stats.datasets,
            [
                DataSet(
                    label='動画',
                    data=[3, 1]
                ),
                DataSet(
                    label='写真',
                    data=[2, 1]
                ),
            ]
        )
        self.assertEqual(
            stats.monthly_limited_item_stats.datasets,
            [
                DataSet(
                    label='無料プラン',
                    data=[1, 1]
                ),
                DataSet(
                    label='有料プラン',
                    data=[1, 1]
                ),
            ]
        )
