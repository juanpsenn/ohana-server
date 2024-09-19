from django.urls import path

from app.events import views

urlpatterns = [
    path("get/<int:event_id>/", views.EventGetApi.as_view()),
    path("list/", views.EventListApi.as_view()),
    path("list/self/", views.MyEventsListApi.as_view()),
    path("create/", views.EventCreateApi.as_view()),
    path("update/<int:event_id>/", views.EventUpdateApi.as_view()),
    path("delete/<int:event_id>/", views.EventDeleteApi.as_view()),
    path("categories/list/", views.CategoryListApi.as_view()),
    path("item/done/", views.EventItemDoneApi.as_view()),
    path("like/<int:event_id>/", views.LikeEventApi.as_view()),
    path("share/<int:event_id>/", views.ShareEventApi.as_view()),
]
