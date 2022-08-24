from django.urls import path

from .views import AllList, ArticleCreate, ArticleDetail, signup_function, login_function, logout_function, ArticleDetail, account_function,ArticleDelete, LikeHome, LikeDetail, likelist_function, FollowHome, FollowDetail, FollowList, accountUpdate_function


urlpatterns = [
    path('signup/', signup_function, name='signup'),
    path('login/', login_function, name='login'),
    path('logout/', logout_function, name='logout'),
    path('list/', AllList.as_view(), name='list'),
    path('create/', ArticleCreate.as_view(), name='create'),
    path('detail/<int:pk>', ArticleDetail.as_view(), name='detail'),
    path('delete/<int:pk>', ArticleDelete.as_view(), name='delete'),
    path('like_home/<int:pk>', LikeHome.as_view(), name='like_home'),
    path('like_detail/<int:pk>', LikeDetail.as_view(), name='like_detail'),
    path('likelist/', likelist_function, name='likelist'),
    path('follow_home/<int:pk>', FollowHome.as_view(), name='follow_home'),
    path('follow_detail/<int:pk>', FollowDetail.as_view(), name='follow_detail'),
    path('followlist/', FollowList.as_view(), name='followlist'),
    path('account/<str:user_id>', account_function, name='account'),
    path('accountupdate/', accountUpdate_function, name='accountupdate')

]
