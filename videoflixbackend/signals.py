from django.conf import settings
import os
from dotenv import load_dotenv
load_dotenv()

from django.dispatch import receiver

from videoflixbackend.tasks import  convert_and_save_quality, create_thumbnail
from .models import Video
from django.db.models.signals import post_save, post_delete, pre_save
import django_rq
from django.core.cache import cache
from django.core.mail import send_mail
# from django.contrib.auth.models import User
from user.models import CustomUser



# These imports sare for the passwort reset logic from DRF 
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(post_save, sender =Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        print('Neues Video erstellt', instance.video_file.path)
        queue = django_rq.get_queue('default',autocommit=True)          
       
        # base, _ = os.path.splitext(instance.video_file.path)
        # base = base.replace(settings.MEDIA_ROOT + '/', '', 1)

        thumbnail_output = f'thumbnails/{instance.id}-thumbnail.jpg'
        queue.enqueue(create_thumbnail, instance.video_file.path, thumbnail_output, instance.id)
              
        #Jobs zur KOnvertierung werden in die queue gestellt
        queue.enqueue(convert_and_save_quality, instance, '360px', '480x360')
        queue.enqueue(convert_and_save_quality, instance,  '720p', '1280x720')
        queue.enqueue(convert_and_save_quality, instance,'1080p', '1920x1080')

         # E-Mail an (alle) Superuser senden
        subject = 'Neues Video hochgeladen'
        message = f'Ein neues Video mit dem Titel "{instance.title}" wurde hochgeladen und wartet auf Überprüfung.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = CustomUser.objects.filter(is_superuser=True).values_list('email', flat=True)
        send_mail(subject, message, email_from, recipient_list)
        
        # queue.enqueue(convert_480p, instance.video_file.path, base + '-480p.mp4')
        # queue.enqueue(convert_720p, instance.video_file.path, base + '-720p.mp4')
        # queue.enqueue(convert_1080p, instance.video_file.path, base + '-1080p.mp4')
       
         #Löschen des Cache
    cache.delete('video_list_cache_key')


@receiver(post_delete, sender = Video)        
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            base, _ = os.path.splitext(instance.video_file.path)
            os.remove(instance.video_file.path)
            os.remove( base + '-720p.mp4')
            os.remove( base + '-480p.mp4')
            os.remove( base + '-1080p.mp4')
            print ('Video wurde gelöscht')   
             #Löschen des Cache
        cache.delete('video_list_cache_key')


@receiver(pre_save, sender = Video)
def video_pre_delete_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Video` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Video.objects.get(pk=instance.pk).video_file
    except Video.DoesNotExist:
        return False

    new_file = instance.video_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_password_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_password_token.key}"

    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': reset_password_url
    }

    email_html_message = render_to_string('user_reset_password.html', context)
    email_plaintext_message = render_to_string('user_reset_password.txt', context)

         
    msg = EmailMultiAlternatives(
        "Password Reset for {title}".format(title="Password Reset for Videoflix"),
        email_plaintext_message,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
