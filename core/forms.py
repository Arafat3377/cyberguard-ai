from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError


class EmailLoginForm(forms.Form):
    email = forms.CharField(
        label='البريد الإلكتروني',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'autocomplete': 'email',
            'placeholder': 'name@example.com',
            'dir': 'ltr',
        }),
    )
    password = forms.CharField(
        label='كلمة المرور',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'current-password',
            'placeholder': 'أدخل كلمة المرور',
        }),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('email', '').strip()
        password = cleaned_data.get('password')
        if not identifier or not password:
            return cleaned_data

        user_model = get_user_model()
        user = None
        if '@' in identifier:
            matches = user_model.objects.filter(email__iexact=identifier)
            if matches.count() == 1:
                user = authenticate(
                    self.request,
                    username=matches.first().get_username(),
                    password=password,
                )

        if user is None:
            user = authenticate(
                self.request,
                username=identifier,
                password=password,
            )

        if user is None:
            raise ValidationError('البريد الإلكتروني أو كلمة المرور غير صحيحة.')

        self.user = user
        return cleaned_data


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label='البريد الإلكتروني',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'autocomplete': 'email',
            'placeholder': 'name@example.com',
            'dir': 'ltr',
        }),
    )
    password = forms.CharField(
        label='كلمة المرور',
        min_length=8,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
            'placeholder': '8 أحرف على الأقل',
        }),
    )
    password_confirm = forms.CharField(
        label='تأكيد كلمة المرور',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
            'placeholder': 'أعد إدخال كلمة المرور',
        }),
    )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=email).exists():
            raise ValidationError('يوجد حساب مسجل بهذا البريد الإلكتروني.')
        return email

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data['password_confirm']
        if password and password != password_confirm:
            raise ValidationError('كلمتا المرور غير متطابقتين.')
        return password_confirm

    def create_user(self):
        email = self.cleaned_data['email']
        username_base = email[:130]
        username = username_base
        suffix = 1
        user_model = get_user_model()
        while user_model.objects.filter(username=username).exists():
            username = f'{username_base[:140]}-{suffix}'
            suffix += 1

        return user_model.objects.create_user(
            username=username,
            email=email,
            password=self.cleaned_data['password'],
        )
