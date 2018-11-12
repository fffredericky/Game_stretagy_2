"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any
from stonehenge import StonehengeGame, StonehengeState
from game import Game
from game_state import GameState
from copy import deepcopy
from typing import List

# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Game) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)

def rough_outcome_strategy(game: Game) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2 # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


# TODO: Implement a recursive version of the minimax strategy.
def depth(obj: Game):
    """ Return the depth of obj
    """
    if obj.is_over(obj.current_state):
        return 1
    elif isinstance(obj, list):
        return 1 + max([depth(x) for x in obj])




def recursive_minimax(game: Game) -> Any:
    """
    Return the best move
    >>> g = StonehengeGame(True, 2)
    >>> g.current_state = g.current_state.make_move('C')
    >>> g.current_state = g.current_state.make_move('B')
    >>> g.current_state = g.current_state.make_move('D')
    >>> g.current_state = g.current_state.make_move('F')
    >>> recursive_minimax(g)
    'E'
    >>> h = StonehengeGame(True, 2)
    >>> h.current_state = h.current_state.make_move('A')
    >>> h.current_state = h.current_state.make_move('F')
    >>> h.current_state = h.current_state.make_move('D')
    >>> recursive_minimax(h)
    'E'
    """
    potential_games = []
    moves = game.current_state.get_possible_moves()
    for move in moves:
        #print(move)
        potential_game = deepcopy(game)
        potential_game.current_state = game.current_state.make_move(move)
        potential_games.append(potential_game)
    scores = []
    for g in potential_games:
        score = (-1 * recursive_minimax_deeper
                (g, g.current_state.get_current_player_name()))
        scores.append(score)
    for i in range(len(scores)):
        if scores[i] == 1:
            return moves[i]
    for k in range(len(scores)):
        if scores[k] == 0:
            return moves[k]
    for j in range(len(scores)):
        if scores[j] == -1:
            return moves[j]


def recursive_minimax_deeper(game: Game, current_player: str) -> Any:
    """
    Return a move for game by picking a move which results in a state where the
    player cannot lose.
    >>> g = StonehengeGame(True, 2)
    >>> g.current_state = g.current_state.make_move('C')
    >>> g.current_state = g.current_state.make_move('B')
    >>> g.current_state = g.current_state.make_move('D')
    >>> g.current_state = g.current_state.make_move('F')
    >>> recursive_minimax_deeper(g, g.current_state.get_current_player_name())
    -1
    >>> g = StonehengeGame(True, 2)
    >>> g.current_state = g.current_state.make_move('A')
    >>> g.current_state = g.current_state.make_move('D')
    >>> g.current_state = g.current_state.make_move('F')
    >>> g.current_state = g.current_state.make_move('B')
    >>> recursive_minimax_deeper(g, g.current_state.get_current_player_name())
    -1
    """
    if current_player == 'p1':
        other_player = 'p2'
    else:
        other_player = 'p1'
    if game.is_over(game.current_state):
        #print(game.current_state.get_current_player_name())
        if game.is_winner(current_player):
            return 1
        elif game.is_winner(other_player):
            return -1
        else:
            return 0
    else:
        potential_games = []
        for move in game.current_state.get_possible_moves():
            potential_game = deepcopy(game)
            potential_game.current_state = game.current_state.make_move(move)
            potential_games.append(potential_game)
        return max([
            -1 * recursive_minimax_deeper(x,
                                     x.current_state.get_current_player_name())
            for x in potential_games])


    # current_game = game
    # current_player = current_game.current_state.get_current_player_name()
    # potential_games = []
    # moves = current_game.current_state.get_possible_moves()
    # for move in moves:
    #     potential_game = deepcopy(current_game)
    #     potential_game.current_state = current_game.current_state.make_move(
    #         move)
    #     potential_games.append(potential_game)
    # pot_scores = recursive_minimax_list_int(potential_games, current_player)
    # for i in range(len(pot_scores)):
    #     return(pot_scores)




# TODO: Implement an iterative version of the minimax strategy.

if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
