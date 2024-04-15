import subprocess
import os

from django.conf import settings

from user.models import CustomUser
from .models import Video, VideoQuality

from django.utils import timezone
from datetime import timedelta


def create_thumbnail(source, output, video_id):
    base_dir = os.path.join(settings.MEDIA_ROOT)
    thumbnail_dir = os.path.join(base_dir, 'thumbnails')  
    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir) 

    thumbnail_base_name = os.path.basename(output)
    thumbnail_path = os.path.join(thumbnail_dir, thumbnail_base_name)

    cmd = [
        'ffmpeg',
        '-i', source,
        '-ss', '00:00:01',
        '-vframes', '1',
        '-s', '1280x720',
        thumbnail_path  
    ]

    subprocess.run(cmd, capture_output=True)

    thumbnail_rel_path = os.path.join('thumbnails', thumbnail_base_name)
    video = Video.objects.get(id=video_id)
    video.thumbnail.name = thumbnail_rel_path
    video.save()


def convert_and_save_quality(video, quality_label, resolution):
    video_filename = os.path.basename(video.video_file.name)
    quality_filename = f'{quality_label}-{video_filename}'

    quality_video_path = os.path.join(settings.MEDIA_ROOT, 'videos', quality_filename)

    cmd = [
        'ffmpeg',
        '-i', video.video_file.path,
        '-s', resolution,
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        quality_video_path
    ]
    subprocess.run(cmd, capture_output=True)
    
    relative_quality_path = os.path.join('videos', quality_filename)
    
    VideoQuality.objects.create(
        video=video,
        quality=quality_label,
        video_file=relative_quality_path
    )




# def convert_480p(source, output):
#     print('hey convert_480p wird ausgeführt')

#     cmd = [
#         'ffmpeg',
#         '-i', source,
#         '-s', 'hd480',
#         '-c:v', 'libx264',
#         '-crf', '23',
#         '-c:a', 'aac',
#         '-strict', '-2',
#         output
#     ]
#     run = subprocess.run(cmd, capture_output=True)
#     if run.returncode == 0:  # Nur wenn ffmpeg erfolgreich war
#         video_quality = VideoQuality.objects.create(
#             video=Video.objects.get(video_file=source),
#             quality='480p',
#             video_file=output.replace(settings.MEDIA_ROOT, '')  # Speichere relativen Pfad
#         )
#         video_quality.save()

  
    
    
    

# def convert_720p(source, output):
           
#         cmd = [
#         'ffmpeg',
#         '-i', source,
#         '-s', 'hd720',
#         '-c:v', 'libx264',
#         '-crf', '23',
#         '-c:a', 'aac',
#         '-strict', '-2',
#         output
#     ]
#         run = subprocess.run(cmd, capture_output=True)
#         if run.returncode == 0:  # Nur wenn ffmpeg erfolgreich war
#             video_quality = VideoQuality.objects.create(
#                 video=Video.objects.get(video_file=source),
#                 quality='720p',
#                 video_file=output.replace(settings.MEDIA_ROOT, '')  # Speichere relativen Pfad
#             )
#             video_quality.save()


# def convert_1080p(source, output):
           
#         cmd = [
#         'ffmpeg',
#         '-i', source,
#         '-s', 'hd1080',
#         '-c:v', 'libx264',
#         '-crf', '23',
#         '-c:a', 'aac',
#         '-strict', '-2',
#         output
#     ]
#         run = subprocess.run(cmd, capture_output=True)
#         if run.returncode == 0:  # Nur wenn ffmpeg erfolgreich war
#             video_quality = VideoQuality.objects.create(
#                 video=Video.objects.get(video_file=source),
#                 quality='1080p',
#                 video_file=output.replace(settings.MEDIA_ROOT, '')  # Speichere relativen Pfad
#             )
#             video_quality.save()
