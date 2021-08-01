
from users.decorators import student_required, teacher_required
from users.forms import TeacherSignUpForm, StudentSignUpForm
from django.shortcuts import render, redirect
# from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.http import HttpResponse


from users.models import User
# Create your views here.


# send email with django
from django.core.mail import send_mail
from core.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.tokens import account_activation_token

# ............................

# send otp...............

from twilio.rest import Client
import os
import random
from users.send_otp import send_otp


from dotenv import load_dotenv
load_dotenv()


def index(request):
    return render(request, 'landing.html')


def teacher_signup(request):
    if request.method == "POST":
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            email = form['email'].value()
            # form.clean_email(email)
            user.save()
            # email = user.get("email")
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            context = {
                "email": email,
                'user': email,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            }
            html_message = render_to_string(
                'mail_message.html', context)
            send_mail("Thank you for using role based authentication system", "Please activate your account by clicking in link below",
                      EMAIL_HOST_USER, [email], html_message=html_message, fail_silently=False)
            # prescription = "prescription has been sent successfully to "+" "+email
            # return render(request, 'doctor/prescription_form.html', {'recepient': prescription})
            return redirect("account_activation_sent")
        else:
            context = {
                'form': form
            }
            return render(request, 'registration/signup_teacher.html', context)

    form = TeacherSignUpForm()
    context = {
        'form': form,
        'user_type': 'teacher'
    }
    return render(request, 'registration/signup_teacher.html', context)


def auth_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Please enter valid credentials")
            # messages.info(request, "Invalid username or password")
            return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/login.html')


def auth_logout(request):
    logout(request)
    return redirect("index")


def student_signup(request):
    if request.method == "POST":
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            email = form['email'].value()
            # form.clean_email(email)
            user.save()
            # email = user.get("email")
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            context = {
                "email": email,
                'user': email,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            }
            html_message = render_to_string(
                'mail_message.html', context)
            send_mail("Thank you for using role based authentication system", "Please activate your account by clicking in link below",
                      EMAIL_HOST_USER, [email], html_message=html_message, fail_silently=False)
            # prescription = "prescription has been sent successfully to "+" "+email
            # return render(request, 'doctor/prescription_form.html', {'recepient': prescription})
            return redirect("account_activation_sent")
        else:
            context = {
                'form': form
            }
            return render(request, 'registration/signup_student.html', context)
    form = StudentSignUpForm()
    context = {
        'form': form,
        'user_type': 'student'
    }
    return render(request, 'registration/signup_student.html', context)


@login_required(login_url='login')
@student_required
def studentView(request):
    return HttpResponse("Views only for student")


@login_required(login_url='login')
@teacher_required
def studentView(request):
    return HttpResponse("Views only for teachers")


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request):
    uidb64 = request.GET.get("uid")
    token = request.GET.get("token")
    # print(uidb64, token)
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
        print(user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'account_activation_invalid.html')


# Send otp

def otp_login(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')

        user = User.objects.filter(phone_number=mobile).first()

        if user is None:
            context = {'message': 'User not found', 'class': 'danger'}
            return render(request, 'registration/otp_login.html', context)

        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()
        send_otp(otp, mobile)
        request.session['mobile'] = mobile
        return redirect('enter_otp')
    return render(request, 'registration/otp_login.html')


def enter_otp(request):
    mobile = request.session['mobile']
    context = {'mobile': mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = User.objects.filter(phone_number=mobile).first()

        if otp == user.otp:
            user = User.objects.get(id=user.id)
            login(request, user)
            return redirect('index')
        else:
            context = {'message': 'Wrong OTP',
                       'class': 'danger', 'mobile': mobile}
            return render(request, 'registration/otp.html', context)

    return render(request, 'registration/otp.html', context)


# def send_otp(mobile, otp):
#     print("FUNCTION CALLED")
#     conn = http.client.HTTPSConnection("api.msg91.com")
#     authkey = settings.AUTH_KEY
#     headers = {'content-type': "application/json"}
#     url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message=" + \
#         "Your otp is "+otp + "&mobile="+mobile+"&authkey="+authkey+"&country=91"
#     conn.request("GET", url, headers=headers)
#     res = conn.getresponse()
#     data = res.read()
#     print(data)
#     return None


# def login_attempt(request):
#     if request.method == 'POST':
#         mobile = request.POST.get('mobile')

#         user = Profile.objects.filter(mobile=mobile).first()

#         if user is None:
#             context = {'message': 'User not found', 'class': 'danger'}
#             return render(request, 'login.html', context)

#         otp = str(random.randint(1000, 9999))
#         user.otp = otp
#         user.save()
#         send_otp(mobile, otp)
#         request.session['mobile'] = mobile
#         return redirect('login_otp')
#     return render(request, 'login.html')
