from tkinter import *
from tkinter.font import Font
import tkinter as tk
import sqlite3
from registeration.lobby import Lobby
import sys

class Sign_up:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("sign up")
        self.root.geometry("650x400")


    def main(self):
        huge_font = Font(family="Microsoft YaHei UI Light", size=35, weight="bold")
        big_font = Font(family="Microsoft YaHei UI Light", size=18, weight="bold")
        medium_font = Font(family="Microsoft YaHei UI Light", size=13)

        conn = sqlite3.connect('users_list.db')
        c = conn.cursor()

        #c.execute("""CREATE TABLE users(
        #   username text, phone text, gmail text, password text, score int, is_online int
        #   )""")

        #c.execute("INSERT INTO addresses VALUES('maayan12', 0507766752, 'mgmaayan@gmail.com', 'mosh123')")
        #conn.commit()


        def submit():
            can_register , msg = is_everything_correct()
            if can_register is True:
                conn = sqlite3.connect('users_list.db')
                c = conn.cursor()
                name = name_entry.get()
                if is_name_exist(name) is False:

                    c.execute("INSERT INTO users VALUES(:username, :phone, :gmail, :password, 0, 1)",
                              {
                                  'username': name_entry.get(),
                                  'phone': phone_entry.get(),
                                  'gmail': gmail_entry.get(),
                                  'password': password_entry.get()
                              })

                    conn.commit()
                    conn.close()

                    self.root.destroy()
                    game_lobby = Lobby(name, 0)
                    game_lobby.main()

                else:
                    print("there is a player called by this name")

            else:
                print(msg)

        def is_name_exist(name):
            conn = sqlite3.connect('users_list.db')
            c = conn.cursor()
            c.execute("SELECT *, oid FROM users")
            records = c.fetchall()
            for record in records:
                if record[0] == name:
                    return True
            return False

        def show_users():
            conn = sqlite3.connect('users_list.db')
            c = conn.cursor()
            c.execute("SELECT *, oid FROM users")
            records = c.fetchall()
            print(records)
            conn.commit()
            conn.close()


        def is_everything_correct():
            can_submit = True
            msg =""
            if name_entry.get() == "":
                msg += "you didn't write a username" + "\n"
                can_submit = False

            if phone_entry.get() == "":
                msg += "you didn't write a phone number" + "\n"
                can_submit = False

            if gmail_entry.get() == "":
                msg += "you didn't write a gmail" + "\n"
                can_submit = False

            if password_entry.get() == "":
                msg += "you didn't write a password" + "\n"
                can_submit = False

            return can_submit, msg

        def back_to_start():
            self.root.destroy()
            try:
                from open_window import Open_window
                open_win = Open_window()
                open_win.main()
            except:
                pass

        frame = Frame(self.root, width=650, height=400, bg="tan").place(x=0, y=0)
        sign_up = Label(frame, text="sign up", font=huge_font, bg="tan").place(x=250, y=20)
        register = Button(frame, text="register", font=big_font, width=8, height=1, bg="white", command=submit).place(x=250, y=320)
        back = Button(frame, text="back", font=big_font, width=4, height=1, bg="white", command=back_to_start).place(x=570, y=345)
        show = Button(frame, text="show users", font=big_font, width=8, height=1, bg="white", command=show_users).place(x=250, y=360)



        name_label = Label(frame, text="username", font=big_font, bg="tan").place(x=30, y=100)
        name_entry = Entry(frame, width=30, borderwidth=5, font=medium_font)
        name_entry.place(x=200, y=100)

        phone_label = Label(frame, text="phone", font=big_font, bg="tan").place(x=30, y=150)
        phone_entry = Entry(frame, width=30, borderwidth=5, font=medium_font)
        phone_entry.place(x=200, y=150)

        gmail_label = Label(frame, text="gmail", font=big_font, bg="tan").place(x=30, y=200)
        gmail_entry = Entry(frame, width=30, borderwidth=5, font=medium_font)
        gmail_entry.place(x=200, y=200)

        password_label = Label(frame, text="password", font=big_font, bg="tan").place(x=30, y=250)
        password_entry = Entry(frame, width=30, borderwidth=5, font=medium_font)
        password_entry.place(x=200, y=250)


        conn.commit()
        conn.close()
        self.root.mainloop()
