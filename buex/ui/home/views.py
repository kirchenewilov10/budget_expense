import datetime
from datetime import timedelta
import threading
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.http import HttpResponse

from buex.database.orm.models import *
from buex.module.buex import common as mcm
from buex.module.buex import email as eml
from buex.module.glb.ret_code import *
from buex.module.buex.constant import *
# Create your views here.

# ***********************************************************************************
# @Function: Check Token
# -----------------------------------------------------------------------------------
def check_token(user_uid, token):
    try:
        class Mocked(PasswordResetTokenGenerator):
            def __init__(self, today):
                self._today_val = today

            def _today(self):
                return self._today_val

        p1 = Mocked(datetime.date.today() + timedelta(1))

        user_obj = tbl_user.objects.get(uid=user_uid)
        ret = p1.check_token(user_obj, token)
        return ret

    except Exception as e:
        return False

@login_required
def index_view(request):
    return redirect('/buex/dashboard')

# ***********************************************************************************
# @Function: Login View
# -----------------------------------------------------------------------------------
def login_view(request, template_name='home/login-page.html'):
    try:
        if request.user.is_authenticated:
            return redirect('/buex/dashboard')

        key_ary = ['username', 'password']
        if mcm.check_keys(key_ary, request.POST) == False:
            return render(request, template_name)
        username = request.POST['username']
        password = request.POST['password']
        ret_code, user_obj = mcm.authenticate_user(username, password)

        if ret_code != AUTH_SUCCESS:
            alert_str = AUTH_ALERT_STRING[ret_code]
            data = {
                'username': username,
                'password': password,
                'alert_str': alert_str
            }
            return render(request, template_name, data)

        django_login(request, user_obj)

        request.session['username'] = username
        request.session.save()

        return redirect('/buex/dashboard')

    except Exception as e:
        return render(request, template_name)


# ***********************************************************************************
# @Function: Logout
# -----------------------------------------------------------------------------------
def logout(request):
    django_logout(request)
    request.session.clear()
    return redirect('/')

# ***********************************************************************************
# @Function: Forgot Password View
# -----------------------------------------------------------------------------------
def forgot_password_view(request, template_name='home/forgot_password.html'):
    if request.user.is_authenticated == True:
        return redirect('/')
    if 'email' not in request.POST:
        return render(request, template_name)

    email = request.POST['email']
    try:
        user_obj = tbl_user.objects.get(email=email)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user_obj)
        user_uid = user_obj.uid

        password_reset_url = SITE_BASE_URL + 'reset_password?uid=' + str(user_uid) + '&token=' + token
        th = threading.Thread(target=send_pwd_reset_email_thread, args=(user_obj.email, user_obj.first_name, password_reset_url))
        th.start()

    except Exception as e:
        pass

    data = {
        'email': email,
        'alert_str': 'Password reset link is sent.'
    }
    return render(request, template_name, data)


# ***********************************************************************************
# @Function: Reset Password View
# -----------------------------------------------------------------------------------
def reset_password_view(request, template_name='home/reset_password.html'):
    try:
        user_uid = request.GET['uid']
        token = request.GET['token']
        res = check_token(user_uid, token)
        if res == False:
            raise Exception()

        if 'password' not in request.POST:
            return render(request, template_name)

        password = request.POST['password']
        user_obj = tbl_user.objects.get(uid=user_uid)
        user_obj.set_password(password)
        user_obj.s_password = password
        user_obj.save()
        request.session['email'] = user_obj.email
        request.session['language'] = user_obj.language
        django_login(request, user_obj)

        return redirect('/')

    except Exception as e:
        return redirect('/')

# ***********************************************************************************
# @Function: Send Password Reset Email Thread
# -----------------------------------------------------------------------------------
def send_pwd_reset_email_thread(user_email, user_name, pwd_reset_url):
    eml.send_password_reset_url_email_en(user_email, user_name, pwd_reset_url)
