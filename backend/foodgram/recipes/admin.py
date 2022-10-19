from django.contrib import admin

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


class IngredientInline(admin.StackedInline):
    model = IngredientInRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
    list_display = ('name', 'author', 'text')
    list_filter = ('author', 'name', 'tags')


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
