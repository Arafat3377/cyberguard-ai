from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('', include('security_monitoring.urls')),
]
