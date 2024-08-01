from django.test import TestCase

# Create your tests here.
from .models import Video

class VideoModelTestCase(TestCase):

    def setUp(self):
        Video.objects.create(title="This is my first title")

    def test_validate_title(self):
        qs = Video.objects.filter(title="This is my first title")
        self.assertEqual(qs.exists(), 1)

    def test_video_count(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 1)


    def test_draft_case(self):
        qs = Video.objects.filter(state=Video.VideoStateOptions.DRAFT)
        self.assertEqual(qs.count(),1)