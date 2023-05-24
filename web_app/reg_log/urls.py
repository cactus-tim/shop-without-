from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.reg_log, name='home'),
    path('reg/', views.reg, name='reg'),
    path('log/', views.log, name='log'),
    path('logout/', views.out, name='logout'),
    path('reg_log/', views.reg_log, name='reg_log'),
    path('about_us/', views.footer, name='footer'),
    path('politics/', views.politics, name='politics')
]
