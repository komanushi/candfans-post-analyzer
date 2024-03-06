from unittest.mock import patch
from django.test import TestCase

from usecase import users as users_use_case
from tests.factories.models import CandfansUserFactory, CandfansUserDetailFactory
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
        user_model = await users_use_case.create_new_candfans_user(user_code)
        self.assertEqual(user_model.user_id, user_info.user.id)
        self.assertEqual(user_model.user_code, user_code)
        self.assertIsNotNone(user_model.detail)

    @patch('modules.candfans_gateway.service.get_candfans_user_info_by_user_code')
    async def test_create_new_candfans_user_change_user_code(
        self,
        mocked_get_candfans_user_info_by_user_code,
    ):
        new_user_code = 'updated_user_code'
        queried_user = CandfansClientQueriedUserFactory(
            user_code=new_user_code
        )
        before_detail = await CandfansUserDetailFactory.create(user_id=queried_user.id)
        await CandfansUserFactory.create(
            user_id=queried_user.id,
            user_code='old_user_code',
            detail=before_detail
        )
        user_info = CandfansClientUserInfoFactory.create(
            user=queried_user
        )

        mocked_get_candfans_user_info_by_user_code.return_value = user_info
        user_model = await users_use_case.create_new_candfans_user(new_user_code)
        self.assertEqual(user_model.user_id, user_info.user.id)
        self.assertEqual(user_model.user_code, new_user_code)
        self.assertNotEqual(user_model.detail_id, before_detail.id)
        self.assertEqual(user_model.detail.user_code, new_user_code)
