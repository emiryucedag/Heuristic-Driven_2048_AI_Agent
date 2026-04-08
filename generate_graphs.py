import matplotlib.pyplot as plt
import numpy as np

# --- 1. DEPTH VS TIME COMPLEXITY (LINE CHART) ---
def plot_time_complexity():
    depths = [2, 3, 4]
    times = [2.88, 6.95, 59.16]

    plt.figure(figsize=(8, 5))
    plt.plot(depths, times, marker='o', linestyle='-', color='red', linewidth=2, markersize=8)
    plt.title('Time Complexity: Decision Time per Move vs. Search Depth', fontsize=14, fontweight='bold')
    plt.xlabel('Search Depth (Ply)', fontsize=12)
    plt.ylabel('Average Time per Move (ms)', fontsize=12)
    plt.xticks(depths)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Add data labels
    for i, txt in enumerate(times):
        plt.annotate(f"{txt} ms", (depths[i], times[i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.tight_layout()
    plt.savefig('fig_time_complexity.png', dpi=300)
    plt.close()
    print("Created: fig_time_complexity.png")

# --- 2. DEPTH VS AVERAGE SCORE (BAR CHART) ---
def plot_depth_scores():
    depths = ['Depth 2', 'Depth 3\n(Horizon Effect)', 'Depth 4']
    scores = [33317, 24366, 72008]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(depths, scores, color=['#4C72B0', '#C44E52', '#55A868'])
    plt.title('Performance Comparison Across Different Search Depths', fontsize=14, fontweight='bold')
    plt.ylabel('Average Score', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1000, int(yval), ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig('fig_depth_scores.png', dpi=300)
    plt.close()
    print("Created: fig_depth_scores.png")

# --- 3. CACHE OPTIMIZATION (BAR CHART) ---
def plot_cache_optimization():
    modes = ['Cache OFF', 'Cache ON']
    times = [11.28, 6.19]

    plt.figure(figsize=(6, 5))
    bars = plt.bar(modes, times, color=['#8172B2', '#64B5CD'], width=0.5)
    plt.title('Transposition Table Optimization (Depth 3)', fontsize=14, fontweight='bold')
    plt.ylabel('Average Time per Move (ms)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, f"{yval} ms", ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig('fig_cache_optimization.png', dpi=300)
    plt.close()
    print("Created: fig_cache_optimization.png")

# --- 4. HEURISTIC ABLATION STUDY (BAR CHART) ---
def plot_ablation_study():
    modes = ['Empty Cells Only', 'Snake Matrix + Empty Cells']
    scores = [36962, 156044]

    plt.figure(figsize=(7, 5))
    bars = plt.bar(modes, scores, color=['#CCB974', '#1F77B4'], width=0.6)
    plt.title('Heuristic Ablation Study Impact on Score', fontsize=14, fontweight='bold')
    plt.ylabel('Average Score', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 2000, int(yval), ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig('fig_ablation_study.png', dpi=300)
    plt.close()
    print("Created: fig_ablation_study.png")

if __name__ == "__main__":
    print("Generating IEEE format graphs...")
    plot_time_complexity()
    plot_depth_scores()
    plot_cache_optimization()
    plot_ablation_study()
    print("All graphs successfully generated and saved to current directory!")