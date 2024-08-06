from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

# Register your models here.
from .models import Video, VideoPublishedProxy, VideoAllProxy


class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title', 'id','state','video_id','active','is_published','get_playlist_id']
    list_filter = ['state','active']
    search_fields = ['title']
    readonly_fields = ['id','is_published','published_timestamp']
    class Meta:
        model = VideoAllProxy

class VideoProxyAdmin(admin.ModelAdmin):
    list_display = ['title','video_id']
    list_filter = ['video_id']
    search_fields = ['title']
    readonly_fields = ['id','is_published','published_timestamp']
    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active=True)


admin.site.register(VideoPublishedProxy,VideoProxyAdmin)

admin.site.register(VideoAllProxy, VideoAllAdmin)
