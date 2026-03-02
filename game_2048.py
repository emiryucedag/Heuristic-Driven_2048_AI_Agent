import tkinter as tk
import numpy as np
import random

# Tasarım ve Renk Paleti (İnsan benzeri hissetmesi için orijinal renkler)
COLORS = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 
          128: "#edcf72", 256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}

class Game2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('YAP 441 - 2048 AI Project')
        self.score = 0
        self.ai_running = False
        
        # Üst Kısım: Skor Tabelası ve Bilgi
        self.header = tk.Frame(self, bg="#faf8ef", width=400, height=100)
        self.header.grid(row=0, column=0, sticky="nsew")
        
        self.score_label = tk.Label(self.header, text=f"SCORE: {self.score}", 
                                    font=("Helvetica", 24, "bold"), bg="#bbada0", fg="white", 
                                    width=12, height=2)
        self.score_label.pack(pady=10)

        # Oyun Alanı (Ana Izgara)
        self.main_grid = tk.Frame(self, bg="#bbada0", bd=3, width=400, height=400)
        self.main_grid.grid(row=1, column=0, pady=10)
        
        self.make_gui()
        self.start_game()
        
        # Kontroller: Ok Tuşları (Manuel) ve 'A' Tuşu (AI Başlat)
        self.master.bind("<Left>", lambda event: self.move("Left"))
        self.master.bind("<Right>", lambda event: self.move("Right"))
        self.master.bind("<Up>", lambda event: self.move("Up"))
        self.master.bind("<Down>", lambda event: self.move("Down"))
        self.master.bind("a", lambda event: self.toggle_ai())

    def make_gui(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(self.main_grid, bg="#cdc1b4", width=100, height=100)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg="#cdc1b4", justify=tk.CENTER, 
                                        font=("Helvetica", 30, "bold"), width=4, height=2)
                cell_number.grid(row=i, column=j)
                row.append(cell_number)
            self.cells.append(row)

    def start_game(self):
        self.matrix = np.zeros((4, 4), dtype=int)
        self.add_new_tile()
        self.add_new_tile()
        self.update_gui()

    def add_new_tile(self):
       
        empty_cells = list(zip(*np.where(self.matrix == 0)))
        if empty_cells:
            row, col = random.choice(empty_cells)
            value = 4 if random.random() < 0.1 else 2
            self.matrix[row][col] = value
            with open("game_log.txt", "a") as f:
                f.write(f"Tile Spawned: {value} at ({row}, {col})\n")

    def update_gui(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j].configure(text="", bg="#cdc1b4")
                else:
                    self.cells[i][j].configure(text=str(cell_value), 
                                               bg=COLORS.get(cell_value, "#3c3a32"), 
                                               fg="#776e65" if cell_value <= 4 else "white")
        self.score_label.configure(text=f"SCORE: {self.score}")
        self.update_idletasks()

    # --- Temel Hareket Mantığı ---
    
    def stack(self, matrix):
        new_matrix = np.zeros((4, 4), dtype=int)
        for i in range(4):
            fill_pos = 0
            for j in range(4):
                if matrix[i][j] != 0:
                    new_matrix[i][fill_pos] = matrix[i][j]
                    fill_pos += 1
        return new_matrix

    def combine(self, matrix):
        for i in range(4):
            for j in range(3):
                if matrix[i][j] != 0 and matrix[i][j] == matrix[i][j+1]:
                    matrix[i][j] *= 2
                    self.score += matrix[i][j] # Gerçek skor burada güncellenir
                    matrix[i][j+1] = 0
        return matrix

    def move(self, direction):
        old_matrix = self.matrix.copy()
        
        # Matris operasyonları ile yönlendirme
        if direction == "Left":
            self.matrix = self.stack(self.matrix)
            self.matrix = self.combine(self.matrix)
            self.matrix = self.stack(self.matrix)
        elif direction == "Right":
            self.matrix = np.flip(self.matrix, axis=1)
            self.matrix = self.stack(self.matrix)
            self.matrix = self.combine(self.matrix)
            self.matrix = self.stack(self.matrix)
            self.matrix = np.flip(self.matrix, axis=1)
        elif direction == "Up":
            self.matrix = np.transpose(self.matrix)
            self.matrix = self.stack(self.matrix)
            self.matrix = self.combine(self.matrix)
            self.matrix = self.stack(self.matrix)
            self.matrix = np.transpose(self.matrix)
        elif direction == "Down":
            self.matrix = np.transpose(self.matrix)
            self.matrix = np.flip(self.matrix, axis=1)
            self.matrix = self.stack(self.matrix)
            self.matrix = self.combine(self.matrix)
            self.matrix = self.stack(self.matrix)
            self.matrix = np.flip(self.matrix, axis=1)
            self.matrix = np.transpose(self.matrix)

        if not np.array_equal(old_matrix, self.matrix):
            self.add_new_tile()
            self.update_gui()

    # --- Yapay Zeka (AI) Bölümü ---

    def evaluate_board(self, matrix):
        # METODOLOJİ: Sezgisel Puanlama 
        empty_cells = len(np.where(matrix == 0)[0])
        monotonicity = 0
        for i in range(4):
            for j in range(3):
                if matrix[i][j] >= matrix[i][j+1]: monotonicity += 1
                if matrix[j][i] >= matrix[j+1][i]: monotonicity += 1
        
        max_tile = np.max(matrix)
        is_max_in_corner = (matrix[0,0] == max_tile or matrix[0,3] == max_tile or 
                           matrix[3,0] == max_tile or matrix[3,3] == max_tile)
        corner_bonus = 200 if is_max_in_corner else 0
        
        return (empty_cells * 20) + (monotonicity * 10) + corner_bonus + max_tile

    def combine_logic_only(self, matrix):
        # Simülasyon için skoru etkilemeyen birleştirme mantığı
        for i in range(4):
            for j in range(3):
                if matrix[i][j] != 0 and matrix[i][j] == matrix[i][j+1]:
                    matrix[i][j] *= 2
                    matrix[i][j+1] = 0
        return matrix

    def simulate_move(self, matrix, direction):
        temp_matrix = matrix.copy()
        if direction == "Left":
            temp_matrix = self.stack(temp_matrix); temp_matrix = self.combine_logic_only(temp_matrix); temp_matrix = self.stack(temp_matrix)
        elif direction == "Right":
            temp_matrix = np.flip(temp_matrix, axis=1); temp_matrix = self.stack(temp_matrix); temp_matrix = self.combine_logic_only(temp_matrix); temp_matrix = self.stack(temp_matrix); temp_matrix = np.flip(temp_matrix, axis=1)
        elif direction == "Up":
            temp_matrix = np.transpose(temp_matrix); temp_matrix = self.stack(temp_matrix); temp_matrix = self.combine_logic_only(temp_matrix); temp_matrix = self.stack(temp_matrix); temp_matrix = np.transpose(temp_matrix)
        elif direction == "Down":
            temp_matrix = np.transpose(temp_matrix); temp_matrix = np.flip(temp_matrix, axis=1); temp_matrix = self.stack(temp_matrix); temp_matrix = self.combine_logic_only(temp_matrix); temp_matrix = self.stack(temp_matrix); temp_matrix = np.flip(temp_matrix, axis=1); temp_matrix = np.transpose(temp_matrix)
        
        moved = not np.array_equal(matrix, temp_matrix)
        return temp_matrix, moved

    def toggle_ai(self):
        self.ai_running = not self.ai_running
        if self.ai_running: self.ai_move()

    def ai_move(self):
        if not self.ai_running: return
        
        directions = ["Left", "Right", "Up", "Down"]
        best_score = -1
        best_move = None
        
        for move_dir in directions:
            simulated_matrix, moved = self.simulate_move(self.matrix, move_dir)
            if moved:
                score = self.evaluate_board(simulated_matrix)
                if score > best_score:
                    best_score = score
                    best_move = move_dir
        
        if best_move:
            self.move(best_move)
            self.after(100, self.ai_move) # 100ms gecikme ile hamle yapar

if __name__ == "__main__":
    Game2048().mainloop()