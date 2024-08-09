from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from .models import Playlist,PublishedStateOptions
from videos.models import Video

class PlaylistModelTestCase(TestCase):
    
    def create_videos(self):
        video_a         = Video.objects.create(title="This is my first title",video_id="abc4321")
        video_b         = Video.objects.create(title="This is my first title",video_id="abc4322")
        video_c         = Video.objects.create(title="This is my first title",video_id="abc4323")
        self.video_a    = video_a
        self.video_b    = video_b
        self.video_c    = video_c
        self.video_qs   = Video.objects.all()

    def create_show_with_seasons(self):
        the_office  = Playlist.objects.create(title='The Office Series')
        season_1    = Playlist.objects.create(parent=the_office,title='The Office Series Season 1',order=1)
        season_2    = Playlist.objects.create(parent=the_office,title='The Office Series Season 2',order=1)
        season_3    = Playlist.objects.create(parent=the_office,title='The Office Series Season 3',order=1)
        shows       = Playlist.objects.filter(parent__isnull=True)
        self.show   = the_office

    def setUp(self):
        self.create_videos()
        self.create_show_with_seasons()
        self.obj_a = Playlist.objects.create(title="This is my first title",video=self.video_a)
        obj_b = Playlist.objects.create(title="This is my 2nd title",state=PublishedStateOptions.PUBLISH,video=self.video_a)
        obj_b.videos.set(self.video_qs)
        obj_b.save()
        self.obj_b = obj_b

    def test_show_has_seasons(self):
        seasons  = self.show.playlist_set.all()
        self.assertTrue(seasons.exists())
        self.assertEqual(seasons.count(),3)

    def test_playlist_video_through_model(self):
        v_qs = sorted(list(self.video_qs.values_list("id")))
        video_qs = sorted(list(self.obj_b.videos.all().values_list('id')))
        playlistItem_qs =  sorted(list(self.obj_b.playlistitem_set.all().values_list('video')))
        self.assertEqual(v_qs,video_qs,playlistItem_qs)

    def test_video_playlist(self):
        qs = self.video_a.featured_published.all()
        self.assertEqual(qs.count(),2)

    def test_playlist_video(self):
        self.assertEqual(self.obj_a.video,self.video_a)

    def test_vido_playlist_ids_property(self):
        reverse_id = self.obj_a.video.get_playlist_id()
        actual_id = list(Playlist.objects.filter(video=self.video_a).values_list('id', flat=True))
        self.assertEqual(reverse_id,actual_id)

    def test_slugify(self):
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.obj_a.slug)

    def test_validate_title(self):
        qs = Playlist.objects.filter(title="This is my first title")
        self.assertEqual(qs.exists(), 1)

    def test_Playlist_count(self):
        qs = Playlist.objects.all()
        self.assertEqual(qs.count(), 6)

    def test_draft_case(self):
        qs = Playlist.objects.filter(state=PublishedStateOptions.DRAFT)
        self.assertEqual(qs.count(),5)

    def test_publish_case(self):
        now = timezone.now()
        qs = Playlist.objects.filter(state=PublishedStateOptions.PUBLISH,published_timestamp__lte=now)
        self.assertTrue(qs.exists())

    def test_published_manager(self):
        qs = Playlist.objects.all().published()
        qs_2 = Playlist.objects.published()
        self.assertTrue(qs.count(),qs_2.count())
    