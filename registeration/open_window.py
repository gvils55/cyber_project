from tkinter import *
from tkinter.font import Font
import tkinter as tk
from registeration.sign_up import Sign_up
from registeration.login import Login


class Open_window:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("open window")
        self.root.geometry("650x400")

    def main(self):
        huge_font = Font(family="Microsoft YaHei UI Light", size=35, weight="bold")
        big_font = Font(family="Microsoft YaHei UI Light", size=15, weight="bold")

        def sign_up():
            self.root.destroy()
            new_window = Sign_up()
            new_window.main()

        def login():
            self.root.destroy()
            new_window = Login()
            new_window.main()


        frame = Frame(self.root, width=650, height=400, bg="tan").place(x=0, y=0)
        open_label = Label(frame, text="Gvili's site", font=huge_font, bg="tan").place(x=210, y=20)
        greetings_label1 = Label(frame, text="Welcome to my site.", font=big_font, bg="tan").place(x=20, y=110)
        greetings_label2 = Label(frame, text="If you wish to enter, press sign up, but if you are already", font=big_font, bg="tan").place(x=20, y=140)
        greetings_label3 = Label(frame, text="registered, press login.", font=big_font, bg="tan").place(x=20, y=170)
        greetings_label4 = Label(frame, text="Hope tou enjoy.", font=big_font, bg="tan").place(x=20, y=200)

        login = Button(frame, text="login", font=big_font, width=10, height=1, bg="white", command=login).place(x=450, y=320)
        sign_up = Button(frame, text="sign up", font=big_font, width=10, height=1, bg="white", command=sign_up).place(x=300, y=320)

        self.root.mainloop()

if __name__ == '__main__':
    window = Open_window()
    window.main()