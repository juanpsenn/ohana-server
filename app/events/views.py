from rest_framework.response import Response
from rest_framework.views import APIView

from app.events.selectors.events import list_events
from app.events.serializers import EventSerializer
from utilities.http import CustomPageNumberPagination


class EventListApi(APIView, CustomPageNumberPagination):
    def get(self, request):
        events = list_events()
        paginated_events = self.paginate_queryset(
            events, request, view=self
        )
        return self.get_paginated_response(
            EventSerializer(paginated_events, many=True).data
        )