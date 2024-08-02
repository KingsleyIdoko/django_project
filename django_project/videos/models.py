from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.

class PublishedStateOptions(models.TextChoices):
        PUBLISH = 'PU','Publish'
        DRAFT   = 'DR','DRAFT'

class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(state=PublishedStateOptions.PUBLISH, published_timestamp__lte=now)

class ModelManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()

class Video(models.Model):
    title               = models.CharField(max_length=50)
    description         = models.TextField(blank=True, null=True)
    slug                = models.SlugField(blank=True, null=True)
    video_id            = models.CharField(max_length=50, unique=True)
    active              = models.BooleanField(default=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    state               = models.CharField(max_length=2, choices=PublishedStateOptions.choices,default=PublishedStateOptions.DRAFT)
    published_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects = ModelManager()

    @property
    def is_published(self):
        return self.active
    
    def __str__(self):
        return self.title[:20]


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

def published_state_pref_save(sender, instance, *args, **kwargs):
    is_publish = instance.state == PublishedStateOptions.PUBLISH 
    is_draft = instance.state == PublishedStateOptions.DRAFT
    if is_publish and instance.published_timestamp is None:
        instance.published_timestamp = timezone.now()
    elif is_draft:
        instance.published_timestamp = None
pre_save.connect(published_state_pref_save, sender=Video)


def slugify_pre_save(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
pre_save.connect(slugify_pre_save, sender=Video)