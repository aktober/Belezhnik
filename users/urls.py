from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path(r'login/', views.LoginPage.as_view(), name='login'),
    path(r'logout/', views.LogoutPage.as_view(), name='logout'),
    path(r'profile/', views.ProfilePage.as_view(), name='profile'),
    path(r'register/', views.RegisterPage.as_view(), name='register'),
    path(r'activate/<int:pk>/<token>/', views.activate, name='activate'),
    # todo: add reset password
]