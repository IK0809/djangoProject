import tkinter as tk
import random

class WhackAMole:
    def __init__(self, root):
        self.root = root
        self.root.title("Whack-A-Mole")
        self.score = 0
        self.mole_buttons = []
        self.create_board()
        self.update_moles()

        # スコア表示用ラベル
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=('Helvetica', 14))
        self.score_label.grid(row=15, column=0, columnspan=15, pady=10)

    def create_board(self):
        for i in range(15):
            row_buttons = []
            for j in range(15):
                button = tk.Button(self.root, width=7, height=3, command=lambda row=i, col=j: self.hit_mole(row, col))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.mole_buttons.append(row_buttons)

    def update_moles(self):
        for row in self.mole_buttons:
            for button in row:
                button.config(text='', state=tk.NORMAL, bg='SystemButtonFace', fg='black')
        row = random.randint(0, 14)
        col = random.randint(0, 14)
        self.mole_buttons[row][col].config(text='Mole', state=tk.NORMAL, bg='brown', fg='white')
        self.root.after(1000, self.update_moles)  # 1秒ごとにモグラの位置を更新

    def hit_mole(self, row, col):
        if self.mole_buttons[row][col].cget('text') == 'Mole':
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.mole_buttons[row][col].config(text='', state=tk.DISABLED, bg='SystemButtonFace', fg='black')

if __name__ == "__main__":
    root = tk.Tk()
    game = WhackAMole(root)
    root.mainloop()
