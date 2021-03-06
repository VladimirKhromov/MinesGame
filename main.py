import tkinter as tk
from tkinter.messagebox import showinfo, showerror
from random import shuffle

colors_lst = ['blue', 'green', 'red', '#130091', '#5e0000', '#005e40', '#1a0000', '#07001a']
colors = {i + 1: colors_lst[i] for i in range(len(colors_lst))}


class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, height=5, width=10, font="Calibri 12 bold", *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return f"But {self.x}-{self.y}:{self.number} {self.is_mine} "


class MineSweeper:
    window = tk.Tk()
    window.title("MineSweeper")
    game_place = tk.Frame(window)
    game_place.place(relwidth=1, relheight=0.8)
    info_place = tk.Frame(window)
    info_place.place(rely=0.8, relwidth=1, relheight=0.2)
    ROW = 19
    COLUMNS = 15
    MINES = 20
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttons = []
        for i in range(self.ROW + 2):
            temp = []
            for j in range(self.COLUMNS + 2):
                btn = MyButton(self.game_place, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind("<Button-3>", self.right_click)
                temp.append(btn)
            self.buttons.append(temp)
        self.geometry(self.ROW, self.COLUMNS)
        self.mines_count = self.MINES
        self.info_widgets()

    def geometry(self, row, column):
        width = 200 if column < 6 else column * 25
        height = 220 if row < 6 else row * 25
        return self.window.geometry(f'{width}x{height}')

    def right_click(self, event):
        if self.IS_GAME_OVER or self.IS_FIRST_CLICK:
            return None

        cur_btn = event.widget
        if cur_btn['state'] == "normal":
            cur_btn['state'] = "disabled"
            cur_btn['disabledforeground'] = 'black'
            cur_btn["text"] = "????"
            self.mines_count -= 1
            self.info_widgets()
        elif cur_btn["text"] == "????":
            cur_btn['state'] = "normal"
            cur_btn["text"] = ""
            self.mines_count += 1
            self.info_widgets()

    def click(self, clicked_button: MyButton):

        if self.IS_GAME_OVER:
            return None

        if self.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            # self.print_buttons()
            self.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            clicked_button.is_open = True
            self.IS_GAME_OVER = True
            for i in range(1, self.ROW + 1):
                for j in range(1, self.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
            showinfo("Game Over", '???? ??????????????????!')
            self.info_widgets(True)
        else:
            color = colors.get(clicked_button.count_bomb)

            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disable')
        clicked_button.config(relief=tk.SUNKEN)

        _count = 0
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_open:
                    _count += 1

        if _count == self.COLUMNS * self.ROW - self.MINES and not self.IS_GAME_OVER:
            for i in range(1, self.ROW + 1):
                for j in range(1, self.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '????'
            showinfo("WIN!", '???? ????????????????!\n?????? ?????????????????? ????????????!')
            self.IS_GAME_OVER = True

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:

            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disable')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and next_btn not in queue and 1 <= next_btn.x <= self.ROW and \
                                1 <= next_btn.y <= self.COLUMNS:
                            queue.append(next_btn)

    def reload(self):
        [child.destroy() for child in self.game_place.winfo_children()]
        [child.destroy() for child in self.info_place.winfo_children()]
        self.__init__()
        self.create_widgets()
        self.IS_FIRST_CLICK = True
        self.IS_GAME_OVER = False

    def create_settings_window(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title("??????????????????")
        # 1
        tk.Label(win_settings, text="???????????????????? ??????????").grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, self.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        # 2
        tk.Label(win_settings, text="???????????????????? ??????????????").grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, self.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        # 3
        tk.Label(win_settings, text="???????????????????? ??????").grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, self.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        # save button
        save_btn = tk.Button(win_settings, text="??????????????????",
                             command=lambda: self.change_settings(row_entry, column_entry, mines_entry))

        save_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def change_settings(self, row, column, mines):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror("????????????", '???????????? ???????????????? ????????????????!')
        self.ROW = int(row.get())
        self.COLUMNS = int(column.get())
        self.MINES = int(mines.get())
        self.reload()

    def create_widgets(self):

        # menu
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="????????????", command=self.reload)
        settings_menu.add_command(label="??????????????????", command=self.create_settings_window)
        settings_menu.add_command(label="??????????", command=self.window.destroy)
        menubar.add_cascade(label='????????', menu=settings_menu)

        # game_place

        count = 1
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick="NWSE")
                count += 1

        for i in range(1, self.ROW + 1):
            tk.Grid.rowconfigure(self.game_place, i, weight=1)
        for i in range(1, self.COLUMNS + 1):
            tk.Grid.columnconfigure(self.game_place, i, weight=1)

    def info_widgets(self, game_over=False):
        if game_over:
            btn = tk.Button(self.info_place, text="????????????!", font=15, command=self.reload)
            btn.pack(expand=1)
        else:
            mine_info = tk.Label(self.info_place, text=f"????????: {self.mines_count}", font=15)
            mine_info.place(relx=0.45, rely=0.1)

    def start(self):
        self.create_widgets()
        self.window.mainloop()

    def print_buttons(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print("B", end="")
                else:
                    print(btn.count_bomb, end='')
            print()

    def get_mines_plases(self, exclide_nember: int):
        indexes = list(range(1, self.ROW * self.COLUMNS + 1))
        indexes.remove(exclide_nember)
        shuffle(indexes)
        return indexes[:self.MINES]

    def insert_mines(self, nember: int):
        index_mines = self.get_mines_plases(nember)
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mines_in_buttons(self):
        for i in range(1, self.ROW + 1):
            for j in range(1, self.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb


game = MineSweeper()
game.start()
