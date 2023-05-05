from django.urls import path
from . import views

urlpatterns = [
    path('', views.reg_log, name='home'),
    path('registration/', views.reg, name='reg'),
    path('login/', views.log, name='log')
]
