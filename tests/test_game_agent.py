"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

from importlib import reload

import isolation
import game_agent

import sample_players
import game_agent

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    def test_greedy_player(self):
        """Test against GreedPlayer"""
        # create an isolation board (by default 7x7)
        player1 = game_agent.MinimaxPlayer()
        player2 = sample_players.GreedyPlayer()
        game = isolation.Board(player1, player2)

        # play the game automatically
        winner, history, outcome = game.play()
        print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
        print(game.to_string())
        print("Move history:\n{!s}".format(history))

if __name__ == '__main__':
    unittest.main()
