# Generated by Django 2.1 on 2018-12-10 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0003_auto_20181210_1738'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='new_flag',
            new_name='new',
        ),
        migrations.RenameField(
            model_name='topicen',
            old_name='new_flag',
            new_name='new',
        ),
    ]
