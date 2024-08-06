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

    def setUp(self):
        self.create_videos()
        self.obj_a = Playlist.objects.create(title="This is my first title",video=self.video_a)
        obj_b = Playlist.objects.create(title="This is my 2nd title",
                                    state=PublishedStateOptions.PUBLISH,video=self.video_a)
        obj_b.set(videos=[self.video_a,self.video_b,self.video_c])
        obj_b.save()
        self.obj_b = obj_b

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
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Playlist.objects.filter(state=PublishedStateOptions.DRAFT)
        self.assertEqual(qs.count(),1)

    def test_publish_case(self):
        now = timezone.now()
        qs = Playlist.objects.filter(state=PublishedStateOptions.PUBLISH,published_timestamp__lte=now)
        self.assertTrue(qs.exists())

    def test_published_manager(self):
        qs = Playlist.objects.all().published()
        qs_2 = Playlist.objects.published()
        self.assertTrue(qs.count(),qs_2.count())
    