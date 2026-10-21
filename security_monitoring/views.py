from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.db.models import Count
from core.models import Device, SecurityEvent, Alert
from .services import answer_question

@login_required
def devices(request): return render(request, 'devices.html', {'devices': Device.objects.all().order_by('name')})

@login_required
def events(request):
    qs = SecurityEvent.objects.select_related('device').order_by('-timestamp')
    severity = request.GET.get('severity')
    status = request.GET.get('status')
    q = request.GET.get('q')
    if severity: qs = qs.filter(severity=severity)
    if status: qs = qs.filter(status=status)
    if q: qs = qs.filter(description__icontains=q) | qs.filter(event_type__icontains=q) | qs.filter(event_id__icontains=q)
    return render(request, 'events.html', {
        'events': qs,
        'severity': severity,
        'severities': SecurityEvent.SEVERITIES,
        'status': status,
        'q': q or '',
    })

@login_required
def event_detail(request, pk): return render(request, 'event_detail.html', {'event': get_object_or_404(SecurityEvent, pk=pk)})

@login_required
@require_POST
def update_status(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    event = get_object_or_404(SecurityEvent, pk=pk)
    new_status = request.POST.get('status')
    if new_status in dict(SecurityEvent.STATUSES): event.status = new_status; event.save(update_fields=['status'])
    return redirect('event_detail', pk=pk)

@login_required
def alerts(request): return render(request, 'alerts.html', {'alerts': Alert.objects.select_related('event').order_by('-created_at')[:100]})

@login_required
def reports(request):
    events = SecurityEvent.objects.all()
    stats = {'total': events.count(), 'critical': events.filter(severity='Critical').count(), 'high': events.filter(severity='High').count(), 'medium': events.filter(severity='Medium').count(), 'low': events.filter(severity='Low').count(), 'anomalous': events.exclude(event_type='Normal Activity').count()}
    by_type = events.values('event_type').annotate(total=Count('id')).order_by('-total')
    return render(request, 'reports.html', {'stats': stats, 'by_type': by_type})

@login_required
def assistant(request):
    answer = None
    if request.method == 'POST': answer = answer_question(request.POST.get('question',''))
    return render(request, 'assistant.html', {'answer': answer})

@login_required
def dashboard_api(request):
    events = SecurityEvent.objects.all()
    return JsonResponse({'total': events.count(), 'critical': events.filter(severity='Critical').count(), 'high': events.filter(severity='High').count(), 'medium': events.filter(severity='Medium').count(), 'low': events.filter(severity='Low').count()})
