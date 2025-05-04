from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Organization, Kudo

User = get_user_model()

class ModelTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="TestOrg")
        self.user1 = User.objects.create_user(
            username="user1", 
            password="testpass123", 
            organization=self.org
        )
        self.user2 = User.objects.create_user(
            username="user2", 
            password="testpass123", 
            organization=self.org
        )

    def test_create_kudo(self):
        kudo = Kudo.objects.create(
            from_user=self.user1,
            to_user=self.user2,
            message="Great job!"
        )
        self.assertEqual(str(kudo), f"Kudo from {self.user1} to {self.user2}")

class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.org = Organization.objects.create(name="TestOrg")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            organization=self.org
        )
        self.client.force_authenticate(user=self.user)

    def test_get_users(self):
        res = self.client.get('/api/users/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_give_kudo(self):
        user2 = User.objects.create_user(
            username="user2",
            password="testpass123",
            organization=self.org
        )
        payload = {
            'to_user_id': str(user2.id),
            'message': 'Great work!'
        }
        res = self.client.post('/api/kudos/give_kudo/', payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

# Create your tests here.
