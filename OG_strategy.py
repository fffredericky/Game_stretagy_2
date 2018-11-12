"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any, List


# TODO: Adjust the type annotation as needed.
# The following are the needed Tree class and Stack class
class Tree:
    """
    ADT tree
    """
    def __init__(self, value: object=None, children: List['Tree']=None) -> None:
        """
        Create tree
        """
        self.value = value
        self.children = children[:] if children is not None else []
        self.score = None


class Stack:
    """ Last-in, first-out (LIFO) stack.
    """

    def __init__(self) -> None:
        """ Create a new, empty Stack self.

        >>> s = Stack()
        """
        self._contains = []

    def add(self, obj: object) -> None:
        """ Add object obj to top of Stack self.

        >>> s = Stack()
        >>> s.add(5)
        """
        self._contains.append(obj)

    def remove(self) -> object:
        """
        Remove and return top element of Stack self.

        Assume Stack self is not emp.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._contains.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add(5)
        >>> s.is_empty()
        False
        """
        return len(self._contains) == 0


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
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
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

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
def recursive_minimax_strategy(game):
    """
    minimax
    """
    game_state = game.current_state
    moves = game_state.get_possible_moves()
    best_move = moves[0]
    best_score = -1
    for move in moves:
        new_state = game_state.make_move(move)
        score = min_play(new_state, game)
        if score > best_score:
            best_move = move
            best_score = score
    return best_move


def min_play(game_state, game):
    """helper"""
    state = game_state
    if game.is_over(state):
        if game.is_winner(game_state.get_current_player_name()):
            return 1
        elif game.is_winner('p1') or game.is_winner('p2'):
            return -1
        return 0
    moves = game_state.get_possible_moves()
    best_score = -1
    for move in moves:
        new_state = game_state.make_move(move)
        score = max_play(new_state, game)
        if score < best_score:
            best_score = score
    return best_score


def max_play(game_state, game):
    """
    helper
    """
    state = game_state
    if game.is_over(state):
        if game.is_winner(game_state.get_current_player_name()):
            return 1
        elif game.is_winner('p1') or game.is_winner('p2'):
            return -1
        return 0
    moves = state.get_possible_moves()
    best_score = 1
    for move in moves:
        new_state = game_state.make_move(move)
        score = min_play(new_state, game)
        if score > best_score:
            best_score = score
    return best_score


# TODO: Implement an iterative version of the minimax strategy.
# TODO cancer cancer cancer cancer cancer cancer
def iterative_minimax_strategy(game: Any) -> Any:
    """
    iterative minimax strategy
    """
    current_state = game.current_state
    move_list = current_state.get_possible_moves()
    state_tree = Tree(current_state)
    state_stack = Stack()
    state_stack.add(state_tree)
    while not state_stack.is_empty():
        act_state = state_stack.remove()
        cur_state = act_state.value
        if act_state.children != []:
            act_state.score = max([c.score * -1 for c in act_state.children])
        elif cur_state.get_possible_moves() == []:
            game.current_state = cur_state
            if game.is_winner(cur_state.get_current_player_name()):
                act_state.score = 1
            elif game.is_winner('p1') or game.is_winner('p2'):
                act_state.score = -1
            else:
                act_state.score = 0
        else:
            act(act_state)
            state_stack.add(act_state)
            for c in act_state.children:
                state_stack.add(c)

    score_list = [c.score for c in act_state.children]
    act_state.score = act_state.score * -1
    # print(score_list)
    # print(act_state.score)
    # print(move_list[score_list.index(act_state.score)])
    return move_list[score_list.index(act_state.score)]


def act(state: Tree) -> None:
    """
    act on a state
    """
    # cur_state = state.value
    # if cur_state.get_possible_moves() == []:
    #     game.current_state = cur_state
    #     if game.is_winner(cur_state.get_current_player_name()):
    #         state.score = 1
    #     elif game.is_winner('p1') or game.is_winner('p2'):
    #         state.score = -1
    #     else:
    #         state.score = 0
    cur_state = state.value
    state.children = [Tree(cur_state.make_move(m)) for m in cur_state.get_possible_moves()]


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
