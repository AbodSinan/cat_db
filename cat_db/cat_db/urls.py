from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from rest_framework.authtoken import views as auth_views
from rest_framework_simplejwt import views as jwt_views

from cats import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cats.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'), #a url to retrieve jwt tokens
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),#a url to retrieve existing jwt tokens
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]