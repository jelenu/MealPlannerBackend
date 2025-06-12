from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class CreateRecipeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="StrongPassword123!"
        )
        self.url = reverse('my-recipes')

    def test_create_recipe_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Test Recipe",
            "description": "A simple test recipe.",
            "preparation_time": 30,
            "ingredients": "Eggs, Flour, Milk",
            "steps": "Mix ingredients. Bake.",
            "category": "Dessert",
            "is_public": True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)
        recipe = Recipe.objects.first()
        self.assertEqual(recipe.title, "Test Recipe")
        self.assertEqual(recipe.author, self.user)

    def test_create_recipe_unauthenticated(self):
        data = {
            "title": "Test Recipe",
            "description": "A simple test recipe.",
            "preparation_time": 30,
            "ingredients": "Eggs, Flour, Milk",
            "steps": "Mix ingredients. Bake.",
            "category": "Dessert",
            "is_public": True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)