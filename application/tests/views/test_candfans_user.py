from unittest.mock import patch, ANY
from django.test import TestCase, AsyncClient

from tests.factories.models.candfans_user import CandfansUserFactory
from tests.factories.domain_models.analyzer import CandFansUserModelFactory, CandfansPlanModelFactory
from usecase import users as users_usecase


class CandfansUserViewTest(TestCase):

    async def test_create_candfans_user_ok(self):
        user = await CandfansUserFactory.create()
        client = AsyncClient()
        response = await client.get(f'/user/{user.user_code}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.user_code)

    async def test_create_candfans_user_no_user(self):
        user_code = 'not_found_user'
        client = AsyncClient()
        response = await client.get(f'/user/{user_code}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'このユーザ({ user_code })は存在しません。')


class CandfansRefreshViewTest(TestCase):
    @patch('django_rq.enqueue')
    @patch('usecase.users.create_new_candfans_user')
    @patch('modules.analyzer.service.set_sync_status')
    async def test_ok_first(
        self,
        mock_set_sync_status,
        mock_create_new_candfans_user,
        mocked_enqueue
    ):
        user_code = 'new'
        user = CandFansUserModelFactory(
            user_code=user_code
        )
        mock_create_new_candfans_user.return_value = (
            user,
            [CandfansPlanModelFactory.create(user=user)]
        )
        client = AsyncClient()
        response = await client.post(f'/user/{user_code}/refresh')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(mock_create_new_candfans_user.called)
        self.assertTrue(mock_set_sync_status.called)
        mocked_enqueue.assert_called_once_with(
            users_usecase.sync_user_stats,
            ANY
        )
