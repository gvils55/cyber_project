from tic_tac_toe.constant import *

class Board:

    def __init__(self):
        self.squares = [[' ', ' ', ' '] for col in range(DIMENSION)]

    @staticmethod
    def is_in_boundaries(*args):
        for args in args:
            if args < 0 or args > 2:
                return False
        return True

    def is_valid_move(self, curr_sq):
        if self.squares[curr_sq[0]][curr_sq[1]] == ' ':
            return True
        return False


    def move(self, curr_sq, curr_player):
        self.squares[curr_sq[0]][curr_sq[1]] = curr_player


    def three_row(self, curr_player):
        for row in range(DIMENSION):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] == curr_player:
                return True
        return False


    def three_col(self, curr_player):
        for col in range(DIMENSION):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] == curr_player:
                return True
        return False


    def three_diagnoal(self, curr_player):
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] == curr_player:
            return True
        elif self.squares[0][2] == self.squares[1][1] == self.squares[2][0] == curr_player:
            return True
        return False