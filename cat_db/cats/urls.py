from django.urls import path, include

from cats import views

urlpatterns = [
    path('', views.api_root),
    path('users/', views.UserList.as_view(), name = 'user-list'),
	path('users/<int:pk>/', views.UserDetail.as_view(), name = 'user-detail'),
	#path('register/', views.UserRegistration.as_view(), name = 'user-register'),
    path('cats/', views.CatList.as_view(), name = 'cat-list'),
    path('cats/<int:pk>/', views.CatDetail.as_view(), name = 'cats-detail'),
    path('homes/', views.HomeList.as_view(), name = 'home-list'),
    path('home/<int:pk>/', views.HomeDetail.as_view(), name = 'home-detail'),
    path('humans/', views.HumanList.as_view(), name = 'human-list'),
    path('human/<int:pk>/', views.HumanDetail.as_view(), name = 'human-detail'),
    path('breeds/', views.BreedList.as_view(), name = 'breed-list'),
    path('breeds/<int:pk>/', views.BreedDetail.as_view(), name = 'breed-detail'),
]