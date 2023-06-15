from connect_four.constant import *
import os

class Board:

    def __init__(self):
        self.squares = [[' ', ' ', ' ', ' ', ' ', ' ', ' '] for col in range(COL)]
        self.img = os.path.join(fr'../images/icons/bo2.png')

    @staticmethod
    def is_in_boundaries(curr_sq):
        if curr_sq[1] < 530 or curr_sq[1] > 590:
            return False
        for col in range(7):
            if curr_sq[0] >= (col*85)+8 and curr_sq[0] <= (col*85)+ 78:
                return True

        return False

    def is_valid_move(self, curr_sq):
        for row in range(6):
            if self.squares[row][curr_sq[1]] == ' ':
                return True
        return False

    def move(self, curr_sq, curr_player):
        for row in range(ROW-1, -1, -1):
            if self.squares[row][curr_sq[1]] == ' ':
                self.squares[row][curr_sq[1]] = curr_player
                break

    def row_sequence(self, curr_player):
        for col in range(COL-3):
            for row in range(ROW):
                if self.squares[row][col] == curr_player and self.squares[row][col+1] == curr_player and self.squares[row][col+2] == curr_player and self.squares[row][col+3] == curr_player:
                    return True
        return False


    def col_sequence(self, curr_player):
        for row in range(ROW-3):
            for col in range(COL):
                if self.squares[row][col] == curr_player and self.squares[row+1][col] == curr_player and self.squares[row+2][col] == curr_player and self.squares[row+3][col] == curr_player:
                    return True
        return False

    def diagnoal_sequence(self, curr_player):
        for col in range(COL - 3):
            for row in range(ROW - 3):
                if self.squares[row][col] == curr_player and self.squares[row+1][col + 1] == curr_player and \
                        self.squares[row+2][col + 2] == curr_player and self.squares[row+3][col + 3] == curr_player:
                    return True

        for col in range(COL - 3):
            for row in range(3, ROW):
                if self.squares[row][col] == curr_player and self.squares[row - 1][col+1] == curr_player and \
                        self.squares[row - 2][col+2] == curr_player and self.squares[row - 3][col+3] == curr_player:
                    return True
        return False