from unittest.mock import patch, ANY
from django.test import TestCase, AsyncClient

from tests.factories.models.candfans_user import CandfansUserFactory
from tests.factories.domain_models.candfans_user import CandFansUserModelFactory
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
    async def test_ok_first(self, mock_create_new_candfans_user, mocked_enqueue):
        user_code = 'new'
        mock_create_new_candfans_user.return_value = CandFansUserModelFactory(
            user_code=user_code
        )
        client = AsyncClient()
        response = await client.post(f'/user/{user_code}/refresh')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(mock_create_new_candfans_user.called)
        mocked_enqueue.assert_called_once_with(
            users_usecase.sync_user_stats,
            ANY
        )
