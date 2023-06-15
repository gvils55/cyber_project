
class Player:
    def __init__(self, mark):
        self.mark = mark
        if mark == "o":
            self.your_turn = False
        else:
            self.your_turn = True
        self.won = False