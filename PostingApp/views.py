from imaplib import _Authenticator
import profile
from .models import MyUser
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import re


# Create your views here.

# 登録
def signup_function(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        profile_image = request.FILES['profile_image']

        # バリデーション
        user_idRegex = '^[a-zA-Z0-9_-]{4,10}$'

        try:
            if(not re.match(user_idRegex, user_id)):
                return render(request, 'signup.html', {'error': 'ユーザーIDは英数字かアンダーバーのみです。'})
            else:
                user = MyUser.objects.create_user(
                    user_id, firstName, lastName, email, password, profile_image)
        except IntegrityError:
            return render(request, 'signup.html', {'error': 'このユーザーは既に登録されています。'})
        except KeyError:
            pass

    return redirect('login')

# ログイン


def login_function(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        password = request.POST['password']
        user = authenticate(request, user_id=user_id, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page. 成功した時のリダイレクト先
            return redirect('list')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'message': 'ユーザーIDかパスワードが間違えています。'})

    return render(request, 'login.html', {})

# ログアウト


def logout_function(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login')


@login_required
def list_function(request):
    return render(request, 'list.html', {'message': '成功'})
