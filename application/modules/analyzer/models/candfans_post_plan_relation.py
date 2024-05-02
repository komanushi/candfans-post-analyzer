from django.db import models

from .candfans_post import CandfansPost
from .candfans_plan import CandfansPlan


class CandFansPostPlanRelation(models.Model):
    candfans_plan = models.ForeignKey('CandfansPlan', on_delete=models.CASCADE, related_name='candfans_plan_rel')
    candfans_post = models.ForeignKey('CandfansPost', on_delete=models.CASCADE, related_name='candfans_post_rel')
    backnumber_id = models.IntegerField(null=True)
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
            update_fields=['updated_at', 'backnumber_id'],
        )

    @classmethod
    async def delete_by_post(cls, candfans_post: CandfansPost):
        return cls.objects.filter(candfans_post=candfans_post).adelete()

    @classmethod
    async def get_list_by_post_ids(cls, candfans_post_ids: list[int]) -> list['CandFansPostPlanRelation']:
        rels = []
        async for rel in cls.objects.filter(candfans_post_id__in=candfans_post_ids):
            rels.append(rel)
        return rels
