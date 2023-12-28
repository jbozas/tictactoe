from rest_framework import serializers
from .models import Player, Game


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("id", "name", "symbol")


class CreateGameSerializer(serializers.Serializer):
    players = PlayerSerializer(many=True, required=True)
    starting_player = serializers.CharField(required=False)


class GameOutputSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField()
    movements_played = serializers.SerializerMethodField()
    next_turn = serializers.SerializerMethodField()
    board = serializers.SerializerMethodField()
    winner = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ("id", "players", "movements_played", "next_turn", "board", "winner")

    def get_players(self, instance) -> list[str]:
        return [str(instance.player_one), str(instance.player_two)]

    def get_movements_played(self, instance) -> int:
        return instance.board.movements.count()

    def get_next_turn(self, instance) -> str:
        return str(instance.board.next_turn)

    def get_board(self, instance) -> list:
        return list(instance.board.board)

    def get_winner(self, instance) -> str:
        return str(instance.board.winner)


class SubmitPlaySerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    player = serializers.CharField()
    row = serializers.IntegerField(min_value=1, max_value=3)
    column = serializers.IntegerField(min_value=1, max_value=3)

    def validate(self, data):
        """
        The `validate` function checks if a game exists, if it has already finished, if a player exists, if
        the player belongs to the game, and if it is the player's turn.

        :param data: The `data` parameter is a dictionary that contains the information needed to validate
        the game and player. It is expected to have the following keys:
        :return: the `data` parameter that was passed to it.
        """

        # Validate game exists
        try:
            game = Game.objects.get(pk=data.get("game_id"))
        except Game.DoesNotExist:
            raise serializers.ValidationError("Game do not exist")

        if game.winner() or game.deleted:
            raise serializers.ValidationError(
                "The game has already finished. You cannot make a next move."
            )

        # Validations about player.

        # Validates that player exists
        player = Player.objects.filter(name=data.get("player")).first()
        if not player:
            raise serializers.ValidationError("Player do not exist.")

        if player.name not in [game.player_one.name, game.player_two.name]:
            raise serializers.ValidationError(
                "Player do not belong to the current game."
            )

        if player.name != game.get_next_turn().name:
            raise serializers.ValidationError("Its not the turn for this player.")
        next_move = data.get("row") * data.get("column") - 1

        if game.board.board[next_move] != " ":
            raise serializers.ValidationError("Square already used.")

        return data


class GameListSerializer(serializers.ModelSerializer):
    movements_played = serializers.SerializerMethodField()
    is_finished = serializers.SerializerMethodField()
    is_deleted = serializers.BooleanField(source="deleted")

    class Meta:
        model = Game
        fields = ("id", "movements_played", "is_finished", "is_deleted")

    def get_is_finished(self, instance) -> bool:
        return instance.board.winner is not None

    def get_movements_played(self, instance) -> int:
        return instance.board.movements.count()
