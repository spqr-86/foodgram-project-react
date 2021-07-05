from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

handler404 = "views.page_not_found"  # noqa
handler500 = "views.server_error"  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('about-author/', views.flatpage,
         {'url': '/about-author/'}, name='author'),
    path('about-spec/', views.flatpage,
         {'url': '/about-spec/'}, name='spec'),
    path('help/', views.flatpage,
         {'url': '/help/'}, name='help'),
    path('purchases/', include('shopping_list.urls')),
    path('', include('recipes.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
