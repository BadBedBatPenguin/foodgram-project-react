from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ingredient(models.Model):
    name = models.TextField(verbose_name='Название')
    # value = models.PositiveSmallIntegerField(
    #     verbose_name='Количество',
    #     # validators=[year_validator],
    # )
    measurement_unit = models.CharField(max_length=10, verbose_name='Единица измерения')

    def __str__(self):
        return f'Ингредиент {self.name}'

    class Meta:
        """Дополнительная информация по управлению моделью Ingredient."""
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        # ordering = ('-pub_date',)


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество'
    )


class Tag(models.Model):
    name = models.TextField(verbose_name='Название')
    color = models.CharField(max_length=7, verbose_name='Цвет') # надо ещё валидацию придумать
    slug = models.SlugField(
        unique=True,
        # max_length=50,
        verbose_name='Идентификатор',
    )

    def __str__(self):
        return f'Тэг {self.name}'

    class Meta:
        """Дополнительная информация по управлению моделью Tag."""
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        # ordering = ('-pub_date',)

class Recipe(models.Model):
    """Recipe model"""
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        to=IngredientInRecipe,
        verbose_name='Ингредиенты',
        blank=True,
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name='Тэги',
        blank=True,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/', # настроить эту папку!
        blank=True
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField('Текст', help_text='Введите текст рецепта')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        # validators=[year_validator],
    )

    # def is_favorited(self):
    #     return self.id in self.favorite # доделать как организую раздел избранное
    #
    # def is_in_shopping_cart(self):
    #     return self.id in self.shopping_cart # доделать как организую корзину

    def __str__(self):
        return f'Рецепт {self.name}'

    class Meta:
        """Дополнительная информация по управлению моделью Recipe."""
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        # ordering = ('-pub_date',)
