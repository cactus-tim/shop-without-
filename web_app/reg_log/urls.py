from django.urls import path
from . import views

urlpatterns = [
    path('', views.reg_log, name='home'),
    path('reg/', views.reg, name='reg'),
    path('log/', views.log, name='log'),
    path('reg_log/',views.reg_log,name='reg_log')
]
