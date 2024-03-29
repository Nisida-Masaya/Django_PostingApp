from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, user_id, firstName=None, lastName=None, email=None, password=None, profile_image=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not user_id:
            raise ValueError('Users must have an userId')

        user = self.model(
            user_id=user_id,
            firstName=firstName,
            lastName=lastName,
            password=password,
            email=email,
            profile_image=profile_image
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            user_id=user_id,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(verbose_name='ユーザID', primary_key=True, max_length=20)
    firstName = models.CharField(verbose_name='名', max_length=15, blank=True, null=True)
    lastName = models.CharField(verbose_name='姓', max_length=15, blank=True, null=True)
    profile_image = models.ImageField(verbose_name='プロフィール画像' , upload_to ='', blank=True ,null=True, default=None)
    email = models.EmailField(verbose_name='メールアドレス', max_length=50, unique=True, blank=True, null=True)
    introduction = models.TextField(verbose_name='自己紹介', max_length=300, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'user_id'

    def __str__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

# 投稿記事モデル
class Article(models.Model):
    # MyUserモデルから参照しているon_delete=models.CASCADEは削除時の挙動
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField()
    article_image = models.ImageField(upload_to ='', null=True, blank=True)
    # related_nameは逆参照する時に指定する
    like = models.ManyToManyField(MyUser, related_name='related_post', blank=True)
    create_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
       return self.content

    # 降順
    class Meta:
        ordering = ['-create_at']

# フォローモデル
class Follow(models.Model):
    user_id = models.OneToOneField(MyUser, verbose_name='ユーザID' ,on_delete=models.CASCADE)
    following = models.ManyToManyField(MyUser, verbose_name='フォロー' ,related_name='following', blank=True)

    def __str__(self):
        return str(self.user_id)