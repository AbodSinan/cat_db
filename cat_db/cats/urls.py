from django.urls import path, include

from rest_framework.routers import DefaultRouter

from cats import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'cats', views.CatViewSet)
router.register(r'homes', views.HomeViewSet)
router.register(r'breeds', views.BreedViewSet)
router.register(r'humans', views.HumanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]