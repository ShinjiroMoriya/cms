# Generated by Django 2.1 on 2019-01-23 14:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('topic', '0001_initial'),
        ('introduction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(blank=True, null=True)),
                ('youtube_id', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.IntegerField(default=2)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('published_at', models.DateTimeField(default=datetime.datetime.now)),
                ('category', models.ManyToManyField(blank=True, to='category.Category')),
                ('introduction', models.ManyToManyField(blank=True, to='introduction.Introduction')),
                ('topic', models.ManyToManyField(blank=True, to='topic.Topic')),
                ('video', models.ManyToManyField(blank=True, related_name='_video_video_+', to='video.Video')),
            ],
            options={
                'db_table': 'video',
                'ordering': ['-id', '-published_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoEn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(blank=True, null=True)),
                ('youtube_id', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.IntegerField(default=2)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('published_at', models.DateTimeField(default=datetime.datetime.now)),
                ('category', models.ManyToManyField(blank=True, to='category.Category')),
                ('introduction', models.ManyToManyField(blank=True, to='introduction.IntroductionEn')),
                ('topic', models.ManyToManyField(blank=True, to='topic.TopicEn')),
                ('video', models.ManyToManyField(blank=True, related_name='_videoen_video_+', to='video.VideoEn')),
            ],
            options={
                'db_table': 'video_en',
                'ordering': ['-id', '-published_at'],
                'abstract': False,
            },
        ),
    ]
