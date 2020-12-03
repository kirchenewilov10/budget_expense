from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('login', views.login_view, name='login_view'),
    path('logout', views.logout, name='logout'),
    path('forgot_password', views.forgot_password_view, name='forgot_password_view'),
    path('reset_password', views.reset_password_view, name='reset_password_view'),
]