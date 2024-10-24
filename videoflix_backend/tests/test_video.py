from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from videos.signals import video_post_save
from videos.models import Video
from videos.serializers import SingleVideoSerializer, VideoSerializer

class VideoTests(APITestCase):
    
    def setUp(self):
        post_save.disconnect(video_post_save, sender=Video)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.video = Video.objects.create(title='Test Video', description='Test Beschreibung', genre='animals')
    
    def test_detail_view_video(self):
        url = reverse('single-video') + f'?video_id={self.video.id}'
        response = self.client.get(url)
        expected_data = SingleVideoSerializer(self.video).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], expected_data['title'])
        self.assertEqual(response.data['description'], expected_data['description'])
        self.assertEqual(response.data['genre'], expected_data['genre'])
         
    def test_list_video(self):
        url = reverse('all-videos')
        response = self.client.get(url)
        expected_data = VideoSerializer(Video.objects.all(), many=True).data
        
        self.assertEqual(response.data, expected_data)
        
    def test_detail_view_video_unauthorized(self):
        url = reverse('single-video') + f'?video_id={self.video.id}'
        self.client.credentials()
        response = self.client.get(url)
        
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_list_video_unauthorized(self):
        url = reverse('all-videos')
        self.client.credentials()
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_detail_view_video_no_id(self):
        url = reverse('single-video') + '?video_id=999999'  # Ungültige ID
        response = self.client.get(url)
        
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            