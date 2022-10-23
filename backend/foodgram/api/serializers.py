from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.models import Follow, User

LEAST_ONE_INGREDIENT_MESSAGE = 'Требуется не менее одного ингредиента для рецепта'
UNIQUE_INGREDIENT_MESSAGE = 'Ингредиенты должны быть уникальными'
LEAST_ONE_AMOUNT_MESSAGE = 'Количество ингредиента должно быть не менее 1'


class CustomUserSerializer(UserSerializer):
    username = serializers.RegexField(
        r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('username', 'email', 'id', 'first_name', 'last_name',
                  'is_subscribed')
        model = User
        lookup_field = 'username'

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'first_name',
                  'last_name', 'password')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
        }


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(source='ingredient.measurement_unit')
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        many=True,
        read_only=True,
        source='ingredientinrecipe_set'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'tags',
                  'image', 'name', 'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientInRecipeSerializer(
        many=True,
        source='ingredientinrecipe_set'
    )

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags',
                  'image', 'name', 'text', 'cooking_time')

    def validate_ingredients(self, data):
        print('validation started')
        print(f'data: {data}')
        ingredients = data
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': LEAST_ONE_INGREDIENT_MESSAGE})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['ingredient']['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError(UNIQUE_INGREDIENT_MESSAGE)
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': LEAST_ONE_AMOUNT_MESSAGE
                })
        return data

    def create_ingredients(self, ingredients, recipe):
        print('create_ingredients started')
        IngredientInRecipe.objects.bulk_create(
            [IngredientInRecipe(
                recipe=recipe,
                ingredient_id=ingredient.get('ingredient').get('id'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        print('create method started')
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredientinrecipe_set')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        print('update method started')
        print(f'validated_data: {validated_data}')
        instance.tags.clear()
        tags_data = validated_data.pop('tags')
        instance.tags.set(tags_data)
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        self.create_ingredients(validated_data.pop('ingredientinrecipe_set'), instance)
        super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        data = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return ShortRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
