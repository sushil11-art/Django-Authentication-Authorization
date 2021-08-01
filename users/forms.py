from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from users.models import User

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class TeacherSignUpForm(UserCreationForm):
    phone_number = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(
        initial='NP', attrs={'class': 'form-control'}))
    phone_number.error_messages['invalid'] = 'Enter valid phone number!'

    class Meta(UserCreationForm.Meta):
        model = User

        fields = ('username', 'email', 'password1',
                  'password2', 'phone_number',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Please enter valid and unique email address")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(
        initial='NP', attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User

        fields = ('username', 'email', 'password1', 'password2', )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Please enter valid and unique email address")
        return email
