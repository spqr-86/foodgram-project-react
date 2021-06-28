from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('about-author/', views.flatpage,
         {'url': '/about-author/'}, name='author'),
    path('about-spec/', views.flatpage,
         {'url': '/about-spec/'}, name='spec'),
    path('purchases/', include('shopping_list.urls')),
    path('', include('recipes.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
