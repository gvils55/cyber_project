class Square:


    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece


    def has_piece(self):
        return self.piece is not None

    def is_empty(self):
        return self.piece is None

    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color


    @staticmethod
    def is_in_boundaries(*args):
        for args in args:
            if args < 0 or args > 7:
                return False
        return True

    @staticmethod
    def get_col_letter(col):
        COLS_IN_LETTERS ={0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        return COLS_IN_LETTERS[col]
