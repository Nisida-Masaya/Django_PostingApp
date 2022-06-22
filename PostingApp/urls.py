from django.urls import path
from .views import ArticleCreate, signup_function, login_function, logout_function, list_function, articledetail_function, ArticleDelete, LikeHome, LikeDetail, likelist_function


urlpatterns = [
    path('signup/', signup_function, name='signup'),
    path('login/', login_function, name='login'),
    path('logout/', logout_function, name='logout'),
    path('list/', list_function, name='list'),
    path('create/', ArticleCreate.as_view(), name='create'),
    path('detail/<int:pk>', articledetail_function, name='detail'),
    path('delete/<int:pk>', ArticleDelete.as_view(), name='delete'),
    path('like_home/<int:pk>', LikeHome.as_view(), name='like_home'),
    path('like_detail/<int:pk>', LikeDetail.as_view(), name='like_detail'),
    path('likelist/', likelist_function, name='likelist')
]
