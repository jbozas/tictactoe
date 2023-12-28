from django.db import models

from .timestampmodel import TimeStampModel
from .player import Player
from .board import Board


class Game(TimeStampModel):
    player_one = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player_one"
    )
    player_two = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player_two"
    )
    board = models.OneToOneField(Board, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Game between {self.player_one} and {self.player_two} - {self.created_at}"
        )

    def winner(self) -> Player:
        return self.board.winner

    def get_next_turn(self) -> Player:
        return self.board.next_turn

    def submit_play(self, player: Player, destination: tuple) -> None:
        self.board.set_next_move(player, destination)
        next_to_move = (
            self.player_one if player.name == self.player_two.name else self.player_two
        )
        self.board.next_turn = next_to_move
        self.board.save()
