from django.urls import path

from app.auth.views import AuthApi
from app.auth.views import SignupApi

urlpatterns = [
    path("signin/", AuthApi.as_view()),
    path("signup/", SignupApi.as_view()),
]
