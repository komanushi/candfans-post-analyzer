from typing import Optional

from django.db import models


class CandfansPlan(models.Model):
    plan_id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey('CandfansUser', on_delete=models.CASCADE)
    support_price = models.IntegerField()
    total_support_price = models.IntegerField()
    plan_name = models.CharField(max_length=200)
    plan_detail = models.TextField()
    backnumber_id = models.IntegerField(null=True)
    backnumber_price = models.IntegerField(null=True)
    total_backnumber_price = models.IntegerField(null=True)
    can_see_backnumber_plan_pay = models.BooleanField()
    can_buy_backnumber_not_entry_plan = models.BooleanField()
    add_backnumber_date = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.plan_name

    @classmethod
    async def create(cls, **params) -> 'CandfansPlan':
        return await cls.objects.acreate(**params)

    @classmethod
    async def get_by_plan_id(cls, plan_id: int) -> Optional['CandfansPlan']:
        return await (
            cls.objects.filter(plan_id=plan_id).select_related('user', 'user__detail').afirst()
        )
