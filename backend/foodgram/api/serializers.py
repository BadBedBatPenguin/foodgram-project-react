from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient
from users.models import User


# class CreateUserSerializer(serializers.Serializer):
#     username = serializers.RegexField(
#         r'^[\w.@+-]+$',
#         max_length=150,
#         required=True
#     )
#     email = serializers.EmailField(required=True, max_length=254)

    # def validate_username(self, value):
    #     if value == 'me':
    #         raise serializers.ValidationError(
    #             'Имя пользователя "me" не допустимо!'
    #         )
    #     return value


# class UserSerializer(serializers.ModelSerializer):
#     username = serializers.RegexField(
#         r'^[\w.@+-]+$',
#         max_length=150,
#         required=True
#     )
#
#     class Meta:
#         fields = ['username', 'email', 'first_name',
#                   'last_name', 'password']
#         model = User
#         lookup_field = 'username'
#         extra_kwargs = {
#             'email': {'required': True},
#             'first_name': {'required': True},
#             'last_name': {'required': True},
#             'password': {'required': True},
#         }


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'author', 'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'value', 'measurement_unit']
