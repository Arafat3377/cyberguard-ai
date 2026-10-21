from django.contrib import admin
from .models import Device, SecurityEvent, Alert, AuditLog, Recommendation
admin.site.register([Device, SecurityEvent, Alert, AuditLog, Recommendation])
