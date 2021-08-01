"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
# from django.contrib import admin
from django.urls import path
from django.conf.urls import url
# from django.urls.conf import include
from django.views.generic.base import RedirectView
from users import views
from users.views import index, teacher_signup, student_signup, auth_login, auth_logout, studentView

urlpatterns = [
    path('', RedirectView.as_view(url="index/")),
    path('index/', views.index, name='index'),
    path('teacher/signup/', views.teacher_signup, name="teacher_signup"),
    path('student/signup/', views.student_signup, name="student_signup"),
    path('login/', views.auth_login, name="login"),
    path('logout/', views.auth_logout, name="logout"),
    path('student/view', views.studentView, name="student_view"),
    path('account_activation_sent/', views.account_activation_sent,
         name='account_activation_sent'),
    # url(
    #     r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('activate/', views.activate),
    # path('admin/', admin.site.urls),
]
