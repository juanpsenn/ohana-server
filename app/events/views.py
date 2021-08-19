from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from app.events.selectors.events import get_event
from app.events.selectors.events import list_events
from app.events.serializers import EventSerializer
from app.events.services.events import event_create
from app.events.services.events import event_update
from utilities.http import CustomPageNumberPagination
from utilities.serializers import inline_serializer


class EventGetApi(APIView, CustomPageNumberPagination):
    def get(self, request, event_id):
        event = get_event(event_id)
        if event:
            return Response(EventSerializer(event).data, status=200)
        return Response(
            {"detail": f"Event <id:{event_id}> not found."}, status=404
        )


class EventListApi(APIView, CustomPageNumberPagination):
    class FilterSerializer(serializers.Serializer):
        q = serializers.CharField(max_length=128, required=False)

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        events = list_events(filters=filters_serializer.validated_data)

        paginated_events = self.paginate_queryset(events, request, view=self)
        return self.get_paginated_response(
            EventSerializer(paginated_events, many=True).data
        )


class EventCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=128)
        event_type = serializers.IntegerField()
        init_date = serializers.DateField()
        end_date = serializers.DateField()
        description = serializers.CharField(max_length=255)
        contact = inline_serializer(
            fields={
                "name": serializers.CharField(max_length=128),
                "phone": serializers.CharField(max_length=32),
                "email": serializers.EmailField(allow_null=True),
            },
            allow_null=True,
        )
        location = inline_serializer(
            fields={
                "street": serializers.CharField(max_length=128),
                "address_line": serializers.CharField(max_length=128),
                "postal_code": serializers.IntegerField(allow_null=True),
            },
            allow_null=True,
        )
        attention_schedule = inline_serializer(
            fields={
                "day": serializers.IntegerField(),
                "from_time": serializers.TimeField(),
                "to_time": serializers.TimeField(),
            },
            many=True,
            allow_null=True,
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = event_create(**serializer.validated_data)
        return Response(EventSerializer(event).data, status=201)


class EventUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=128)
        event_type = serializers.IntegerField()
        init_date = serializers.DateField()
        end_date = serializers.DateField()
        description = serializers.CharField(max_length=255)
        contact = inline_serializer(
            fields={
                "id": serializers.IntegerField(required=False),
                "name": serializers.CharField(max_length=128),
                "phone": serializers.CharField(max_length=32),
                "email": serializers.EmailField(allow_null=True),
            },
            allow_null=True,
        )
        location = inline_serializer(
            fields={
                "id": serializers.IntegerField(required=False),
                "street": serializers.CharField(max_length=128),
                "address_line": serializers.CharField(max_length=128),
                "postal_code": serializers.IntegerField(allow_null=True),
            },
            allow_null=True,
        )
        attention_schedule = inline_serializer(
            fields={
                "id": serializers.IntegerField(required=False),
                "day": serializers.IntegerField(),
                "from_time": serializers.TimeField(),
                "to_time": serializers.TimeField(),
            },
            many=True,
            allow_null=True,
        )

    def put(self, request, event_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = event_update(**serializer.validated_data, id=event_id)
        return Response(EventSerializer(event).data, status=201)
