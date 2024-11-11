from colorama import Fore, Style, init
import tkinter as tk
from tkinter import messagebox

init()

grid = [
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
]


def print_puzzle(grid):
    string = ""
    for i in range(1, 4):
        for z in range(1, 4):
            for x in range(1, 4):
                for y in range(1, 4):
                    if grid[(i - 1) * 3 + x - 1][y - 1 + (z - 1) * 3] == None:
                        grid[(i - 1) * 3 + x - 1][y - 1 + (z - 1) * 3] = 0
                    string += f" {str(grid[(i-1) * 3 + x - 1][y - 1 + (z-1)*3])}"
                    if grid[(i - 1) * 3 + x - 1][y - 1 + (z - 1) * 3] == 0:
                        grid[(i - 1) * 3 + x - 1][y - 1 + (z - 1) * 3] = None
                if x == 1 or x == 2:
                    string += Fore.GREEN + " |" + Style.RESET_ALL
            if z != 3:
                string += "\n"
            elif i != 3 or z != 3:
                string += Fore.GREEN + "\n - - - - - - - - - - - \n" + Style.RESET_ALL

    print(string)


def on_cell_click(event, row, col, entry_widgets):
    value = entry_widgets[row][col].get()
    value = value.strip()
    if value and value.isdigit():
        num = int(value)
        if 1 <= num <= 9:
            grid[int(row / 3) * 3 + int(col / 3)][(row % 3) * 3 + col % 3] = num
            entry_widgets[row][col].delete(0, tk.END)
            entry_widgets[row][col].insert(0, str(num))
        elif num == 0:
            grid[int(row / 3) * 3 + int(col / 3)][(row % 3) * 3 + col % 3] = num
            entry_widgets[row][col].delete(0, tk.END)
            entry_widgets[row][col].insert(0, str(num))
        else:
            messagebox.showerror(
                "Invalid input", "Please enter a number between 1 and 9."
            )


def update_grid_from_gui(entry_widgets):
    error = False
    for row in range(9):
        for col in range(9):
            num = entry_widgets[row][col].get()
            num = num.strip()
            if num.isdigit():
                num = int(num)
                if 1 <= num <= 9:
                    grid[int(row / 3) * 3 + int(col / 3)][(row % 3) * 3 + col % 3] = num
                    entry_widgets[row][col].delete(0, tk.END)
                    entry_widgets[row][col].insert(0, str(num))
                elif num == 0:
                    grid[int(row / 3) * 3 + int(col / 3)][(row % 3) * 3 + col % 3] = num
                    entry_widgets[row][col].delete(0, tk.END)
                    entry_widgets[row][col].insert(0, str(num))

    if error:
        messagebox.showerror(
            "Invalid input", "Please make sure all inputs are numbers 1-9"
        )
        return False
    return True


