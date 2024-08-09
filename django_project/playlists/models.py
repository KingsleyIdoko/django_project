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
    class PlaylistTypeChoices(models.TextChoices):
        MOVIE           = 'MOV','Movie'
        SHOW            = 'TVS','TV Show'
        SEASON          = 'SEA','Season'
        PLAYLIST        = 'PLY','Playlist'

    parent              = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    order               = models.IntegerField(default=1)
    title               = models.CharField(max_length=50)
    type                = models.CharField(max_length=3, choices=PlaylistTypeChoices.choices, default=PlaylistTypeChoices.PLAYLIST)
    description         = models.TextField(blank=True, null=True)
    slug                = models.SlugField(blank=True, null=True)
    video               = models.ForeignKey(Video, null=True, blank=True, related_name='featured_published',on_delete=models.SET_NULL)
    videos              = models.ManyToManyField(Video,related_name="playlist_items", blank=True, through='PlaylistItem')
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

class TVShowProxyManager(PlaylistManager):
    def get_queryset(self):
        return super().get_queryset().filter(parent__isnull=True,type=Playlist.PlaylistTypeChoices.SHOW)

class TVShowSeasonManager(PlaylistManager):
    def get_queryset(self):
        return super().get_queryset().filter(parent__isnull=False,type=Playlist.PlaylistTypeChoices.SEASON)
    
class MovieProxyManager(PlaylistManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Playlist.PlaylistTypeChoices.MOVIE)
    
class MovieProxy(Playlist):
    objects = MovieProxyManager()
    class Meta:
        verbose_name  = 'TV Show'
        verbose_name_plural = 'TV Shows'
        proxy  = True

    def save(self,*args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.MOVIE
        super().save(*args, **kwargs)

class TVShowProxy(Playlist):
    objects = TVShowProxyManager()
    class Meta:
        verbose_name  = 'TV Show'
        verbose_name_plural = 'TV Shows'
        proxy  = True

    def save(self,*args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SHOW
        super().save(*args, **kwargs)

class TVShowSeasonProxy(Playlist):
    objects = TVShowSeasonManager()
    class Meta:
        verbose_name  = 'Season'
        verbose_name_plural = 'Seasons'
        proxy = True
    def save(self,*args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SEASON
        super().save(*args, **kwargs)

pre_save.connect(published_state_pref_save, sender=Playlist)
pre_save.connect(slugify_pre_save, sender=Playlist)

class PlaylistItem(models.Model):
    playlist            = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video               = models.ForeignKey(Video, on_delete=models.CASCADE)
    order               = models.IntegerField(default=1)
    timestamp           = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-timestamp']
