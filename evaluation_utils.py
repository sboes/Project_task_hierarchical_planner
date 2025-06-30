
import matplotlib.pyplot as plt
import pandas as pd

def plot_benchmark_results(df, save_path=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    df_sorted = df.sort_values("scene")
    bar = ax.bar(df_sorted["scene"], df_sorted["path_length"], color="skyblue", label="Pfadlänge")
    ax.set_ylabel("Pfadlänge")
    ax.set_xlabel("Testumgebung")
    ax.set_title("Pfadlänge pro Umgebung")
    ax.set_xticklabels(df_sorted["scene"], rotation=45, ha="right")
    ax.grid(True, linestyle="--", alpha=0.6)

    # Erfolg markieren
    for idx, success in enumerate(df_sorted["success"]):
        color = "green" if success else "red"
        ax.text(idx, df_sorted["path_length"].iloc[idx] + 1, "✔" if success else "✘",
                ha="center", va="bottom", color=color, fontsize=12)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def summarize_results(df):
    success_rate = df["success"].mean()
    avg_length = df[df["success"]]["path_length"].mean()
    avg_time = df["duration_sec"].mean()
    print(f"✔ Erfolgsquote: {success_rate*100:.1f}%")
    print(f"📏 Ø Pfadlänge: {avg_length:.1f}")
    print(f"⏱️ Ø Rechenzeit: {avg_time:.2f}s")
