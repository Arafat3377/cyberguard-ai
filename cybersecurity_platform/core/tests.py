from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import SecurityEvent


class RoleBasedInterfaceTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin = user_model.objects.create_superuser(
            username='admin-test',
            email='admin@example.com',
            password='test-password',
        )
        self.regular_user = user_model.objects.create_user(
            username='viewer-test',
            password='test-password',
        )
        self.event = SecurityEvent.objects.create(
            event_id='EVT-ROLE-TEST',
            timestamp=timezone.now(),
            source_ip='10.0.0.2',
            destination_ip='192.168.1.10',
            event_type='Suspicious Login',
            description='Test event for role permissions.',
        )

    def test_admin_sees_management_dashboard(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse('dashboard'))

        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response, 'Management shortcuts')

    def test_regular_user_sees_read_only_dashboard(self):
        self.client.force_login(self.regular_user)

        response = self.client.get(reverse('dashboard'))

        self.assertTemplateUsed(response, 'user_dashboard.html')
        self.assertContains(response, 'Read-only overview')
        self.assertNotContains(response, 'Management shortcuts')

    def test_regular_user_cannot_change_event_status(self):
        self.client.force_login(self.regular_user)

        response = self.client.post(
            reverse('update_status', args=[self.event.pk]),
            {'status': 'Resolved'},
        )

        self.assertEqual(response.status_code, 403)
        self.event.refresh_from_db()
        self.assertEqual(self.event.status, 'New')

    def test_regular_user_cannot_access_admin_site(self):
        self.client.force_login(self.regular_user)

        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 302)

    def test_regular_user_event_details_are_read_only(self):
        self.client.force_login(self.regular_user)

        response = self.client.get(
            reverse('event_detail', args=[self.event.pk]),
        )

        self.assertContains(response, 'Read-only view')
        self.assertNotContains(response, 'Update Status')

    def test_admin_can_change_event_status(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('update_status', args=[self.event.pk]),
            {'status': 'Resolved'},
        )

        self.assertRedirects(
            response,
            reverse('event_detail', args=[self.event.pk]),
        )
        self.event.refresh_from_db()
        self.assertEqual(self.event.status, 'Resolved')

    def test_admin_can_access_admin_site(self):
        self.client.force_login(self.admin)

        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 200)


class EmailAuthenticationTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='member@example.com',
            email='member@example.com',
            password='strong-test-password',
        )

    def test_login_page_uses_email_and_offers_registration(self):
        response = self.client.get(reverse('login'))

        self.assertContains(response, 'type="email"')
        self.assertContains(response, reverse('register'))

    def test_user_can_login_with_email(self):
        response = self.client.post(reverse('login'), {
            'email': 'MEMBER@example.com',
            'password': 'strong-test-password',
        })

        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_admin_can_still_login_with_username(self):
        admin = get_user_model().objects.create_superuser(
            username='legacy-admin',
            email='legacy-admin@example.com',
            password='admin-password',
        )
        response = self.client.post(reverse('login'), {
            'email': admin.username,
            'password': 'admin-password',
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(response.wsgi_request.user.is_staff)

    def test_registration_creates_and_logs_in_regular_user(self):
        response = self.client.post(reverse('register'), {
            'email': 'new.member@example.com',
            'password': 'new-strong-password',
            'password_confirm': 'new-strong-password',
        })

        new_user = get_user_model().objects.get(email='new.member@example.com')
        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(new_user.is_staff)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.pk, new_user.pk)

    def test_registration_rejects_duplicate_email_case_insensitively(self):
        response = self.client.post(reverse('register'), {
            'email': 'MEMBER@example.com',
            'password': 'new-strong-password',
            'password_confirm': 'new-strong-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'يوجد حساب مسجل بهذا البريد الإلكتروني')
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_registration_rejects_mismatched_passwords(self):
        response = self.client.post(reverse('register'), {
            'email': 'new.member@example.com',
            'password': 'new-strong-password',
            'password_confirm': 'different-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'كلمتا المرور غير متطابقتين')
        self.assertFalse(
            get_user_model().objects.filter(email='new.member@example.com').exists()
        )
