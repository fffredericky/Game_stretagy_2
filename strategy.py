"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.

NOTE: I use the Tree and Stack class and the code is from course website
"""
from typing import Any, List
from copy import deepcopy


# TODO: Adjust the type annotation as needed.
# The following are the needed Tree class and Stack class
class Tree:
    """
    ADT tree
    """
    def __init__(self, value: object = None,
                 children: List['Tree'] = None) -> None:
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
def recursive_minimax_strategy(game: Any) -> Any:
    """
    recursive minimax strategy
    """
    new_states = []
    scores_list = []
    moves = game.current_state.get_possible_moves()
    for move in moves:
        # print(move)
        game_copy = deepcopy(game)
        game_copy.current_state = game.current_state.make_move(move)
        new_states.append(game_copy)
    for state in new_states:
        score = (-1 * recursive_helper(state))
        scores_list.append(score)
    return moves[scores_list.index(max(scores_list))]


def recursive_helper(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state where the
    player cannot lose.
    """
    if game.is_over(game.current_state):
        # print(game.current_state.get_current_player_name())
        if game.is_winner(game.current_state.get_current_player_name()):
            return 1
        elif game.is_winner('p1') or game.is_winner('p2'):
            return -1
        return 0
    else:
        new_states = []
        for move in game.current_state.get_possible_moves():
            game_copy = deepcopy(game)
            game_copy.current_state = game.current_state.make_move(move)
            new_states.append(game_copy)
        return max([-1 * recursive_helper(s)
                    for s in new_states])


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
        state = state_stack.remove()
        actual_state = state.value
        if state.children != []:
            state.score = max([c.score * -1 for c in state.children])
        elif actual_state.get_possible_moves() == []:
            game.current_state = actual_state
            if game.is_winner(actual_state.get_current_player_name()):
                state.score = 1
            elif game.is_winner('p1') or game.is_winner('p2'):
                state.score = -1
            else:
                state.score = 0
        else:
            act(state)
            state_stack.add(state)
            for c in state.children:
                state_stack.add(c)
    score_list = [-1 * c.score for c in state.children]
    return move_list[score_list.index(state.score)]


def act(state: Tree) -> None:
    """
    act helper to make move on a state
    """
    cur_state = state.value
    state.children = [Tree(cur_state.make_move(m)) for m in
                      cur_state.get_possible_moves()]


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
