from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

User = settings.AUTH_USER_MODEL


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='название ингредиента',
        db_index=True
    )
    unit = models.CharField(
        max_length=15,
        verbose_name='единица измерения',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.unit}'


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='тег')
    slug = models.SlugField(max_length=50, unique=True)
    color = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='цвет тега',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        related_name='recipes',
    )
    name = models.CharField(max_length=200, verbose_name='название рецепта')
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name='картинка',
    )
    description = models.TextField(verbose_name='текстовое описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
    )
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_amounts',
        verbose_name='рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        validators=[MinValueValidator(1)],
        verbose_name='количество',
    )

    class Meta:
        verbose_name = 'рецепт-ингредиент'
        verbose_name_plural = 'рецепты-ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient',
            )
        ]

    def __str__(self):
        name = (
            f"{self.ingredient.name} - {self.amount} "
            f"{self.ingredient.unit}"
        )
        return name


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='follower',

    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = ('author',)
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow')]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='рецепт',
    )

    def __str__(self):
        return self.recipe.name

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'избранное'
        ordering = ('user', )
