from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class AdministrationTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email= 'test@test.de')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def test_login(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_login_wrong_data(self):
        url = reverse('login')
        data = {
            'username': 'testuser2',
            'password': 'testpassword2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_user_not_active(self):
        url = reverse('login')
        self.user.is_active = False
        self.user.save()
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_register(self):
        url = reverse('register')
        data = {
            'username': 'testuser2',
            'password': 'testpassword',
            'email': 'testuser@test.de'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_register_user_already_exists(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@test.de'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_reset_password(self):
        url = reverse('reset-password')
        data = {
            'email': 'test@test.de'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_reset_password_wrong_mail(self):
        url = reverse('reset-password')
        data = {
            'email': 'test2@test.de'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_set_new_password(self):
        url = reverse('set-new-password')
        data = {
            'email': 'test@test.de',
            'password': 'test1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_set_new_password_wrong_password(self):
        url = reverse('set-new-password')
        data = {
            'email': 'test2@test.de',
            'password': 'test1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)