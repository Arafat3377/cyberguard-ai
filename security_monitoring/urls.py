from django.urls import path
from . import views
urlpatterns = [
    path('devices/', views.devices, name='devices'),
    path('events/', views.events, name='events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/status/', views.update_status, name='update_status'),
    path('alerts/', views.alerts, name='alerts'),
    path('reports/', views.reports, name='reports'),
    path('assistant/', views.assistant, name='assistant'),
    path('api/dashboard/', views.dashboard_api, name='dashboard_api'),
]
