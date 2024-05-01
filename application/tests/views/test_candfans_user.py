from unittest.mock import patch
from django.test import TransactionTestCase, AsyncClient

from tests.factories.models.candfans_user import CandfansUserFactory


class CandfansUserViewTest(TransactionTestCase):

    @patch('usecase.plans_case.resync_candfans_plan')
    @patch('modules.analyzer.service.set_sync_status')
    @patch('usecase.stats_case.generate_stats')
    async def test_create_candfans_user_ok(
            self,
            mock_generate_stats,
            mock_set_sync_status,
            mock_resync_candfans_plan
    ):
        user = await CandfansUserFactory.create()
        client = AsyncClient()
        response = await client.get(f'/user/{user.user_code}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.user_code)

        self.assertTrue(mock_resync_candfans_plan.called)
        self.assertTrue(mock_set_sync_status.called)
        self.assertTrue(mock_generate_stats.called)

    async def test_create_candfans_user_no_user(self):
        user_code = 'not_found_user'
        client = AsyncClient()
        response = await client.get(f'/user/{user_code}')
        self.assertEqual(response.status_code, 302)
