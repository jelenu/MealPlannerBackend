from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class DetailRecipeTests(APITestCase):
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
            title="Recipe Detail",
            description="Detail desc",
            preparation_time=15,
            ingredients="Eggs, Milk",
            steps="Step 1, Step 2",
            category="Test",
            is_public=True
        )
        self.url = reverse('my-recipe-detail', args=[self.recipe.id])

    def test_detail_recipe_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Recipe Detail")
        self.assertEqual(response.data['author'], self.user.id)

    def test_detail_recipe_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_recipe_not_author(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)