import pygame as p
from tic_tac_toe.board import Board
from tic_tac_toe.constant import *

class Game:

    def __init__(self):
        self.curr_player = 'x'
        self.board = Board()
        self.ready_to_start = False
        self.game_over = False
        self.tie = False
        self.winner = ""
        self.disconnected = False

    def next_turn(self):
        if self.curr_player == 'x':
            self.curr_player = 'o'
        else:
            self.curr_player = 'x'

    def draw_board(self, screen, player):
        line_width = 6
        screen.fill(p.Color("tan1"))
        dark_color = p.Color("sienna4")
        for x in range(1,4):
            p.draw.line(screen, dark_color, (0, x*150), (WIDTH, x*150), line_width)
            p.draw.line(screen, dark_color, (x*150, 0), (x*150, 450), line_width)

        font = p.font.SysFont("freesansbold.ttf", 40, bold=False)
        label = font.render(("your'e    " + player.mark), 1, p.Color("red"))
        label_pos = (10, 480)
        screen.blit(label, label_pos)

        if self.game_over is False:
            if player.your_turn is True:
                label2 = font.render(("your turn"), 1, p.Color("red"))
            else:
                label2 = font.render(("his turn"), 1, p.Color("red"))
            label_pos2 = (180, 550)
            screen.blit(label2, label_pos2)

        else:
            if self.tie is True:
                label3 = font.render("stalemate, a draw!!", 1, p.Color("red"))
            elif player.mark == self.winner:
                label3 = font.render("checkmate!!, you won ", 1, p.Color("red"))
            else:
                label3 = font.render("checkmate!!, you lost ", 1, p.Color("red"))
            label_pos3 = (140, 540)
            screen.blit(label3, label_pos3)



    def draw_pieces(self, screen):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                if self.board.squares[row][col] == 'o':
                    p.draw.circle(screen, p.Color("white"),
                                  ((col + 0.5) * SQ_SIZE, (row + 0.5) * SQ_SIZE),
                                  OPENED_CIRCLE_RADIUS, OPENED_CIRCLE_WIDTH)
                elif self.board.squares[row][col] == 'x':
                    p.draw.line(screen, p.Color("black"), ((col + 0.2)*SQ_SIZE, (row + 0.2)*SQ_SIZE),
                                ((col + 0.8)*SQ_SIZE, (row + 0.8)*SQ_SIZE), 6)

                    p.draw.line(screen, p.Color("black"), ((col + 0.8) * SQ_SIZE, (row + 0.2) * SQ_SIZE),
                                ((col + 0.2) * SQ_SIZE, (row + 0.8) * SQ_SIZE), 6)


    def is_game_over(self):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                if self.board.squares[row][col] == ' ':
                    return False
        return True

    def player_has_won(self, curr_player):
        if self.board.three_row(curr_player) is True:
            return True
        elif self.board.three_col(curr_player) is True:
            return True
        elif self.board.three_diagnoal(curr_player) is True:
            return True
        return False

