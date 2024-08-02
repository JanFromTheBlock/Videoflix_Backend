from django.db import models
from datetime import date
from django_resized import ResizedImageField
from .tasks import video_upload_to

class Video(models.Model):
    create_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    thumbnail = ResizedImageField(force_format="WEBP", size=[500, None], quality=75, upload_to="thumbnails", blank=True, null=True)
    video_file = models.FileField(upload_to=video_upload_to, blank=True, null=True)
    
    def __str__(self):
        return self.title
    

