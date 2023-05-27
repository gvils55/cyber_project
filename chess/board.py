import copy

from chess.Constant import *
from chess.move import Move
from chess.piece import *
from chess.square import Square


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

        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
        for col in range(DIMENSION):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        self.squares[row_other][0] = Square(row_pawn, 0, Rook(color))
        self.squares[row_other][7] = Square(row_pawn, 7, Rook(color))

        self.squares[row_other][4] = Square(row_pawn, 4, King(color))

        self.squares[row_other][3] = Square(row_pawn, 3, Queen(color))

        self.squares[row_other][6] = Square(row_pawn, 6, Knight(color))
        self.squares[row_other][1] = Square(row_pawn, 1, Knight(color))

        self.squares[row_other][5] = Square(row_pawn, 5, Bishop(color))
        self.squares[row_other][2] = Square(row_pawn, 2, Bishop(color))


    def is_in_check(self, move, piece):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(move, temp_piece)


        for row in range(DIMENSION):
            for col in range(DIMENSION):
                if temp_board.squares[row][col].has_rival_piece(temp_piece.color):
                    curr_piece = temp_board.squares[row][col].piece
                    temp_board.calc_moves(row, col, curr_piece, False)
                    for curr_move in curr_piece.moves:
                        if isinstance(curr_move.end_square.piece, King):
                            return True
        return False


    def calc_moves(self, row, col, piece, bool= True):
        start_sq = Square(row, col, piece)

        def add_valid_moves(possible_moves):
            for possible_moves in possible_moves:
                possible_row, possible_col = possible_moves
                if Square.is_in_boundaries(possible_row, possible_col):
                    if self.squares[possible_row][possible_col].is_empty():
                        end_sq = Square(possible_row, possible_col)
                        move = Move(start_sq, end_sq, "move")
                        if bool:
                            if not self.is_in_check(move, piece):
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)


                    elif self.squares[possible_row][possible_col].has_rival_piece(piece.color):
                        final_piece = self.squares[possible_row][possible_col].piece
                        end_sq = Square(possible_row, possible_col, final_piece)
                        move = Move(start_sq, end_sq, "eat")
                        if bool:
                            if not self.is_in_check(move, piece):
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)


        def add_sequence_moves(move_options):
            for move_option in move_options:
                possible_row = move_option[0] +row
                possible_col = move_option[1] + col
                while True:
                    if Square.is_in_boundaries(possible_row, possible_col):
                        final_piece = self.squares[possible_row][possible_col].piece
                        end_sq = Square(possible_row, possible_col, final_piece)

                        if self.squares[possible_row][possible_col].is_empty():
                            move = Move(start_sq, end_sq, "move")
                            if bool:
                                if not self.is_in_check(move, piece):
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)



                        elif self.squares[possible_row][possible_col].has_rival_piece(piece.color):
                            move = Move(start_sq, end_sq, "eat")
                            if bool:
                                if not self.is_in_check(move, piece):
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)
                            break

                        else:
                            break

                    else:
                        break
                    possible_row += move_option[0]
                    possible_col += move_option[1]

        def nothing_between(castle_row, start_col, end_col):
            for pos in range(start_col + 1, end_col):
                if self.squares[castle_row][pos].has_piece() is True:
                    return False
            return True

        if piece.name == 'pawn':
            num_of_steps = 1 if piece.moved is True else 2

            start = row + piece.dir
            end = row + (piece.dir * (1 + num_of_steps))
            for possible_row in range(start, end , piece.dir):
                if Square.is_in_boundaries(possible_row):
                    if self.squares[possible_row][col].is_empty():
                        end_sq = Square(possible_row, col)
                        move = Move(start_sq, end_sq, "move")
                        if bool is True:
                            if not self.is_in_check(move, piece):
                                piece.add_moves(move)

                        else: piece.add_moves(move)

                    else: break
                else: break

            possible_row = piece.dir +row
            possible_cols =[col+1, col-1]
            for moves in possible_cols:
                if Square.is_in_boundaries(possible_row, moves):
                    if self.squares[possible_row][moves].has_rival_piece(piece.color):
                        final_piece = self.squares[possible_row][moves].piece
                        end_sq = Square(possible_row, moves, final_piece)
                        move = Move(start_sq, end_sq, "eat")
                        if bool:
                            if not self.is_in_check(move, piece):
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)

        elif piece.name == 'king':
            possible_moves = [(row-1, col), (row+1, col), (row, col-1), (row, col+1), (row-1, col-1),
                              (row-1, col+1), (row+1, col-1), (row+1, col+1)]
            add_valid_moves(possible_moves)

            if piece.moved is False:
                if self.squares[row][0].has_piece() and self.squares[row][0].piece.name == "rook":
                    left_rook = self.squares[row][0].piece
                    if left_rook.moved is False:
                        if nothing_between(row, 0, 4) is True:
                            castling_move = Move(start_sq, Square(row, 2), "left_castle")
                            if bool:
                                if not self.is_in_check(castling_move, piece):
                                    piece.add_moves(castling_move)
                            else:
                                piece.add_moves(castling_move)

                if self.squares[row][7].has_piece() and self.squares[row][7].piece.name == "rook":
                    right_rook = self.squares[row][7].piece
                    if right_rook.moved is False:
                        if nothing_between(row, 4, 7) is True:
                            castling_move = Move(start_sq, Square(row, 6), "right_castle")
                            if bool:
                                if not self.is_in_check(castling_move, piece):
                                    piece.add_moves(castling_move)
                            else:
                                piece.add_moves(castling_move)


        elif piece.name == 'knight':
            possible_moves = [(row-2, col+1), (row-2, col-1), (row-1, col-2), (row-1, col+2), (row+2, col-1),
                              (row+2, col+1), (row+1, col-2), (row+1, col+2)]
            add_valid_moves(possible_moves)

        elif piece.name == 'queen':
            possible_directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1), (1, 1), (1, -1)]
            add_sequence_moves(possible_directions)

        elif piece.name == 'rook':
            possible_directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
            add_sequence_moves(possible_directions)

        elif piece.name == 'bishop':
            possible_directions = [(-1, 1), (-1, -1), (1, 1), (1, -1)]
            add_sequence_moves(possible_directions)

    def check_promotion(self, piece, curr_sq):
        if piece.name == "pawn":
            if curr_sq.row == 0 or curr_sq.row == 7:
                self.squares[curr_sq.row][curr_sq.col].piece = Queen(piece.color)


    def move(self, curr_move, piece):
        end_sq = curr_move.end_square
        start_sq = curr_move.start_square
        if curr_move.kind == "eat":
            self.squares[end_sq.row][end_sq.col].piece = None
        self.squares[start_sq.row][start_sq.col].piece = None
        self.squares[end_sq.row][end_sq.col].piece = piece

        if curr_move.kind == "right_castle" or curr_move.kind == "left_castle":
            self.castling(curr_move)

        self.check_promotion(piece, end_sq)
        piece.moved = True
        self.clear_moves()

    def castling(self, curr_move):
        curr_sq = curr_move.end_square
        right_rook = self.squares[curr_sq.row][7].piece
        left_rook = self.squares[curr_sq.row][0].piece
        if curr_move.kind == "right_castle":
            self.squares[curr_sq.row][7].piece = None
            self.squares[curr_sq.row][5].piece = right_rook
            right_rook.moved = True
        if curr_move.kind == "left_castle":
            self.squares[curr_sq.row][0].piece = None
            self.squares[curr_sq.row][3].piece = left_rook
            left_rook.moved = True


    def print_moves(self, piece):
        for move in piece.moves:
            print(piece.name, piece.color, move.end_square.row, move.end_square.col)

    def clear_moves(self):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                if self.squares[row][col].has_piece():
                    self.squares[row][col].piece.moves = []


    def rival_cant_move(self, curr_player):

        for row in range(DIMENSION):
            for col in range(DIMENSION):
                if self.squares[row][col].has_rival_piece(curr_player):
                    rival_piece = self.squares[row][col].piece
                    self.calc_moves(row, col, rival_piece, True)
                    if rival_piece.moves != []:
                        self.clear_moves()
                        return False
        return True

    def is_king_threated(self, curr_player):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                if self.squares[row][col].has_piece() and self.squares[row][col].piece.color == curr_player:
                    my_piece = self.squares[row][col].piece
                    self.calc_moves(row, col, my_piece, True)
                    for move in my_piece.moves:
                        if isinstance(move.end_square.piece, King):
                            return True
        return False


