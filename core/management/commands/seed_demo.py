from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
from core.models import Device, SecurityEvent, Alert, Recommendation

class Command(BaseCommand):
    help = 'Create safe simulated cybersecurity data for the academic prototype.'
    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists(): User.objects.create_superuser('admin','admin@example.com','Admin12345!')
        devices=[]
        types=['server','workstation','router','switch','iot']
        for i in range(1,9):
            d,_=Device.objects.update_or_create(ip_address=f'192.168.10.{i}', defaults={'name':f'Device-{i:02d}','mac_address':f'AA:BB:CC:DD:EE:{i:02X}','device_type':types[(i-1)%len(types)],'status':'online' if i%4 else 'offline','risk_level':['Low','Medium','High'][i%3]})
            devices.append(d)
        threat_data=[('Normal Activity','Low'),('Suspicious Login','Medium'),('Port Scanning','High'),('Brute Force','High'),('Abnormal Traffic','High'),('Malware-like Activity','Critical')]
        actions={'Normal Activity':'No action required; continue monitoring.','Suspicious Login':'Review the account and authentication logs.','Port Scanning':'Investigate the source and review network access controls.','Brute Force':'Review authentication attempts and consider account protection measures.','Abnormal Traffic':'Inspect the affected device and monitor traffic patterns.','Malware-like Activity':'Isolate the affected asset according to organizational incident procedures and investigate.'}
        for i in range(1,61):
            typ,sev=random.choice(threat_data)
            ts=timezone.now()-timedelta(hours=random.randint(0,240))
            e,_=SecurityEvent.objects.update_or_create(event_id=f'EVT-{i:04d}', defaults={'timestamp':ts,'source_ip':f'10.0.0.{random.randint(2,250)}','destination_ip':f'192.168.10.{random.randint(1,8)}','device':random.choice(devices),'event_type':typ,'description':f'Simulated {typ.lower()} detected during controlled academic testing.','severity':sev,'status':random.choice(['New','Investigating','Resolved','Closed']),'detection_method':'Anomaly Detection + Classification','anomaly_score':round(random.uniform(.05,.99),3),'explanation':f'Observed feature pattern is consistent with the selected simulated {typ.lower()} scenario.','recommended_action':actions[typ]})
            if sev in ['High','Critical']:
                Alert.objects.get_or_create(event=e, defaults={'message':f'{sev} security event detected: {typ}','severity':sev})
        for typ,sev,action in [('Brute Force','High',actions['Brute Force']),('Port Scanning','High',actions['Port Scanning']),('Malware-like Activity','Critical',actions['Malware-like Activity'])]:
            Recommendation.objects.get_or_create(title=f'Defensive guidance: {typ}', threat_type=typ, severity=sev, defaults={'action':action})
        self.stdout.write(self.style.SUCCESS('Demo data created. Login: admin / Admin12345!'))
