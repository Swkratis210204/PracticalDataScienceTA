"""Figures for the git and GitHub handbook. Run: python make_figures.py"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(exist_ok=True)
INK, BLUE, GREEN, ORANGE, GREY = "#1f2937", "#2563eb", "#16a34a", "#ea580c", "#9ca3af"


def box(ax, x, y, w, h, title, sub, color, fs=(10.5, 9.5)):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=color, ec="none", alpha=0.14))
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc="none", ec=color, lw=2))
    ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center", fontsize=fs[0], weight="bold", color=INK)
    ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center", fontsize=fs[1], color=INK)


def arrow(ax, x0, x1, y, label, color, back=False):
    ax.add_patch(FancyArrowPatch((x1, y) if back else (x0, y), (x0, y) if back else (x1, y),
                                 arrowstyle="-|>", mutation_scale=18, lw=2, color=color))
    ax.text((x0 + x1) / 2, y + 0.16, label, ha="center", va="bottom", fontsize=11, weight="bold",
            color=color, family="monospace")


# 1. the four places ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 3.3))
ax.set_xlim(0, 14.6); ax.set_ylim(0, 4); ax.axis("off")
box(ax, 0.1, 1.3, 2.7, 1.5, "Working folder", "the files you edit", BLUE)
box(ax, 4.2, 1.3, 2.7, 1.5, "Staging area", "what goes in the\nnext commit", ORANGE)
box(ax, 8.3, 1.3, 2.7, 1.5, "Local repo", "your commits\n(the .git folder)", GREEN)
box(ax, 12.2, 1.3, 2.3, 1.5, "GitHub", "remote copy\n(origin)", INK)
arrow(ax, 2.95, 4.05, 2.35, "add", ORANGE)
arrow(ax, 7.05, 8.15, 2.35, "commit", GREEN)
arrow(ax, 11.15, 12.05, 2.35, "push", INK)
arrow(ax, 11.15, 12.05, 1.55, "pull", INK, back=True)
ax.text(5.5, 0.55, "your laptop", ha="center", fontsize=10, color=GREY)
ax.plot([0.1, 11.0], [0.9, 0.9], color=GREY, lw=1.2)
ax.text(13.35, 0.55, "the internet", ha="center", fontsize=10, color=GREY)
ax.plot([12.2, 14.5], [0.9, 0.9], color=GREY, lw=1.2)
fig.savefig(OUT / "four_places.png", dpi=200, bbox_inches="tight", transparent=False, facecolor="white")
plt.close(fig)

# 2. history graph ---------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 3.1))
ax.set_xlim(0, 12); ax.set_ylim(-0.4, 2.9); ax.axis("off")


def commit(x, y, color, msg, h, up=False, dx=0, ha="center"):
    ax.add_patch(Circle((x, y), 0.17, fc=color, ec="white", lw=2, zorder=3))
    ax.text(x, y + (0.62 if up else -0.42), h, ha="center", fontsize=8.5, family="monospace", color=GREY)
    ax.text(x + dx, y + 0.34, msg, ha=ha, fontsize=8.5, color=INK)


def line(x0, y0, x1, y1, color):
    ax.plot([x0, x1], [y0, y1], color=color, lw=2.4, zorder=1, solid_capstyle="round")


main = [(0.9, "initial commit", "a1b2c3d"), (2.5, "key to .env", "9f8e7d6"), (5, "crawl 3 pages", "4c5d6e7")]
for x, m, h in main:
    if m == "crawl 3 pages":
        commit(x, 0.6, BLUE, m, h, dx=0.1, ha="right")
    else:
        commit(x, 0.6, BLUE, m, h)
line(0.9, 0.6, 5, 0.6, BLUE)
line(5, 0.6, 6.9, 0.6, BLUE)
# feature branch
line(5, 0.6, 6, 1.9, GREEN); line(6, 1.9, 8, 1.9, GREEN); line(8, 1.9, 9.2, 0.6, GREEN)
commit(6, 1.9, GREEN, "add rating", "b7c8d9e", up=True)
commit(8, 1.9, GREEN, "fix price", "e1f2a3b", up=True)
commit(6.9, 0.6, BLUE, "add docs", "0d1c2b3")
line(6.9, 0.6, 9.2, 0.6, BLUE)
commit(9.2, 0.6, ORANGE, "merge commit", "5a6b7c8")
line(9.2, 0.6, 11, 0.6, BLUE)
ax.text(11.15, 0.6, "main", fontsize=11, weight="bold", color=BLUE, va="center", family="monospace")
ax.text(8.6, 1.85, "new-feature", fontsize=11, weight="bold", color=GREEN, family="monospace")
ax.annotate("", xy=(11, 0.6), xytext=(10.7, 0.6))
fig.savefig(OUT / "history_graph.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)

# 3. the pull request loop --------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 2.1))
ax.set_xlim(0, 12.6); ax.set_ylim(0, 2.6); ax.axis("off")
steps = [("1 Branch", "git switch -c\nidea", BLUE), ("2 Commit, push", "git push -u\norigin idea", GREEN),
         ("3 Pull request", "describe it,\nread the diff", ORANGE), ("4 Checks", "tests run:\ngreen tick", GREEN),
         ("5 Merge", "then on your\nlaptop: git pull", INK)]
for i, (t, s, c) in enumerate(steps):
    x = 0.05 + i * 2.53
    box(ax, x, 0.5, 2.15, 1.5, t, s, c, fs=(9, 8.5))
    if i < 4:
        ax.add_patch(FancyArrowPatch((x + 2.2, 1.25), (x + 2.5, 1.25), arrowstyle="-|>", mutation_scale=14, lw=1.8, color=GREY))
fig.savefig(OUT / "pr_loop.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("ok")
