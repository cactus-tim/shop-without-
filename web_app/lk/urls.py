from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('lk', views.lk, name='lk'),
    path('logout/', views.out, name='logout'),
    path('camera-work', views.camera_work, name='camera-work'),
    path('katalog/', views.katalog, name='katalog'),
    path('politics/', views.politics, name='politics'),
    path('balance/', views.balance, name='balance'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('update_product_count/', views.update_product_count, name='update_product_count'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
