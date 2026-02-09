from django.urls import path
from .views import ProfileView, RegisterView, CreateAdminOnce


urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('create-admin/', CreateAdminOnce.as_view(), name='create-admin'),
]