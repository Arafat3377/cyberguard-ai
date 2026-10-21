from django.db import models

class Device(models.Model):
    DEVICE_TYPES = [('server','Server'),('workstation','Workstation'),('router','Router'),('switch','Switch'),('iot','IoT Device')]
    name = models.CharField(max_length=120)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=32, blank=True)
    device_type = models.CharField(max_length=30, choices=DEVICE_TYPES)
    status = models.CharField(max_length=20, choices=[('online','Online'),('offline','Offline')], default='online')
    risk_level = models.CharField(max_length=20, choices=[('Low','Low'),('Medium','Medium'),('High','High'),('Critical','Critical')], default='Low')
    last_seen = models.DateTimeField(auto_now=True)
    def __str__(self): return f'{self.name} ({self.ip_address})'

class SecurityEvent(models.Model):
    TYPES = [('Normal Activity','Normal Activity'),('Suspicious Login','Suspicious Login'),('Port Scanning','Port Scanning'),('Brute Force','Brute Force'),('Abnormal Traffic','Abnormal Traffic'),('Malware-like Activity','Malware-like Activity')]
    SEVERITIES = [('Low','Low'),('Medium','Medium'),('High','High'),('Critical','Critical')]
    STATUSES = [('New','New'),('Investigating','Investigating'),('Resolved','Resolved'),('Closed','Closed')]
    event_id = models.CharField(max_length=40, unique=True)
    timestamp = models.DateTimeField()
    source_ip = models.GenericIPAddressField()
    destination_ip = models.GenericIPAddressField()
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    event_type = models.CharField(max_length=80, choices=TYPES)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITIES, default='Low')
    status = models.CharField(max_length=30, choices=STATUSES, default='New')
    detection_method = models.CharField(max_length=80, default='ML Pipeline')
    anomaly_score = models.FloatField(default=0.0)
    explanation = models.TextField(blank=True)
    recommended_action = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.event_id

class Alert(models.Model):
    event = models.ForeignKey(SecurityEvent, on_delete=models.CASCADE, related_name='alerts')
    message = models.CharField(max_length=255)
    severity = models.CharField(max_length=20)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class AuditLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=120)
    target = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Recommendation(models.Model):
    title = models.CharField(max_length=160)
    threat_type = models.CharField(max_length=100)
    action = models.TextField()
    severity = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
