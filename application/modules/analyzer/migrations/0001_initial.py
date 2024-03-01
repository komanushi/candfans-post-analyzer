# Generated by Django 4.2.10 on 2024-03-01 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CandfansUser',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_code', models.CharField(max_length=255, unique=True)),
                ('user_name', models.TextField()),
                ('last_synced_at', models.DateTimeField(default=None, null=True)),
            ],
        ),
    ]
