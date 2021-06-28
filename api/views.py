from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins
from rest_framework.views import APIView

from recipes.models import Ingredient, Follow, Favorite, Recipe


from .serializers import (IngredientSerializer)

User = get_user_model()

SUCCESS_RESPONSE = JsonResponse({'success': True})
BAD_RESPONSE = JsonResponse({'success': False}, status=400)


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['^name', ]


class SubscribeView(APIView):
    def post(self, request):
        author_id = int(self.request.data.get('id'))
        author = get_object_or_404(User, id=author_id)
        user = request.user
        if author_id and author != user:
            Follow.objects.get_or_create(user=user, author=author)
            return SUCCESS_RESPONSE
        else:
            return BAD_RESPONSE

    def delete(self, request, author_id):
        follow = Follow.objects.filter(user=request.user, author=author_id)
        follow.delete()
        return SUCCESS_RESPONSE


class FavoriteView(APIView):
    def post(self, request):
        recipe_id = int(self.request.data.get('id'))
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        if recipe_id:
            Favorite.objects.get_or_create(user=user, recipe=recipe)
            return SUCCESS_RESPONSE
        else:
            return BAD_RESPONSE

    def delete(self, request, recipe_id):
        Favorite.objects.filter(
            user=request.user, recipe=recipe_id).delete()
        return SUCCESS_RESPONSE
