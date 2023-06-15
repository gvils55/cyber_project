
class Player:
    def __init__(self, color):
        self.color = color
        if color == "black":
            self.your_turn = False
        else:
            self.your_turn = True
        self.won = False



