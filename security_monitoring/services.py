from django.db.models import Count
from core.models import SecurityEvent, Device

def answer_question(question):
    q = question.strip().lower()
    events = SecurityEvent.objects.all()
    if not q: return 'Please enter a security question.'
    if any(k in q for k in ['latest','recent','آخر','اخر']):
        rows = events.order_by('-timestamp')[:5]
        return 'Recent incidents:\n' + '\n'.join(f'- {e.event_id}: {e.event_type} ({e.severity})' for e in rows) if rows else 'No incidents are available.'
    if 'critical' in q or 'حرج' in q:
        return f"There are {events.filter(severity='Critical').count()} Critical incidents."
    if 'high' in q or 'عالي' in q:
        return f"There are {events.filter(severity='High').count()} High severity incidents."
    if 'device' in q or 'جهاز' in q:
        return f"The platform currently has {Device.objects.count()} devices, {Device.objects.filter(status='online').count()} online."
    if 'how many' in q or 'count' in q or 'عدد' in q:
        return f"The platform contains {events.count()} security events."
    if 'brute' in q:
        n = events.filter(event_type='Brute Force').count(); return f"Brute Force incidents: {n}."
    if 'recommend' in q or 'توصي' in q:
        return 'Recommendations are generated per incident. Open an incident to review its suggested defensive action.'
    return 'I can answer questions about incident counts, severity levels, recent incidents, devices, threat types, and recommendations using the data stored in the platform.'
