from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from recipes.models import FavoriteRecipe

User = get_user_model()

class FavoriteRecipeTests(APITestCase):
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
        self.client.force_authenticate(user=self.user)
        self.uri = "http://www.edamam.com/ontologies/edamam.owl#recipe_test"
        self.label = "Chicken Soup"
        self.image = "https://www.edamam.com/web-img/test.jpg"
        self.favorite = FavoriteRecipe.objects.create(
            user=self.user,
            uri=self.uri,
            label=self.label,
            image=self.image
        )
        self.url = reverse('favorite-recipes')

    def test_add_favorite_recipe(self):
        data = {
            "uri": "http://www.edamam.com/ontologies/edamam.owl#recipe_new",
            "label": "New Recipe",
            "image": "https://www.edamam.com/web-img/new.jpg"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FavoriteRecipe.objects.filter(user=self.user, uri=data["uri"]).exists())

    def test_add_duplicate_favorite_recipe(self):
        data = {
            "uri": self.uri,
            "label": self.label,
            "image": self.image
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_favorite_recipes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(f['uri'] == self.uri for f in response.data))

    def test_delete_favorite_recipe(self):
        delete_url = reverse('favorite-recipe-delete', args=[self.favorite.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FavoriteRecipe.objects.filter(id=self.favorite.id).exists())

    def test_cannot_delete_other_users_favorite(self):
        other_favorite = FavoriteRecipe.objects.create(
            user=self.other_user,
            uri="http://www.edamam.com/ontologies/edamam.owl#recipe_other",
            label="Other Recipe",
            image="https://www.edamam.com/web-img/other.jpg"
        )
        delete_url = reverse('favorite-recipe-delete', args=[other_favorite.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_cannot_add_favorite(self):
        self.client.force_authenticate(user=None)
        data = {
            "uri": "http://www.edamam.com/ontologies/edamam.owl#recipe_unauth",
            "label": "Unauth Recipe",
            "image": "https://www.edamam.com/web-img/unauth.jpg"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_cannot_list_favorites(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_cannot_delete_favorite(self):
        self.client.force_authenticate(user=None)
        delete_url = reverse('favorite-recipe-delete', args=[self.favorite.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)