# Generated by Django 2.1 on 2019-01-08 14:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0005_auto_20190108_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='event_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='topicen',
            name='event_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]