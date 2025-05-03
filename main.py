import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeAI:
    def __init__(self, difficulty='Medium'):
        self.difficulty = difficulty

    def get_move(self, board, player):
        if self.difficulty == 'Easy':
            return self.random_move(board)
        elif self.difficulty == 'Medium':
            return self.medium_move(board, player)
        elif self.difficulty == 'Hard':
            return self.minimax_move(board, player)

    def random_move(self, board):
        available = [i for i, spot in enumerate(board) if spot == '']
        return random.choice(available)

    def medium_move(self, board, player):
        opponent = 'O' if player == 'X' else 'X'
        for i in range(9):
            if board[i] == '':
                board_copy = board[:]
                board_copy[i] = player
                if self.check_win(board_copy, player):
                    return i
                board_copy[i] = opponent
                if self.check_win(board_copy, opponent):
                    return i
        return self.random_move(board)

    def minimax_move(self, board, player):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if board[i] == '':
                board[i] = player
                score = self.minimax(board, False, player)
                board[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, is_maximizing, player):
        opponent = 'O' if player == 'X' else 'X'
        if self.check_win(board, player):
            return 1
        elif self.check_win(board, opponent):
            return -1
        elif '' not in board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = player
                    score = self.minimax(board, False, player)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = opponent
                    score = self.minimax(board, True, player)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score

    def check_win(self, board, player):
        win_combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        return any(all(board[i] == player for i in combo) for combo in win_combos)

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Fancy Tic Tac Toe with AI")
        self.board = [''] * 9
        self.current_player = 'X'
        self.buttons = []
        self.ai = None

        self.difficulty = tk.StringVar(value="Medium")

        self.create_widgets()

    def create_widgets(self):
        difficulty_frame = tk.Frame(self.root)
        tk.Label(difficulty_frame, text="Select Difficulty:").pack(side=tk.LEFT)
        for level in ['Easy', 'Medium', 'Hard']:
            tk.Radiobutton(
                difficulty_frame, text=level, variable=self.difficulty, value=level,
                command=self.set_difficulty
            ).pack(side=tk.LEFT)
        difficulty_frame.pack()

        self.board_frame = tk.Frame(self.root)
        for i in range(9):
            button = tk.Button(self.board_frame, text='', width=10, height=3,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)
        self.board_frame.pack()

        self.set_difficulty()

    def set_difficulty(self):
        self.ai = TicTacToeAI(difficulty=self.difficulty.get())

    def on_button_click(self, index):
        if self.board[index] == '' and self.current_player == 'X':
            self.board[index] = 'X'
            self.buttons[index].config(text='X', state='disabled')
            if self.check_win('X'):
                self.show_result('Player X wins!')
            elif '' not in self.board:
                self.show_result('Draw!')
            else:
                self.current_player = 'O'
                self.ai_move()

    def ai_move(self):
        move = self.ai.get_move(self.board, 'O')
        self.board[move] = 'O'
        self.buttons[move].config(text='O', state='disabled')
        if self.check_win('O'):
            self.show_result('Player O wins!')
        elif '' not in self.board:
            self.show_result('Draw!')
        else:
            self.current_player = 'X'

    def check_win(self, player):
        win_combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        return any(all(self.board[i] == player for i in combo) for combo in win_combos)

    def show_result(self, message):
        messagebox.showinfo("Game Over", message)
        self.reset_game()

    def reset_game(self):
        self.board = [''] * 9
        for button in self.buttons:
            button.config(text='', state='normal')
        self.current_player = 'X'
        self.set_difficulty()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()

## INSTALL tkinter-tooltip in replit power-shell using this command " pip install tkinter-tooltip " 
