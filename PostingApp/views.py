from .models import MyUser
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
import re


# Create your views here.

# 登録
def signup(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        password = request.POST['password']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        # profile_image = request.POST['profile_image']
        email = request.POST['email']

        # バリデーション
        user_idRegex='^[a-zA-Z0-9_-]{4,10}$'

        try:
            if(not re.match(user_idRegex, user_id)):
                return render(request, 'signup.html', {'error' : 'ユーザーIDは英数字かアンダーバーのみです。'})
            else:
                user = MyUser.objects.create_user(user_id, password, firstName, lastName, email)
        except IntegrityError:
            return render(request, 'signup.html', {'error' : 'このユーザーは既に登録されています。'})
        except KeyError:
            pass
    
    return render(request, 'signup.html', {})
