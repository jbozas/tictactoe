from django.db import transaction

from game.models import Game, Board, Player, Movement
from game.errors import GameDeletionError


class GameService:
    @transaction.atomic
    def create_game(players: list, starting_player: str = None) -> Game:
        """
        The `create_game` function creates a new game with two players and a board, and sets the starting
        player if specified.
        """
        player_one = Player.objects.create(
            name=players[0].get("name"), symbol=players[0].get("symbol", "X")
        )
        player_two = Player.objects.create(
            name=players[1].get("name"), symbol=players[1].get("symbol", "O")
        )
        next_turn = (
            Player.objects.filter(name=starting_player).first()
            if starting_player
            else player_one
        )
        board = Board.objects.create(next_turn=next_turn)
        return Game.objects.create(
            player_one=player_one, player_two=player_two, board=board
        )

    @transaction.atomic
    def submit_play(game: int, player: str, destination: tuple) -> Game:
        """
        The `submit_play` function takes in a game ID, player name, and destination coordinates, retrieves
        the corresponding game and player objects, submits the play to the game, creates a movement object
        with the player name and destination, adds the movement to the game's board, and returns the updated
        game object.
        """
        game = Game.objects.get(id=game)
        player = Player.objects.filter(name=player).first()
        game.submit_play(player, destination)
        movement = Movement.objects.create(
            player_name=player.name, destination=destination
        )
        game.board.movements.add(movement)
        return game

    @transaction.atomic
    def destroy_game(game: Game) -> Game:
        """
        The `destroy_game` function marks a game as deleted and saves the changes.
        """
        if game.deleted:
            raise GameDeletionError(f"Game {game.id} already deleted")
        game.deleted = True
        game.save()
        return game
