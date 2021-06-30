from django.contrib.auth import get_user_model
from django.http import JsonResponse
from recipes.models import Favorite, Follow, Ingredient
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from shopping_list.mixins import ShopList

from .serializers import (FavoriteSerializer, IngredientSerializer,
                          SubscribeSerializer)

User = get_user_model()

SUCCESS_RESPONSE = JsonResponse({'success': True})
BAD_RESPONSE = JsonResponse({'success': False}, status=400)


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['^name', ]


class SubscribeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscribeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscribeDeleteViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, author_id):
        follow = Follow.objects.filter(user=request.user, author=author_id)
        if follow:
            follow.delete()
            return SUCCESS_RESPONSE
        return BAD_RESPONSE


class FavoriteDeleteViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, recipe_id):
        favorite = Favorite.objects.filter(
            user=request.user, recipe=recipe_id)
        if favorite:
            favorite.delete()
            return SUCCESS_RESPONSE
        return BAD_RESPONSE


class ShopListViewSet(APIView):
    def post(self, request):
        shop_list = ShopList(request)
        recipe_id = self.request.data.get('id')
        if recipe_id is not None:
            shop_list.add(int(recipe_id))
            return SUCCESS_RESPONSE
        return BAD_RESPONSE

    def delete(self, request, recipe_id):
        shop_list = ShopList(request)
        shop_list.remove(int(recipe_id))
        return SUCCESS_RESPONSE
