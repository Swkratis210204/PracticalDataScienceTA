"""Draws figures/merge_one_to_many.png: a merge repeats a row when its key appears twice in the other table.

A neutral toy example (orders and e-mails), so that it does not give away Broken 2.
Run from this folder:  python make_merge_figure.py     (needs only matplotlib)
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

ANN, BOB, CY, RED = "#cfe0f5", "#fbe3c6", "#d5ecd4", "#c0392b"
HEAD, TXT = "#e3e3e3", "#222222"
H = 0.95

fig, ax = plt.subplots(figsize=(14, 6.2))
ax.set_xlim(0, 28)
ax.set_ylim(0, 12.4)
ax.axis("off")


def box(x, y, w, text, fc="white", bold=False, size=10.5, ec="#222", lw=1.2):
    ax.add_patch(Rectangle((x, y), w, H, fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + H / 2, text, ha="center", va="center", fontsize=size,
            fontweight="bold" if bold else "normal", color=TXT)


def table(x0, y_top, headers, widths, rows, fills, red=()):
    x = x0
    for head, w in zip(headers, widths):
        box(x, y_top - H, w, head, fc=HEAD, bold=True)
        x += w
    for i, (row, fc) in enumerate(zip(rows, fills)):
        x = x0
        for cell, w in zip(row, widths):
            box(x, y_top - H * (i + 2), w, cell, fc=fc,
                ec=RED if i in red else "#222", lw=3 if i in red else 1.2)
            x += w


# ------------------------------------------------------------------ left: orders
ax.text(0.2, 11.5, "orders", fontsize=13, fontweight="bold")
ax.text(2.6, 11.5, "(3 rows)", fontsize=10, color="#666")
table(0.2, 11.0, ["order", "customer"], [1.8, 2.6],
      [("1", "Ann"), ("2", "Bob"), ("3", "Cy")], [ANN, BOB, CY])

# ------------------------------------------------------------------ middle: emails
ax.text(0.2, 6.4, "emails", fontsize=13, fontweight="bold")
ax.text(2.6, 6.4, "(the table we look things up in)", fontsize=10, color="#666")
table(0.2, 5.9, ["customer", "email"], [2.6, 4.0],
      [("Ann", "ann@home.org"), ("Ann", "ann@work.org"), ("Bob", "bob@mail.org"), ("Cy", "cy@mail.org")],
      [ANN, ANN, BOB, CY], red=(1,))
ax.text(7.1, 5.9 - H * 3.5, "Ann appears twice", fontsize=10.5, color=RED, fontweight="bold", va="center")

# ------------------------------------------------------------------ arrow
ax.add_patch(FancyArrowPatch((9.2, 8.2), (11.6, 8.2), arrowstyle="-|>", mutation_scale=22, lw=2.2, color="#222"))
ax.text(10.4, 9.0, "merge", ha="center", fontsize=11, family="monospace", color="#555")
ax.text(10.4, 7.7, 'on="customer"\nhow="left"', ha="center", va="top", fontsize=9, family="monospace", color="#555")

# ------------------------------------------------------------------ right: result
ax.text(12.4, 11.5, "result", fontsize=13, fontweight="bold")
ax.text(14.2, 11.5, "(4 rows!)", fontsize=10.5, color=RED, fontweight="bold")
table(12.4, 11.0, ["order", "customer", "email"], [1.8, 2.6, 4.0],
      [("1", "Ann", "ann@home.org"), ("1", "Ann", "ann@work.org"), ("2", "Bob", "bob@mail.org"), ("3", "Cy", "cy@mail.org")],
      [ANN, ANN, BOB, CY], red=(1,))
ax.text(21.2, 11.0 - H * 3.5, "order 1 is\nrepeated", fontsize=10.5, color=RED, fontweight="bold", va="center")

# ------------------------------------------------------------------ takeaway
ax.text(12.4, 5.6,
        "A merge looks up EVERY matching row.\n"
        "One match  ->  one result row.\n"
        "Two matches  ->  two result rows.",
        fontsize=11.5, color="#2e5fa8", va="top", linespacing=1.7)
ax.text(12.4, 2.6, "3 rows in, 4 rows out:  the row count changed\nalthough we only wanted to add a column.",
        fontsize=12, color=RED, fontweight="bold", va="top", linespacing=1.6)

plt.savefig("merge_one_to_many.png", dpi=130, bbox_inches="tight", facecolor="white")
