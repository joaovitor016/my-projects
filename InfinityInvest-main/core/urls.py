from django.urls import path
from core import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path(r'logout/', views.logout_session, name="logout"),
    path('login/', views.login_session, name="login"),
    path('change_password/', views.change_password, name="change_password"),
    path('customers_list/', views.customers_list, name="customers_list"),
    path('token/', views.token, name="token"),
    path('register/', views.register, name="register"),
]
