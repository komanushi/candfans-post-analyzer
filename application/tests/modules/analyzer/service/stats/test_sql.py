from django.test import TransactionTestCase

from modules.analyzer.models import CandfansPost
from modules.analyzer.service.stats import sql

from tests.factories.models.candfans_user import CandfansUserFactory
from tests.factories.models.candfans_post import CandfansPostFactory


# factoryとsqlモジュールで別コネクションになるのでTransactionTestCaseが必要
class CandfansPostServiceTest(TransactionTestCase):
    async def test_query(self):
        user = await CandfansUserFactory.create()
        await CandfansPostFactory.create(user=user)
        await CandfansPostFactory.create(user=user)
        self.assertEqual(await CandfansPost.objects.acount(), 2)
        result = await sql.get_query_result(
            f'select * from analyzer_candfanspost where user_id = %s',
            [user.user_id]
        )
        self.assertEqual(len(result), 2)
