from django.urls import path

from app.users.views import UserInfoUpdateApi

urlpatterns = [path("info/update/<int:id>/", UserInfoUpdateApi.as_view())]
