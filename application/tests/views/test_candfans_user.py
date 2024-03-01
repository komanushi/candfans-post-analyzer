from django.test import TestCase, AsyncClient

from tests.factories.candfans_user import CandfansUserFactory


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
