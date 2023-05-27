import socket
from _thread import *
import pickle
import sys
from registeration.constant import *

from checkers import game as checkers_game
from chess import game as chess_game
from tic_tac_toe import game as tic_tac_toe_game
from connect_four import game as connect_four_game

from chess import player as player1
from tic_tac_toe import player as player2




class Server:

    def __init__(self):
        server = SERVER
        port = PORT_NUM
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.bind((server, port))
        except socket.error as e:
            str(e)

        self.s.listen()
        print("game server started")
        print("waiting for connection")
        self.players = [player1.Player("white"), player1.Player("black")]
        self.players2 = [player2.Player("x"), player2.Player("o")]
        self.tic_tac_toe_idCount = 0
        self.tic_tac_toe_games = {}
        self.chess_idCount = 0
        self.chess_games = {}
        self.checkers_idCount = 0
        self.checkers_games = {}
        self.connect_four_idCount = 0
        self.connect_four_games = {}
        self.connected = set()

    def threaded_chess_client(self, client, p, gameId):
        client.send(pickle.dumps(self.players[p]))
        reply = ""
        while True:
            try:
                data = pickle.loads(client.recv(4096 * 2))
                if gameId in self.chess_games:
                    game = self.chess_games[gameId]
                    if not data:
                        print("disconnected")
                        break
                    else:
                        if data == "next turn":
                            game.next_turn()
                        elif data == "quit":
                            game.disconnected = True
                        elif data != "get":
                            piece = data[0]
                            move = data[1]
                            game.board.move(piece, move)
                            if game.board.rival_cant_move(game.curr_player):
                                if game.board.is_king_threated(game.curr_player):
                                    game.winner = game.curr_player
                                else:
                                    game.tie = True
                                game.game_over = True

                        reply = game
                        client.sendall(pickle.dumps(reply))
                        if game.disconnected is True:
                            break
                else:
                    break
            except:
                print("entered the except")
                break
        print("lost connection")
        try:
            del self.chess_games[gameId]
            print("closing game ")
        except:
            pass
        self.chess_idCount -= 1
        client.close()


    def threaded_checkers_client(self, client, p, gameId):
        client.send(pickle.dumps(self.players[p]))
        reply = ""
        while True:
            try:
                data = pickle.loads(client.recv(4096*2))
                if gameId in self.checkers_games:
                    game = self.checkers_games[gameId]
                    if not data:
                        print("disconnected")
                        break
                    else:
                        if data == "next turn":
                            game.next_turn()
                        elif data == "quit":
                            game.disconnected = True
                        elif data != "get":
                            piece = data[0]
                            move = data[1]
                            game.board.move(piece, move)
                            print("moved")
                            if game.board.is_game_over(game.curr_player):
                                game.winner = game.curr_player
                                game.game_over = True

                        reply = game
                        client.sendall(pickle.dumps(reply))
                        if game.disconnected is True:
                            break
                else:
                    break
            except Exception as e:
                print("entered the except")
                break
        print("lost connection")
        try:
            del self.checkers_games[gameId]
            print("closing game ")
        except:
            pass
        self.checkers_idCount -=1
        client.close()

    def threaded_tic_tac_toe_client(self, client, p, gameId):
        client.send(pickle.dumps(self.players2[p]))
        reply = ""
        while True:
            try:
                data = pickle.loads(client.recv(4096 * 2))

                if gameId in self.tic_tac_toe_games:
                    game = self.tic_tac_toe_games[gameId]
                    if not data:
                        print("disconnected")
                        break
                    else:
                        if data == "next turn":
                            game.next_turn()
                        elif data == "quit":
                            game.disconnected = True
                        elif data != "get":
                            move = data
                            game.board.move(move, game.curr_player)
                            if game.player_has_won(game.curr_player) is True:
                                game.game_over = True
                                game.winner = game.curr_player

                            elif game.is_game_over() is True:
                                game.game_over = True
                                game.tie = True

                        reply = game
                        client.sendall(pickle.dumps(reply))
                        if game.disconnected is True:
                            break
                else:
                    break
            except Exception as e:
                print("entered the except")
                break
        print("lost connection")
        try:
            del self.tic_tac_toe_games[gameId]
            print("closing game ")
        except:
            pass
        self.tic_tac_toe_idCount -= 1
        client.close()

    def threaded_connect_four_client(self, client, p, gameId):
        client.send(pickle.dumps(self.players[p]))
        reply = ""
        while True:
            try:
                data = pickle.loads(client.recv(4096 * 2))

                if gameId in self.connect_four_games:
                    game = self.connect_four_games[gameId]
                    if not data:
                        print("disconnected")
                        break
                    else:
                        if data == "next turn":
                            game.next_turn()
                        elif data == "quit":
                            game.disconnected = True
                        elif data != "get":
                            move = data
                            game.board.move(move, game.curr_player)
                            if game.player_has_won(game.curr_player) is True:
                                game.game_over = True
                                game.winner = game.curr_player

                            elif game.is_game_over() is True:
                                game.game_over = True
                                game.tie = True

                        reply = game
                        client.sendall(pickle.dumps(reply))
                        if game.disconnected is True:
                            break
                else:
                    break
            except Exception as e:
                print("entered the except")
                break
        print("lost connection")
        try:
            del self.connect_four_games[gameId]
            print("closing game ")
        except:
            pass
        self.connect_four_idCount -= 1
        client.close()

    def main(self):

        while True:
            client, addr = self.s.accept()
            print("connected to: ", addr)

            name = pickle.loads(client.recv(4096 * 2))
            print(name)
            if name == "chess":
                self.chess_idCount += 1
                p = 0
                game_id = (self.chess_idCount - 1) // 2
                if self.chess_idCount % 2 == 1:
                    # new_game = chess_game.Game()
                    new_game = chess_game.Game()
                    self.chess_games[game_id] = new_game
                    print("creating new chess game")
                else:
                    self.chess_games[game_id].ready_to_start = True
                    p = 1
                start_new_thread(self.threaded_chess_client, (client, p, game_id))

            elif name == "checkers":
                # from checkers import game
                self.checkers_idCount += 1
                p = 0
                game_id = (self.checkers_idCount - 1) // 2
                if self.checkers_idCount % 2 == 1:
                    # new_game = checkers_game.Game()
                    new_game = checkers_game.Game()
                    self.checkers_games[game_id] = new_game
                    print("creating new checkers game")
                else:
                    self.checkers_games[game_id].ready_to_start = True
                    p = 1
                start_new_thread(self.threaded_checkers_client, (client, p, game_id))

            elif name == "tic tac toe":
                self.tic_tac_toe_idCount += 1
                p = 0
                game_id = (self.tic_tac_toe_idCount - 1) // 2
                if self.tic_tac_toe_idCount % 2 == 1:
                    new_game = tic_tac_toe_game.Game()
                    self.tic_tac_toe_games[game_id] = new_game
                    print("creating new tic tac toe game")
                else:
                    self.tic_tac_toe_games[game_id].ready_to_start = True
                    p = 1
                start_new_thread(self.threaded_tic_tac_toe_client, (client, p, game_id))

            elif name == "connect four":
                self.connect_four_idCount += 1
                p = 0
                game_id = (self.connect_four_idCount - 1) // 2
                if self.connect_four_idCount % 2 == 1:
                    new_game = connect_four_game.Game()
                    self.connect_four_games[game_id] = new_game
                    print("creating new connect four game")
                else:
                    self.connect_four_games[game_id].ready_to_start = True
                    p = 1
                start_new_thread(self.threaded_connect_four_client, (client, p, game_id))



if __name__ == '__main__':
    server = Server()
    server.main()