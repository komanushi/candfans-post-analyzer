from django.db import models


class CandfansPlanFansHistory(models.Model):
    plan = models.ForeignKey('CandfansPlan', on_delete=models.SET_NULL, null=True)
    plan_name = models.CharField(max_length=300)
    user = models.ForeignKey('CandfansUser', on_delete=models.CASCADE)
    fans_cnt = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.plan_name}({self.created_at})'
