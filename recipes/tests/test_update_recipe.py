from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class UpdateRecipeTests(APITestCase):
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
        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Original Title",
            description="Original description.",
            preparation_time=20,
            ingredients="Eggs, Flour",
            steps="Mix and bake.",
            category="Breakfast",
            is_public=False
        )
        self.url = reverse('my-recipe-detail', args=[self.recipe.id])

    def test_update_recipe_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Updated Title",
            "description": "Updated description.",
            "preparation_time": 25,
            "ingredients": "Eggs, Flour, Milk",
            "steps": "Mix, bake, and serve.",
            "category": "Brunch",
            "is_public": True
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, "Updated Title")
        self.assertEqual(self.recipe.description, "Updated description.")
        self.assertEqual(self.recipe.is_public, True)

    def test_update_recipe_unauthenticated(self):
        data = {
            "title": "Should Not Update",
            "description": "Should Not Update.",
            "preparation_time": 10,
            "ingredients": "None",
            "steps": "None",
            "category": "None",
            "is_public": False
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_recipe_not_author(self):
        self.client.force_authenticate(user=self.other_user)
        data = {
            "title": "Hacker Update",
            "description": "Hacker Update.",
            "preparation_time": 10,
            "ingredients": "None",
            "steps": "None",
            "category": "None",
            "is_public": False
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)