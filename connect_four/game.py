import pygame as p
from connect_four.board import Board
from connect_four.constant import *

class Game:

    def __init__(self):
        self.curr_player = 'white'
        self.board = Board()
        self.ready_to_start = False
        self.game_over = False
        self.tie = False
        self.winner = ""
        self.disconnected = False

    def next_turn(self):
        if self.curr_player == 'white':
            self.curr_player = 'black'
        else:
            self.curr_player = 'white'

    def draw_board(self, screen, player):
        screen.fill(p.Color("tan2"))
        img = p.image.load(self.board.img)
        img_center = (0, 0)
        screen.blit(img, img_center)

        font = p.font.SysFont("freesansbold.ttf", 40, bold=False)
        label = font.render(("your'e  " + player.color), 1, p.Color("red"))
        label_pos = (10, 610)
        screen.blit(label, label_pos)

        for col in range(COL):
            button = p.Rect((85 * col) + 8, 530, 70, 60)
            p.draw.rect(screen, (p.Color("red")), button)
            label4 = font.render(("click"), 1, p.Color("black"))
            label_pos4 = ((85*col)+ 9, 540)
            screen.blit(label4, label_pos4)



        if self.game_over is False:
            if player.your_turn is True:
                label2 = font.render(("your turn"), 1, p.Color("red"))
            else:
                label2 = font.render(("his turn"), 1, p.Color("red"))
            label_pos2 = (225, 690)
            screen.blit(label2, label_pos2)

        else:
            if self.tie is True:
                label3 = font.render("stalemate, a draw!!", 1, p.Color("red"))
            elif player.color == self.winner:
                label3 = font.render("checkmate!!, you won ", 1, p.Color("red"))
            else:
                label3 = font.render("checkmate!!, you lost ", 1, p.Color("red"))
            label_pos3 = (140, 650)
            screen.blit(label3, label_pos3)



    def draw_pieces(self, screen):
        for row in range(ROW):
            for col in range(COL):
                if self.board.squares[row][col] == 'white':
                    p.draw.circle(screen, p.Color("white"),
                                  ((col + 0.51) * SQ_SIZE, (row + 0.5) * SQ_SIZE),
                                  OPENED_CIRCLE_RADIUS)
                elif self.board.squares[row][col] == 'black':
                    p.draw.circle(screen, p.Color("black"),
                                  ((col + 0.51) * SQ_SIZE, (row + 0.51) * SQ_SIZE),
                                  OPENED_CIRCLE_RADIUS)


    def is_game_over(self):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                if self.board.squares[row][col] == ' ':
                    return False
        return True


    def player_has_won(self, curr_player):
        if self.board.row_sequence(curr_player) is True:
            return True
        elif self.board.col_sequence(curr_player) is True:
            return True
        elif self.board.diagnoal_sequence(curr_player) is True:
            return True
        return False