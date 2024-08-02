from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
from .tasks import convert_480p

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        convert_480p(instance.video_file.path)
    
@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
    
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)