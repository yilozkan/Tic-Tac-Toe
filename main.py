import tkinter as tk
from tkinter import messagebox


def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score


def best_move(board):
    best_score = -float('inf')
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move


def check_winner(board):

    lines = []
    lines.extend(board)
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line == ['X', 'X', 'X']:
            return 'X'
        elif line == ['O', 'O', 'O']:
            return 'O'
    return None


def is_board_full(board):
    for row in board:
        if '' in row:
            return False
    return True


def on_click(row, col):
    global board, buttons, current_player

    if board[row][col] == '' and current_player == 'X':
        board[row][col] = 'X'
        buttons[row][col].config(text='X', state='disabled')

        if check_winner(board) == 'X':
            messagebox.showinfo("Oyun Bitti", "Kazandınız!")
            root.quit()
            return
        elif is_board_full(board):
            messagebox.showinfo("Oyun Bitti", "Berabere!")
            root.quit()
            return


        move = best_move(board)
        if move != (-1, -1):
            board[move[0]][move[1]] = 'O'
            buttons[move[0]][move[1]].config(text='O', state='disabled')

            if check_winner(board) == 'O':
                messagebox.showinfo("Oyun Bitti", "Kaybettiniz")
                root.quit()
                return
            elif is_board_full(board):
                messagebox.showinfo("Oyun Bitti", "Berabere!")
                root.quit()
                return


root = tk.Tk()
root.title("Tic Tac Toe")

board = [['' for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
current_player = 'X'

for i in range(3):
    for j in range(3):
        btn = tk.Button(root, text='', font=('Arial', 40), width=5, height=2,
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j)
        buttons[i][j] = btn

root.mainloop()
