from django.test import TestCase
from django.db import transaction
from game.errors import InvalidMove
from game.models import Game, Board, Player
from game.services import GameService


class GameServiceTestCase(TestCase):
    def test_create_game(self):
        players = [{"name": "Player1"}, {"name": "Player2"}]
        starting_player = "Player1"

        with transaction.atomic():
            game = GameService.create_game(players, starting_player)

        self.assertEqual(game.player_one.name, "Player1")
        self.assertEqual(game.player_two.name, "Player2")
        self.assertEqual(game.board.next_turn.name, "Player1")

    def test_submit_play(self):
        # Assuming you have a valid game already created
        player = Player.objects.create(name="Player1", symbol="X")
        game = Game.objects.create(
            player_one=player,
            player_two=Player.objects.create(name="Player2", symbol="Y"),
            board=Board.objects.create(next_turn=player),
        )
        destination = (1, 1)

        with transaction.atomic():
            updated_game = GameService.submit_play(game.id, player.name, destination)

        self.assertEqual(updated_game.board.movements.count(), 1)
        self.assertEqual(updated_game.board.movements.first().player_name, "Player1")

    def test_submit_play_invalid_player(self):
        # Test submitting a play with an invalid player name
        players = [{"name": "Player1"}, {"name": "Player2"}]
        starting_player = "Player1"

        game = GameService.create_game(players, starting_player)
        player = Player.objects.create(name="InvalidPlayer", symbol="InvalidSymbol")
        with self.assertRaises(InvalidMove):
            game.board.is_valid_move(player, 4)
