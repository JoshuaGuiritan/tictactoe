import tkinter as tk

def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in wins:
        a, b, c = combo
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    if all(cell != "" for cell in board):
        return "Draw"
    return None

def minimax(board, is_maximizing):
    result = check_winner(board)
    if result == "X":
        return 10
    if result == "O":
        return -10
    if result == "Draw":
        return 0

    if is_maximizing:
        best = -1000
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, False)
                board[i] = ""
                best = max(best, score)
        return best
    else:
        best = 1000
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, True)
                board[i] = ""
                best = min(best, score)
        return best

def best_move_x(board):
    best_score = -1000
    move = -1
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            score = minimax(board, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

def best_move_o(board):
    best_score = 1000
    move = -1
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, True)
            board[i] = ""
            if score < best_score:
                best_score = score
                move = i
    return move

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe — AI vs AI")
        self.root.resizable(False, False)

        self.board = [""] * 9
        self.current_player = "X"
        self.running = False
        self.delay = 600

        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self.root, text="Tic-Tac-Toe  AI vs AI ",
                         font=("Helvetica", 16, "bold"), pady=8)
        title.pack()
        self.status_var = tk.StringVar(value="Press  Start  to begin!")
        status = tk.Label(self.root, textvariable=self.status_var,
                          font=("Helvetica", 12), fg="#444")
        status.pack(pady=(0, 6))
        board_frame = tk.Frame(self.root, bg="#222")
        board_frame.pack(padx=20, pady=4)
        self.buttons = []
        for i in range(9):
            btn = tk.Button(board_frame, text="", width=5, height=2,
                            font=("Helvetica", 28, "bold"),
                            bg="#f9f9f9", relief="flat",
                            state="disabled")
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self.buttons.append(btn)
        score_frame = tk.Frame(self.root)
        score_frame.pack(pady=8)
        self.score = {"X": 0, "O": 0, "Draw": 0}
        tk.Label(score_frame, text="X Wins:", font=("Helvetica", 11)).grid(row=0, column=0, padx=6)
        self.x_score_lbl = tk.Label(score_frame, text="0",
                      font=("Helvetica", 11, "bold"), fg="#e74c3c")
        self.x_score_lbl.grid(row=0, column=1, padx=6)
        tk.Label(score_frame, text="O Wins:", font=("Helvetica", 11)).grid(row=0, column=2, padx=6)
        self.o_score_lbl = tk.Label(score_frame, text="0",
                                    font=("Helvetica", 11, "bold"), fg="#2980b9")
        self.o_score_lbl.grid(row=0, column=3, padx=6)
        tk.Label(score_frame, text="Draws:", font=("Helvetica", 11)).grid(row=0, column=4, padx=6)
        self.draw_score_lbl = tk.Label(score_frame, text="0",
                                       font=("Helvetica", 11, "bold"), fg="#27ae60")
        self.draw_score_lbl.grid(row=0, column=5, padx=6)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        self.start_btn = tk.Button(btn_frame, text="Start", width=10,
                                   font=("Helvetica", 11, "bold"),
                                   bg="#2ecc71", fg="white",
                                   command=self.start_game)
        self.start_btn.grid(row=0, column=0, padx=6)
        self.reset_btn = tk.Button(btn_frame, text="Reset", width=10,
                                   font=("Helvetica", 11),
                                   command=self.reset_all)
        self.reset_btn.grid(row=0, column=1, padx=6)
    def _color_for(self, player):
        return "#e74c3c" if player == "X" else "#2980b9"
    def _highlight_winner(self, winner):
        wins = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        color = self._color_for(winner)
        for combo in wins:
            a, b, c = combo
            if self.board[a] == self.board[b] == self.board[c] == winner:
                for idx in combo:
                    self.buttons[idx].config(bg=color, fg="white")

    def start_game(self):
        self.running = True
        self.start_btn.config(state="disabled")
        self._next_move()

    def _next_move(self):
        if not self.running:
            return
        result = check_winner(self.board)
        if result:
            self._end_game(result)
            return
        if self.current_player == "X":
            move = best_move_x(self.board)
            self.status_var.set("AI X is thinking…")
        else:
            move = best_move_o(self.board)
            self.status_var.set("AI O is thinking…")
        self.board[move] = self.current_player
        btn = self.buttons[move]
        btn.config(text=self.current_player,
                   fg=self._color_for(self.current_player))
        self.current_player = "O" if self.current_player == "X" else "X"
        self.root.after(self.delay, self._next_move)

    def _end_game(self, result):
        self.running = False
        self.score[result] += 1
        self.x_score_lbl.config(text=str(self.score["X"]))
        self.o_score_lbl.config(text=str(self.score["O"]))
        self.draw_score_lbl.config(text=str(self.score["Draw"]))
        if result == "Draw":
            self.status_var.set("It's a Draw!")
        else:
            self._highlight_winner(result)
            self.status_var.set(f"AI {result} wins!")

        self.start_btn.config(state="normal", text="Play Again")
        self._reset_board_only()

    def _reset_board_only(self):
        self.root.after(1800, self._clear_board)

    def _clear_board(self):
        self.board = [""] * 9
        self.current_player = "X"
        for btn in self.buttons:
            btn.config(text="", bg="#f9f9f9", fg="#333")
        self.status_var.set("Press Play Again for another round!")

    def reset_all(self):
        self.running = False
        self.score = {"X": 0, "O": 0, "Draw": 0}
        self.x_score_lbl.config(text="0")
        self.o_score_lbl.config(text="0")
        self.draw_score_lbl.config(text="0")
        self.board = [""] * 9
        self.current_player = "X"
        for btn in self.buttons:
            btn.config(text="", bg="#f9f9f9", fg="#333")
        self.start_btn.config(state="normal", text="Start")
        self.status_var.set("Press  Start  to begin!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()