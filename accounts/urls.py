from django.urls import path
from . import views
from .views import register, login_user, logout_user, profile

urlpatterns = [

    path(
        'register/',
        register,
        name='register'
    ),

    path(
        'login/',
        login_user,
        name='login'
    ),

    path(
        'logout/',
        logout_user,
        name='logout'
    ),

  path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        'profile/',
        profile,
        name='profile'
    ),

]