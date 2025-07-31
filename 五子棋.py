import tkinter as tk
from tkinter import messagebox


class GomokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋游戏")

        self.board_size = 15
        self.cell_size = 40
        self.radius = 18
        self.current_player = "black"  # 黑方先行
        self.record = []  # 记录已下棋子的位置
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        self.create_menu()

    def create_menu(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=100)

        tk.Label(self.menu_frame, text="五子棋游戏", font=("Arial", 24)).pack(pady=20)

        tk.Button(
            self.menu_frame,
            text="开始游戏",
            font=("Arial", 16),
            command=self.start_game
        ).pack(pady=10)

        tk.Button(
            self.menu_frame,
            text="退出游戏",
            font=("Arial", 16),
            command=self.root.quit
        ).pack(pady=10)

    def start_game(self):
        self.menu_frame.destroy()

        canvas_width = self.board_size * self.cell_size
        canvas_height = self.board_size * self.cell_size
        self.canvas = tk.Canvas(
            self.root,
            width=canvas_width,
            height=canvas_height,
            bg="burlywood"
        )
        self.canvas.pack()

        self.draw_board()

        self.canvas.bind("<Button-1>", self.callback1)  # 左键黑子
        self.canvas.bind("<Button-3>", self.callback2)  # 右键白子

        tk.Button(
            self.root,
            text="返回菜单",
            command=self.return_to_menu
        ).pack(pady=10)

    def return_to_menu(self):
        self.canvas.destroy()
        self.create_menu()
        self.current_player = "black"
        self.record = []
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

    def draw_board(self):
        for i in range(self.board_size):
            self.canvas.create_line(
                self.cell_size // 2,
                self.cell_size // 2 + i * self.cell_size,
                self.cell_size // 2 + (self.board_size - 1) * self.cell_size,
                self.cell_size // 2 + i * self.cell_size
            )
            self.canvas.create_line(
                self.cell_size // 2 + i * self.cell_size,
                self.cell_size // 2,
                self.cell_size // 2 + i * self.cell_size,
                self.cell_size // 2 + (self.board_size - 1) * self.cell_size
            )

    def callback1(self, event):
        if self.current_player != "black":
            return

        x, y = event.x, event.y
        col = round((x - self.cell_size // 2) / self.cell_size)
        row = round((y - self.cell_size // 2) / self.cell_size)

        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            self.place_stone(row, col, "black")

    def callback2(self, event):
        if self.current_player != "white":
            return

        x, y = event.x, event.y
        col = round((x - self.cell_size // 2) / self.cell_size)
        row = round((y - self.cell_size // 2) / self.cell_size)

        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            self.place_stone(row, col, "white")

    def place_stone(self, row, col, color):
        if (row, col) in self.record:
            return

        self.record.append((row, col))
        self.board[row][col] = color

        x = self.cell_size // 2 + col * self.cell_size
        y = self.cell_size // 2 + row * self.cell_size
        self.canvas.create_oval(
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius,
            fill=color,
            outline="black" if color == "white" else "white"
        )

        if self.check_win(row, col, color):
            winner = "黑方" if color == "black" else "白方"
            messagebox.showinfo("游戏结束", f"{winner}获胜！")
            self.return_to_menu()
            return

        self.current_player = "white" if color == "black" else "black"

    def check_win(self, row, col, color):
        directions = [
            [(0, 1), (0, -1)],
            [(1, 0), (-1, 0)],
            [(1, 1), (-1, -1)],
            [(1, -1), (-1, 1)]
        ]

        for direction_pair in directions:
            count = 1

            for dx, dy in direction_pair:
                x, y = row + dx, col + dy
                while 0 <= x < self.board_size and 0 <= y < self.board_size:
                    if self.board[x][y] == color:
                        count += 1
                        x += dx
                        y += dy
                    else:
                        break

            if count >= 5:
                return True

        return False


if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGame(root)
    root.mainloop()