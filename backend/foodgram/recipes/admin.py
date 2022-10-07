from django.contrib import admin
from .models import Tag, Ingredient, Recipe, IngredientInRecipe


class IngredientInline(admin.StackedInline):
    model = IngredientInRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
    list_display = ['image', 'name', 'text', 'cooking_time']


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
