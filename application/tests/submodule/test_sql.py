from pydantic import BaseModel
from django.test import TransactionTestCase

from modules.analyzer.models import CandfansPost
from submodule import sql

from tests.factories.models.candfans_user import CandfansUserFactory
from tests.factories.models.candfans_post import CandfansPostFactory


# factoryとsqlモジュールで別コネクションになるのでTransactionTestCaseが必要
class SqlHelperTest(TransactionTestCase):
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

    async def test_get_query_result_via_model(self):
        user = await CandfansUserFactory.create()
        await CandfansPostFactory.create(user=user)
        await CandfansPostFactory.create(user=user)

        class PostType(BaseModel):
            post_id: int
            month: str

        post_type_factory = lambda x: PostType(post_id=x.post_id, month=x.month)
        result = await sql.get_query_results_via_model(
            sql.QueryModel(
                query='select post_id, month from analyzer_candfanspost where user_id = %s',
                row_to_model=post_type_factory,
            ),
            params=[user.user_id]
        )

        self.assertEqual(len(result), 2)
        self.assertTrue(isinstance(result[0], PostType))
