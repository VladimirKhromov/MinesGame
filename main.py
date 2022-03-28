import tkinter as tk
from random import shuffle


class MyButton(tk.Button):

    def __init__(self, master, x, y, *args, number, **kwargs):
        super(MyButton, self).__init__(master, width=3, font="Calibri 15 bold", *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False

    def __repr__(self):
        return f"But {self.x}-{self.y}:{self.number} {self.is_mine} "


class MineSweeper:
    window = tk.Tk()
    ROW = 10
    COLUMNS = 7
    MINES = 15

    def __init__(self):
        self.buttons = []
        count = 1
        for i in range(self.ROW):
            temp = []
            for j in range(self.COLUMNS):
                btn = MyButton(self.window, x=i, y=j, number=count)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
                count += 1
            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
        else:
            clicked_button.config(text=clicked_button.number, disabledforeground='black')
        clicked_button.config(state='disable')

    def create_widgets(self):
        for i in range(self.ROW):
            for j in range(self.COLUMNS):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def start(self):
        self.create_widgets()
        self.insert_mines()
        self.print_buttons()

        self.window.mainloop()

    def print_buttons(self):
        for row_btn in self.buttons:
            print(row_btn)

    def insert_mines(self):
        index_mines = self.get_mines_plases()
        for row_btn in self.buttons:
            for btn in row_btn:
                if btn.number in index_mines:
                    btn.is_mine = True

    def get_mines_plases(self):
        indexes = list(range(1, self.ROW * self.COLUMNS + 1))
        shuffle(indexes)
        return indexes[:self.MINES]


game = MineSweeper()
game.start()
