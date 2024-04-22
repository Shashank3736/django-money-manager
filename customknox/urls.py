from knox import views as knox_views
from .views import LogoutAllView
from django.urls import path

urlpatterns = [
    path(r'login/', knox_views.LoginView.as_view(), name='knox_login'),
    path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', LogoutAllView.as_view(), name='knox_logoutall'),
]
