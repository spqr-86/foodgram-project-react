from django.urls import path

from . import views

urlpatterns = (
    path('',
         views.ShoppingListView.as_view(),
         name='purchases',
         ),
    path('<int:recipe_id>/',
         views.ShoppingListView.as_view(),
         name='delete_purchase'),
    path('get-pdf/',
         views.get_pdf,
         name='get_pdf'),
)
