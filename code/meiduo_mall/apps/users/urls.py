from django.urls import path
from apps.users.views import UsernameCountView, MobileCountView, RegisterView, LoginView, LogoutView
from apps.users.views import CenterView, EmailView, EmailVerifyView, AddressCreateView, AddressView

urlpatterns = [
    # 判断用户名是否重复
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    # 判断手机号是否重复
    path('mobiles/<mobile:mobile>/count/', MobileCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/', CenterView.as_view()),
    path('emails/', EmailView.as_view()),
    path('emails/verification/', EmailVerifyView.as_view()),
    path('addresses/create/', AddressCreateView.as_view()),
    path('addresses/', AddressView.as_view()),
]
