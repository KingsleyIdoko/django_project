from django.db import models
from django.utils import timezone
# Create your models here.

class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        PUBLISH = 'PU','Publish'
        DRAFT = 'DR','DRAFT'

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, choices=VideoStateOptions.choices,default=VideoStateOptions.DRAFT)
    published_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    @property
    def is_published(self):
        return self.active
    
    def __str__(self):
        return self.title[:20]
    
    def save(self,*args, **kwargs):
        if self.state == self.VideoStateOptions.PUBLISH and self.published_timestamp is None:
            self.published_timestamp = timezone.now()
        elif self.state == self.VideoStateOptions.DRAFT:
            self.published_timestamp = None
        super().save(*args,**kwargs)

class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'

class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'