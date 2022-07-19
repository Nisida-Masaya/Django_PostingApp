from django.urls import reverse_lazy
from .models import MyUser
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Article, Follow, MyUser
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.contrib import messages
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

        # if request.FILES['profile_image'] == 'null':
        # image_path = 'no_image.jpg'
        profile_image = request.FILES['no_image.jpg']

        # profile_image = request.FILES['profile_image']
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

# プロフィール詳細


@login_required
def account_function(request, user_id):
    pro_info = {
        'User': MyUser.objects.get(user_id=user_id)
    }
    return render(request, 'account.html', pro_info)

# プロフィール編集


def accountUpdate_function(request):
    if request.method == 'GET':
        login_user = request.user
        return render(request, 'accountupdate.html', {'login_user': login_user})
    else:
        user = request.user
        user.firstName = request.POST['firstName']
        user.lastName = request.POST['lastName']
        user.email = request.POST['email']
        user.profile_image = request.FILES['profile_image']
        user.introduction = request.POST['introduction']
        user.save()
        return redirect('list')


# 投稿リスト

@method_decorator(login_required, name='dispatch')
class AllList(ListView):
    # フォローしたユーザの投稿リスト表示
    model = Article
    template_name = 'list.html'

    def get_context_data(self, *arg, **kwargs):
        # コネクションに関するオブジェクト情報をコンテクストに追加
        context = super().get_context_data(*arg, **kwargs)
        context['connection'] = Follow.objects.get_or_create(
            user_id=self.request.user)
        print(context['connection'])
        return context


# 投稿作成
@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class ArticleDetail(DetailView):
    # フォローしたユーザの投稿リスト表示
    model = Article
    template_name = 'detail.html'

    def get_context_data(self, *arg, **kwargs):
        # コネクションに関するオブジェクト情報をコンテクストに追加
        context = super().get_context_data(*arg, **kwargs)
        context['connection'] = Follow.objects.get_or_create(
            user_id=self.request.user)
        print(context['connection'])
        return context
# 投稿記事の削除


@method_decorator(login_required, name='dispatch')
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
        # LikeBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        # homeにリダイレクト
        return redirect('list')


class LikeDetail(LikeBase):
    # 詳細ページでいいねした場合
    def get(self, request, *args, **kwargs):
        # LikeBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']
        # detailにリダイレクト
        return redirect('detail', pk)

# いいねリスト


@login_required
def likelist_function(request):
    object_list = Article.objects.all()
    login_user = request.user
    return render(request, 'likelist.html', {'object_list': object_list, 'login_user': login_user})

# フォロー機能


class FollowBase(View):
    # フォローのベースクラス、リダイレクト先を以降で継承先で設定
    def get(self, request, *args, **kwargs):
        # ユーザーの取得
        pk = self.kwargs['pk']
        target_user = Article.objects.get(pk=pk).user_id

        # ユーザー情報よりコネクション情報を取得、存在しなければ作成
        my_follow = Follow.objects.get_or_create(user_id=self.request.user)

        if str(my_follow[0]) == str(target_user):
            messages.warning(request, '自分はフォローできません。')
        else:

            # フォローテーブル内にすでにユーザーが存在する場合
            if target_user in my_follow[0].following.all():
                # テーブルからユーザーを削除
                obj = my_follow[0].following.remove(target_user)
            # フォローテーブル内にすでにユーザーが存在しない場合
            else:
                # テーブルにユーザーを追加
                obj = my_follow[0].following.add(target_user)
            return obj


class FollowHome(FollowBase):
    # homeでフォローした時
    def get(self, request, *arg, **kwargs):
        super().get(request, *arg, **kwargs)
        return redirect('list')


class FollowDetail(FollowBase):
    # detailでフォローした時
    def get(self, request, *arg, **kwargs):
        super().get(request, *arg, **kwargs)
        pk = self.kwargs['pk']
        return redirect('detail', pk)


# @@method_decorator(login_required, name='dispatch')

class FollowList(ListView):
    # フォローしたユーザの投稿リスト表示
    model = Article
    template_name = 'list.html'

    def get_queryset(self):
        # フォローリスト内にユーザーが含まれている場合のみクエリセット返す
        my_follow = Follow.objects.get_or_create(user_id=self.request.user)
        all_follow = my_follow[0].following.all()
        return Article.objects.filter(user_id__in=all_follow)

    def get_context_data(self, *arg, **kwargs):
        # コネクションに関するオブジェクト情報をコンテクストに追加
        context = super().get_context_data(*arg, **kwargs)
        context['connection'] = Follow.objects.get_or_create(
            user_id=self.request.user)
        print(context['connection'])
        return context
