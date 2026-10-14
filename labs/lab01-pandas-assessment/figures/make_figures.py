"""Draws figures/toy_tables.png: the three small tables used in the Block 2 quiz.

Run from this folder:  python make_figures.py
Needs only matplotlib. The tables are written out by hand, the same values as in the notebook.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

GREY, HEAD, KEY1, KEY2, NONE = "#f0f0f0", "#e3e3e3", "#cfe0f5", "#fbe3c6", "#f7f7f7"


def table(ax, x0, y0, headers, rows, widths, fills=None, h=0.8, nan_red=True):
    """Draw a table with its top-left corner at (x0, y0). fills: colour per row (or None)."""
    x = x0
    for head, w in zip(headers, widths):
        ax.add_patch(Rectangle((x, y0 - h), w, h, fc=HEAD, ec="#222", lw=1.2))
        ax.text(x + w / 2, y0 - h / 2, head, ha="center", va="center", fontsize=11, fontweight="bold")
        x += w
    for i, row in enumerate(rows):
        x = x0
        y = y0 - h * (i + 2)
        for j, (cell, w) in enumerate(zip(row, widths)):
            fc = fills[i] if fills else "white"
            ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec="#222", lw=1.2))
            is_nan = cell == "NaN"
            ax.text(x + w / 2, y + h / 2, cell, ha="center", va="center", fontsize=11,
                    color="#c0392b" if (is_nan and nan_red) else "#222",
                    style="italic" if is_nan else "normal")
            x += w


fig, ax = plt.subplots(figsize=(13, 4.4))
ax.set_xlim(0, 26)
ax.set_ylim(0, 7.6)
ax.axis("off")

# --- toy: index labels, team, score
ax.text(0.2, 7.2, "toy", fontsize=14, fontweight="bold")
ax.text(1.4, 7.2, "(Q1 - Q5)", fontsize=10, color="#666")
rows = [("10", "a", "10.0"), ("11", "a", "NaN"), ("12", "b", "7.0"), ("13", "b", "3.0"), ("14", "c", "NaN")]
table(ax, 0.2, 6.7, ["index", "team", "score"], rows, [1.7, 1.6, 1.7])
for i in range(5):
    ax.add_patch(Rectangle((0.2, 6.7 - 0.8 * (i + 2)), 1.7, 0.8, fc=GREY, ec="#222", lw=1.2))
    ax.text(1.05, 6.7 - 0.8 * (i + 2) + 0.4, rows[i][0], ha="center", va="center", fontsize=11, fontweight="bold")
    ax.text(5.35, 6.7 - 0.8 * (i + 2) + 0.4, f"position {i}", ha="left", va="center", fontsize=9, color="#777")
ax.text(0.2, 1.0, "the index holds the LABELS 10 to 14;\nthe POSITIONS are 0 to 4 (the grey text)",
        fontsize=9.5, color="#2e5fa8", va="center")

# --- left and right: keys coloured by value
key_fill = {1: NONE, 2: KEY1, 3: KEY2, 4: NONE}
ax.text(10.2, 7.2, "left", fontsize=14, fontweight="bold")
lrows = [(1, "a"), (2, "b"), (2, "c"), (3, "d")]
table(ax, 10.2, 6.7, ["k", "x"], [(str(k), v) for k, v in lrows], [1.5, 1.5],
      fills=[key_fill[k] for k, _ in lrows])
ax.text(15.6, 7.2, "right", fontsize=14, fontweight="bold")
ax.text(17.5, 7.2, "(Q6 - Q7)", fontsize=10, color="#666")
rrows = [(2, "w"), (3, "x"), (3, "y"), (4, "z")]
table(ax, 15.6, 6.7, ["k", "y"], [(str(k), v) for k, v in rrows], [1.5, 1.5],
      fills=[key_fill[k] for k, _ in rrows])
ax.text(10.2, 1.0, "same colour = same key value",
        fontsize=9.5, color="#2e5fa8", va="center")

plt.savefig("toy_tables.png", dpi=130, bbox_inches="tight", facecolor="white")
