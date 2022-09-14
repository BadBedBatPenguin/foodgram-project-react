# Generated by Django 4.0.4 on 2022-09-14 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_ingredients_alter_recipe_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='value',
        ),
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient')),
            ],
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, to='recipes.ingredientinrecipe', verbose_name='Ингредиенты'),
        ),
    ]
