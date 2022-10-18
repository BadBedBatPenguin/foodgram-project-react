from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Модель Ingredient"""
    name = models.TextField(verbose_name='Название')
    measurement_unit = models.CharField(max_length=10, verbose_name='Единица измерения')

    class Meta:
        """Дополнительная информация по управлению моделью Ingredient."""
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique ingredient'
            )
        ]

    def __str__(self):
        return {self.name}


class Tag(models.Model):
    """Модель Tag"""
    name = models.TextField(verbose_name='Название')
    color = models.CharField(max_length=7, verbose_name='Цвет') # надо ещё валидацию придумать
    slug = models.SlugField(
        unique=True,
        # max_length=50,
        verbose_name='Идентификатор',
    )

    class Meta:
        """Дополнительная информация по управлению моделью Tag."""
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель Recipe"""
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        verbose_name='Ингредиенты',
        through='IngredientInRecipe',
        related_name='recipes',
        # through_fields=('recipe'
        # , 'ingredient')
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name='Тэги',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='backend_media/'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(validators.MinValueValidator(
            1, message='Минимальное время приготовления - 1 минута'
        ),),
    )

    # def is_favorited(self):
    #     return self.id in self.favorite # доделать как организую раздел избранное
    #
    # def is_in_shopping_cart(self):
    #     return self.id in self.shopping_cart # доделать как организую корзину

    class Meta:
        """Дополнительная информация по управлению моделью Recipe."""
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(validators.MinValueValidator(
            1, message='Минимальное количество - 1 единица'
        ),)
    )

    class Meta:
        """Дополнительная информация по управлению моделью IngredientInRecipe."""
        verbose_name = 'Ингредиент с количеством'
        verbose_name_plural = 'Ингредиенты с количеством'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique ingredients recipe'
            )
        ]

    def __str__(self):
        return self.ingredient.name


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique cart user')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique favorite recipe for user')
        ]
