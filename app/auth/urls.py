from django.urls import path

from app.auth.views import AuthApi

urlpatterns = [
    path("signin/", AuthApi.as_view()),
]
