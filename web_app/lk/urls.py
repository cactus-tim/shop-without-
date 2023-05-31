from django.urls import path
from . import views

urlpatterns = [
    path('lk', views.lk, name='lk'),
    path('logout/', views.out, name='logout'),
    # path('run-script', views.run_script, name='run-script'),
    path('camera-work', views.camera_work, name='camera-work')
]
