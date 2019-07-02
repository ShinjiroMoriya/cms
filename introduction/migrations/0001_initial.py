# Generated by Django 2.1 on 2019-01-23 14:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Introduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(default=2)),
                ('thumbnail', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('published_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'introduction',
                'ordering': ['-id', '-published_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IntroductionEn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(default=2)),
                ('thumbnail', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('published_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'introduction_en',
                'ordering': ['-id', '-published_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'title',
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TitleEn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'title_en',
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='introductionen',
            name='titles',
            field=models.ManyToManyField(blank=True, to='introduction.TitleEn'),
        ),
        migrations.AddField(
            model_name='introduction',
            name='titles',
            field=models.ManyToManyField(blank=True, to='introduction.Title'),
        ),
    ]
