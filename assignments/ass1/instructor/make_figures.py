"""Draws the figures used in student/assignment1_student.md.

Run from anywhere:  python instructor/make_figures.py
Writes into ../student/figures/.
Needs only matplotlib. Writes pipeline.png, persona_grid.png, label_scale.png and annotator_anatomy.png.
Colours: blue, orange and aqua are the first three slots of a colour-blind-safe categorical palette;
every box also carries a text label, so colour is never the only signal.
All four figures have exactly the same width (12 inches, 1 unit = 1 inch), so that at the same display width
their text has the same size.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

INK, MUTED = "#0b0b0b", "#52514e"
BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#6b6a66"
TINT = {BLUE: "#e6f0fc", ORANGE: "#fdeee7", AQUA: "#e3f6ee", GREY: "#efefec"}
# one-hue ordinal ramp for the 1-5 scale (steps 250, 350, 450, 550, 650 of the blue ramp)
RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281"]
DPI = 160
WIDTH = 12.0  # inches, the same for every figure; content lives between x = 0 and x = 11.8


def canvas(ymin, ymax):
    """A WIDTH-wide figure whose axes fill it, 1 unit = 1 inch both ways, so nothing is stretched."""
    fig = plt.figure(figsize=(WIDTH, ymax - ymin))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-0.1, WIDTH - 0.1)
    ax.set_ylim(ymin, ymax)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, title, sub, color, title_size=10, sub_size=9.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12", fc=TINT[color], ec=color, lw=2))
    ax.text(x + w / 2, y + h * 0.67, title, ha="center", va="center", fontsize=title_size, fontweight="bold", color=INK)
    ax.text(x + w / 2, y + h * 0.30, sub, ha="center", va="center", fontsize=sub_size, color=MUTED, linespacing=1.3)


def arrow(ax, p, q, color=MUTED):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, lw=1.8, color=color, shrinkA=0, shrinkB=0))


OUT = Path(__file__).resolve().parent.parent / "student" / "figures"


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, dpi=DPI, facecolor="white")  # no cropping: every figure keeps the same width
    plt.close(fig)
    print("wrote", name)


def pipeline():
    fig, ax = canvas(-0.42, 4.25)
    w, h, gap = 1.72, 0.92, 0.28
    xs = [0.05 + i * (w + gap) for i in range(6)]
    top, mid, bot = 2.55, 1.55, 0.55  # bottom edges of the three rows
    cy = lambda y: y + h / 2

    # the whole model part gets one frame, so that it reads as one thing next to the human part
    fx0, fx1 = xs[2] - 0.14, xs[3] + w + 0.14
    fy0, fy1 = bot - 0.25, top + h + 0.72
    ax.add_patch(FancyBboxPatch((fx0, fy0), fx1 - fx0, fy1 - fy0, boxstyle="round,pad=0,rounding_size=0.18",
                                fc="#f3fbf7", ec=AQUA, lw=2, linestyle=(0, (5, 3)), zorder=0))
    ax.text(fx0 + 0.18, fy1 - 0.2, "Model annotation", ha="left", va="center", fontsize=12.5, fontweight="bold", color=INK)
    ax.text(fx0 + 0.18, fy1 - 0.48, "identities + a baseline, two settings", ha="left", va="center", fontsize=10, color=MUTED)

    box(ax, xs[0], mid, w, h, "A  Load,\nannotate", "20 comments", ORANGE)
    box(ax, xs[1], mid, w, h, "B  Your\nannotations", "check your ratings", ORANGE)
    # branch 1: generate, then annotate with the conversation as context
    box(ax, xs[2], top, w, h, "C  Generate", "one talk per item,\nrandom personas", BLUE)
    box(ax, xs[3], top, w, h, "D  With context", "they read the\ntalk first", AQUA)
    # branch 2: annotate the item alone
    box(ax, xs[2], bot, w, h, "E  No context", "they see the\nitem alone", AQUA)
    box(ax, xs[4], mid, w, h, "F  Agreement", "compare all\nthe labels", GREY)
    box(ax, xs[5], mid, w, h, "G  Story", "what context\nchanges", GREY)

    arrow(ax, (xs[0] + w, cy(mid)), (xs[1], cy(mid)))
    arrow(ax, (xs[1] + w, cy(mid)), (xs[2], cy(top)))
    arrow(ax, (xs[1] + w, cy(mid)), (xs[2], cy(bot)))
    arrow(ax, (xs[2] + w, cy(top)), (xs[3], cy(top)))
    arrow(ax, (xs[3] + w, cy(top)), (xs[4], cy(mid) + 0.28))
    arrow(ax, (xs[2] + w, cy(bot)), (xs[4], cy(mid) - 0.28))
    arrow(ax, (xs[4] + w, cy(mid)), (xs[5], cy(mid)))

    # legend
    lx = 0.05
    for color, label in [(BLUE, "data and generation"), (ORANGE, "human annotation (you)"), (AQUA, "model annotation"), (GREY, "analysis")]:
        ax.add_patch(Rectangle((lx, -0.34), 0.22, 0.22, fc=TINT[color], ec=color, lw=2))
        ax.text(lx + 0.32, -0.23, label, va="center", fontsize=10, color=INK)
        lx += 0.32 + 0.095 * len(label) + 0.55
    save(fig, "pipeline.png")


def persona_grid():
    fig, ax = canvas(0.0, 3.75)
    x0, cw, ch = 2.3, 1.8, 0.62
    top = 2.4  # top edge of the grid rows
    genders = ["woman", "man"]
    politics = ["left", "right"]
    ages = ["under 30", "over 50"]

    ax.text(0.05, 3.55, "A small starting grid (an example): who the annotator is", fontsize=13, fontweight="bold", color=INK, va="center")

    # column headers: who it is (gender, then politics)
    ax.text(x0 - 0.12, 3.05, "gender", ha="right", va="center", fontsize=10.5, color=MUTED, style="italic")
    ax.text(x0 - 0.12, 2.64, "politics", ha="right", va="center", fontsize=10.5, color=MUTED, style="italic")
    for g, gender in enumerate(genders):
        gx = x0 + g * 2 * cw
        ax.add_patch(FancyBboxPatch((gx + 0.04, 2.85), 2 * cw - 0.08, 0.4, boxstyle="round,pad=0,rounding_size=0.08", fc="#d7e6fa", ec=BLUE, lw=1.5))
        ax.text(gx + cw, 3.05, gender, ha="center", va="center", fontsize=12, fontweight="bold", color=INK)
        for p, pol in enumerate(politics):
            ax.text(gx + (p + 0.5) * cw, 2.64, pol, ha="center", va="center", fontsize=11, color=INK)

    # row header: age
    ax.text(0.9, top - ch, "age", rotation=90, ha="center", va="center", fontsize=10.5, color=MUTED, style="italic")

    for r, age in enumerate(ages):
        y = top - (r + 1) * ch
        ax.text(x0 - 0.12, y + ch / 2, age, ha="right", va="center", fontsize=11.5, fontweight="bold", color=INK)
        for c in range(4):
            gender, pol = genders[c // 2], politics[c % 2]
            x = x0 + c * cw
            ax.add_patch(Rectangle((x + 0.04, y + 0.04), cw - 0.08, ch - 0.08, fc=TINT[BLUE], ec=BLUE, lw=1.2))
            ax.text(x + cw / 2, y + ch / 2, f"{gender} / {pol} / {age}", ha="center", va="center", fontsize=9, color=INK)

    # the baseline, next to the grid
    bx = x0 + 4 * cw + 0.35
    box(ax, bx, top - ch - 0.5, 1.85, 1.0, "+ baseline", "no persona at all", ORANGE, title_size=12, sub_size=10)

    ax.text(0.05, 0.18, "Each cell is one persona, and each persona becomes one annotator. This grid is only a starting point: you will adapt it.", fontsize=10.5, color=MUTED)
    save(fig, "persona_grid.png")


def label_scale():
    fig, ax = canvas(0.0, 3.15)
    sw, gap, x0 = 1.75, 0.35, 0.8
    sy, sh = 1.45, 0.95
    for i in range(5):
        x = x0 + i * (sw + gap)
        ax.add_patch(Rectangle((x, sy), sw, sh, fc=RAMP[i], ec="white", lw=2))
        ax.text(x + sw / 2, sy + sh / 2, str(i + 1), ha="center", va="center", fontsize=22, fontweight="bold", color=INK if i < 2 else "white")
    left = x0 + sw / 2
    right = x0 + 4 * (sw + gap) + sw / 2
    ax.text(left, sy - 0.12, "fully civil", ha="center", va="top", fontsize=11, color=INK)
    ax.text(right, sy - 0.12, "very toxic", ha="center", va="top", fontsize=11, color=INK)

    # numeric view (top bracket)
    xa, xb = x0, x0 + 5 * sw + 4 * gap
    ax.plot([xa, xa, xb, xb], [sy + sh + 0.1, sy + sh + 0.24, sy + sh + 0.24, sy + sh + 0.1], color=MUTED, lw=1.5)
    ax.text((xa + xb) / 2, sy + sh + 0.36, "numeric view: five ordered levels  (weighted kappa, Spearman)", ha="center", va="bottom", fontsize=11, color=INK)

    # categorical view (bottom brackets)
    by = 0.78

    def span(i0, i1, label, color):
        xs = x0 + i0 * (sw + gap)
        xe = x0 + i1 * (sw + gap) + sw
        ax.plot([xs, xs, xe, xe], [by + 0.13, by, by, by + 0.13], color=color, lw=2.5)
        ax.text((xs + xe) / 2, by - 0.1, label, ha="center", va="top", fontsize=12, fontweight="bold", color=INK)

    span(0, 1, "civil (1-2)", BLUE)
    span(2, 4, "toxic (3-5)", ORANGE)
    ax.text((xa + xb) / 2, 0.16, "categorical view: two classes  (Cohen's kappa)", ha="center", va="center", fontsize=11, color=INK)
    save(fig, "label_scale.png")


def annotator_anatomy():
    fig, ax = canvas(0.0, 4.1)
    w, h = 4.5, 0.9
    x_in = 0.1  # left edge of the input boxes
    ys = [3.1, 2.1, 1.1, 0.1]
    box(ax, x_in, ys[0], w, h, "Persona  (one per annotator)", "who it is (never how to rate),\nor none (the baseline)", ORANGE, title_size=11.5, sub_size=10)
    box(ax, x_in, ys[1], w, h, "Context  (2 conditions)", "none, or the small talk\nabout the item", AQUA, title_size=11.5, sub_size=10)
    box(ax, x_in, ys[2], w, h, "Instructions  (fixed)", "what the label means,\nanswer with one number from 1 to 5", GREY, title_size=11.5, sub_size=10)
    box(ax, x_in, ys[3], w, h, "Item to label  (fixed)", "one of the 20 comments", GREY, title_size=11.5, sub_size=10)
    box(ax, 5.9, 1.25, 2.4, 1.5, "Annotator-agent", "same model,\nsame settings", GREY, title_size=12, sub_size=10.5)
    box(ax, 9.0, 1.25, 2.7, 1.5, "Label", "a number from 1 to 5", BLUE, title_size=12, sub_size=10.5)
    targets = [2.5, 2.2, 1.8, 1.5]
    colors = [ORANGE, AQUA, MUTED, MUTED]
    for y, t, c in zip(ys, targets, colors):
        arrow(ax, (x_in + w, y + h / 2), (5.9, t), c)
    arrow(ax, (8.3, 2.0), (9.0, 2.0))
    ax.text(8.5, 0.55, "Two things vary: the persona and the context.", ha="center", va="center", fontsize=11.5, style="italic", color=INK)
    save(fig, "annotator_anatomy.png")


if __name__ == "__main__":
    pipeline()
    persona_grid()
    label_scale()
    annotator_anatomy()
