from rest_framework import serializers
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.events.exceptions import UnauthorizedUpdate
from app.events.selectors.categories import list_categories
from app.events.selectors.events import get_event
from app.events.selectors.events import list_events
from app.events.serializers import CategorySerializer, ItemSerializerComplete
from app.events.serializers import EventSerializer
from app.events.services.event_items import event_item_update
from app.events.services.events import event_create
from app.events.services.events import event_delete
from app.events.services.events import event_update
from app.events.services.likes import like_event
from utilities.http import CustomPageNumberPagination
from utilities.serializers import inline_serializer


class EventGetApi(APIView, CustomPageNumberPagination):
    def get(self, request, event_id):
        event = get_event(event_id)
        if event:
            return Response(EventSerializer(event).data, status=200)
        return Response({"detail": f"Event <id:{event_id}> not found."}, status=404)


class CategoryListApi(APIView):
    def get(self, request):
        categories = list_categories()
        if categories:
            return Response(CategorySerializer(categories, many=True).data, status=200)
        return Response({"detail": "No categories found."}, status=204)


class EventListApi(APIView, CustomPageNumberPagination):
    class FilterSerializer(serializers.Serializer):
        q = serializers.CharField(max_length=128, required=False)
        cancelled = serializers.BooleanField(required=False)

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        events = list_events(filters=filters_serializer.validated_data)

        paginated_events = self.paginate_queryset(events, request, view=self)
        return self.get_paginated_response(
            EventSerializer(
                paginated_events, context={"user": request.user.id}, many=True
            ).data
        )


class MyEventsListApi(APIView, CustomPageNumberPagination):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    class FilterSerializer(serializers.Serializer):
        q = serializers.CharField(max_length=128, required=False)
        cancelled = serializers.BooleanField(required=False)

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        filters = filters_serializer.validated_data
        filters.update({"owner_id": request.user.id})

        events = list_events(filters=filters)

        paginated_events = self.paginate_queryset(events, request, view=self)
        return self.get_paginated_response(
            EventSerializer(paginated_events, many=True).data
        )


class EventCreateApi(APIView):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=128)
        event_type = serializers.IntegerField()
        init_date = serializers.DateField()
        end_date = serializers.DateField()
        description = serializers.CharField(max_length=255)
        goal = serializers.DecimalField(decimal_places=2, max_digits=15)
        image = serializers.URLField(required=False)
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
        category = serializers.IntegerField(allow_null=True)
        attention_schedule = inline_serializer(
            fields={
                "day": serializers.IntegerField(),
                "from_time": serializers.TimeField(),
                "to_time": serializers.TimeField(),
            },
            many=True,
            allow_null=True,
        )
        items = serializers.ListField(allow_null=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = event_create(**serializer.validated_data, user=request.user.id)
        return Response(EventSerializer(event).data, status=201)


class EventUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=128)
        event_type = serializers.IntegerField()
        init_date = serializers.DateField()
        end_date = serializers.DateField()
        description = serializers.CharField(max_length=255)
        image = serializers.URLField(required=False)
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
        category = serializers.IntegerField(allow_null=True)
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
        items = serializers.ListField(allow_null=True)

    def put(self, request, event_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            event = event_update(
                **serializer.validated_data,
                id=event_id,
                user_request=request.user.id,
            )
        except UnauthorizedUpdate:
            return Response(
                {"error": "No autorizado"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(EventSerializer(event).data, status=201)


class EventDeleteApi(APIView):
    def put(self, request, event_id):
        try:
            event = event_delete(
                event_id=event_id,
                user_request=request.user.id,
            )
        except UnauthorizedUpdate:
            return Response(
                {"error": "No autorizado"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(EventSerializer(event).data, status=201)


class EventItemDoneApi(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        done = serializers.BooleanField()

    def put(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = event_item_update(**serializer.validated_data)
        return Response(ItemSerializerComplete(item).data, status=201)


class LikeEventApi(APIView):
    def put(self, request, event_id):
        like = like_event(event_id, request.user.id)
        return Response(
            EventSerializer(like.event, context={"user": request.user.id}).data,
            status=201,
        )
