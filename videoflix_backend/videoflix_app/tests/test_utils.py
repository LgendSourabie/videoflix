from django.http import Http404
from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import CustomUser
from videoflix_app.models import Video
from fixtures.factories import VideoFactory,UserFactory
from videoflix_app.api.utils import get_or_404, delete_files_starting_with

class GetOr404Test(APITestCase):
    """Test get model or return 404 Not found"""
    
    def setUp(self):
        self.video = VideoFactory()
        self.user = UserFactory()


    def tearDown(self):
        Video.objects.all().delete()
        CustomUser.objects.all().delete()


    def test_get_model_from_pk(self):
        """Test get model for existing model and integer key"""

        model = get_or_404(CustomUser, self.user.pk)
        self.assertIsInstance(model,CustomUser)
        model = get_or_404(Video, str(self.video.pk))
        self.assertIsInstance(model,Video)


    def test_get_model_from_bad_pk(self):
        """Test get model for existing model and integer key"""

        with self.assertRaisesMessage(ValueError, "The ID must be an integer"):
            get_or_404(CustomUser, 'null')
        with self.assertRaisesMessage(Http404,"Model does not exist"):
            get_or_404(Video, 100)

