#  Heuristic-Driven 2048 AI Agent

An autonomous Artificial Intelligence agent designed to master the stochastic puzzle game **2048**. The game is formally modeled as a **Markov Decision Process (MDP)**, and the agent navigates its non-deterministic environment using **Expectimax search**, a **monotonic Snake heuristic**, and **Transposition Table** caching.

> 📄 This repository is the practical implementation of the IEEE-formatted term paper:  
> *"Evaluation of an Autonomous 2048 AI Agent: Optimizing Expectimax Search for Stochastic Environments"*  
> YAP 441 Term Project — Spring 2026, TOBB University of Economics and Technology

---

## Key Features

| Feature | Description |
|---|---|
| **Expectimax Search** | Models tile spawns via chance nodes (P=0.9 for "2", P=0.1 for "4") |
| **Snake Heuristic Matrix** | Geometrically progressive weight matrix (2¹⁶ → 2¹) enforcing monotonicity and corner locking |
| **Transposition Tables** | Hash-map caching of board states, providing a 1.82x decision speedup |
| **Vectorized NumPy Ops** | C-level matrix manipulations to minimize per-move latency |
| **Decoupled OOP Design** | Game Engine and AI Agent are fully isolated modules |
| **Tkinter GUI** | Real-time visualization with tile color coding and live score |
| **Stochastic Data Logger** | All random tile spawns logged to `game_log.txt` for statistical post-analysis |

---

## 📊 Experimental Results

Performance validated over **100+ automated simulations**.

### Search Depth vs. Performance (10 games each)

| Depth | Avg. Score | 2048 Win | 4096 Win | 8192 Win | Avg. Time/Move |
|:---:|---:|:---:|:---:|:---:|---:|
| 2 | 33,317 | 80% | 10% | 0% | 2.88 ms |
| 3 | 24,366 | 50% | 0% | 0% | 6.95 ms |
| **4** | **72,008** | 0% | **80%** | **20%** | 59.16 ms |

> ⚠️ The performance drop at Depth 3 is a documented **Horizon Effect**: odd-depth trees terminate on chance nodes, making the heuristic overly pessimistic.

### Ablation Study: Snake Matrix vs. Empty-Cells-Only (Depth 2, 5 games)

| Heuristic | Avg. Score | 2048+ Win | Peak Tile |
|---|---:|:---:|:---:|
| Empty Cells Only | 36,962 | 0% | 1024 |
| **Snake Matrix** | **156,044** | **60%** | **4096** |

The Snake Matrix delivers a **4.2x score multiplier**, proving that geometric tile arrangement is more critical than short-term board survival.

### Transposition Table Speedup (Depth 3)

| Cache State | Avg. Time/Move |
|---|---:|
| OFF | 11.28 ms |
| ON | 6.19 ms |

**~45% latency reduction → 1.82x speedup.**

---

## Installation and Usage

**Requirements:** Python 3.x, NumPy, Tkinter (standard library)

```bash
# 1. Clone the repository
git clone https://github.com/emiryucedag/Heuristic-Driven_2048_AI_Agent.git
cd Heuristic-Driven_2048_AI_Agent

# 2. Install dependencies
pip install numpy

# 3. Run the application
python game_2048.py
```

### Controls

| Key | Action |
|---|---|
| `← → ↑ ↓` | Manual play |
| `A` | Toggle AI (Expectimax, Depth 3) |
| `S` | Run 10-game simulation at Depth 4 |
| `C` | Run Transposition Table cache benchmark |
| `D` | Run heuristic ablation study |

---


## Algorithm Overview

The Expectimax search alternates between **Max Nodes** (agent maximizes score) and **Chance Nodes** (environment spawns a random tile). The expected utility at a chance node is:

$$V_{chance}(s) = \sum_{i \in \{2,4\}} P(i) \cdot V_{max}(s_i) = 0.9 \cdot V_{max}(s_2) + 0.1 \cdot V_{max}(s_4)$$

The Snake weight matrix used for leaf-node evaluation:

$$W = \begin{bmatrix} 2^{16} & 2^{15} & 2^{14} & 2^{13} \\ 2^{9} & 2^{10} & 2^{11} & 2^{12} \\ 2^{8} & 2^{7} & 2^{6} & 2^{5} \\ 2^{1} & 2^{2} & 2^{3} & 2^{4} \end{bmatrix}$$

---

##  References

1. G. Cirulli, "2048," GitHub, 2014. https://github.com/gabrielecirulli/2048  
2. R. Xiao, "2048-AI," GitHub, 2014. https://github.com/nneonneo/2048-ai  
3. N. Rodgers and J. Levine, "An investigation into 2048 AI strategies," *IEEE CIG*, 2014.  
4. M. Szubert and W. Jaśkowski, "Temporal difference learning of N-tuple networks for 2048," *IEEE CIG*, 2014.  
5. I.-C. Wu et al., "Multi-stage temporal difference learning for 2048-like games," *IEEE TCIAIG*, vol. 7, no. 1, 2015.  
6. L. Hu et al., "lmgame-Bench: How Good are LLMs at Playing Games?", *arXiv:2505.15146*, 2025.
