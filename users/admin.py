from __future__ import unicode_literals, absolute_import
from .models import Student, User
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django import forms

# from users.model import User, Student

# Register your models here.
# admin.site.register(User)


admin.site.register(Student)


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

        fields = ('username', 'email', 'password1', 'password2', )

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_email(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        users = User.objects.filter(email__iexact=email).exclude(
            username__iexact=username)
        if users:
            raise forms.ValidationError("Email's already taken.")
        return email.lower()


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = AuthUserAdmin.fieldsets + (
        ('Extended Field', {'fields': ('is_student',
                                       'is_teacher', 'email_confirmed')}),
    )
    list_display = ('username', 'is_student', 'is_teacher',
                    'is_superuser', 'is_active')
    search_fields = ['username']
