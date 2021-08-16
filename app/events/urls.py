from django.urls import path

from app.events import views

urlpatterns = [
    path("list/", views.EventListApi.as_view()),
    path("create/", views.EventCreateApi.as_view()),
    path("update/<int:event_id>/", views.EventUpdateApi.as_view()),
]
