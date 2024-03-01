from django.test import TestCase

from modules.analyzer import service as analyzer_sv
from modules.analyzer.domain_models import CandfansUserModel
from tests.factories.candfans_user import CandfansUserFactory


class AnalyzerServiceTest(TestCase):

    async def test_create_candfans_user(self):
        created_user = await analyzer_sv.create_candfans_user(CandfansUserModel(
            user_id=1,
            user_code='user_1',
            user_name='user_name_1',
            last_synced_at=None
        ))
        self.assertEqual(created_user.user_id, 1)
        self.assertEqual(created_user.last_synced_at, None)
