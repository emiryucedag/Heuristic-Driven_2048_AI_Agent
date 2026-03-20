# 🧩 Heuristic-Driven 2048 AI Agent

An autonomous Artificial Intelligence agent designed to master the stochastic puzzle game **2048**. By modeling the game as a Markov Decision Process (MDP), this project effectively navigates the non-deterministic nature of the game to consistently achieve high-value tiles.

## 🚀 Key Features and Architecture

The agent abandons traditional adversarial algorithms (like Minimax) in favor of a probabilistically robust architecture:

* **Expectimax Search Algorithm:** Evaluates the expected utility of future board states by integrating "chance nodes" to account for the 90% (`2`) and 10% (`4`) random tile spawn probabilities.
* **Monotonic 'Snake' Heuristic Matrix:** Uses a mathematically designed, geometrically progressive weight matrix ($4^{15}$ down to $4^0$). 
* **Transposition Tables (State Caching):** Mitigates the $O(b^d)$ exponential time complexity of deep search trees.
* **Vectorized Computations:** Utilizes `NumPy` for high-performance, C-level matrix manipulations.
* **Decoupled OOP Design & GUI:** Separates the core game engine from the AI decision logic, featuring an interactive `Tkinter` graphical interface for real-time visualization.
* **Stochastic Data Logging:** Automatically records all random tile spawns and coordinates into `game_log.txt` for post-game statistical analysis and horizon effect detection.

## 📊 Experimental Results & Performance

The agent's performance was empirically validated through over 100 automated simulations. 

**Key Milestones:**
* **4.2x Score Multiplier:** The ablation study proved that switching from a baseline "Empty-Cells-Only" strategy to the "Snake Matrix" increased the average score from 36,962 to 156,044.
* **1.82x Speedup:** Caching previously computed board states reduced the average decision time per move at Depth 3 by 45% (from 11.28 ms to 6.19 ms).
* **Peak Performance (Depth 4):**
    * **4096 Tile:** 100% Win Rate
    * **8192 Tile:** 20% Win Rate
    * **Average Score:** 72,008

### Performance Across Search Depths (10 Games Each)

| Depth | Avg. Score | 2048 Win | 4096 Win | 8192 Win | Avg. Time/Move |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **2** | 33,317 | 80% | 10% | 0% | 2.88 ms |
| **3** | 24,366 | 50% | 0% | 0% | 6.95 ms |
| **4** | 72,008 | 0% | 80% | 20% | 59.16 ms |

*(Note: The performance drop at Depth 3 is a documented manifestation of the "Horizon Effect" inherent to odd-depth game tree searches terminating on chance nodes.)*

## ⚙️ Installation and Usage

Follow these steps to run the AI agent on your local machine:

* **Clone the repository:**
    ```bash
    git clone [https://github.com/emiryucedag/Heuristic-Driven_2048_AI_Agent.git](https://github.com/emiryucedag/Heuristic-Driven_2048_AI_Agent.git)
    cd Heuristic-Driven_2048_AI_Agent
    ```
* **Install required dependencies:**
    ```bash
    pip install numpy
    ```
* **Run the simulation:**
    ```bash
    python main.py
    ```

## 📄 Academic Paper

This repository is the practical implementation of the IEEE-formatted academic term project: **"Evaluation of an Autonomous 2048 AI Agent: Optimizing Expectimax Search for Stochastic Environments"** developed at TOBB University of Economics and Technology.
