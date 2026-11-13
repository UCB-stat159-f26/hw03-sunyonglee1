import matplotlib.pyplot as plt


def plot_age_matches(data):
    required = {"player_age", "age_difference", "result"}
    if not required.issubset(data.columns) or data.empty:
        raise ValueError("Data must contain player ages, age differences, and results.")
    win_color, loss_color = "#42C5E8", "#963A91"
    colors = data["result"].map({"W": win_color, "L": loss_color})
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.scatter(data["player_age"], data["age_difference"], c=colors,
               s=18, alpha=0.9, edgecolors="none")
    _style_axes(ax, data)
    _add_legend(ax, win_color, loss_color)
    fig.tight_layout()
    return fig


def _style_axes(ax, data):
    low = int(data["player_age"].min())
    high = int(data["player_age"].max())
    ax.set_title(f"Professional Matches, Age {low} to {high}",
                 fontsize=15, fontweight="bold", pad=18)
    ax.set_xlabel("Player age")
    ax.set_ylabel("Age difference (player − opponent)")
    ax.set_xlim(low - 0.5, high + 1)
    ax.set_ylim(-20, 22)
    ax.set_xticks(range(low - low % 2, high + 1, 2))
    ax.set_yticks([-20, -10, 0, 10, 20])
    ax.grid(True, color="#DDDDDD", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.axhline(y=0, color="#888888", linewidth=1)


def _add_legend(ax, win_color, loss_color):
    handles = [
        plt.Line2D([], [], marker="o", linestyle="none",
                   markerfacecolor=win_color, markeredgecolor="none",
                   markersize=7, label="Match won"),
        plt.Line2D([], [], marker="o", linestyle="none",
                   markerfacecolor=loss_color, markeredgecolor="none",
                   markersize=7, label="Match lost"),
    ]
    ax.legend(handles=handles, loc="upper center",
              bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=False)