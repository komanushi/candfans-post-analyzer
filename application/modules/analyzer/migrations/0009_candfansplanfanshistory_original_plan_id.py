# Generated by Django 4.2.10 on 2024-03-12 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0008_candfansplan_candfanspost_candfansplanfanshistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='candfansplanfanshistory',
            name='original_plan_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
