from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe, Tag, Ingredient
from users.models import Follow, User


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


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        # fields = ['username', 'email', 'id', 'first_name',
        #           'last_name', 'is_subscribed']
        fields = ['username', 'email', 'id', 'first_name',
                  'last_name']
        model = User
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
        }

        def get_is_subscribed(self, obj):
            return Follow.objects.filter(user=self.context['request'].user, author=obj.id).exists()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'author', 'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']
        read_only_fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'value', 'measurement_unit']
        read_only_fields = ['id', 'name', 'value', 'measurement_unit']


class FollowSerializer(serializers.ModelSerializer):
    # recipes = serializers.SerializerMethodField(read_only=True)
    # recipes_count = serializers.SerializerMethodField(read_only=True)
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        many=True
    )

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author',)
            ),
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()

    def validate(self, data):
        user = self.context('request').user
        if user == data['author']:
            raise serializers.ValidationError('на себя нельзя подписаться')
        return data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeSubscribeSerializer(queryset, many=True).data
