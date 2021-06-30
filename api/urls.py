from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteDeleteViewSet, FavoriteViewSet, IngredientViewSet,
                    ShopListViewSet, SubscribeDeleteViewSet, SubscribeViewSet)

v1_patterns = (
    [
        path('subscriptions/<int:author_id>/',
             SubscribeDeleteViewSet.as_view(),
             name='delete_follow',
             ),
        path('favorites/<int:recipe_id>/',
             FavoriteDeleteViewSet.as_view(),
             name='delete_follow',
             ),
        path('purchases/',
             ShopListViewSet.as_view(),
             name='purchases',
             ),
        path('purchases/<int:recipe_id>/',
             ShopListViewSet.as_view(),
             name='delete_purchase'),
    ]
)

v1_router = DefaultRouter()

v1_router.register(r'ingredients',
                   IngredientViewSet,
                   basename='ingredients')
v1_router.register(r'subscriptions',
                   SubscribeViewSet,
                   basename='add_follow')
v1_router.register(r'favorites',
                   FavoriteViewSet,
                   basename='add_favorite')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(v1_patterns)),

]
