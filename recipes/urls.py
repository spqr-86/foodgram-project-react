from django.urls import path

from . import views

urlpatterns = [
    path('',
         views.IndexView.as_view(),
         name='index'),
    path('<int:recipe_id>/<slug:slug>/',
         views.RecipeDetail.as_view(),
         name='recipe_detail'
         ),
    path('recipe-new/',
         views.RecipeNew.as_view(),
         name='new_recipe'),
    path('recipe-edit/<str:username>/<int:pk>/',
         views.RecipeUpdate.as_view(),
         name='recipe_edit'),
    path('recipe-delete/<str:username>/<int:pk>/',
         views.RecipeDelete.as_view(),
         name='recipe_delete'),
    path('follow/',
         views.MyFollowView.as_view(),
         name='my_follow'),
    path('favorites/',
         views.FavoriteListView.as_view(),
         name='my_favorite'),
    path('<str:author>/',
         views.AuthorView.as_view(),
         name='author'),
]
