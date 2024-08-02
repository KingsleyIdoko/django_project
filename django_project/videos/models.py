from django.db import models
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.

class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(state=Video.VideoStateOptions.PUBLISH, published_timestamp__lte=now)

class ModelManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()

class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        PUBLISH = 'PU','Publish'
        DRAFT = 'DR','DRAFT'

    title               = models.CharField(max_length=50)
    description         = models.TextField(blank=True, null=True)
    slug                = models.SlugField(blank=True, null=True)
    video_id            = models.CharField(max_length=50, unique=True)
    active              = models.BooleanField(default=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    state               = models.CharField(max_length=2, choices=VideoStateOptions.choices,default=VideoStateOptions.DRAFT)
    published_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects = ModelManager()

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
        if not self.slug:
            self.slug = slugify(self.title)
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