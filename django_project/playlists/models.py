from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
from djangoflix.db.receivers import published_state_pref_save, slugify_pre_save
from djangoflix.db.models import PublishedStateOptions
from videos.models import Video

class PlaylistQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(state=PublishedStateOptions.PUBLISH, published_timestamp__lte=now)

class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()

class Playlist(models.Model):
    title               = models.CharField(max_length=50)
    description         = models.TextField(blank=True, null=True)
    slug                = models.SlugField(blank=True, null=True)
    video               = models.ForeignKey(Video, null=True, related_name='featured_published',on_delete=models.SET_NULL)
    videos              = models.ManyToManyField(Video,related_name="playlist_items", blank=True)
    active              = models.BooleanField(default=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    state               = models.CharField(max_length=2, choices=PublishedStateOptions.choices,default=PublishedStateOptions.DRAFT)
    published_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    objects = PlaylistManager()

    @property
    def is_published(self):
        return self.active
    
    def __str__(self):
        return self.title[:20]


pre_save.connect(published_state_pref_save, sender=Playlist)

pre_save.connect(slugify_pre_save, sender=Playlist)