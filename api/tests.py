from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user_registration')
        self.valid_payload = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword',
            'password_confirmation': 'testpassword',
            'referral_code': 'referrer@example.com'
        }
        self.invalid_payload = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword',
            'password_confirmation': 'differentpassword',
            'referral_code': 'nonexistent@example.com'
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_failure(self):
        response = self.client.post(self.register_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
