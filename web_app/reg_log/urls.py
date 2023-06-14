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
    path('politics/', views.politics, name='politics'),
    path('katalog/', views.katalog, name='katalog'),
    path('lk/', views.LichnyK, name='lk'),
    path('balance/', views.balance, name='balance'),
    path('profile/', views.profile, name='profile'),
    path('how_to_use/',views.how_to_use,name='how_to_use'),
    path('akcii/',views.akcii,name='akcii')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
