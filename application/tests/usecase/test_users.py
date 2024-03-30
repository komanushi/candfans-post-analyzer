from unittest.mock import patch, MagicMock

from candfans_client.models.timeline import PostType
from django.test import TestCase

from usecase import users_case
from modules.analyzer.models import CandfansPost, CandfansPlan, CandFansPostPlanRelation
from tests.factories.models import (
    CandfansUserFactory,
    CandfansUserDetailFactory,
    CandfansPlanFactory,
)
from tests.factories.domain_models.candfans_gateway import (
    TimelinePostsModelFactory,
    PostMapFactory,
    PostFactory,
    ShortPlanFactory,
)
from tests.factories.external.candfans_client_user_info import (
    CandfansClientUserInfoFactory,
    CandfansClientQueriedUserFactory
)


class UserUseCaseTest(TestCase):

    @patch('modules.candfans_gateway.service.get_candfans_user_info_by_user_code')
    async def test_create_new_candfans_user_new(
        self,
        mocked_get_candfans_user_info_by_user_code,
    ):
        user_code = 'new_user_code'
        user_info = CandfansClientUserInfoFactory.create(
            user=CandfansClientQueriedUserFactory(
                user_code=user_code
            )
        )
        mocked_get_candfans_user_info_by_user_code.return_value = user_info
        user_model, plans = await users_case.create_new_candfans_user(user_code)
        self.assertEqual(user_model.user_id, user_info.user.id)
        self.assertEqual(user_model.user_code, user_code)
        self.assertIsNotNone(user_model.detail)
        self.assertEqual(plans, [])

    @patch('modules.candfans_gateway.service.get_candfans_user_info_by_user_code')
    async def test_create_new_candfans_user_change_user_code(
        self,
        mocked_get_candfans_user_info_by_user_code,
    ):
        new_user_code = 'updated_user_code'
        old_user_code = 'old_user_code'
        queried_user = CandfansClientQueriedUserFactory(
            user_code=new_user_code
        )
        before_detail = await CandfansUserDetailFactory.create(
            user_id=queried_user.id,
            user_code=old_user_code
        )
        await CandfansUserFactory.create(
            user_id=queried_user.id,
            user_code=old_user_code,
            detail=before_detail
        )
        user_info = CandfansClientUserInfoFactory.create(
            user=queried_user
        )

        mocked_get_candfans_user_info_by_user_code.return_value = user_info
        user_model, plans = await users_case.create_new_candfans_user(new_user_code)
        self.assertEqual(user_model.user_id, user_info.user.id)
        self.assertEqual(user_model.user_code, new_user_code)
        self.assertNotEqual(user_model.detail.id, before_detail.id)
        self.assertEqual(user_model.detail.user_code, new_user_code)

    @patch('modules.candfans_gateway.service.get_timelines')
    async def test_sync_user_stats(
        self,
        mocked_get_timelines: MagicMock,
    ):

        detail = await CandfansUserDetailFactory.create()
        user = await CandfansUserFactory.create(
            user_id=detail.user_id,
            user_code=detail.user_code,
            detail=detail
        )
        short_plan = ShortPlanFactory.create(
            backnumber_id=1,
            backnumber_price=1000,
            total_backnumber_price=1000,
        )
        plan = await CandfansPlanFactory.create(
            plan_id=short_plan.plan_id,
            user=user,
        )
        mocked_get_timelines.return_value = [
            TimelinePostsModelFactory.create(
                month='2024-03',
                post_map=PostMapFactory(
                    public_item=[PostFactory.create(
                        month='2024-03',
                        user_id=user.user_id,
                        user_code=user.user_code,
                        post_type=PostType.PUBLIC_ITEM.value,
                        contents_text=f'2024-03_public_{i}',
                    ) for i in range(2)],
                    limited_access_item=[PostFactory.create(
                        month='2024-03',
                        user_id=user.user_id,
                        user_code=user.user_code,
                        post_type=PostType.LIMITED_ACCESS_ITEM.value,
                        contents_text=f'2024-03_limited_{i}',
                        plans=[short_plan],
                    ) for i in range(3)],
                    individual_access_item=[PostFactory.create(
                        month='2024-03',
                        user_id=user.user_id,
                        user_code=user.user_code,
                        post_type=PostType.INDIVIDUAL_ITEM.value,
                    )],
                    back_number_item=[],
                )
            ),
            TimelinePostsModelFactory.create(
                month='2024-02',
                post_map=PostMapFactory(
                    public_item=[],
                    limited_access_item=[],
                    individual_access_item=[],
                    back_number_item=[PostFactory.create(
                        month='2024-02',
                        user_id=user.user_id,
                        user_code=user.user_code,
                        post_type=PostType.BACK_NUMBER_ITEM.value,
                        plans=[short_plan],
                    )],
                )
            ),
        ]
        await users_case.sync_user_stats(user.user_id)
        posts = []
        async for post in CandfansPost.objects.filter(user_id=user.user_id):
            posts.append(post)
        self.assertEqual(len(posts), 7)

        rels = []
        async for rel in CandFansPostPlanRelation.objects.filter(
                candfans_plan=plan
        ):
            rels.append(rel)
        # limited_access_item(3) + back_number_item(1)
        self.assertEqual(len(rels), 4)

