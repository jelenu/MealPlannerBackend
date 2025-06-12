from django.urls import path
from .views import RecipeListCreateView, RecipeRetrieveUpdateDestroyView

urlpatterns = [
    path('my/', RecipeListCreateView.as_view(), name='my-recipes'),
    path('my/<int:pk>/', RecipeRetrieveUpdateDestroyView.as_view(), name='my-recipe-detail'),
]