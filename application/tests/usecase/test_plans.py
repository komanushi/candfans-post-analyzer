from unittest.mock import patch
from django.test import TestCase

from modules.analyzer.models import CandfansPlanFansHistory, CandfansPlan
from usecase import plans_case
from tests.factories.models import CandfansUserFactory
from tests.factories.external.candfans_client_user_info import (
    CandfansClientUserInfoFactory,
    CandfansClientQueriedUserFactory,
    CandfansClientPlanFactory,
)


class PlansUseCaseTest(TestCase):

    @patch('modules.candfans_gateway.service.get_candfans_user_info_by_user_code')
    async def test_resync_candfans_plan(
        self,
        mocked_get_candfans_user_info_by_user_code,
    ):
        user_code = 'new_user_code'
        user = CandfansClientQueriedUserFactory(
            user_code=user_code
        )
        user_info = CandfansClientUserInfoFactory.create(
            user=user,
            plans=[CandfansClientPlanFactory.create(user_id=user.id)]
        )
        await CandfansUserFactory.create(
            user_id=user.id,
            user_code=user_code
        )
        mocked_get_candfans_user_info_by_user_code.return_value = user_info
        new_plans = await plans_case.resync_candfans_plan(user_code)
        self.assertEqual(len(new_plans), 1)
        self.assertEqual(await CandfansPlan.objects.acount(), 1)
        self.assertEqual(await CandfansPlanFansHistory.objects.acount(), 1)
