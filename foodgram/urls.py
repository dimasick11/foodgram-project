from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('api/', include('api.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('django.contrib.flatpages.urls')),
]


urlpatterns += [
     path('about/about-author/', views.flatpage,
          {'url': '/about-author/'}, name='about-author'),
     path('about/about-spec/', views.flatpage,
          {'url': '/about-spec/'}, name='about-spec'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)


handler404 = 'foodgram.views.page_not_found' # noqa
handler500 = 'foodgram.views.server_error' # noqa
