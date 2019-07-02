# Generated by Django 2.1 on 2019-01-23 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('video_id', models.IntegerField()),
                ('lang', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'favorite',
                'ordering': ['id'],
            },
        ),
    ]
