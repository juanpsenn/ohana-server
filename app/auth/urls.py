from django.urls import path

from app.auth.views import AuthApi
from app.auth.views import CreateMPAccount
from app.auth.views import GetMPAccount
from app.auth.views import SignupApi

urlpatterns = [
    path("signin/", AuthApi.as_view()),
    path("signup/", SignupApi.as_view()),
    path("create-mp-account/", CreateMPAccount.as_view()),
    path("get-mp-account/", GetMPAccount.as_view()),
]
