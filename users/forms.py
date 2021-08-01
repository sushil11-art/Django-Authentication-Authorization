from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class TeacherSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

        fields = ('username', 'email', 'password1', 'password2', )

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
