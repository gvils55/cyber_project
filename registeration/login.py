from tkinter import *
from tkinter.font import Font
import tkinter as tk
import sqlite3
from lobby import Lobby

class Login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("login")
        self.root.geometry("650x400")

    def main(self):

        huge_font = Font(family="Microsoft YaHei UI Light", size=35, weight="bold")
        big_font = Font(family="Microsoft YaHei UI Light", size=18, weight="bold")
        medium_font = Font(family="Microsoft YaHei UI Light", size=13)

        conn = sqlite3.connect('users_list.db')
        c = conn.cursor()

        def submit():
            can_register, msg = is_everything_correct()
            is_registered = False
            name= name_entry.get()
            if can_register is True:
                conn = sqlite3.connect('users_list.db')
                c = conn.cursor()

                c.execute("SELECT *, oid FROM clients")
                records = c.fetchall()
                for record in records:
                    if record[0] == name_entry.get() and record[3] == password_entry.get():
                        is_registered = True
                        break
                conn.commit()
                conn.close()

                if is_registered is True:
                    self.root.destroy()
                    game_lobby = Lobby(name)
                    game_lobby.main()

                else:
                    print("this username or password is not in our database")

            else:
                print(msg)

        def is_everything_correct():
            can_submit = True
            msg =""
            if name_entry.get() == "":
                msg += "you didn't write a username" + "\n"
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
        sign_up = Label(frame, text="login", font=huge_font, bg="tan").place(x=260, y=20)
        button = Button(frame, text="login", font=big_font, width=8, height=1, bg="white", command=submit).place(x=250, y=320)
        back = Button(frame, text="back", font=big_font, width=4, height=1, bg="white", command=back_to_start).place(x=570, y=345)




        name_label = Label(frame, text="username", font=big_font, bg="tan").place(x=30, y=150)
        name_entry = Entry(frame, width=30, borderwidth=5, font=medium_font)
        name_entry.place(x=200, y=150)

        password_label = Label(frame, text="password", font=big_font, bg="tan").place(x=30, y=220)
        password_entry = Entry(frame, width=30, borderwidth=5, font=medium_font)
        password_entry.place(x=200, y=220)


        conn.commit()
        conn.close()


        self.root.mainloop()

