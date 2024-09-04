import factory
from modules.analyzer.models.candfans_plan import CandfansPlan
from faker import Faker

from .base import AsyncMixin

faker = Faker()


class CandfansPlanFactory(AsyncMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = CandfansPlan

    plan_id = factory.Sequence(lambda n: n)
    user = None
    thanks_message_template_id = factory.Sequence(lambda n: n)
    plan_name = factory.Faker('word')
    support_price = factory.Sequence(lambda n: n)
    total_support_price = factory.Sequence(lambda n: n)
    plan_detail = factory.Faker('text')
    status = factory.Sequence(lambda n: n)
    fans_cnt = factory.Sequence(lambda n: n)
    is_fans = factory.Faker('boolean')
    is_price_update = factory.Sequence(lambda n: n)
    change_support_price = factory.Sequence(lambda n: n)
    content_length = factory.Sequence(lambda n: n)
    delete_at = factory.Faker('date_time')
    backnumber_price = factory.Sequence(lambda n: n)
    limit_after_backnumber = factory.Sequence(lambda n: n)
    this_month_after_backnumber = factory.Sequence(lambda n: n)
    can_see_backnumber_plan_pay = factory.Faker('boolean')
    can_buy_backnumber_not_entry_plan = factory.Faker('boolean')
    done_transfar_backnumber = factory.Faker('boolean')
    done_transfar_limit_backnumber = factory.Faker('boolean')
    entry_disabled = factory.Faker('boolean')
    upper_limit_entry_cnt = factory.Sequence(lambda n: n)
