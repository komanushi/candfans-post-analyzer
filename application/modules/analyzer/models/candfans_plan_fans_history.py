from django.db import models

from .candfans_plan import CandfansPlan


class CandfansPlanFansHistory(models.Model):
    plan = models.ForeignKey('CandfansPlan', on_delete=models.SET_NULL, null=True)
    original_plan_id = models.IntegerField()
    plan_name = models.CharField(max_length=300)
    user = models.ForeignKey('CandfansUser', on_delete=models.CASCADE)
    fans_cnt = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.plan_name}({self.created_at})'

    @classmethod
    async def create(cls, plan: CandfansPlan) -> 'CandfansPlanFansHistory':
        return await cls.objects.acreate(
            plan=plan,
            original_plan_id=plan.plan_id,
            plan_name=plan.plan_name,
            user=plan.user,
            fans_cnt=plan.fans_cnt,
        )
