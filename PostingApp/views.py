from django.urls import reverse_lazy
from .models import MyUser
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Article
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView

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

    return render(request, 'signup.html')

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


# 投稿リスト
@login_required
def list_function(request):
    object_list = Article.objects.all()
    login_user = request.user
    return render(request, 'list.html', {'object_list': object_list, 'login_user': login_user})

# 投稿作成


class ArticleCreate(CreateView):
    template_name = 'create.html'
    model = Article
    fields = ('user_id', 'content', 'article_image')
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        """投稿ユーザーをリクエストユーザーと紐付け"""
        form.instance.user = self.request.user
        return super().form_valid(form)

# 投稿記事の詳細


def articledetail_function(request, pk):
    object = get_object_or_404(Article, pk=pk)
    login_user = request.user
    return render(request, 'detail.html', {'object': object, 'login_user': login_user})

# 投稿記事の削除


class ArticleDelete(DeleteView):
    template_name = 'delete.html'
    model = Article
    success_url = reverse_lazy('list')

# いいね機能


class LikeBase(View):
    # いいねのベースクラス、リダイレクト先を以降で継承先で設定
    def get(self, request, *args, **kwargs):
        # 記事の取得
        pk = self.kwargs['pk']
        related_post = Article.objects.get(pk=pk)

        # いいねテーブル内にすでにユーザーが存在する場合
        if self.request.user in related_post.like.all(): 
           # テーブルからユーザーを削除 
           obj = related_post.like.remove(self.request.user)
         # いいねテーブル内にすでにユーザーが存在しない場合
        else:
           # テーブルにユーザーを追加                           
           obj = related_post.like.add(self.request.user)  
        return obj

class LikeHome(LikeBase):
    # HOMEページでいいねした場合
    def get(self, request, *args, **kwargs):
       #LikeBaseでリターンしたobj情報を継承
       super().get(request, *args, **kwargs)
       #homeにリダイレクト
       return redirect('list')

class LikeDetail(LikeBase):
    # 詳細ページでいいねした場合
    def get(self, request, *args, **kwargs):
       #LikeBaseでリターンしたobj情報を継承
       super().get(request, *args, **kwargs)
       pk = self.kwargs['pk'] 
       #detailにリダイレクト
       return redirect('detail', pk)