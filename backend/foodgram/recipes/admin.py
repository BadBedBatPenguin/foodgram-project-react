from django.contrib import admin

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


class IngredientInline(admin.StackedInline):
    model = IngredientInRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')

    @admin.display()
    def count_favorites(self, obj):
        return obj.favorites.count()
    count_favorites.short_description = (
        'Общее число добавлений рецепта в избранное'
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
