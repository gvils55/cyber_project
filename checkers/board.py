from checkers.Constant import *
from checkers.move import Move
from checkers.piece import *
from checkers.square import Square

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(DIMENSION)]
        self.create_board()
        self.create_pieces('white')
        self.create_pieces('black')

    def create_board(self):

        for row in range(DIMENSION):
            for col in range(DIMENSION):
                self.squares[row][col] = Square(row, col)


    def create_pieces(self, color):

        row_1, row_2 = (6, 7) if color == 'white' else (1, 0)
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                if (row+col) %2 == 0:
                    if row == row_1 or row == row_2:
                        self.squares[row][col] = Square(row, col, Pawn(color))


    def calc_moves(self, row, col, piece):
            start_sq = Square(row, col, piece)

            def add_valid_moves(possible_moves):
                for possible_moves in possible_moves:
                    possible_row, possible_col = possible_moves
                    if Square.is_in_boundaries(possible_row, possible_col):
                        if self.squares[possible_row][possible_col].is_empty():
                            end_sq = Square(possible_row, possible_col)
                            move = Move(start_sq, end_sq, ("move"))
                            piece.add_moves(move)


            def add_valid_captures(possible_captures):
                for moves in possible_captures:
                    possible_row, possible_col = moves
                    row_between = int((possible_row - row)/2 + row)
                    col_between = int((possible_col - col)/2 +col)
                    if Square.is_in_boundaries(possible_row, possible_col):
                        if self.squares[possible_row][possible_col].is_empty() and self.squares[row_between][col_between].has_rival_piece(piece.color):
                            sq_between = Square(row_between, col_between, self.squares[row_between][col_between].piece)
                            end_sq = Square(possible_row, possible_col)
                            move = Move(start_sq, end_sq, ("eat",sq_between))
                            piece.add_moves(move)

            def add_sequence_moves(move_options):
                for move_option in move_options:
                    possible_row = move_option[0] + row
                    possible_col = move_option[1] + col
                    while True:
                        if Square.is_in_boundaries(possible_row, possible_col):
                            final_piece = self.squares[possible_row][possible_col].piece
                            end_sq = Square(possible_row, possible_col, final_piece)

                            if self.squares[possible_row][possible_col].is_empty():
                                move = Move(start_sq, end_sq, ("move"))
                                piece.add_moves(move)


                            elif self.squares[possible_row][possible_col].has_rival_piece(piece.color):
                                sq_between = Square(possible_row, possible_col, self.squares[possible_row][possible_col].piece)
                                possible_row += move_option[0]
                                possible_col += move_option[1]
                                if Square.is_in_boundaries(possible_row, possible_col):
                                    final_piece = self.squares[possible_row][possible_col].piece
                                    end_sq = Square(possible_row, possible_col, final_piece)
                                    if self.squares[possible_row][possible_col].is_empty():
                                        move = Move(start_sq, end_sq, ("eat", sq_between))
                                        piece.add_moves(move)
                                break

                            else:
                                break

                        else:
                            break
                        possible_row += move_option[0]
                        possible_col += move_option[1]

            if piece.name == 'pawn':
                if piece.color == "white":
                    possible_moves = [(row - 1, col - 1), (row - 1, col + 1)]
                    possible_captures = [(row - 2, col - 2), (row - 2, col + 2)]
                else:
                    possible_moves = [(row + 1, col - 1), (row + 1, col + 1)]
                    possible_captures = [(row + 2, col - 2), (row + 2, col + 2)]
                add_valid_moves(possible_moves)
                add_valid_captures(possible_captures)

            elif piece.name == 'king':
                possible_directions = [(-1, 1), (-1, -1), (1, 1), (1, -1)]
                add_sequence_moves(possible_directions)


    def move(self, curr_move, piece):
        end_sq = curr_move.end_square
        start_sq = curr_move.start_square
        if curr_move.kind[0] == "eat":
            sq_between = curr_move.kind[1]
            self.squares[sq_between.row][sq_between.col].piece = None
        self.squares[start_sq.row][start_sq.col].piece = None
        self.squares[end_sq.row][end_sq.col].piece = piece
        self.clear_moves()
        self.check_promotion(piece, curr_move.end_square)


    def clear_moves(self):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                if self.squares[row][col].has_piece():
                    self.squares[row][col].piece.moves = []

    def check_promotion(self, piece, curr_sq):
        if piece.name == "pawn":
            if curr_sq.row == 0 or curr_sq.row == 7:
                self.squares[curr_sq.row][curr_sq.col].piece = King(piece.color)

    def is_game_over(self, curr_player):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                if self.squares[row][col].has_rival_piece(curr_player):
                    return False
        return True