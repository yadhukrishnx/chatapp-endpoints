from django.urls import path
from .views import register_user, user_login,user_chat,token_balance

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('chat/', user_chat, name='chat'),
    path('tokenbalance/',token_balance,name='token_balance'),
]