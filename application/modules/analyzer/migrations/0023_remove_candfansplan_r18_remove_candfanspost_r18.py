# Generated by Django 4.2.10 on 2024-09-04 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0022_rename_candfansrankingcreator_candfanscreatordailyranking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candfansplan',
            name='r18',
        ),
        migrations.RemoveField(
            model_name='candfanspost',
            name='r18',
        ),
    ]
