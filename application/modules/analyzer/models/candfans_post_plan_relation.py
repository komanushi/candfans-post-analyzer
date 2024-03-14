from django.db import models

from .candfans_post import CandfansPost
from .candfans_plan import CandfansPlan


class CandFansPostPlanRelation(models.Model):
    candfans_plan = models.ForeignKey('CandfansPlan', on_delete=models.CASCADE)
    candfans_post = models.ForeignKey('CandfansPost', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["candfans_plan", "candfans_post"],
                name="candfans_post_plan_rel_uniq"
            ),
        ]

    def __str__(self):
        return f'{self.candfans_plan} of {self.candfans_post}'

    @classmethod
    async def create(cls, candfans_plan: CandfansPlan, candfans_post: CandfansPost) -> 'CandFansPostPlanRelation':
        return await cls.objects.acreate(
            candfans_plan=candfans_plan,
            CandfansPost=candfans_post,
        )

    @classmethod
    async def bulk_create(cls, rels: list['CandFansPostPlanRelation']) -> list['CandFansPostPlanRelation']:
        return await cls.objects.abulk_create(
            rels,
            unique_fields=['candfans_plan', 'candfans_post'],
            update_conflicts=True,
            update_fields=['updated_at']
        )

    @classmethod
    async def delete_by_post(cls, candfans_post: CandfansPost):
        return cls.objects.filter(candfans_post=candfans_post).delete()
