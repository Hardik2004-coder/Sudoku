import tkinter as tk
from tkinter import messagebox
import random
import copy

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")

        # Generate a random puzzle
        self.puzzle = self.generate_random_sudoku()
        self.solution = copy.deepcopy(self.puzzle)
        self.solve(self.solution)

        # Create a grid for the Sudoku board
        self.cells = []
        for i in range(9):
            row_cells = []
            for j in range(9):
                cell = tk.Entry(root, width=3, font=("Arial", 16), justify='center')
                cell.grid(row=i, column=j, padx=2, pady=2)
                if self.puzzle[i][j] != 0:
                    cell.insert(0, str(self.puzzle[i][j]))
                    cell.config(state='disabled', disabledforeground='black')
                row_cells.append(cell)
            self.cells.append(row_cells)

        # Add Check Solution and Hint buttons
        self.check_button = tk.Button(root, text="Check Solution", command=self.check_solution)
        self.check_button.grid(row=9, column=3, columnspan=3, pady=5)

        self.hint_button = tk.Button(root, text="Hint", command=self.give_hint)
        self.hint_button.grid(row=10, column=3, columnspan=3, pady=5)

    def generate_random_sudoku(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve(board)
        self.remove_numbers(board, 40)
        return board

    def solve(self, board):
        empty = self.find_empty_cell(board)
        if not empty:
            return True
        row, col = empty
        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if self.is_valid(board, num, row, col):
                board[row][col] = num
                if self.solve(board):
                    return True
                board[row][col] = 0
        return False

    def find_empty_cell(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, board, num, row, col):
        if num in board[row]:
            return False
        if num in [board[i][col] for i in range(9)]:
            return False
        box_x, box_y = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[box_x + i][box_y + j] == num:
                    return False
        return True

    def remove_numbers(self, board, count):
        attempts = count
        while attempts > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            while board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            board[row][col] = 0
            attempts -= 1

    def check_solution(self):
        for i in range(9):
            for j in range(9):
                user_value = self.cells[i][j].get()
                if not user_value.isdigit() or int(user_value) != self.solution[i][j]:
                    messagebox.showerror("Incorrect", "Solution is incorrect. Try again!")
                    return
        messagebox.showinfo("Correct", "Congratulations! You solved the Sudoku!")

    def give_hint(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].get() == "":
                    self.cells[i][j].insert(0, str(self.solution[i][j]))
                    return
        messagebox.showinfo("Hint", "No empty cells left for a hint!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGame(root)
    root.mainloop()
