from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('auth','0012_alter_user_first_name_max_length')]
    operations = [
        migrations.CreateModel(name='Device', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=120)), ('ip_address', models.GenericIPAddressField()), ('mac_address', models.CharField(blank=True,max_length=32)),
            ('device_type', models.CharField(choices=[('server','Server'),('workstation','Workstation'),('router','Router'),('switch','Switch'),('iot','IoT Device')],max_length=30)),
            ('status', models.CharField(choices=[('online','Online'),('offline','Offline')],default='online',max_length=20)),
            ('risk_level', models.CharField(choices=[('Low','Low'),('Medium','Medium'),('High','High'),('Critical','Critical')],default='Low',max_length=20)),
            ('last_seen', models.DateTimeField(auto_now=True)),]),
        migrations.CreateModel(name='Recommendation', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=160)),('threat_type',models.CharField(max_length=100)),('action',models.TextField()),('severity',models.CharField(max_length=20)),('active',models.BooleanField(default=True))]),
        migrations.CreateModel(name='SecurityEvent', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('event_id',models.CharField(max_length=40,unique=True)),('timestamp',models.DateTimeField()),('source_ip',models.GenericIPAddressField()),('destination_ip',models.GenericIPAddressField()),
            ('event_type',models.CharField(choices=[('Normal Activity','Normal Activity'),('Suspicious Login','Suspicious Login'),('Port Scanning','Port Scanning'),('Brute Force','Brute Force'),('Abnormal Traffic','Abnormal Traffic'),('Malware-like Activity','Malware-like Activity')],max_length=80)),
            ('description',models.TextField()),('severity',models.CharField(choices=[('Low','Low'),('Medium','Medium'),('High','High'),('Critical','Critical')],default='Low',max_length=20)),('status',models.CharField(choices=[('New','New'),('Investigating','Investigating'),('Resolved','Resolved'),('Closed','Closed')],default='New',max_length=30)),('detection_method',models.CharField(default='ML Pipeline',max_length=80)),('anomaly_score',models.FloatField(default=0.0)),('explanation',models.TextField(blank=True)),('recommended_action',models.TextField(blank=True)),('created_at',models.DateTimeField(auto_now_add=True)),
            ('device',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='events',to='core.device'))]),
        migrations.CreateModel(name='Alert', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('message',models.CharField(max_length=255)),('severity',models.CharField(max_length=20)),('is_read',models.BooleanField(default=False)),('created_at',models.DateTimeField(auto_now_add=True)),('event',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='alerts',to='core.securityevent'))]),
        migrations.CreateModel(name='AuditLog', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('action',models.CharField(max_length=120)),('target',models.CharField(blank=True,max_length=255)),('created_at',models.DateTimeField(auto_now_add=True)),('user',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,to='auth.user'))]),
    ]
