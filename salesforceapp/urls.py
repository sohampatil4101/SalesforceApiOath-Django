from django.urls import path
from salesforceapp import views
urlpatterns = [
    path('',views.home, name="home" ),
    path('login/', views.login_with_salesforce, name='login_with_salesforce'),
    path('welcome', views.welcome, name='welcome'),
]
