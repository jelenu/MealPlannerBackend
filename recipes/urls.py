from django.urls import path
from .views import RecipeListCreateView, RecipeRetrieveUpdateDestroyView, EdamamRecipeSearchView, EdamamRecipeDetailByUriView
from .views import FavoriteRecipeListCreateView, FavoriteRecipeDestroyView

urlpatterns = [
    path('my/', RecipeListCreateView.as_view(), name='my-recipes'),
    path('my/<int:pk>/', RecipeRetrieveUpdateDestroyView.as_view(), name='my-recipe-detail'),
    
    path('edamam/search/', EdamamRecipeSearchView.as_view(), name='edamam-search'),
    path('edamam/detail/', EdamamRecipeDetailByUriView.as_view(), name='edamam-detail'),

    path('favorites/', FavoriteRecipeListCreateView.as_view(), name='favorite-recipes'),
    path('favorites/<int:pk>/', FavoriteRecipeDestroyView.as_view(), name='favorite-recipe-delete'),
]