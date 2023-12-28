from django.test import TestCase
from django.urls import reverse
from game.services import GameService
import json


class TicTacToeAPITestCase(TestCase):
    def setUp(self):
        self.game = GameService.create_game(
            [
                {"name": "me", "symbol": "X"},
                {"name": "other", "symbol": "Z"},
            ],
            "me",
        )

    def test_create_game(self):
        url = reverse("create_game")
        data = {
            "players": [
                {"name": "me", "symbol": "X"},
                {"name": "other", "symbol": "Z"},
            ],
            "starting_player": "me",
        }

        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        create_game = response.json()
        self.assertIn("id", create_game)
        self.assertEqual(create_game["movements_played"], 0)
        self.assertEqual(create_game["next_turn"], "Player me, symbol: (X)")
        self.assertEqual(
            create_game["board"], [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        )
        self.assertEqual(create_game["winner"], "None")

    def test_get_game(self):
        url = reverse("game-detail", kwargs={"pk": self.game.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        game_data = response.json()
        self.assertEqual(game_data["id"], self.game.id)
        # Add more assertions based on the expected response structure

    def test_list_games(self):
        url = reverse("game-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        games = response.json()
        self.assertGreater(len(games), 0)
        # Add more assertions based on the expected response structure

    def test_delete_game(self):
        url = reverse("game-detail", kwargs={"pk": self.game.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        # Verify that the game is deleted
        self.game.refresh_from_db()
        self.assertTrue(self.game.deleted)
