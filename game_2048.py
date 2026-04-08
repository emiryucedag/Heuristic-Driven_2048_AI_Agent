import tkinter as tk
import numpy as np
import random
import time


COLORS = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 
          128: "#edcf72", 256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}

class Game2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('YAP 441 - 2048 AI Project')
        self.score = 0
        
        # Transposition Table to cache previously calculated board states
        self.transposition_table = {}
        self.ai_running = False
        # Defines the logic AI uses to evaluate the board
        self.heuristic_mode = "snake"
        
        # Top Section: Scoreboard and Information
        self.header = tk.Frame(self, bg="#faf8ef", width=400, height=100)
        self.header.grid(row=0, column=0, sticky="nsew")
        
        self.score_label = tk.Label(self.header, text=f"SCORE: {self.score}", 
                                    font=("Helvetica", 24, "bold"), bg="#bbada0", fg="white", 
                                    width=12, height=2)
        self.score_label.pack(pady=10)

        # Game Area (Main Grid)
        self.main_grid = tk.Frame(self, bg="#bbada0", bd=3, width=400, height=400)
        self.main_grid.grid(row=1, column=0, pady=10)
        
        self.make_gui()
        self.start_game()
        
        # Controls: Arrow Keys (Manual) and 'A' Key (Toggle AI), 'S' Key (Simulation)
        self.master.bind("<Left>", lambda event: self.move("Left"))
        self.master.bind("<Right>", lambda event: self.move("Right"))
        self.master.bind("<Up>", lambda event: self.move("Up"))
        self.master.bind("<Down>", lambda event: self.move("Down"))
        self.master.bind("a", lambda event: self.toggle_ai()) # EMPTY_ONŞY ai agent 
        self.master.bind("s", lambda event: self.run_simulation(num_games=10, test_depth=4)) # for simulating
        self.master.bind("c", lambda event: self.run_cache_test()) # with and without cache comparison
        self.master.bind("d", lambda event: self.run_ablation_test()) # heuristic ablation study (empty_only and snake)

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

    # --- Basic Movement Logic ---
    
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
                    self.score += matrix[i][j] # Actual score is updated here
                    matrix[i][j+1] = 0
        return matrix

    def move(self, direction):
        old_matrix = self.matrix.copy()
        
        # Routing with matrix operations
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

    # --- Artificial Intelligence (AI) Section ---
    def evaluate_board(self, matrix):
        empty_cells = len(np.where(matrix == 0)[0])

        # Dumb AI: Only cares about keeping the board empty, ignores positioning
        if self.heuristic_mode == "empty_only":
            return empty_cells * 1000

        # Smart AI: Uses the standard Snake pattern to keep the largest tiles in the corner
        elif self.heuristic_mode == "snake":
            weight_matrix = np.array([
                [65536, 32768, 16384,  8192],
                [  512,  1024,  2048,  4096],
                [  256,   128,    64,    32],
                [    2,     4,     8,    16]
            ])
            score = np.sum(matrix * weight_matrix)
            score += empty_cells * 1000 
            return score
            
        return 0

    def combine_logic_only(self, matrix):
        # Merge logic that does not affect the actual score for simulation purposes
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

    # --- EXPECTIMAX ALGORITHM (FINAL STAGE) ---
    def expectimax(self, matrix, depth, is_max_node, use_cache=True):
        board_hash = (tuple(matrix.flatten()), depth, is_max_node)
        
        # Return directly from cache if it exists and caching is enabled
        if use_cache and board_hash in self.transposition_table:
            return self.transposition_table[board_hash]
        
        # Reached the depth limit
        if depth == 0:
            score = self.evaluate_board(matrix)
            if use_cache: self.transposition_table[board_hash] = score
            return score

        if is_max_node:
            best_score = -float('inf')
            directions = ["Left", "Right", "Up", "Down"]
            
            for move_dir in directions:
                simulated_matrix, moved = self.simulate_move(matrix, move_dir)
                if moved:
                    score = self.expectimax(simulated_matrix, depth - 1, False, use_cache)
                    best_score = max(best_score, score)
            
            # Game over state for this branch
            if best_score == -float('inf'):
                score = self.evaluate_board(matrix)
                if use_cache: self.transposition_table[board_hash] = score
                return score
                
            if use_cache: self.transposition_table[board_hash] = best_score
            return best_score
            
        else:
            empty_cells = list(zip(*np.where(matrix == 0)))
            if not empty_cells:
                score = self.evaluate_board(matrix)
                if use_cache: self.transposition_table[board_hash] = score
                return score

            expected_score = 0
            for row, col in empty_cells:
                # 90% probability for tile 2
                matrix_2 = matrix.copy()
                matrix_2[row][col] = 2
                expected_score += 0.9 * self.expectimax(matrix_2, depth - 1, True, use_cache) / len(empty_cells)

                # 10% probability for tile 4
                matrix_4 = matrix.copy()
                matrix_4[row][col] = 4
                expected_score += 0.1 * self.expectimax(matrix_4, depth - 1, True, use_cache) / len(empty_cells)
    
            if use_cache: self.transposition_table[board_hash] = expected_score
            return expected_score

    def get_best_move(self, current_depth=3, use_cache=True):
        self.transposition_table.clear()
        best_score = -float('inf')
        best_move = None
        directions = ["Left", "Right", "Up", "Down"]

        for move_dir in directions:
            simulated_matrix, moved = self.simulate_move(self.matrix, move_dir)
            if moved:
                score = self.expectimax(simulated_matrix, current_depth, False, use_cache)
                if score > best_score:
                    best_score = score
                    best_move = move_dir
                    
        return best_move

    def run_simulation(self, num_games=10, test_depth=2):


        print(f"\n--- {test_depth} DERINLIK ICIN {num_games} OYUNLUK TEST BASLIYOR ---")
        results = {4096: 0, 2048: 0, 1024: 0}
        scores = []
        total_moves = 0
        total_time = 0

        with open(f"depth_{test_depth}_results.txt", "w", encoding="utf-8") as file:
            file.write(f"--- DEPTH {test_depth} TEST RESULTS ---\n\n")

            for i in range(num_games):
                self.start_game()
                self.score = 0
                self.score_label.config(text=f"SCORE: {self.score}")
                
                game_moves = 0
                game_time = 0
    
                while True:
                    # KRONOMETREYİ BAŞLAT
                    start_time = time.time()
                    
                    # Hamleyi belirlenen derinliğe göre bul
                    best_move = self.get_best_move(current_depth=test_depth) 
                    
                    # KRONOMETREYİ DURDUR
                    end_time = time.time()
                    
                    if best_move:
                        self.move(best_move)
                        self.update_idletasks()
                        game_moves += 1
                        game_time += (end_time - start_time)
                    else:
                        break
                
                max_tile = np.max(self.matrix)
                scores.append(self.score)
                total_moves += game_moves
                total_time += game_time
                
                log_text = f"Game {i+1} Over | Score: {self.score} | Max Tile: {max_tile} | Moves: {game_moves}"
                print(log_text)
                file.write(log_text + "\n")
                
                if max_tile >= 4096: results[4096] += 1
                elif max_tile >= 2048: results[2048] += 1
                elif max_tile >= 1024: results[1024] += 1
    
            avg_score = int(sum(scores)/len(scores)) if scores else 0
            avg_time_per_move = (total_time / total_moves) * 1000 if total_moves > 0 else 0
            
            final_report = (
                f"\n=== DEPTH {test_depth} STATISTICS ===\n"
                f"Total Games Played: {num_games}\n"
                f"Average Score: {avg_score}\n"
                f"Average Time Per Move: {avg_time_per_move:.2f} ms\n"
                f"4096 Win Rate: {(results[4096]/num_games)*100}%\n"
                f"2048 Win Rate: {(results[2048]/num_games)*100}%\n"
                f"1024 Win Rate: {(results[1024]/num_games)*100}%\n"
                f"=================================\n"
            )
            
            print(final_report)
            file.write(final_report)


    def run_cache_test(self, current_depth=3):
        print(f"\n--- STARTING CACHE OFF TEST (DEPTH {current_depth}) ---")
        time_off, moves_off = 0, 0
        
        # Playing only 3 games because it is significantly slower without cache
        for i in range(3):
            self.start_game()
            while True:
                start_time = time.time()
                move = self.get_best_move(current_depth=current_depth, use_cache=False)
                end_time = time.time()
                
                if move:
                    self.move(move)
                    self.update_idletasks()
                    time_off += (end_time - start_time)
                    moves_off += 1
                else:
                    break
            print(f"Game {i+1} without cache finished.")

        avg_off = (time_off / moves_off) * 1000 if moves_off > 0 else 0
        print(f"-> CACHE OFF Average Time Per Move: {avg_off:.2f} ms")

        print(f"\n--- STARTING CACHE ON TEST (DEPTH {current_depth}) ---")
        time_on, moves_on = 0, 0
        
        for i in range(3):
            self.start_game()
            while True:
                start_time = time.time()
                move = self.get_best_move(current_depth=current_depth, use_cache=True)
                end_time = time.time()
                
                if move:
                    self.move(move)
                    self.update_idletasks()
                    time_on += (end_time - start_time)
                    moves_on += 1
                else:
                    break
            print(f"Game {i+1} with cache finished.")

        avg_on = (time_on / moves_on) * 1000 if moves_on > 0 else 0
        print(f"-> CACHE ON Average Time Per Move: {avg_on:.2f} ms")

        speedup = (avg_off / avg_on) if avg_on > 0 else 0
        print(f"\n=== ENGINEERING RESULT ===")
        print(f"Transposition Table optimization sped up the algorithm by {speedup:.2f} TIMES!")
        print("==========================\n")   

    def run_ablation_test(self, num_games=5, current_depth=2):
        modes = ["empty_only", "snake"]
        
        with open("ablation_results.txt", "w", encoding="utf-8") as file:
            file.write(f"--- HEURISTIC ABLATION STUDY (DEPTH {current_depth}, {num_games} GAMES PER MODE) ---\n\n")
            
            for mode in modes:
                self.heuristic_mode = mode
                print(f"\n--- TESTING HEURISTIC MODE: {mode.upper()} ---")
                file.write(f"--- TESTING HEURISTIC MODE: {mode.upper()} ---\n")
                
                scores = []
                results = {2048: 0, 1024: 0, 512: 0, 256: 0}
                
                for i in range(num_games):
                    self.start_game()
                    while True:
                        move = self.get_best_move(current_depth=current_depth, use_cache=True)
                        if move:
                            self.move(move)
                            self.update_idletasks()
                        else:
                            break
                    
                    max_tile = np.max(self.matrix)
                    scores.append(self.score)
                    log_text = f"Mode: {mode.upper()} | Game {i+1} | Score: {self.score} | Max Tile: {max_tile}"
                    print(log_text)
                    file.write(log_text + "\n")
                    
                    if max_tile >= 2048: results[2048] += 1
                    elif max_tile >= 1024: results[1024] += 1
                    elif max_tile >= 512: results[512] += 1
                    else: results[256] += 1
                    
                avg_score = int(sum(scores)/len(scores)) if scores else 0
                summary = (
                    f"\n=== SUMMARY FOR {mode.upper()} ===\n"
                    f"Average Score: {avg_score}\n"
                    f"2048 Win Rate: {(results[2048]/num_games)*100}%\n"
                    f"1024 Reach Rate: {(results[1024]/num_games)*100}%\n"
                    f"512 Reach Rate: {(results[512]/num_games)*100}%\n"
                    f"=================================\n"
                )
                print(summary)
                file.write(summary + "\n")
                
        print("Ablation study complete. All results saved to 'ablation_results.txt'.")
        self.heuristic_mode = "snake" # Reset to default after test

    def ai_move(self):
        if not self.ai_running: return
        
        # Find the best move with Expectimax
        best_move = self.get_best_move()
        
        if best_move:
            self.move(best_move)
            # AI's move speed (Milliseconds)
            self.after(50, self.ai_move) 
        else:
            print(f"Game Over! Reached Score: {self.score}")
            self.ai_running = False

if __name__ == "__main__":
    Game2048().mainloop()
