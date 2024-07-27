import tkinter as tk
from tkinter import messagebox

class Othello:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'O'
        self.board[3][4] = 'X'
        self.board[4][3] = 'X'
        self.board[4][4] = 'O'
        self.current_player = 'X'  # X starts first

    def is_valid_move(self, row, col):
        if row < 0 or row >= 8 or col < 0 or col >= 8 or self.board[row][col] != ' ':
            return False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            if self.is_valid_direction(row, col, d):
                return True
        return False

    def is_valid_direction(self, row, col, direction):
        dr, dc = direction
        r, c = row + dr, col + dc
        if r < 0 or r >= 8 or c < 0 or c >= 8 or self.board[r][c] == ' ' or self.board[r][c] == self.current_player:
            return False
        r += dr
        c += dc
        while r >= 0 and r < 8 and c >= 0 and c < 8:
            if self.board[r][c] == ' ':
                return False
            if self.board[r][c] == self.current_player:
                return True
            r += dr
            c += dc
        return False

    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            return False
        self.board[row][col] = self.current_player
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            if self.is_valid_direction(row, col, d):
                self.flip_direction(row, col, d)
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def flip_direction(self, row, col, direction):
        dr, dc = direction
        r, c = row + dr, col + dc
        cells_to_flip = []
        while r >= 0 and r < 8 and c >= 0 and c < 8 and self.board[r][c] != ' ' and self.board[r][c] != self.current_player:
            cells_to_flip.append((r, c))
            r += dr
            c += dc
        if r >= 0 and r < 8 and c >= 0 and c < 8 and self.board[r][c] == self.current_player:
            for (flip_r, flip_c) in cells_to_flip:
                self.board[flip_r][flip_c] = self.current_player

    def game_over(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == ' ' and self.is_valid_move(i, j):
                    return False
        return True

    def count_pieces(self):
        count_X = sum(row.count('X') for row in self.board)
        count_O = sum(row.count('O') for row in self.board)
        return count_X, count_O

class OthelloGUI:
    def __init__(self, root):
        self.game = Othello()
        self.root = root
        self.root.title("Othello")
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.create_board()
        self.update_board()

    def create_board(self):
        for i in range(8):
            for j in range(8):
                button = tk.Button(self.root, width=4, height=2, command=lambda row=i, col=j: self.handle_click(row, col))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def handle_click(self, row, col):
        if self.game.make_move(row, col):
            self.update_board()
            if self.game.game_over():
                self.end_game()

    def update_board(self):
        for i in range(8):
            for j in range(8):
                if self.game.board[i][j] == 'X':
                    self.buttons[i][j].config(text='X', state=tk.DISABLED)
                elif self.game.board[i][j] == 'O':
                    self.buttons[i][j].config(text='O', state=tk.DISABLED)
                else:
                    self.buttons[i][j].config(text='', state=tk.NORMAL)

    def end_game(self):
        count_X, count_O = self.game.count_pieces()
        message = f"Game over! X: {count_X}, O: {count_O}\n"
        if count_X > count_O:
            message += "X wins!"
        elif count_O > count_X:
            message += "O wins!"
        else:
            message += "It's a tie!"
        messagebox.showinfo("Game Over", message)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = OthelloGUI(root)
    root.mainloop()
