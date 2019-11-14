from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from rest_framework.authtoken import views as auth_views

from cats import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cats.urls')),
    path('api-auth-token/', views.signin, name='api-token-auth'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]