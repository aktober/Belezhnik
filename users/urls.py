from django.conf.urls import url
from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path(r'login/', views.user_login, name='login'),
    path(r'register/', views.user_register, name='register'),
    path(r'logout/', views.logout_view, name='logout'),
    path(r'activate/(?P<userid>[-\w]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='activate'),
    path(r'profile/', views.profile_view, name='profile'),
]