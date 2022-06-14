from django.urls import path
from .views import signup_function, login_function, logout_function, list_function


urlpatterns = [
    path('signup/', signup_function, name='signup'),
    path('login/', login_function, name='login'),
    path('logout/', logout_function, name='logout'),
    path('list/', list_function, name='list')
]
