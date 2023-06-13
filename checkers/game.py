import pygame as p
import pygame.image
import os
from checkers.square import Square
from checkers.Constant import *
from checkers.board import Board


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
        screen.fill(p.Color("black"))
        light_color = p.Color("tan1")
        dark_color = p.Color("sienna4")
        font = p.font.SysFont("monospace", 18, bold=True)
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                rect_color = light_color if (col + row) % 2 == 0 else dark_color
                rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                p.draw.rect(screen, rect_color, rect)
                label_color = dark_color if (col + row) % 2 == 0 else light_color
                if col == 0:
                    label = font.render(str(DIMENSION-row), 1, label_color)
                    label_pos = (5, 5 + row * SQ_SIZE)
                    screen.blit(label, label_pos)

                if row == 7:
                    label = font.render(Square.get_col_letter(col), 1, label_color)
                    label_pos = (col * SQ_SIZE + SQ_SIZE - 15, HEIGHT - 170)
                    screen.blit(label, label_pos)

        font = p.font.SysFont("freesansbold.ttf", 40, bold=False)
        label = font.render(("your " + player.color + " player"), 1, p.Color("red"))
        label_pos = (7, 620)
        screen.blit(label, label_pos)

        if self.game_over is False:
            if player.your_turn is True:
                label2 = font.render(("you're turn"), 1, p.Color("red"))
            else:
                label2 = font.render(("his turn"), 1, p.Color("red"))
            label_pos2 = (235, 700)
            screen.blit(label2, label_pos2)

        else:
            if self.tie is True:
                label3 = font.render("stalemate, a draw!!", 1, p.Color("red"))
            elif player.color == self.winner:
                label3 = font.render("checkmate!!, you won ", 1, p.Color("red"))
            else:
                label3 = font.render("checkmate!!, you lost ", 1, p.Color("red"))
            label_pos3 = (235, 700)
            screen.blit(label3, label_pos3)


    def draw_pieces(self, screen):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                if self.board.squares[row][col].has_piece():
                    my_piece = self.board.squares[row][col].piece
                    img = pygame.image.load(my_piece.shape)
                    img_center = (col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2)
                    my_piece.shape_rect = img.get_rect(center=img_center)
                    screen.blit(img, my_piece.shape_rect)

    def show_moves(self, screen, piece, row, col):
        if Square.is_in_boundaries(row, col):
            rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, CIRCLE_COLOR, rect)
        for move in piece.moves:
            if move.kind[0] != "eat":
                p.draw.circle(screen, CIRCLE_COLOR,
                              ((move.end_square.col + 0.5) * SQ_SIZE, (move.end_square.row + 0.5) * SQ_SIZE),
                              FULL_CIRCLE_RADIUS)
            else:
                p.draw.circle(screen, CIRCLE_COLOR,
                              ((move.end_square.col + 0.5) * SQ_SIZE, (move.end_square.row + 0.5) * SQ_SIZE),
                              OPENED_CIRCLE_RADIUS, OPENED_CIRCLE_WIDTH)

    def play_sound(self, curr_move):
        p.mixer.init()
        if curr_move.kind == "move":
            curr_sound = os.path.join("C:/Users/Owner/PycharmProjects/newExpo/sounds/move-self.mp3")
        else:
            curr_sound = os.path.join("C:/Users/Owner/PycharmProjects/newExpo/sounds/capture.mp3")
        p.mixer.music.load(curr_sound)
        p.mixer.music.play()

