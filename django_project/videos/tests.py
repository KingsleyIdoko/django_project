from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
# Create your tests here.
from .models import Video


class VideoModelTestCase(TestCase):

    def setUp(self):
        self.obj_a  = Video.objects.create(title="This is my first title", video_id='abc')
        self.obj_b  = Video.objects.create(title="This is my 2nd title", state=Video.VideoStateOptions.PUBLISH,video_id='acc')

    def test_slugify(self):
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.obj_a.slug)

    def test_validate_title(self):
        qs = Video.objects.filter(title="This is my first title")
        self.assertEqual(qs.exists(), 1)

    def test_video_count(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Video.objects.filter(state=Video.VideoStateOptions.DRAFT)
        self.assertEqual(qs.count(),1)

    def test_publish_case(self):
        now = timezone.now()
        qs = Video.objects.filter(state=Video.VideoStateOptions.PUBLISH,published_timestamp__lte=now)
        self.assertTrue(qs.exists())

    def test_published_manager(self):
        qs = Video.objects.all().published()
        qs_2 = Video.objects.published()
        self.assertTrue(qs.count(),qs_2.count())
    