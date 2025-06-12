from rest_framework import serializers
from .models import Recipe, FavoriteRecipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['author', 'created_at']

class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ['id', 'uri', 'label', 'image', 'added_at']
        read_only_fields = ['id', 'added_at']

    def validate(self, data):
        user = self.context['request'].user
        uri = data.get('uri')
        if FavoriteRecipe.objects.filter(user=user, uri=uri).exists():
            raise serializers.ValidationError({'uri': 'This recipe is already in your favorites.'})
        return data