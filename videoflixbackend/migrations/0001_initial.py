# Generated by Django 5.0 on 2024-04-15 18:35

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(default=datetime.date.today)),
                ('title', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=500)),
                ('category', models.CharField(choices=[('allgemein', 'Allgemein'), ('kids', 'Kids'), ('funny', 'Funny'), ('noidea', 'Noidea'), ('action', 'Action'), ('drama', 'Drama'), ('horror', 'Horror'), ('krimi', 'Krimi'), ('thriller', 'Thriller')], default='allgemein', max_length=20)),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnails')),
                ('view_count', models.IntegerField(default=0)),
                ('film_rating', models.IntegerField(default=0)),
                ('isVisible', models.BooleanField(default=False)),
                ('created_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='likers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VideoQuality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quality', models.CharField(max_length=20)),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qualities', to='videoflixbackend.video')),
            ],
        ),
    ]