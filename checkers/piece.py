import os

class Piece:

    def __init__(self, name, color, shape=None, shape_rect=None):
        self.name = name
        self.color = color
        self.shape = shape
        self.set_shape()
        self.shape_rect = shape_rect
        self.moves = []
        self.moved = False

    def set_shape(self):
        self.shape = os.path.join(f'C:/Users/Owner/PycharmProjects/newExpo/images/checkers_pieces/{self.color}_{self.name}.png')

    def add_moves(self, move):
        self.moves.append(move)

    def remove_moves(self, move):
        new_moves = []
        for m in self.moves:
            if m != move:
                new_moves.append(m)

        self.moves = new_moves
        for m in self.moves:
            print(m.end_square.row, m.end_square.col)


    def is_valid_move(self, sq):
        for move in self.moves:
            valid_square = move.end_square
            if valid_square.row == sq[0] and valid_square.col == sq[1]:
                return True
        return False

    def get_move(self, sq):
        for move in self.moves:
            valid_square = move.end_square
            if valid_square.row == sq[0] and valid_square.col == sq[1]:
                return move
        return None


class Pawn(Piece):
    def __init__(self, color):
        super().__init__('pawn', color)



class King(Piece):
    def __init__(self, color):
        super().__init__('king', color)