# Generated by Django 2.1 on 2018-12-11 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('introduction', '0002_auto_20181210_1811'),
    ]

    operations = [
        migrations.RenameField(
            model_name='introduction',
            old_name='body',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='introductionen',
            old_name='body',
            new_name='text',
        ),
    ]