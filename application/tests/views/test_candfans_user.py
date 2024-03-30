from unittest.mock import patch, ANY
from django.test import TestCase, AsyncClient

from tests.factories.models.candfans_user import CandfansUserFactory


class CandfansUserViewTest(TestCase):

    @patch('usecase.plans_case.resync_candfans_plan')
    @patch('modules.analyzer.service.set_sync_status')
    async def test_create_candfans_user_ok(self, mock_set_sync_status, mock_resync_candfans_plan):
        user = await CandfansUserFactory.create()
        client = AsyncClient()
        response = await client.get(f'/user/{user.user_code}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.user_code)

        self.assertTrue(mock_resync_candfans_plan.called)
        self.assertTrue(mock_set_sync_status.called)

    async def test_create_candfans_user_no_user(self):
        user_code = 'not_found_user'
        client = AsyncClient()
        response = await client.get(f'/user/{user_code}')
        self.assertEqual(response.status_code, 302)
