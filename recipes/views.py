from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Recipe, FavoriteRecipe
from .serializers import RecipeSerializer, FavoriteRecipeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.edamam import search_recipes, get_recipe_by_uri

class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class RecipeListCreateView(generics.ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class RecipeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
    queryset = Recipe.objects.all()

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

class EdamamRecipeSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = search_recipes(
            query=request.query_params.get('q'),
            ingredients=request.query_params.get('ingr'),
            diet_labels=request.query_params.getlist('diet'),
            health_labels=request.query_params.getlist('health'),
            cuisine_type=request.query_params.get('cuisineType'),
            meal_type=request.query_params.get('mealType'),
            dish_type=request.query_params.get('dishType'),
        )
        return Response(data)

class EdamamRecipeDetailByUriView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        uri = request.query_params.get('uri')
        if not uri:
            return Response({'error': 'Query parameter "uri" is required.'}, status=status.HTTP_400_BAD_REQUEST)
        data = get_recipe_by_uri(uri)
        return Response(data)

class FavoriteRecipeListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteRecipe.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteRecipeDestroyView(generics.DestroyAPIView):
    serializer_class = FavoriteRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteRecipe.objects.filter(user=self.request.user)