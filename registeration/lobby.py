from tkinter import *
from tkinter.font import Font
import tkinter as tk
from PIL import ImageTk, Image
import sqlite3

from checkers import client as checkers_client
from chess import client as chess_client
from tic_tac_toe import client as tic_tac_toe_client
from connect_four import client as connect_four_client


class Lobby:

    def __init__(self, username, score):
        self.root = tk.Tk()
        self.username = username
        self.score = score
        self.root.title("hi " + self.username + "                     " + str(self.score))
        self.root.geometry("650x400")


    def main(self):
        huge_font = Font(family="Microsoft YaHei UI Light", size=35, weight="bold")
        mid_font = Font(family="Microsoft YaHei UI Light", size=10, weight="bold")
        frame = Frame(self.root, width=650, height=400, bg="tan").place(x=0, y=0)
        open_label = Label(frame, text="game lobby", font=huge_font, bg="tan").place(x=200, y=20)

        chess_label = Label(frame, text="chess", font=mid_font, bg="tan").place(x=170, y=205)
        checkers_label = Label(frame, text="checkers", font=mid_font, bg="tan").place(x=160, y=345)
        tic_tac_toe_label = Label(frame, text="tic tac toe", font=mid_font, bg="tan").place(x=400, y=205)
        connect_four_label = Label(frame, text="connect four", font=mid_font, bg="tan").place(x=400, y=345)




        def enter_checkers():

            # from checkers import client
            self.root.destroy()
            new_user = checkers_client.Client(self.username)
            new_user.main()


        def enter_chess():

            # from chess import client
            self.root.destroy()
            new_user = chess_client.Client(self.username)
            new_user.main()

        def enter_tic_tac_toe():

            # from tic tac toe import client
            self.root.destroy()
            new_user = tic_tac_toe_client.Client(self.username)
            new_user.main()

        def enter_connect_four():

            # from connect four import client
            self.root.destroy()
            new_user = connect_four_client.Client(self.username)
            new_user.main()


        chess_image = Image.open('C:/Users/Owner/PycharmProjects/newExpo/images/icons/chess.png')
        resized = chess_image.resize((75, 75), Image.ANTIALIAS)
        new_chess = ImageTk.PhotoImage(resized)
        chess_btn = Button(frame, image=new_chess, command=enter_chess, background="tan")
        chess_btn.place(x=150, y=120)


        checkers_image = Image.open('C:/Users/Owner/PycharmProjects/newExpo/images/icons/checkers.png')
        resized = checkers_image.resize((75, 75), Image.ANTIALIAS)
        new_checkers = ImageTk.PhotoImage(resized)
        checkers_btn = Button(frame, image=new_checkers, command=enter_checkers, background="tan")
        checkers_btn.place(x=150, y=260)
        tic_tac_toe_image = Image.open('C:/Users/Owner/PycharmProjects/newExpo/images/icons/tic-tac-toe.png')
        resized = tic_tac_toe_image.resize((75, 75), Image.ANTIALIAS)
        new_tic_tac_toe = ImageTk.PhotoImage(resized)
        tic_tac_toe_btn = Button(frame, image=new_tic_tac_toe, command=enter_tic_tac_toe, background="tan")
        tic_tac_toe_btn.place(x=400, y=120)
        connect_four_image = Image.open('C:/Users/Owner/PycharmProjects/newExpo/images/icons/four_row.png')
        resized = connect_four_image.resize((75, 75), Image.ANTIALIAS)
        new_connect_four = ImageTk.PhotoImage(resized)
        connect_four_btn = Button(frame, image=new_connect_four, command=enter_connect_four, background="tan")
        connect_four_btn.place(x=400, y=260)
        self.root.mainloop()

        self.not_online()

    def not_online(self):
        conn = sqlite3.connect('users_list.db')
        c = conn.cursor()
        c.execute("UPDATE users SET is_online = 0 WHERE username = ?", (self.username,))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    lobby = Lobby()
    lobby.main()