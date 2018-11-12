"""
Stonehenge game and game state
"""
from typing import Any, Dict, List
from copy import deepcopy
from game_state import GameState
from game import Game


class StonehengeGame(Game):
    """
    Stonehenge game class.
    """

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """
        Game.__init__(self, p1_starts)
        self.size = int(input('Please enter side length: '))
        h = self.game_board_h_ley_line(self.size)
        self.current_state = SGState(self.is_p1_turn,
                                     self.game_board_h_ley_line(self.size),
                                     self.dr_ley_line(h), self.dl_ley_line(h))

    def game_board_h_ley_line(self, size: int) -> Dict[int, List[str]]:
        """
        create all horizontal ley line for the game
        """
        letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                  'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                  'Y', 'Z']
        h_ley_line = {}
        n = size
        total_letter_num = int((n ** 2 + 5 * n)/2)
        letters = letter[:total_letter_num]
        while len(letters) > n:
            for i in range(1, n + 1):
                h_ley_line[i] = letters[:i + 1]
                for let in h_ley_line[i]:
                    letters.remove(let)
        h_ley_line[len(h_ley_line) + 1] = letters
        for i in range(1, len(h_ley_line) + 1):
            h_ley_line[i] += ['@']
        return h_ley_line

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        return 'Players take turns claiming cells. A player captures ' \
               'at least half of the cells in a ley-line is the winner.'

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        return self.current_state.has_ley_line(player) >= 1.5 * (self.size + 1)

    def str_to_move(self, string: str) -> Any:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        # if string in self.current_state.get_possible_moves():
        return string.strip().upper()
        # return ''

    def is_over(self, state: "SGState") -> bool:
        """
        Return whether or not this game is over at state.
        """
        return state.get_possible_moves() == []

    def dr_ley_line(self, h: Dict[int, List[str]]) -> Dict[int, List[str]]:
        """
        get a dictionary contains all down right ley lines in order
        """
        dr = {}
        n = self.size
        for i in range(n, 0, -1):
            dr[n + 1 - i] = [h[i + c][c] for c in range(0, n + 1 - i)]
            dr[n + 1 - i].append(h[len(h)][n - i])
            dr[n + 1 - i].append(self.whoes_line(dr[n + 1 - i]))
        dr[n + 1] = [h[j][j] for j in range(1, n + 1)]
        dr[n + 1] += [self.whoes_line(dr[n + 1])]
        return dr

    def dl_ley_line(self, h: Dict[int, List[str]]) -> Dict[int, List[str]]:
        """
        get a dictionary contains all down left ley lines in order
        """
        dl = {}
        n = self.size
        dl[1] = [h[i][0] for i in range(1, n + 1)]
        dl[1] += [self.whoes_line(dl[1])]
        for i in range(1, n + 1):
            dl[i + 1] = [h[j][i] for j in range(i, n + 1)]
            dl[i + 1] += (h[n + 1][i - 1])
            dl[i + 1] += [self.whoes_line(dl[i + 1])]
        return dl

    def whoes_line(self, line: List[str]) -> str:
        """
        return if the line is claimed
        """
        if line.count('1') >= len(line)/2:
            return '1'
        elif line.count('2') >= len(line)/2:
            return '2'
        return '@'


class SGState(GameState):
    """
    The state of Stonehenge game at a certain point in time.
    """
    WIN: int = 1
    LOSE: int = -1
    DRAW: int = 0
    p1_turn: bool

    def __init__(self, is_p1_turn: bool, h_ley_lines: Dict[int, List[str]],
                 dr_ley_line: Dict[int, List[str]],
                 dl_ley_line: Dict[int, List[str]]) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        """
        GameState.__init__(self, is_p1_turn)
        self.h_ley_line = h_ley_lines
        self.dl = dl_ley_line
        self.dr = dr_ley_line
        self.size = len(h_ley_lines) - 1

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        >>> g = SGState(True, {1: ['A', 'B', '@'], 2: ['C', 'D', 'E', '@'], 3: ['F', 'G', '@']})
        >>> print(g)
               @   @
              /   /
         @ - A - B   @
            / \\ / \\ /
        @ - C - D - E
             \\ / \\ / \\
          @ - F - G   @
               \\   \\
                @   @
        >>> g = SGState(True, {1: ['1', 'B', '1'], 2: ['C', '2', 'E', '@'], 3: ['F', '1']})
        >>> print(g)
               1   @
              /   /
         1 - 1 - B   1
            / \\ / \\ /
        @ - C - 2 - E
             \\ / \\ / \\
          1 - F - 1   @
               \\   \\
                @   1
        """
        if self.size == 1:
            return self.board_length_1()
        elif self.size == 2:
            return self.board_length_2()
        elif self.size == 3:
            return self.board_length_3()
        elif self.size == 4:
            return self.board_length_4()
        return self.board_length_5()

    def board_length_1(self) -> str:
        """
        return the game baord for size 1
        """
        dl = self.dl
        dr = self.dr
        h = self.h_ley_line
        board = ''
        board += '      {}   {}'.format(dl[1][-1], dl[2][-1]) + '\n'
        board += '     /   /' + '\n'
        board += '{} - {} - {}'.format(h[1][-1], h[1][0],
                                       h[1][1]) + '\n'
        board += '     \\ / \\ ' + '\n'
        board += '  {} - {}   {}'.format(h[2][-1], h[2][0], dr[2][-1]) + '\n'
        board += '       \\ ' + '\n'
        board += '        {}'.format(dr[1][-1])
        return board

    def board_length_2(self) -> str:
        """
        return the game baord for size 2
        """
        dl = self.dl
        dr = self.dr
        h = self.h_ley_line
        board = ''
        board += '        {}   {} '.format(dl[1][-1], dl[2][-1]) + '\n'
        board += '       /   /' + '\n'
        board += '  {} - {} - {}   {}'.format(h[1][-1], h[1][0],
                                              h[1][1], dl[3][-1]) + '\n'
        board += '     / \\ / \\ /' + '\n'
        board += '{} - {} - {} - {}'.format(h[2][-1], h[2][0], h[2][1],
                                            h[2][2]) + '\n'
        board += '     \\ / \\ / \\' + '\n'
        board += '  {} - {} - {}   {}'.format(h[3][-1],
                                              h[3][0], h[3][1],
                                              dr[3][-1]) + '\n'
        board += '       \\   \\' + '\n'
        board += '        {}   {}'.format(dr[1][-1], dr[2][-1])
        return board

    def board_length_3(self) -> str:
        """
        return the game baord for size 3
        """
        dl = self.dl
        dr = self.dr
        h = self.h_ley_line
        board = ''
        board += '          {}   {}'.format(dl[1][-1], dl[2][-1]) + '\n'
        board += '         /   /' + '\n'
        board += '    {} - {} - {}   {}'.format(h[1][-1],
                                                h[1][0], h[1][1],
                                                dl[3][-1]) + '\n'
        board += '       / \\ / \\ /' + '\n'
        board += '  {} - {} - {} - {}   {}'.format(h[2][-1],
                                                   h[2][0], h[2][1], h[2][2],
                                                   dl[4][-1]) + '\n'
        board += '     / \\ / \\ / \\ /' + '\n'
        board += '{} - {} - {} - {} - {}'.format(h[3][-1], h[3][0], h[3][1],
                                                 h[3][2], h[3][3]) + '\n'
        board += '     \\ / \\ / \\ / \\' + '\n'
        board += '  {} - {} - {} - {}   {}'.format(h[4][-1],
                                                   h[4][0], h[4][1], h[4][2],
                                                   dr[4][-1]) + '\n'
        board += '       \\   \\   \\' + '\n'
        board += '       {}    {}   {}'.format(dr[1][-1],
                                               dr[2][-1],
                                               dr[3][-1])
        return board

    def board_length_4(self) -> str:
        """
        return the game baord for size 4
        """
        dl = self.dl
        dr = self.dr
        h = self.h_ley_line
        board = ''
        board += '            {}   {}'.format(dl[1][-1],
                                              dl[2][-1]) + '\n'
        board += '           /   /' + '\n'
        board += '      {} - {} - {}   {}'.format(h[1][-1],
                                                  h[1][0], h[1][1],
                                                  dl[3][-1]) + '\n'
        board += '         / \\ / \\ /' + '\n'
        board += '    {} - {} - {} - {}   {}'.format(h[2][-1],
                                                     h[2][0], h[2][1], h[2][2],
                                                     dl[4][-1]) + '\n'
        board += '       / \\ / \\ / \\ /' + '\n'
        board += '  {} - {} - {} - {} - {}   {}'.format(h[3][-1],
                                                        h[3][0], h[3][1],
                                                        h[3][2], h[3][3],
                                                        dl[5][-1]) + '\n'
        board += '     / \\ / \\ / \\ / \\ /' + '\n'
        board += '{} - {} - {} - {} - {} - {}'.format(h[4][-1],
                                                      h[4][0], h[4][1], h[4][2],
                                                      h[4][3], h[4][4]) + '\n'
        board += '     \\ / \\ / \\ / \\ / \\' + '\n'
        board += '  {} - {} - {} - {} - {}   {}'.format(dl[5][-1],
                                                        h[5][0], h[5][1],
                                                        h[5][2], h[5][3],
                                                        dr[5][-1],) + '\n'
        board += '       \\   \\   \\   \\' + '\n'
        board += '        {}   {}   {}   {}'.format(dr[1][-1], dr[2][-1],
                                                    dr[3][-1], dr[4][-1])
        return board

    def board_length_5(self) -> str:
        """
        return the game baord for size 5
        """
        dl = self.dl
        dr = self.dr
        h = self.h_ley_line
        board = ''
        board += '              {}   {}'.format(dl[1][-1],
                                                dl[2][-1]) + '\n'
        board += '             /   /' + '\n'
        board += '        {} - {} - {}   {}'.format(h[1][-1],
                                                    h[1][0], h[1][1],
                                                    dl[3][-1]) + '\n'
        board += '           / \\ / \\ /' + '\n'
        board += '      {} - {} - {} - {}   {}'.format(h[2][-1],
                                                       h[2][0], h[2][1],
                                                       h[2][2],
                                                       dl[4][-1]) + '\n'
        board += '         / \\ / \\ / \\ /' + '\n'
        board += '    {} - {} - {} - {} - {}   {}'.format(h[3][-1],
                                                          h[3][0], h[3][1],
                                                          h[3][2], h[3][3],
                                                          dl[5][-1]) + '\n'
        board += '       / \\ / \\ / \\ / \\ /' + '\n'
        board += '  {} - {} - {} - {} - {} - {}   {}'.format(h[4][-1], h[4][0],
                                                             h[4][1], h[4][2],
                                                             h[4][3], h[4][4],
                                                             dl[6][-1]) + '\n'
        board += '     / \\ / \\ / \\ / \\ / \\ /' + '\n'
        board += '{} - {} - {} - {} - {} - {} - {}'.format(h[5][-1], h[5][0],
                                                           h[5][1], h[5][2],
                                                           h[5][3], h[5][4],
                                                           h[5][5]) + '\n'
        board += '     \\ / \\ / \\ / \\ / \\ / \\' + '\n'
        board += '  {} - {} - {} - {} - {} - {}   {}'.format(h[6][-1], h[6][0],
                                                             h[6][1], h[6][2],
                                                             h[6][3], h[6][4],
                                                             dr[6][-1]) + '\n'
        board += '       \\   \\   \\   \\   \\' + '\n'
        board += '        {}   {}   {}   {}   {}'.format(dr[1][-1],
                                                         dr[2][-1],
                                                         dr[3][-1],
                                                         dr[4][-1],
                                                         dr[5][-1])
        return board

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        >>> g = SGState(True, {1: ['A', 'B', '@'], 2: ['C', '@']}, {1: ['A', 'C', '@'], 2: ['B', '@']}, {1: ['A', '@'], 2: ['B', 'C', '@']})
        >>> g.get_possible_moves()
        ['A', 'B', 'C']
        """
        h = self.h_ley_line
        move = []
        possible_list = []
        for line in h:
            for letter in h[line]:
                if (not letter.isnumeric()) and letter != '@':
                    possible_list.append(letter)
        if self.has_ley_line('p1') < 1.5 * (self.size + 1) and \
                self.has_ley_line('p2') < 1.5 * (self.size + 1):
            for letter in possible_list:
                move.append(letter)
        return move

    def make_move(self, move: Any) -> 'SGState':
        """
        Return the GameState that results from applying move to this GameState.
        >>> g = SGState(True, {1: ['A', 'B', '@'], 2: ['C', '@']}, {1: ['A', 'C', '@'], 2: ['B', '@']}, {1: ['A', '@'], 2: ['B', 'C', '@']})
        >>> a = g.make_move('A')
        >>> b = g.make_move('E')
        >>> a
        Current player: p2, player 1 has 3 ley line(s), player 2 has 0 ley line(s)
        >>> g
        Current player: p1, player 1 has 0 ley line(s), player 2 has 0 ley line(s)
        """
        player_mark = self.get_current_player_name()[-1]
        new_h_ley_line = deepcopy(self.h_ley_line)
        new_dr = deepcopy(self.dr)
        new_dl = deepcopy(self.dl)
        # print(new_dr, new_dl, new_h_ley_line)
        for line in new_h_ley_line:
            if move in new_h_ley_line[line]:
                new_h_ley_line[line][new_h_ley_line[line].index(move)] \
                    = player_mark
            if move in new_dl[line]:
                new_dl[line][new_dl[line].index(move)] = \
                    player_mark
            if move in new_dr[line]:
                new_dr[line][new_dr[line].index(move)] = \
                    player_mark
        for line in new_dl:
            if new_h_ley_line[line][-1] == '@':
                new_h_ley_line[line][-1] = \
                    self.whoes_line(new_h_ley_line[line][:-1])
            if '@' in new_dr[line]:
                new_dr[line][-1] = self.whoes_line(new_dr[line][:-1])
            if '@' in new_dl[line][-1]:
                new_dl[line][-1] = self.whoes_line(new_dl[line][:-1])
        return SGState(not self.p1_turn, new_h_ley_line, new_dr, new_dl)

    def __repr__(self) -> Any:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        p1_ley_line = self.has_ley_line('p1')
        p2_ley_line = self.has_ley_line('p2')
        if self.p1_turn:
            return 'Current player: p1, player 1 has {} ley line(s), ' \
                   'player 2 has {} ley line(s)'.format(p1_ley_line,
                                                        p2_ley_line)
        return 'Current player: p2, player 1 has {} ley line(s), ' \
               'player 2 has {} ley line(s)'.format(p1_ley_line, p2_ley_line)

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.

        >>> g = SGState(True, {1: ['A', 'B', '@'], 2: ['C', '@']}, {1: ['A', 'C', '@'], 2: ['B', '@']}, {1: ['A', '@'], 2: ['B', 'C', '@']})
        >>> g.rough_outcome()
        1
        """
        if self.get_possible_moves() == []:
            return -1
        player = 'p' + str(3 - int(self.get_current_player_name()[-1]))
        states_list = [self.make_move(m) for m in self.get_possible_moves()]
        for state in states_list:
            if self.p1_turn:
                if state.has_ley_line(self.get_current_player_name()) >= \
                        1.5 * (self.size + 1):
                    return self.WIN
            if state.has_ley_line(player) >= 1.5 * (self.size + 1):
                return self.WIN
        for move in self.get_possible_moves():
            new_state = self.make_move(move)
            for new_move in new_state.get_possible_moves():
                new_new_state = new_state.make_move(new_move)
                if new_new_state.has_ley_line(player) >= 1.5 * (self.size + 1):
                    return self.LOSE
                if new_new_state.has_ley_line(self.get_current_player_name()) \
                        >= 1.5 * (self.size + 1):
                    return self.LOSE
        return self.DRAW

    def has_ley_line(self, player: str) -> int:
        """
        return the number of ley lines player has.
        >>> g = SGState(True, {1: ['1', 'B', '1'], 2: ['C', '1', 'E', '@'], 3: ['F', 'G', '@']})
        >>> g.has_ley_line('p1')
        3
        >>> g = SGState(True, {1: ['A', 'B', '@'], 2: ['C', 'D', '1', '@'], 3: ['F', 'G', '@']})
        >>> g.has_ley_line('p1')
        2
        >>> g = SGState(True, {1: ['2', 'B', '2'], 2: ['1', '1', 'E', '1'], 3: ['2', '1' '2']})
        >>> g.has_ley_line('p1')
        3
        """
        total = 0
        player_mark = player[-1]
        dr = self.dr
        dl = self.dl
        h = self.h_ley_line
        for line in dr:
            if dr[line][-1] == player_mark:
                total += 1
            if dl[line][-1] == player_mark:
                total += 1
            if h[line][-1] == player_mark:
                total += 1
        return total

    def whoes_line(self, line: List[str]) -> str:
        """
        return if the line is claimed
        """
        if line.count('1') >= len(line)/2:
            return '1'
        elif line.count('2') >= len(line)/2:
            return '2'
        return '@'


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
