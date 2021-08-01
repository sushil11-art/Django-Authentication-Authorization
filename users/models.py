from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    phone_number = PhoneNumberField(blank=True)
    otp = models.CharField(max_length=6)


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username
