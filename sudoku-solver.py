import tkinter as tk
from tkinter import messagebox


class SolveTable:
    def __init__(self):
        self.solve_sudoku()

    @staticmethod
    def find_empty_cell():
        for i in range(9):
            for j in range(9):
                if table[i][j].get() == '':
                    return i, j
        return -1

    @staticmethod
    def is_valid(row, col, n):
        for i in range(9):
            if table[i][col].get() == str(n):
                return -1
        for j in range(9):
            if table[row][j].get() == str(n):
                return -1
        row -= row % 3
        col -= col % 3

        for i in range(3):
            for j in range(3):
                if table[row + i][col + j].get() == str(n):
                    return -1

        return 1

    def solve_sudoku(self):
        x, y = -1, -1
        if self.find_empty_cell() == -1:
            return 1
        else:
            x, y = self.find_empty_cell()

        for val in range(1, 10):
            if self.is_valid(x, y, val) == 1:
                table[x][y].set(str(val))
                if self.solve_sudoku():
                    return 1
                table[x][y].set('')
        return 0


class GridCell(tk.Entry):

    def __init__(self, parent, bg, x, y, width=8, bd=3, relief='raised'):
        tk.Entry.__init__(self)
        self.parent = parent
        self.bg = bg
        self.x = x
        self.y = y
        self.entry = tk.Entry(parent, width=width, bd=bd, relief=relief, bg=bg,
                              textvariable=table[x][y],font=("Times New Roman", 12, "bold"))
        self.entry.grid(row=x, column=y)
        self.entry.bind('<FocusOut>',self.bind_func)

    def bind_func(self, event):
        a = self.entry.get()
        color = self.bg
        if a == '':
            return
        a = a[0]
        self.entry.delete(0,'end')
        if a.isdigit() and  a!='0' and SolveTable.is_valid(self.x,self.y,a) == 1:
            table[self.x][self.y].set(a)
        else:
            self.entry.configure(bg='red')
            messagebox.showerror('Invalid Entry!', 'Entry Violates Sudoku Rules, Hence Deleted')
            self.entry.configure(bg=color)


class CreateGrid(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.board = [[0]*9]*9
        self.place_buttons()
        self.resizable(0, 0)

    def place_grid_cells(self):
        for i in range(9):
            for j in range(9):
                if ((j < 3 or j > 5) and (i < 3 or i > 5)) or (j in [3, 4, 5] and i in [3, 4, 5]):
                    color = 'grey'
                else:
                    color = 'white'

                self.board[i][j] = GridCell(self, color, i, j)

    def place_buttons(self):
        btn1 = tk.Button(self,text='Solve ',width=6 ,command=self.solve_sudoku)
        btn1.grid(row=9, column=0)
        btn2 = tk.Button(self,text='Reset',width=6,command=self.reset_board)
        btn2.grid(row=9, column=1)

    @staticmethod
    def solve_sudoku():
        SolveTable()

    @staticmethod
    def reset_board():
        for i in range(9):
            for j in range(9):
                table[i][j].set('')


root = CreateGrid()
table = []
for _ in range(9):
    table.append([tk.StringVar(root), tk.StringVar(root), tk.StringVar(root), tk.StringVar(root), tk.StringVar(root),
                  tk.StringVar(root), tk.StringVar(root), tk.StringVar(root), tk.StringVar(root)])
root.place_grid_cells()
tk.mainloop()