def create_sudoku_window():
    window = tk.Tk()
    window.title("Interactive Sudoku")

    cell_size = 50
    grid_spacing = 10
    line_width = 2

    canvas_size = cell_size * 9 + grid_spacing * 2
    canvas = tk.Canvas(window, width=canvas_size, height=canvas_size)
    canvas.grid(row=0, column=0, padx=10, pady=10)

    for i in range(1, 3):
        canvas.create_line(
            i * 3 * cell_size + i * grid_spacing,
            0,
            i * 3 * cell_size + i * grid_spacing,
            canvas_size,
            width=line_width,
            fill="black",
        )
        canvas.create_line(
            0,
            i * 3 * cell_size + i * grid_spacing,
            canvas_size,
            i * 3 * cell_size + i * grid_spacing,
            width=line_width,
            fill="black",
        )

    entry_widgets = [[None for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            x_pos = j * cell_size + (j // 3) * grid_spacing
            y_pos = i * cell_size + (i // 3) * grid_spacing
            entry = tk.Entry(window, width=2, font=("Arial", 20), justify="center")
            entry.place(x=x_pos + 15, y=y_pos + 15)
            if grid[i][j] is not None:
                entry.insert(0, str(grid[i][j]))
                entry.config(state="readonly")
            entry_widgets[i][j] = entry
            entry.bind(
                "<Button-1>",
                lambda event, row=i, col=j, ew=entry_widgets: on_cell_click(
                    event, row, col, ew
                ),
            )

    def on_solve_button_click():
        if update_grid_from_gui(entry_widgets):
            solve_sudoku()

    solve_button = tk.Button(window, text="Solve", command=on_solve_button_click)
    solve_button.grid(row=1, column=0, pady=10)

    window.mainloop()


def solve_sudoku():
    print_puzzle(grid)

    gridnot = []
    for i in range(1, 10):
        for x in range(1, 10):
            gridnot.append([])

    nonecount = 0
    for i in grid:
        for x in i:
            if x == None:
                nonecount += 1
    loopbreakcount = None

    while nonecount != 0 and nonecount != loopbreakcount:
        loopbreakcount = nonecount
        for i in range(9):
            for x in range(1, 10):
                if grid[i][x - 1] != None:
                    for k in range(1, 10):
                        gridnot[i * 9 + x - 1].append(k)

                for num in grid[i]:
                    if num not in gridnot[i * 9 + x - 1] and num != None:
                        gridnot[i * 9 + x - 1].append(num)

                row = []
                for b in range(3):
                    for y in range(1, 4):
                        row.append(
                            grid[int((i) / 3) * 3 + b][int((x - 1) / 3) * 3 + y - 1]
                        )
                for num in row:
                    if num not in gridnot[i * 9 + x - 1] and num != None:
                        gridnot[i * 9 + x - 1].append(num)

                column = []
                for b in range(3):
                    for y in range(1, 4):
                        column.append(grid[i % 3 + b * 3][(x - 1) % 3 + (y - 1) * 3])
                for num in column:
                    if num not in gridnot[i * 9 + x - 1] and num != None:
                        gridnot[i * 9 + x - 1].append(num)

        for i in range(9):  # fill in 3x3s
            for b in range(1, 10):
                notfound = 0
                pos = None
                for num in range(9):
                    if b not in gridnot[i * 9 : (i + 1) * 9][num]:
                        notfound += 1
                        pos = num

                if notfound == 1:
                    grid[i][pos] = b
                else:
                    notfound = 0

        for i in range(9):  # one possible num
            for b in range(9):
                if len(gridnot[i * 9 + b]) == 8:
                    print(gridnot[i * 9 + b])
                    for num in range(1, 10):
                        if num not in gridnot[i * 9 + b]:
                            grid[i][b] = num
                            break

        for i in range(9):  # fill in columns
            for s in range(9):
                notfound = 0
                pos = [0, 0]
                for num in range(9):
                    for b in range(3):
                        for y in range(3):
                            if (
                                num
                                not in gridnot[(i % 3 + b * 3) * 9 + (s % 3 + y * 3)]
                            ):  # grid[i % 3 + b * 3][(s) % 3 + (y - 1) * 3]:
                                notfound += 1
                                pos = [b, y]
                    if notfound == 1:
                        grid[i % 3 + pos[0] * 3][s % 3 + pos[1] * 3] = num

                    notfound = 0
                    pos = [0, 0]

        for i in range(9):  # fill in rows
            for s in range(9):
                notfound = 0
                pos = [0, 0]
                for num in range(9):
                    for b in range(3):
                        for y in range(3):
                            if (
                                num
                                not in gridnot[
                                    (int(i / 3) * 3 + b) * 9 + (int(s / 3) * 3 + y)
                                ]
                            ):  # grid[int((i) / 3) * 3 + b][int((x - 1) / 3) * 3 + y - 1]
                                notfound += 1
                                pos = [b, y]
                    if notfound == 1:
                        if (
                            grid[int(i / 3) * 3 + pos[0]][(int(s / 3) * 3 + pos[1])]
                            == None
                        ):
                            grid[int(i / 3) * 3 + pos[0]][
                                (int(s / 3) * 3 + pos[1])
                            ] = num

                    notfound = 0
                    pos = [0, 0]

        nonecount = 0
        for i in grid:
            for x in i:
                if x == None:
                    nonecount += 1

        if nonecount == loopbreakcount:
            print(
                "\n\nWhoa, this is wayyyy too complex for my simple algorithms! Check out the advanced section of https://sudoku.com/sudoku-rules/ (I've already tried the easier steps!)\nHere is how far I got:"
            )
            print_puzzle(grid)
            exit()
    print("Solved!\n")
    print_puzzle(grid)


create_sudoku_window()
