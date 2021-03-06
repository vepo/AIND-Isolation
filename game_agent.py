"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def possible_move_weight(game, move):
    """Look aheah! Here I calculate a weight based on the possible moves from the possible moves"""
    r, c = move
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    return len([(r + dr, c + dc) for dr, dc in directions
                if game.move_is_legal((r + dr, c + dc))])

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    player_moves = set(game.get_legal_moves(player))
    opponent_moves = set(game.get_legal_moves(game.get_opponent(player)))
    common_moves = player_moves - opponent_moves

    #deep_factor = 1 / (game.move_count + 1.0)
    # Here I'm calculating the heuristic based on the possible
    # moves and the common moves from both players
    return float(len(player_moves) + len(common_moves) * game.move_count
                  - len(common_moves) / (game.move_count + 1.0)
                  - len(opponent_moves - common_moves))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    player_moves = game.get_legal_moves(player)

    # This heuristic just calculate how many moves the player has more than the other player
    # And multiply this value by the possible_move_weight
    return float(len(player_moves) * sum(possible_move_weight(game, m) for m in player_moves)
            - len(opponent_moves) * sum(possible_move_weight(game, m) for m in opponent_moves))

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    # This is a more simple heuristic, I made a factor based on the possible_move_weight
    return (len(player_moves) *
            sum(possible_move_weight(game, m) for m in player_moves) /
            (1 + sum(possible_move_weight(game, m) for m in opponent_moves)))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    good_start_positions = [(1, 2), (1, 4), (3, 4), (4, 1), (4, 3), (4, 4), (4, 5), (5, 4), (5, 6)]

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Choose a start position from the best
        if (
                game.width == 7 and
                game.height == 7 and
                game.get_player_location(self) is None and
                game.get_player_location(game.get_opponent(self)) is None
        ):
            return random.choice(MinimaxPlayer.good_start_positions)

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            best_move = self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        _, move = max([(self.minimax_min(game.forecast_move(m), depth - 1), m) for m in legal_moves])
        return move

    def minimax_min(self, game, depth):
        """Choose the min value on the tree"""
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.score(game, self)

        value = float("inf")
        for move in legal_moves:
            value = min(value, self.minimax_max(game.forecast_move(move), depth - 1))
        return value

    def minimax_max(self, game, depth):
        """Choose the max value on the tree"""
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.score(game, self)

        value = float("-inf")
        for move in legal_moves:
            value = max(value, self.minimax_min(game.forecast_move(move), depth - 1))
        return value

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    good_start_positions = [(1, 2), (1, 4), (3, 4), (4, 1), (4, 3), (4, 4), (4, 5), (5, 4), (5, 6)]

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        ### Choose a position from the best positions
        if (
                game.width == 7 and
                game.height == 7 and
                game.get_player_location(self) is None and
                game.get_player_location(game.get_opponent(self)) is None
        ):
            return random.choice(AlphaBetaPlayer.good_start_positions)

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            deep = 1
            while True:
                best_move = self.alphabeta(game, deep)
                deep += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return self.alphabeta_max(game, depth, alpha, beta)[1]

    def alphabeta_max(self, game, depth, alpha, beta):
        """Choose max on AlphaBeta Prunning"""
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self), (-1, -1)

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.score(game, self), (-1, -1)

        best_value, best_move = float("-inf"), (-1, -1)
        for move in legal_moves:
            score = self.alphabeta_min(game.forecast_move(move), depth - 1, alpha, beta)[0]
            if score > best_value:
                best_value = score
                best_move = move
            if best_value >= beta:
                return best_value, best_move
            alpha = max(alpha, best_value)
        return best_value, best_move

    def alphabeta_min(self, game, depth, alpha, beta):
        """Choose min on AlphaBeta Prunning"""
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self), (-1, -1)

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.score(game, self), (-1, -1)

        best_value, best_move = float("inf"), (-1, -1)
        for move in legal_moves:
            score = self.alphabeta_max(game.forecast_move(move), depth - 1, alpha, beta)[0]
            if score < best_value:
                best_move = move
                best_value = score
            if best_value <= alpha:
                return best_value, best_move
            beta = min(beta, best_value)
        return best_value, best_move
