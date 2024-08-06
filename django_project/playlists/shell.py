from videos.models import Video
from playlists.models import Playlist

video_a         = Video.objects.create(title="This is my title",video_id="abc4")
playlist_a      = Playlist.objects.create(title="This is my first title",video=video_a)



    