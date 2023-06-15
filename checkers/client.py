import time

import pygame as p
from checkers.Constant import *
from checkers.square import Square
from checkers.network import Network
import sqlite3

class Client:

    def __init__(self, username):
        p.init()
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        self.username = username
        p.display.set_caption(self.username + "'s checkers")



    def draw_lobby(self):
        self.screen.fill(p.Color("tan1"))
        font = p.font.SysFont("freesansbold.ttf", 55, bold=False)

        label = font.render(("waiting for player to connect ..."), 1, p.Color("red"))
        label_pos = (590 - label.get_width(), 300 - label.get_height())
        self.screen.blit(label, label_pos)


    def main(self):
        n = Network()
        player = n.get_player()
        user = (player, self.username)
        piece_was_picked = False
        run = True
        while run:
            try:
                time.sleep(0.15)
                game1 = n.send((user, "get"))
            except Exception as e:
                print(e)
                print("couldn't find game")
                break

            game = game1
            if game.ready_to_start is False:
                self.draw_lobby()
            else:
                game.draw_board(self.screen, player)
                if piece_was_picked:
                    game.show_moves(self.screen, selected_piece, row, col)
                game.draw_pieces(self.screen)

            for e in p.event.get():
                if e.type == p.QUIT:
                    run = False
                    p.QUIT
                    n.send((user, "quit"))


                board = game.board
                if game.game_over is False:
                    if game.ready_to_start is True:
                        if player.color == game.curr_player:
                            player.your_turn = True
                        else:
                            player.your_turn = False

                        if e.type == p.MOUSEBUTTONDOWN and player.your_turn is True:
                            clicked_pos = p.mouse.get_pos()
                            row = int(clicked_pos[1] // SQ_SIZE)
                            col = int(clicked_pos[0] // SQ_SIZE)
                            curr_sq = (row, col)

                            if Square.is_in_boundaries(row, col):
                                if board.squares[row][col].has_piece() and board.squares[row][col].piece.color == player.color:
                                    selected_piece = board.squares[row][col].piece
                                    piece_was_picked = True
                                    board.calc_moves(row, col, selected_piece)

                                elif piece_was_picked is True and selected_piece.is_valid_move(curr_sq):
                                    curr_move = selected_piece.get_move(curr_sq)
                                    data = (curr_move, selected_piece)
                                    n.send((user, data))
                                    game.play_sound(curr_move)
                                    if game.game_over is False:
                                        n.send((user, "next turn"))
                                        piece_was_picked = False

                                elif piece_was_picked is True and board.squares[row][col].has_piece() is False:
                                    piece_was_picked = False

                                elif board.squares[row][col].has_piece() and board.squares[row][col].piece.color != game.curr_player:
                                    piece_was_picked = False

            p.display.update()

        p.quit()
        from registeration import lobby
        conn = sqlite3.connect('users_list.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (self.username,))
        record = c.fetchone()
        conn.commit()
        conn.close()
        new_lobby = lobby.Lobby(self.username, record[4])
        new_lobby.main()
