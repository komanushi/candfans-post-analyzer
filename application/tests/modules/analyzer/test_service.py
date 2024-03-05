from django.test import TestCase

from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import CandfansUserModel, CandfansUserDetailModel
from tests.factories.models.candfans_user import CandfansUserFactory
from tests.factories.domain_models.candfans_user_detail import CandfansUserDetailModelFactory


class AnalyzerServiceTest(TestCase):

    async def test_create_candfans_user(self):
        created_user = await analyzer_sv.create_candfans_user(CandfansUserModel(
            user_id=1,
            user_code='user_1',
            username='user_name_1',
        ))
        self.assertEqual(created_user.user_id, 1)
        self.assertEqual(created_user.last_synced_at, None)


    async def test_get_candfans_user_by_user_code(self):
        user = await CandfansUserFactory.create()
        user_model = await analyzer_sv.get_candfans_user_by_user_code(user_code=user.user_code)
        self.assertEqual(user_model.user_id, user.user_id)
        self.assertEqual(user_model.user_code, user.user_code)
        self.assertEqual(user_model.username, user.username)

    async def test_get_candfans_user_by_user_id(self):
        user = await CandfansUserFactory.create()
        user_model = await analyzer_sv.get_candfans_user_by_user_id(user_id=user.user_id)
        self.assertEqual(user_model.user_id, user.user_id)
        self.assertEqual(user_model.user_code, user.user_code)
        self.assertEqual(user_model.username, user.username)

    async def test_create_candfans_user_detail(self):
        detail = CandfansUserDetailModelFactory(id=None)
        created_detail = await analyzer_sv.create_candfans_user_detail(detail)
        self.assertIsNotNone(created_detail.id)
        self.assertIsNotNone(created_detail.created_at)
        self.assertEqual(created_detail.user_id, detail.user_id)

    async def test_create_candfans_user_with_detail(self):
        detail = CandfansUserDetailModelFactory(id=None)
        created_detail = await analyzer_sv.create_candfans_user_detail(detail)
        created_user = await analyzer_sv.create_candfans_user(
            candfans_user=CandfansUserModel(
                user_id=1,
                user_code='user_1',
                username='user_name_1',
            ),
            candfans_detail=created_detail
        )

        self.assertEqual(created_user.user_id, 1)
        self.assertEqual(created_user.last_synced_at, None)
        self.assertEqual(created_user.detail.id, created_detail.id)
        self.assertEqual(created_user.detail.fans_cnt, created_detail.fans_cnt)
