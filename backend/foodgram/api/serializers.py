from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe, Tag, Ingredient, IngredientInRecipe
from users.models import Follow, User

from djoser import serializers as djoser_serializers
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    # is_subscribed = serializers.SerializerMethodField()
    #
    # def get_is_subscribed(self, obj):
    #     author_id = self.context['view'].kwargs.get('user_id')
    #     author = get_object_or_404(User, id=author_id)
    #     return Follow.filter(user=self.context['request'].user, author=author).exists()

    class Meta:
        fields = ('username', 'email', 'id', 'first_name',
                  # 'last_name', 'is_subscribed')
                  'last_name')
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
        }


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'first_name',
                  # 'last_name', 'is_subscribed')
                  'last_name', 'password')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    id = serializers.ReadOnlyField(source='ingredient.id')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = (
            UniqueTogetherValidator(
                queryset=IngredientInRecipe.objects.all(),
                fields=('ingredient', 'recipe')
            ),
        )
        # fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']
        # read_only_fields = ['id', 'name', 'measurement_unit']


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        many=True,
        read_only=True,
        source='ingredientinrecipe_set'
    )
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'tags',
                  'image', 'name', 'text', 'cooking_time',)
                  # 'is_favorited', 'is_in_shopping_cart')

    # def get_is_favorited(self, obj):
    #     user = self.context.get('request').user
    #     if user.is_anonymous:
    #         return False
    #     return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()
    #
    # def get_is_in_shopping_cart(self, obj):
    #     user = self.context.get('request').user
    #     if user.is_anonymous:
    #         return False
    #     return Recipe.objects.filter(cart__user=user, id=obj.id).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Требуется не менее одного ингредиента для рецепта'})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError('Ингредиенты должны '
                                                  'быть уникальными')
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': 'Количество ингредиента должно быть не менее 1'
                })
        data['ingredients'] = ingredients
        return data

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe = Recipe.objects.create(**validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientInRecipe.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance


class RecipeObtainSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = IngredientSerializer(many=True)
    # is_favorited, is_in_shopping_cart - добавить поля

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListSerializer(child=serializers.IntegerField())
    ingredients = IngredientInRecipeSerializer(many=True)
    # ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()
    cooking_time = serializers.IntegerField()
    # is_favorited, is_in_shopping_cart - добавить поля

    class Meta:
        model = Recipe
        fields = (
            'id', 'author',
            'name', 'image', 'text', 'cooking_time',
            'tags',
            'ingredients',
        )
        read_only_fields = ('author',)

    # def get_ingredients(self, obj):
    #     request = self.context.get('request')
    #     queryset = Recipe.objects.filter(id__in=[ingredient['id'] for ingredient in request.data['ingredients']])
    #     return IngredientInRecipeSerializer(queryset, many=True).data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=User.objects.get(id=self.validated_data), **validated_data)
        IngredientInRecipe.objects.bulk_create(
            [
                IngredientInRecipe(
                    recipe=recipe,
                    ingredient=ingredient['id'],
                    amount=ingredient['amount']
                )
                for ingredient in ingredients
            ]
        )
        for tag in tags:
            recipe.tags.add(tag)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeObtainSerializer(instance, context=context).data

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError('Время готовки не может быть меньше минуты')
        return value


# class FollowSerializer(serializers.ModelSerializer):
#     # recipes = serializers.SerializerMethodField(read_only=True)
#     # recipes_count = serializers.SerializerMethodField(read_only=True)
#     user = serializers.SlugRelatedField(
#         slug_field='username',
#         read_only=True,
#         default=serializers.CurrentUserDefault()
#     )
#     author = serializers.SlugRelatedField(
#         slug_field='username',
#         queryset=User.objects.all(),
#         many=True
#     )
#
#     class Meta:
#         model = Follow
#         fields = ('user', 'author')
#         validators = (
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=('user', 'author',)
#             ),)
#
#     def get_is_subscribed(self, obj):
#         user = self.context.get('request').user
#         if user.is_anonymous:
#             return False
#         return Follow.objects.filter(user=user, author=obj).exists()
#
#     def validate(self, data):
#         user = self.context('request').user
#         if user == data['author']:
#             raise serializers.ValidationError('на себя нельзья подписаться')
#         return data
#
#     def get_recipes_count(self, obj):
#         return Recipe.objects.filter(author=obj).count()
#
#     def get_recipes(self, obj):
#         request = self.context.get('request')
#         limit = request.GET.get('recipes_limit')
#         queryset = Recipe.objects.filter(author=obj)
#         if limit:
#             queryset = queryset[:int(limit)]
#         return RecipeSubscribeSerializer(queryset, many=True).data
