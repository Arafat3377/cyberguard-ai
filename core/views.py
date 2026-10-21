from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import EmailLoginForm, RegistrationForm
from .models import Device, SecurityEvent, Alert


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = EmailLoginForm(request=request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.user)
        next_url = request.POST.get('next', '')
        if url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)
        return redirect('dashboard')

    return render(request, 'login.html', {
        'form': form,
        'next': request.POST.get('next', request.GET.get('next', '')),
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.create_user()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('dashboard')

    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    events = SecurityEvent.objects.select_related('device').order_by('-timestamp')
    context = {
        'total_events': events.count(),
        'critical': events.filter(severity='Critical').count(),
        'high': events.filter(severity='High').count(),
        'medium': events.filter(severity='Medium').count(),
        'low': events.filter(severity='Low').count(),
        'devices': Device.objects.count(),
        'online_devices': Device.objects.filter(status='online').count(),
        'unread_alerts': Alert.objects.filter(is_read=False).count(),
        'recent_events': events[:8],
        'by_type': list(events.values('event_type').annotate(total=Count('id')).order_by('-total')[:8]),
    }
    template = 'dashboard.html' if request.user.is_staff else 'user_dashboard.html'
    return render(request, template, context)
