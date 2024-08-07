from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
import shutil
from .tasks import convert

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        convert(instance.video_file.path)
    
@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        video_file_path = instance.video_file.path
        video_folder = os.path.dirname(video_file_path)
        if os.path.isdir(video_folder):
            shutil.rmtree(video_folder)
    
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)