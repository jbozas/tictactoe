from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from game.serializers import (
    GameListSerializer,
    CreateGameSerializer,
    SubmitPlaySerializer,
    GameOutputSerializer,
)
from game.models import Game
from game.services import GameService
from game.errors import GameCreationError, SubmitPlayError


class CreateGameAPIView(APIView):
    def post(self, request):
        """
        The above function is a request handler that creates a game using the CreateGameSerializer and
        returns the created game if successful, or an error message if the request parameters are invalid.
        """
        serializer = CreateGameSerializer(data=request.data)

        if serializer.is_valid():
            try:
                data = serializer.validated_data
                game = GameService.create_game(
                    data.pop("players"),
                    data.get("starting_player"),
                )
                output_serializer = GameOutputSerializer(game)
                return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            except GameCreationError as e:
                raise (f"Failed creating the Game with error {e}")
        return Response(
            {"error": f"Bad requests params: {serializer.errors}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SubmitPlayAPIView(APIView):
    def post(self, request):
        """
        The function receives a POST request, validates the data using a serializer, and then submits a play
        in a game using the validated data.
        """
        serializer = SubmitPlaySerializer(data=request.data)

        if serializer.is_valid():
            try:
                data = serializer.validated_data
                game = GameService.submit_play(
                    data.get("game_id"),
                    data.get("player"),
                    (data.get("row"), data.get("column")),
                )
                output_serializer = GameOutputSerializer(game)
                return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            except SubmitPlayError as e:
                raise (f"Failed submitting the play with error: {e}")
        return Response(
            {"error": f"Bad requests params: {serializer.errors}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GameViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Game.objects.all()

        is_deleted_param = self.request.query_params.get("deleted", "").lower()
        if is_deleted_param == "true":
            queryset = queryset.filter(deleted=True)
        elif is_deleted_param == "false":
            queryset = queryset.filter(deleted=False)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return GameListSerializer
        return GameOutputSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer_class()(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            GameService.destroy_game(instance)

            return Response(
                {"message": "Game deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": f"Could not delete the game with error: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
