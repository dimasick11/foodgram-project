from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    """Теги"""
    key = models.CharField(max_length=128, primary_key=True, verbose_name='Ключ')
    value = models.CharField(max_length=128, verbose_name='Значение')


class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_author', verbose_name='Автор')
    title = models.CharField(max_length=256, verbose_name='Наименование')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    ingredients = models.ManyToManyField('Ingredient', through='Amount',
                                         through_fields=('recipe', 'ingredient'), verbose_name='Ингредиенты')
    tags = models.ManyToManyField('Tag', verbose_name='Тег')
    time = models.PositiveIntegerField(verbose_name='Время приготовления')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата публикации")
    
    class Meta:
        ordering = ('-pub_date', )
        
    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """Ингредиенты"""
    title = models.CharField(max_length=128, unique=True, verbose_name='Наименование')
    dimension = models.CharField(max_length=128, verbose_name='Мера')
    
    def __str__(self):
        return f"{self.title} ({self.dimension})"
    

class Amount(models.Model):
    """Колличество ингредиетов в рецепте"""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    quantity = models.PositiveIntegerField(verbose_name='Колличество')


class Favorite(models.Model):
    """Рецепты избранные"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite_follower', verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorite_recipe', verbose_name='Понравившейся рецепт')
    
    
class Purchase(models.Model):
    """Рецетов на покупки"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_purchase', verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_purchase', verbose_name='Рецепт')
