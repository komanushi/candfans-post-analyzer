from typing import Optional

from django.db import models


class CandfansPlan(models.Model):
    plan_id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey('CandfansUser', on_delete=models.CASCADE)
    thanks_message_template_id = models.IntegerField(null=True, blank=True)
    plan_name = models.CharField(max_length=200)
    support_price = models.IntegerField()
    total_support_price = models.IntegerField()
    plan_detail = models.TextField()
    r18 = models.IntegerField()
    status = models.IntegerField()
    fans_cnt = models.IntegerField(null=True, blank=True)
    is_fans = models.BooleanField(default=False)
    is_price_update = models.IntegerField(null=True, blank=True)
    change_support_price = models.IntegerField(null=True, blank=True)
    content_length = models.IntegerField()
    delete_at = models.DateTimeField(null=True, blank=True)
    backnumber_price = models.IntegerField(null=True, blank=True)
    limit_after_backnumber = models.IntegerField()
    this_month_after_backnumber = models.IntegerField()
    can_see_backnumber_plan_pay = models.BooleanField(default=False)
    can_buy_backnumber_not_entry_plan = models.BooleanField(default=False)
    done_transfar_backnumber = models.BooleanField(default=False)
    done_transfar_limit_backnumber = models.BooleanField(default=False)
    entry_disabled = models.BooleanField(default=False)
    upper_limit_entry_cnt = models.IntegerField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plan_name

    @classmethod
    async def create(cls, **params) -> 'CandfansPlan':
        return await cls.objects.acreate(**params)

    @classmethod
    async def update_or_create(cls, plan_id, **params) -> 'CandfansPlan':
        plan, is_new = await cls.objects.aupdate_or_create(
            plan_id=plan_id,
            defaults=params
        )
        return plan

    @classmethod
    async def get_by_plan_id(cls, plan_id: int) -> Optional['CandfansPlan']:
        return await (
            cls.objects.filter(plan_id=plan_id).select_related('user', 'user__detail').afirst()
        )

    @classmethod
    async def get_list_by_plan_ids(cls, plan_ids: list[int]) -> list['CandfansPlan']:
        plans = []
        async for plan in cls.objects.filter(plan_id__in=plan_ids):
            plans.append(plan)
        return plans

    @classmethod
    async def delete_by_user_id_and_exclude_plan_ids(cls, user_id: int, exclude_plan_ids: list[int]):
        return await (
            cls.objects.exclude(plan_id__in=exclude_plan_ids).filter(user_id=user_id).adelete()
        )
