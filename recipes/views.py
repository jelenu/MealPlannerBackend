from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Recipe
from .serializers import RecipeSerializer

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
