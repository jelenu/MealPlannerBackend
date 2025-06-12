from django.db import models
from django.conf import settings

class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes")
    ingredients = models.TextField(help_text="Free text or list of ingredients")
    steps = models.TextField(help_text="Recipe steps")
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False, help_text="Is this recipe visible to everyone?")

    def __str__(self):
        return self.title

class FavoriteRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_recipes')
    uri = models.CharField(max_length=255)
    label = models.CharField(max_length=255, blank=True)  # opcional, para mostrar el nombre
    image = models.URLField(blank=True)  # opcional, para mostrar la imagen
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'uri')

    def __str__(self):
        return f"{self.user.username} - {self.label or self.uri}"
