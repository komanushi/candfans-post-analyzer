import factory
from modules.analyzer.models.candfans_plan import CandfansPlan
from faker import Faker

from .base import AsyncMixin

faker = Faker()


class CandfansPlanFactory(factory.django.DjangoModelFactory, AsyncMixin):
    class Meta:
        model = CandfansPlan

    plan_id = factory.Sequence(lambda n: n)
    user = None
    support_price = factory.LazyFunction(lambda: faker.random_int(min=1000, max=10000, step=1000))
    total_support_price = factory.LazyFunction(lambda: faker.random_int(min=10000, max=100000, step=10000))
    plan_name = factory.Faker('sentence')
    plan_detail = factory.Faker('text')
    backnumber_id = factory.Sequence(lambda n: n)
    backnumber_price = factory.LazyFunction(lambda: faker.random_int(min=500, max=5000, step=500))
    total_backnumber_price = factory.LazyFunction(lambda: faker.random_int(min=5000, max=50000, step=5000))
    can_see_backnumber_plan_pay = factory.Faker('boolean')
    can_buy_backnumber_not_entry_plan = factory.Faker('boolean')
    add_backnumber_date = factory.Faker('date')

