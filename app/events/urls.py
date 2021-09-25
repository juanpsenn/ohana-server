from django.urls import path

from app.events import views

urlpatterns = [
    path("get/<int:event_id>/", views.EventGetApi.as_view()),
    path("list/", views.EventListApi.as_view()),
    path("list/self/", views.MyEventsListApi.as_view()),
    path("create/", views.EventCreateApi.as_view()),
    path("update/<int:event_id>/", views.EventUpdateApi.as_view()),
    path("categories/list/", views.CategoryListApi.as_view()),
]
