from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class ListRecipesTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="StrongPassword123!"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            username="otheruser",
            password="StrongPassword123!"
        )
        # Recipes for self.user
        Recipe.objects.create(
            author=self.user,
            title="Recipe 1",
            description="Desc 1",
            preparation_time=10,
            ingredients="Eggs",
            steps="Step 1",
            category="Test",
            is_public=False
        )
        Recipe.objects.create(
            author=self.user,
            title="Recipe 2",
            description="Desc 2",
            preparation_time=20,
            ingredients="Milk",
            steps="Step 2",
            category="Test",
            is_public=True
        )
        # Recipe for other_user
        Recipe.objects.create(
            author=self.other_user,
            title="Other Recipe",
            description="Other Desc",
            preparation_time=15,
            ingredients="Flour",
            steps="Other Step",
            category="Other",
            is_public=True
        )
        self.url = reverse('my-recipes')

    def test_list_recipes_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        titles = [r['title'] for r in response.data]
        self.assertIn("Recipe 1", titles)
        self.assertIn("Recipe 2", titles)
        self.assertNotIn("Other Recipe", titles)

    def test_list_recipes_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)