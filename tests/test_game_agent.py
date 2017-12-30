"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

from importlib import reload
import math

import isolation
import game_agent

import sample_players

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    def test_alpha_beta(self):
        """Test Alfa beta agains GreedPlayer"""
        player1 = game_agent.AlphaBetaPlayer()
        player2 = sample_players.GreedyPlayer()

        game = isolation.Board(player1, player2, 3, 5)

        winner, history, outcome = game.play()
        self.assertEqual(winner, player1, "Alphabeta must win when it starts playing")

    def test_greedy_player(self):
        """Test against GreedPlayer"""
        # create an isolation board (by default 7x7)
        player1 = game_agent.MinimaxPlayer()
        player2 = sample_players.GreedyPlayer()
        game = isolation.Board(player1, player2)

        # play the game automatically
        winner, history, outcome = game.play()
        self.assertEqual(winner, player1, "Minimax must win when it start playing!")

        game = isolation.Board(player2, player1)

        # play the game automatically
        winner, history, outcome = game.play()
        self.assertEqual(winner, player1, "Minimax must win when greed start playing!")

        game = isolation.Board(player2, player1)

        game.apply_move((math.floor(game.height / 2), math.floor(game.width / 2)))

        # play the game automatically
        winner, history, outcome = game.play()
        self.assertEqual(winner, player1, "Minimax must win when greed start playing in the middle!")

        game = isolation.Board(player1, player2, 15, 15)

        # play the game automatically
        winner, history, outcome = game.play()
        self.assertEqual(winner, player1, "Minimax must win in a large board!")

        game = isolation.Board(player1, player2, 3, 5)

        # play the game automatically
        winner, history, outcome = game.play()
        self.assertEqual(winner, player1, "Minimax must win in a small board!")


if __name__ == '__main__':
    unittest.main()
