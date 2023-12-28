from django.db import models

from .player import Player
from .movement import Movement
from game.errors import InvalidMove


class Board(models.Model):
    board = models.CharField(max_length=9, default=" " * 9)
    winner = models.ForeignKey(
        Player, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    next_turn = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="next_turn",
    )
    movements = models.ManyToManyField(Movement)

    def is_valid_move(self, player: Player, next_move: int) -> bool:
        if self.winner:
            raise InvalidMove("Game already ended.")

        if self.next_turn.name != player.name:
            raise InvalidMove(f"Player {player.name} is not the next to move.")

        if next_move < 0 or next_move > 8:
            raise InvalidMove("Invalid destination movement params.")

        if self.board[next_move] != " ":
            raise InvalidMove("Square already used.")
        return True

    def set_next_move(self, player: Player, destination: tuple) -> None:
        row = destination[0]
        column = destination[1]
        next_move_index = row * column - 1
        if self.is_valid_move(player, next_move_index):
            board = list(self.board)
            board[next_move_index] = self.next_turn.symbol
            self.board = "".join(board)
            self.get_winner()

    def get_winner(self) -> None:
        """
        If the game is over and there is a winner, returns 'X' or 'O'.
        If the game is a stalemate, it returns ' ' (space)
        If the game isn't over, it returns None.

        The test is to simple check for each combination of winnable
        states --- across, down, and diagonals.
        If none of the winning states is reached and there are
        no empty squares, the game is declared a stalemate.
        """
        WINNING = [
            [0, 1, 2],  # Across top
            [3, 4, 5],  # Across middle
            [6, 7, 8],  # Across bottom
            [0, 3, 6],  # Down left
            [1, 4, 7],  # Down middle
            [2, 5, 8],  # Down right
            [0, 4, 8],  # Diagonal ltr
            [2, 4, 6],  # Diagonal rtl
        ]
        board = list(self.board)
        for wins in WINNING:
            # Create a tuple
            w = (board[wins[0]], board[wins[1]], board[wins[2]])
            if w == tuple(self.next_turn.symbol * 3):
                self.winner = self.next_turn
                return
        # Check for stalemate
        if " " not in board:
            stalemate = Player.objects.get_or_create(name="Stalemate", symbol="?")
            self.winner = stalemate
