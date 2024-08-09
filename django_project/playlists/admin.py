from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import Playlist, PlaylistItem,TVShowProxy,TVShowSeasonProxy

class PlaylistItemInline(admin. TabularInline):
    model = PlaylistItem
    extra = 0

class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistItemInline]
    fields = ['title','description','type','state','slug']
    class Meta:
        model = Playlist

class TVShowSeasonEpisodeInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0

class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines = [TVShowSeasonEpisodeInline]
    list_display = ['title','parent']
    fields = ['title','description','state','video','slug']
    class Meta:
        model = TVShowSeasonProxy


class TVShowSeasonInline(admin.TabularInline):
    model = TVShowSeasonProxy
    extra = 0
    fields = ['order','title','state']

class TVShowProxyAdmin(admin.ModelAdmin):
    inlines = [TVShowSeasonInline]
    fields = ['title','description','state','video','slug']
    class Meta:
        model = TVShowProxy

admin.site.register(Playlist,PlaylistAdmin)

admin.site.register(TVShowProxy,TVShowProxyAdmin)

admin.site.register(TVShowSeasonProxy,TVShowSeasonProxyAdmin)


