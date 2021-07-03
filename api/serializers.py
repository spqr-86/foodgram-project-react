from django.contrib.auth import get_user_model

from recipes.models import Favorite, Follow, Ingredient, Recipe

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'unit']
        model = Ingredient


class SubscribeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        queryset=User.objects.all(),
        slug_field='id', )
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = Follow
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author']
            )
        ]

    def validate(self, data):
        if (self.context['request'].method == 'POST'
                and data['author'] == data['user']):
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя")
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(
        many=False,
        queryset=Recipe.objects.all(),
        slug_field='id', )
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username', )

    class Meta:
        model = Favorite
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe']
            )
        ]
