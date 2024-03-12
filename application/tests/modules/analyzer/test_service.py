import freezegun
from django.test import TestCase
from django.utils import timezone

from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import CandfansUserModel, SyncStatus
from tests.factories.models.candfans_user import CandfansUserFactory
from tests.factories.domain_models.analyzer import (
    CandfansUserDetailModelFactory,
    CandfansPlanModelFactory,
)


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

    async def test_set_sync_status_syncing(self):
        candfans_user = await CandfansUserFactory.create(
            sync_status=None,
            last_synced_at=None,
            sync_requested_at=None,
        )
        freeze_time = timezone.now()
        with freezegun.freeze_time(freeze_time):
            candfans_user_model = await analyzer_sv.set_sync_status(candfans_user, SyncStatus.SYNCING)

        self.assertEqual(candfans_user_model.last_synced_at, None)
        self.assertEqual(candfans_user_model.sync_status, SyncStatus.SYNCING)
        self.assertEqual(candfans_user_model.sync_requested_at, freeze_time)

        freeze_time = timezone.now()
        with freezegun.freeze_time(freeze_time):
            candfans_user_model = await analyzer_sv.set_sync_status(candfans_user, SyncStatus.FINISHED)

        self.assertEqual(candfans_user_model.last_synced_at, freeze_time)
        self.assertEqual(candfans_user_model.sync_status, SyncStatus.FINISHED)

    async def test_create_candfans_plan(self):
        created_user = await analyzer_sv.create_candfans_user(CandfansUserModel(
            user_id=1,
            user_code='user_1',
            username='user_name_1',
        ))
        plan_model = CandfansPlanModelFactory.create(user=created_user)
        created_plan = await analyzer_sv.create_candfans_plan(plan_model)

        self.assertEqual(created_plan.user.user_id, created_user.user_id)
        self.assertEqual(created_plan.plan_id, plan_model.plan_id)
        self.assertEqual(created_plan.support_price, plan_model.support_price)
        self.assertEqual(created_plan.total_support_price, plan_model.total_support_price)
        self.assertEqual(created_plan.plan_name, plan_model.plan_name)
        self.assertEqual(created_plan.plan_detail, plan_model.plan_detail)
        self.assertEqual(created_plan.backnumber_price, plan_model.backnumber_price)
        self.assertEqual(created_plan.can_see_backnumber_plan_pay, plan_model.can_see_backnumber_plan_pay)
        self.assertEqual(created_plan.can_buy_backnumber_not_entry_plan, plan_model.can_buy_backnumber_not_entry_plan)

