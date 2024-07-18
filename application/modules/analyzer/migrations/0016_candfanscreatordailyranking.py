# Generated by Django 4.2.10 on 2024-07-18 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0015_candfanspostplanrelation_backnumber_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandfansCreatorDailyRanking',
            fields=[
                ('day', models.DateField()),
                ('rank', models.IntegerField()),
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_code', models.CharField(max_length=255)),
                ('username', models.TextField()),
                ('profile_img', models.CharField(max_length=500)),
                ('profile_text', models.TextField()),
                ('follow_cnt', models.IntegerField()),
                ('follower_cnt', models.IntegerField()),
                ('like_cnt', models.IntegerField()),
                ('is_official_creator', models.BooleanField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
