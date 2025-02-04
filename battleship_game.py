import tkinter as tk
import random

class BattleshipGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Battleship Game")

        self.grid_size = 10
        self.ship_size = 3
        self.num_ships = 5

        self.user_grid = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.computer_grid = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.computer_ships = []
        self.user_ships = []

        self.user_hits = []
        self.computer_hits = []

        self.turn_label = tk.Label(self.root, text="Place your ships on the left grid", font=("Arial", 14))
        self.turn_label.pack()

        self.canvas_user = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas_user.pack(side="left", padx=10)

        self.canvas_computer = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas_computer.pack(side="right", padx=10)

        self.canvas_user.bind("<Button-1>", self.place_user_ship)
        self.canvas_computer.bind("<Button-1>", self.user_turn)

        self.draw_grid(self.canvas_user)
        self.draw_grid(self.canvas_computer)

        self.place_computer_ships()

        self.user_ship_count = 0
        self.game_started = False

        self.root.mainloop()

    def draw_grid(self, canvas):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * 40
                y1 = row * 40
                x2 = x1 + 40
                y2 = y1 + 40
                canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    def place_user_ship(self, event):
        if self.user_ship_count >= self.num_ships:
            self.turn_label.config(text="All ships placed! Start the game.")
            self.game_started = True
            return

        col = event.x // 40
        row = event.y // 40

        if self.is_valid_ship(self.user_grid, row, col):
            self.add_ship(self.user_grid, row, col)
            self.user_ships.append([(row, col + i) for i in range(self.ship_size)])
            self.user_ship_count += 1
            self.update_canvas(self.canvas_user, self.user_grid, show_ships=True)

    def is_valid_ship(self, grid, row, col):
        if col + self.ship_size > self.grid_size:
            return False
        for i in range(self.ship_size):
            if grid[row][col + i] != ".":
                return False
        return True

    def add_ship(self, grid, row, col):
        for i in range(self.ship_size):
            grid[row][col + i] = "S"

    def place_computer_ships(self):
        for _ in range(self.num_ships):
            while True:
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - self.ship_size)
                if self.is_valid_ship(self.computer_grid, row, col):
                    self.add_ship(self.computer_grid, row, col)
                    self.computer_ships.append([(row, col + i) for i in range(self.ship_size)])
                    break

    def update_canvas(self, canvas, grid, show_ships=False):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * 40
                y1 = row * 40
                x2 = x1 + 40
                y2 = y1 + 40

                if grid[row][col] == "S" and show_ships:
                    color = "gray"
                elif grid[row][col] == "H":
                    color = "green"
                elif grid[row][col] == "M":
                    color = "red"
                else:
                    color = "white"

                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def user_turn(self, event):
        if not self.game_started:
            self.turn_label.config(text="Place all your ships first!")
            return

        col = event.x // 40
        row = event.y // 40

        if self.computer_grid[row][col] in ("H", "M"):
            return

        if self.computer_grid[row][col] == "S":
            self.computer_grid[row][col] = "H"
            self.user_hits.append((row, col))
            self.turn_label.config(text="Hit!")
        else:
            self.computer_grid[row][col] = "M"
            self.turn_label.config(text="Miss!")

        self.update_canvas(self.canvas_computer, self.computer_grid, show_ships=False)

        if self.check_victory(self.computer_grid):
            self.turn_label.config(text="You win!")
            self.game_started = False
            return

        self.computer_turn()

    def computer_turn(self):
        while True:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)

            if self.user_grid[row][col] in ("H", "M"):
                continue

            if self.user_grid[row][col] == "S":
                self.user_grid[row][col] = "H"
                self.computer_hits.append((row, col))
                self.turn_label.config(text="Computer hit your ship!")
            else:
                self.user_grid[row][col] = "M"
                self.turn_label.config(text="Computer missed!")

            self.update_canvas(self.canvas_user, self.user_grid, show_ships=True)
            break

        if self.check_victory(self.user_grid):
            self.turn_label.config(text="Computer wins!")
            self.game_started = False

    def check_victory(self, grid):
        for row in grid:
            if "S" in row:
                return False
        return True

if __name__ == "__main__":
    BattleshipGame()
