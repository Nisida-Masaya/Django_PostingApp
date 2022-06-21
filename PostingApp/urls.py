from django.urls import path
from .views import ArticleCreate, signup_function, login_function, logout_function, list_function, articledetail_function, ArticleDelete


urlpatterns = [
    path('signup/', signup_function, name='signup'),
    path('login/', login_function, name='login'),
    path('logout/', logout_function, name='logout'),
    path('list/', list_function, name='list'),
    path('create/', ArticleCreate.as_view(), name='create'),
    path('detail/<int:pk>', articledetail_function, name='detail'),
    path('delete/<int:pk>', ArticleDelete.as_view(), name='delete')
]
