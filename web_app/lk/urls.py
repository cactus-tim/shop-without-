from django.urls import path
from . import views

urlpatterns = [
    path('lk', views.lk, name='lk'),
    path('logout/', views.out, name='logout'),
    path('camera-work', views.camera_work, name='camera-work'),
    path('katalog/', views.katalog, name='katalog'),
    path('politics/', views.politics, name='politics'),
    path('balance/', views.balance, name='balance')
]
