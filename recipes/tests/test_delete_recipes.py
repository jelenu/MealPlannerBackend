from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class DeleteRecipeTests(APITestCase):
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
            title="Recipe to Delete",
            description="To be deleted.",
            preparation_time=10,
            ingredients="Eggs",
            steps="Just delete.",
            category="Test",
            is_public=False
        )
        self.url = reverse('my-recipe-detail', args=[self.recipe.id])

    def test_delete_recipe_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=self.recipe.id).exists())

    def test_delete_recipe_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Recipe.objects.filter(id=self.recipe.id).exists())

    def test_delete_recipe_not_author(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=self.recipe.id).exists())