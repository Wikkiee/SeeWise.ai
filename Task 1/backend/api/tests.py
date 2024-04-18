from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Video

class VideoModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.video = Video.objects.create(title='Test Video', url='https://example.com/video.mp4', bucket_id='123', author=self.user)

    def test_video_creation(self):
        """Test creating a new video instance"""
        self.assertEqual(self.video.title, 'Test Video')
        self.assertEqual(self.video.author, self.user)

    def test_video_str_representation(self):
        """Test string representation of Video model"""
        self.assertEqual(str(self.video), 'Test Video')


class VideoViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.video = Video.objects.create(title='Test Video', url='https://example.com/test_video.mp4', bucket_id='789-abc-xyz', author=self.user)

    def test_all_videos_list(self):
        """Test retrieving all videos (GET /videos/)"""
        url = reverse('all-video-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_video(self):
        """Test creating a new video (POST /videos/retrive-and-upload/)"""
        url = reverse('user-video-list')
        data = {'title': 'New Video', 'url': 'https://example.com/new_video.mp4', 'bucket_id': '456'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_video_by_bucket_id(self):
        """Test retrieving a video by bucket ID (GET /videos/get/<bucket_id>/)"""
        url = reverse('get_video_by_id', kwargs={'bucket_id': '789-abc-xyz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'title': 'Test Video',
            'url': 'https://example.com/test_video.mp4',
            'bucket_id': '789-abc-xyz',
            'author': self.user.id  
        }
        filtered_response_data = {
            key: response.data[key] for key in expected_data.keys() if key in response.data
        }
        self.assertDictEqual(filtered_response_data, expected_data)

    def test_get_video_by_wrong_bucket_id(self):
        """Test retrieving a video by wrong bucket ID (GET /videos/get/<bucket_id>/)"""
        url = reverse('get_video_by_id', kwargs={'bucket_id': '123-abc-xyz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        expected_data = {'message': 'Video not found'}
        self.assertDictEqual(response.data, expected_data)

    def test_video_search_with_match(self):
        """Test searching for videos by title with a match (GET /videos/search/<search_term>/)"""
        search_term = 'vid'
        url = reverse('search-video-list', kwargs={'search_term': search_term})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Ensure at least one video is returned

    def test_video_search_with_no_match(self):
        """Test searching for videos by title with no match (GET /videos/search/<search_term>/)"""
        search_term = 'xyz'  
        url = reverse('search-video-list', kwargs={'search_term': search_term})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0) 

    def test_delete_video(self):
        """Test deleting a video (DELETE /videos/delete/<pk>/)"""
        url = reverse('video-delete', kwargs={'pk': self.video.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Video.objects.filter(pk=self.video.pk).exists())

    def test_update_video_title(self):
        """Test updating a video's title (PUT /videos/update/<pk>/)"""
        url = reverse('video-title-update', kwargs={'pk': self.video.pk})
        new_title = 'Updated Test Video'
        data = {'title': new_title}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_video = Video.objects.get(pk=self.video.pk)
        self.assertEqual(updated_video.title, new_title)
