from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_register_success(self):
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "StrongPassword123!",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("msg", response.data)
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())

    def test_register_with_existing_email(self):
        data = {
            "email": "testuser3@example.com",
            "username": "testuser3",
            "password": "StrongPassword123!",
        }
        User.objects.create_user(email="testuser3@example.com", username="testuser3", password="StrongPassword123!")

        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data) 

    def test_register_with_existing_username(self):
        User.objects.create_user(email="uniqueemail@example.com", username="repeateduser", password="StrongPassword123!")
        data = {
            "email": "anotheremail@example.com",
            "username": "repeateduser",
            "password": "StrongPassword123!",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_register_weak_password(self):
        data = {
            "email": "testuser4@example.com",
            "username": "testuser4",
            "password": "123",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_register_missing_fields(self):
        data = {
            "email": "",
            "username": "",
            "password": "", 
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("username", response.data)
        self.assertIn("password", response.data)