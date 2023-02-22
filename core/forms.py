from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2', 'image']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password Confirmation'

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mb-3', })
            field.label = ''
            field.help_text = None
            field.required = True

    def clean(self):
        super(CustomUserCreationForm, self).clean()
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if len(name) < 4:
            self._errors['name'] = self.error_class([
                'Minimum 4 characters required'])

        if len(name) > 50:
            self._errors['name'] = self.error_class([
                'You can use maximum of 50 characters'])

        emails = User.objects.values_list('email', flat=True)
        if email in emails:
            self._errors['email'] = self.error_class([
                'Email Already Exist'])

        try:
            validate_email(email)
        except ValidationError as e:
            self._errors['email'] = self.error_class([
                'Invalid Email'])

        if password1 != password2:
            self._errors['password2'] = self.error_class([
                'Passwords Does not match'])

        return self.cleaned_data


