"""Draw the explanatory figures used in PandasLab.ipynb.

Usage:  python make_figures.py [path/to/online.zip]
The PNG files are written next to this script.  Only the box-plot figure reads
the data (to use the real message lengths); the others are drawn from fixed values.
"""
import json
import sys
import zipfile
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch, Rectangle

matplotlib.use("Agg")

OUT = Path(__file__).parent
BLUE, LBLUE = "#3b6fb6", "#dce8f7"
ORANGE, LORANGE = "#e08a2c", "#fbe9d3"
INK, GRAY, LGRAY = "#222222", "#6b6b6b", "#efefef"
SCALE = 0.6   # inches per drawing unit


def canvas(w, h):
    fig = plt.figure(figsize=(w * SCALE, h * SCALE), dpi=200, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def text(ax, x, y, s, fs=9, color=INK, ha="center", va="center", mono=False, weight="normal", style="normal"):
    ax.text(x, y, s, fontsize=fs, color=color, ha=ha, va=va, weight=weight, style=style,
            family="monospace" if mono else "DejaVu Sans")


def rect(ax, x, y, w, h, fc="white", ec=INK, lw=1.0, ls="-", z=1):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))


def arrow(ax, p0, p1, color=INK, lw=1.6, style="-|>", rad=0.0):
    ax.annotate("", xy=p1, xytext=p0, zorder=5,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw, shrinkA=0, shrinkB=0,
                                connectionstyle=f"arc3,rad={rad}"))


def table(ax, x, y_top, colw, header, rows, rh=0.7, hh=0.7, fs=8.5, mono=False,
          fills=None, hfills=None, index=None, iw=0.9, tcolors=None, dtypes=None):
    """Draw a table; returns (column x edges, header centre y, row centre ys, index x edges)."""
    fills, hfills, tcolors = fills or {}, hfills or {}, tcolors or {}
    xs = [x + (iw if index is not None else 0)]
    for w in colw:
        xs.append(xs[-1] + w)
    y = y_top
    if index is not None:
        rect(ax, x, y - hh, iw, hh, fc=LGRAY)
    for c, name in enumerate(header):
        rect(ax, xs[c], y - hh, colw[c], hh, fc=hfills.get(c, LGRAY))
        text(ax, xs[c] + colw[c] / 2, y - hh / 2, name, fs=fs, weight="bold", mono=mono)
    hc = y - hh / 2
    y -= hh
    if dtypes is not None:
        for c, d in enumerate(dtypes):
            rect(ax, xs[c], y - 0.45, colw[c], 0.45, fc="white", ec=GRAY, lw=0.6)
            text(ax, xs[c] + colw[c] / 2, y - 0.225, d, fs=fs - 1.5, color=GRAY, mono=True)
        if index is not None:
            rect(ax, x, y - 0.45, iw, 0.45, fc="white", ec=GRAY, lw=0.6)
        y -= 0.45
    ys = []
    for r, row in enumerate(rows):
        if index is not None:
            rect(ax, x, y - rh, iw, rh, fc=LGRAY)
            text(ax, x + iw / 2, y - rh / 2, str(index[r]), fs=fs, weight="bold")
        for c, val in enumerate(row):
            rect(ax, xs[c], y - rh, colw[c], rh, fc=fills.get((r, c), "white"))
            text(ax, xs[c] + colw[c] / 2, y - rh / 2, val, fs=fs, mono=mono,
                 color=tcolors.get((r, c), INK))
        ys.append(y - rh / 2)
        y -= rh
    return xs, hc, ys, y


# ---------------------------------------------------------------------- part 1
def fig_json_to_row():
    w, h = 19.5, 6.2
    fig, ax = canvas(w, h)
    text(ax, 3.2, 5.6, "One JSON file = one conversation", fs=11, weight="bold")
    rect(ax, 0.3, 0.9, 5.8, 4.4, fc="#fafafa")
    lines = [
        ("{", None),
        ('  "timestamp": "26-02-09-19-01",', None),
        ('  "id": "1327e2a5-f931-...",', None),
        ('  "users": ["loyal-pool", "jet-boom", ...],', ORANGE),
        ('  "moderator": "moderator",', None),
        ('  "ctx_length": 3,', None),
        ('  "logs": [{"name": ..., "text": ...}, ...]', ORANGE),
        ("}", None),
    ]
    for i, (ln, col) in enumerate(lines):
        text(ax, 0.5, 4.85 - i * 0.5, ln, fs=7.6, ha="left", mono=True, color=col or INK,
             weight="bold" if col else "normal")
    text(ax, 13.2, 4.7, "pd.DataFrame([raw]):  one row, one column per key", fs=11, weight="bold")
    arrow(ax, (6.2, 3.1), (7.7, 3.1))
    colw = [2.0, 1.9, 1.7, 1.8, 1.6, 1.8]
    table(ax, 7.9, 3.7, colw,
          ["timestamp", "id", "users", "moderator", "ctx_length", "logs"],
          [["26-02-09-19-01", "1327e2a5-f9...", "[7 names]", "moderator", "3", "[32 messages]"]],
          fs=7.8, fills={(0, 2): LORANGE, (0, 5): LORANGE}, tcolors={(0, 2): INK, (0, 5): INK},
          hfills={2: LORANGE, 5: LORANGE})
    text(ax, 13.2, 1.7, "The orange keys hold lists, and a list stays inside one cell.\n"
         "That is why the data is called nested.", fs=9.5, color=GRAY)
    fig.savefig(OUT / "fig1_json_to_row.png")


def fig_folders_to_table():
    w, h = 19.5, 6.8
    fig, ax = canvas(w, h)
    text(ax, 3.7, 6.3, "24 folders x 30 files", fs=11, weight="bold")
    names = ["llama70b_constructive_communications.txt", "llama70b_erulemaking.txt", "llama70b_nomod",
             "llama70b_vanilla.txt", "...", "qwen7b_vanilla.txt"]
    for i, n in enumerate(names):
        y = 5.4 - i * 0.85
        if n == "...":
            text(ax, 3.7, y + 0.3, "...", fs=14, color=GRAY)
            continue
        rect(ax, 0.3, y, 6.8, 0.65, fc=LBLUE, ec=BLUE)
        text(ax, 0.5, y + 0.325, n, fs=8, ha="left", mono=True)
    text(ax, 3.7, 0.0 + 0.35, "each folder holds 30 .json files", fs=9, color=GRAY)
    arrow(ax, (7.4, 3.4), (8.7, 3.4))
    text(ax, 8.05, 4.1, "loop over\nfolders\nand files", fs=8.5, color=GRAY)
    text(ax, 14.2, 6.3, "one DataFrame: 720 rows", fs=11, weight="bold")
    colw = [1.6, 1.6, 1.6, 4.2]
    rows = [["1327e2a5...", "[7 names]", "[32 messages]", "llama70b_constructive_communications.txt"],
            ["b3805d66...", "[7 names]", "[32 messages]", "llama70b_constructive_communications.txt"],
            ["70da56c7...", "[7 names]", "[32 messages]", "llama70b_constructive_communications.txt"],
            ["...", "...", "...", "..."],
            ["cc1e33d9...", "[7 names]", "[32 messages]", "qwen7b_vanilla.txt"]]
    table(ax, 8.9, 5.8, colw, ["id", "users", "logs", "experiment"], rows, fs=7.4, rh=0.75,
          hfills={3: LBLUE}, fills={(r, 3): LBLUE for r in range(5)})
    text(ax, 14.2, 0.6, "+ timestamp, moderator and ctx_length columns (not shown)\n"
         "experiment = the folder name: it keeps the model and the moderation setting", fs=8.5, color=GRAY)
    fig.savefig(OUT / "fig1_folders_to_table.png")


# ---------------------------------------------------------------------- part 2
def fig_dataframe_anatomy():
    w, h = 16.2, 7.2
    fig, ax = canvas(w, h)
    colw = [4.3, 2.0, 1.6, 1.8]
    rows = [["llama70b_constructive_communications.txt", "1", "7", "32"],
            ["llama70b_constructive_communications.txt", "1", "7", "32"],
            ["llama70b_nomod", "0", "7", "17"]]
    xs, hc, ys, ybot = table(ax, 2.6, 5.4, colw, ["experiment", "has_moderator", "n_users", "n_messages"],
                             rows, fs=8.3, index=[0, 1, 2], iw=1.0, dtypes=["str", "int64", "int64", "int64"])
    text(ax, 2.6 + 0.5, 6.0, "DataFrame", fs=11, weight="bold", ha="left", color=INK)
    # labels
    text(ax, 1.1, 1.5, "index\n(row labels)", fs=9.5, color=ORANGE, weight="bold")
    arrow(ax, (1.1, 2.0), (2.9, ys[2]), color=ORANGE, rad=-0.2)
    text(ax, 7.5, 0.9, "values", fs=9.5, color=ORANGE, weight="bold")
    arrow(ax, (7.5, 1.3), (7.5, ybot + 0.05), color=ORANGE)
    text(ax, 8.0, 6.4, "column names", fs=9.5, color=ORANGE, weight="bold")
    arrow(ax, (8.0, 6.05), (8.0, hc + 0.3), color=ORANGE)
    dy = 5.4 - 0.7 - 0.225
    text(ax, 14.7, dy, "dtype of\neach column", fs=9.5, color=ORANGE, weight="bold")
    arrow(ax, (13.95, dy), (xs[3] + colw[3] + 0.08, dy), color=ORANGE)
    # one column = Series
    rect(ax, xs[3], ybot, colw[3], 5.4 - ybot, fc="none", ec=BLUE, lw=2.4, z=6)
    text(ax, xs[3] + colw[3] / 2, 1.35, "one column\n= a Series", fs=9.5, color=BLUE, weight="bold")
    fig.savefig(OUT / "fig2_dataframe_anatomy.png")


def fig_missing_to_flag():
    w, h = 13.0, 5.4
    fig, ax = canvas(w, h)
    text(ax, 2.4, 4.9, "df[\"moderator\"]", fs=10, mono=True, weight="bold")
    table(ax, 0.6, 4.4, [2.6], ["moderator"], [["moderator"], ["moderator"], ["NaN"], ["NaN"]],
          fs=9, index=[0, 1, 2, 3], iw=0.8, fills={(2, 0): LORANGE, (3, 0): LORANGE})
    arrow(ax, (4.7, 2.6), (7.1, 2.6))
    text(ax, 5.9, 3.2, ".notna()\n.astype(int)", fs=9, mono=True, color=GRAY)
    text(ax, 9.7, 4.9, "df[\"has_moderator\"]", fs=10, mono=True, weight="bold")
    table(ax, 7.9, 4.4, [3.2], ["has_moderator"], [["1"], ["1"], ["0"], ["0"]],
          fs=9, index=[0, 1, 2, 3], iw=0.8, fills={(2, 0): LORANGE, (3, 0): LORANGE})
    text(ax, 6.5, 0.45, "missing (NaN) = no moderator = 0      moderator present = 1", fs=9.5, color=GRAY)
    fig.savefig(OUT / "fig2_missing_to_flag.png")


def fig_series_vs_frame():
    w, h = 15.0, 5.4
    fig, ax = canvas(w, h)
    text(ax, 3.5, 4.95, 'df["id"]', fs=11, mono=True, weight="bold")
    table(ax, 1.2, 4.45, [3.4], ["id"], [["1327e2a5-f931..."], ["b3805d66-7317..."], ["70da56c7-4b0d..."]],
          fs=8.5, index=[0, 1, 2], iw=0.8)
    text(ax, 3.7, 0.75, "single brackets: a Series\n(one column, 1-D)", fs=9.5, color=BLUE, weight="bold")
    text(ax, 11.0, 4.95, 'df[["id"]]', fs=11, mono=True, weight="bold")
    table(ax, 8.7, 4.45, [3.4], ["id"], [["1327e2a5-f931..."], ["b3805d66-7317..."], ["70da56c7-4b0d..."]],
          fs=8.5, index=[0, 1, 2], iw=0.8, hfills={0: LBLUE}, fills={(r, 0): LBLUE for r in range(3)})
    text(ax, 10.7, 0.75, "double brackets: a DataFrame\n(a list of names, 2-D)", fs=9.5, color=BLUE, weight="bold")
    fig.savefig(OUT / "fig2_series_vs_dataframe.png")


# ---------------------------------------------------------------------- part 3
def fig_loc_iloc():
    w, h = 20.0, 7.8
    fig, ax = canvas(w, h)
    colw = [1.9, 1.7, 2.0]
    header = ["has_moderator", "n_users", "n_messages"]
    rows = [["1", "7", "32"]] * 5 + [["0", "7", "17"]]

    def panel(x0, title, code, sel, stop_row, note, label_head):
        text(ax, x0 + 3.0, 6.9, title, fs=11, weight="bold")
        text(ax, x0 + 3.0, 6.35, code, fs=10.5, mono=True, color=BLUE, weight="bold")
        xs, hc, ys, ybot = table(ax, x0 + 0.5, 5.8, colw, header, rows, fs=8.2, rh=0.65, hh=0.8,
                                 index=[0, 1, 2, 3, 4, 5], iw=1.0,
                                 fills={(r, c): LBLUE for r in sel for c in range(3)})
        text(ax, x0 + 1.0, 5.8 - 0.4, label_head, fs=7.2, color=GRAY, weight="bold")
        for r in sel:
            rect(ax, x0 + 0.5, ys[r] - 0.325, 1.0, 0.65, fc=BLUE, ec=INK)
            text(ax, x0 + 1.0, ys[r], str(r), fs=8.5, weight="bold", color="white")
        if stop_row is not None:
            rect(ax, x0 + 0.5, ys[stop_row] - 0.325, 1.0 + sum(colw), 0.65, fc="none", ec=ORANGE, lw=2.2, ls="--", z=6)
            text(ax, x0 + 7.3, ys[stop_row], "stop here\n(not included)", fs=8.5, color=ORANGE, weight="bold", ha="left")
        text(ax, x0 + 3.5, 0.6, note, fs=9.5, color=INK)

    panel(0.3, "by position", "df.iloc[1:4]", [1, 2, 3], 4,
          "3 rows: positions 1, 2, 3\nthe end (4) is excluded, like a Python list", "position")
    panel(10.3, "by label", "df.loc[1:4]", [1, 2, 3, 4], None,
          "4 rows: labels 1, 2, 3, 4\nthe end (4) is included", "label")
    text(ax, 10.0, 7.55, "Here labels and positions are both 0, 1, 2, ... (the default index). "
         "After filtering or sorting they differ.", fs=8.8, color=GRAY)
    fig.savefig(OUT / "fig3_loc_vs_iloc.png")


# ---------------------------------------------------------------------- part 4
def fig_explode():
    w, h = 24.0, 7.0
    fig, ax = canvas(w, h)
    text(ax, 3.4, 6.4, "before: one row per conversation", fs=10.5, weight="bold")
    table(ax, 0.3, 5.8, [1.5, 3.2], ["id", "logs"],
          [["a1f3...", "[msg 1, msg 2, msg 3]"], ["b7c9...", "[msg 1, msg 2]"]],
          fs=8.5, rh=0.8, fills={(0, 1): LORANGE, (1, 1): LORANGE}, hfills={1: LORANGE})
    arrow(ax, (5.3, 4.5), (6.9, 4.5))
    text(ax, 6.1, 5.15, ".explode(\"logs\")", fs=8.2, mono=True, color=GRAY)
    text(ax, 10.2, 6.4, "after explode: one row per message", fs=10.5, weight="bold")
    table(ax, 7.1, 5.8, [1.5, 2.4], ["id", "logs"],
          [["a1f3...", "msg 1"], ["a1f3...", "msg 2"], ["a1f3...", "msg 3"], ["b7c9...", "msg 1"], ["b7c9...", "msg 2"]],
          fs=8.5, rh=0.7, fills={(r, 0): LBLUE for r in range(5)}, hfills={0: LBLUE})
    text(ax, 9.05, 0.9, "the id is repeated\nfor every message", fs=8.8, color=BLUE, weight="bold")
    arrow(ax, (11.3, 3.6), (13.7, 3.6))
    text(ax, 12.5, 4.45, 'logs.str["name"]\nlogs.str["text"]\nlogs.str["model"]', fs=7.2, mono=True, color=GRAY)
    text(ax, 18.7, 6.4, "after .str[...]: one column per dict key", fs=10.5, weight="bold")
    table(ax, 14.0, 5.8, [1.3, 2.7, 3.2, 2.2], ["id", "speaker", "text", "written_by"],
          [["a1f3...", "grave-convergence", "Not all Trump voters...", "hardcoded"],
           ["a1f3...", "camel-conduit", "So far, he's only...", "hardcoded"],
           ["a1f3...", "grizzled-wireframe", "I see what you're...", "llama70b"],
           ["b7c9...", "noisy-centroid", "&gt;And yet...", "hardcoded"],
           ["b7c9...", "moderator", "\"\"", "qwen7b"]],
          fs=7.2, rh=0.7, hfills={1: LBLUE, 2: LBLUE, 3: LBLUE},
          fills={(r, c): LBLUE for r in range(5) for c in (1, 2, 3)})
    text(ax, 18.7, 0.9, "one row per message, ready to analyse", fs=8.8, color=BLUE, weight="bold")
    fig.savefig(OUT / "fig4_explode.png")


def fig_boxplot(zip_path):
    lens = []
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if name.endswith(".json"):
                for m in json.loads(z.read(name))["logs"]:
                    lens.append(len(m["text"]))
    s = pd.Series(lens)
    q1, med, q3 = s.quantile([0.25, 0.5, 0.75])
    iqr = q3 - q1
    lo = s[s >= q1 - 1.5 * iqr].min()
    hi = s[s <= q3 + 1.5 * iqr].max()
    fig = plt.figure(figsize=(10, 3.8), dpi=200, facecolor="white")
    ax = fig.add_axes([0.04, 0.2, 0.92, 0.72])
    ax.boxplot(s, vert=False, widths=0.5, showfliers=True, whis=1.5,
               boxprops=dict(color=BLUE, lw=1.6), medianprops=dict(color=ORANGE, lw=2.4),
               whiskerprops=dict(color=BLUE, lw=1.6), capprops=dict(color=BLUE, lw=1.6),
               flierprops=dict(marker="o", markerfacecolor="none", markeredgecolor=GRAY, markersize=3))
    ax.set_xlim(-60, 1700)
    ax.set_yticks([])
    ax.set_xlabel("characters per message", fontsize=9)
    ax.spines[["top", "right", "left"]].set_visible(False)

    def label(x, txt, y, color=INK, ha="center", dx=0):
        top = y > 1
        ax.annotate(txt, xy=(x, 1.0 + (0.27 if top else -0.27)), xytext=(x + dx, y), ha=ha, va="center",
                    fontsize=8.5, color=color, arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8))

    label(lo, f"lowest value within\nthe whiskers ({lo})", 1.85)
    label(med, f"median: the middle\nmessage ({med:.0f})", 1.85, ORANGE)
    label(hi, f"upper whisker: Q3 + 1.5 x IQR\n({hi})", 1.85)
    label(q1, f"Q1: 25% of messages\nare shorter ({q1:.0f})", 0.1, ha="right", dx=-25)
    label(q3, f"Q3: 75% of messages\nare shorter ({q3:.0f})", 0.1, ha="left", dx=25)
    ax.text((q1 + q3) / 2 + 60, 1.0, "IQR", ha="center", va="center", fontsize=9, color=BLUE, weight="bold")
    ax.text(1050, 1.85, "IQR = Q3 - Q1 (the box)\npoints beyond the whiskers\nare drawn as outliers",
            ha="left", va="center", fontsize=8.5, color=BLUE)
    ax.text(1690, 0.55, f"outliers continue up to {s.max():,}  >>>", ha="right", va="center", fontsize=8.5, color=GRAY)
    ax.set_ylim(-0.3, 2.3)
    fig.savefig(OUT / "fig4_boxplot_anatomy.png")


# ---------------------------------------------------------------------- part 5
def fig_boolean_mask():
    w, h = 22.0, 6.6
    fig, ax = canvas(w, h)
    rows = [["moderator", '""'], ["quiet-right", "I disagree..."], ["moderator", "Thanks @a, ..."],
            ["gilded-grantor", '""'], ["moderator", '""']]
    empty = [True, False, False, True, True]
    text(ax, 3.4, 6.1, "msgs", fs=10.5, weight="bold", mono=True)
    table(ax, 0.3, 5.6, [2.0, 2.4], ["speaker", "text"], rows, fs=8.2, rh=0.75, index=[0, 1, 2, 3, 4], iw=0.7)
    arrow(ax, (6.0, 3.4), (7.7, 3.4))
    text(ax, 6.85, 4.1, 'msgs["text"]\n== \'""\'', fs=7.6, mono=True, color=GRAY)
    text(ax, 9.4, 6.1, "mask", fs=10.5, weight="bold", mono=True)
    table(ax, 8.0, 5.6, [2.0], ["text"], [[str(e)] for e in empty], fs=8.4, rh=0.75,
          index=[0, 1, 2, 3, 4], iw=0.7,
          fills={(r, 0): (LBLUE if e else "white") for r, e in enumerate(empty)})
    arrow(ax, (11.2, 3.4), (12.9, 3.4))
    text(ax, 12.05, 4.1, "msgs[mask]", fs=7.6, mono=True, color=GRAY)
    text(ax, 16.4, 6.1, "only the rows marked True", fs=10.5, weight="bold")
    keep = [r for r, e in zip(rows, empty) if e]
    table(ax, 13.2, 5.6, [2.0, 2.4], ["speaker", "text"], keep, fs=8.2, rh=0.75, index=[0, 3, 4], iw=0.7,
          fills={(r, c): LBLUE for r in range(3) for c in (0, 1)})
    text(ax, 16.2, 1.7, "the original labels (0, 3, 4) are kept", fs=8.8, color=BLUE, weight="bold")
    text(ax, 11.0, 0.5, "a comparison on a whole column gives a True/False for every row; "
         "putting that mask in [ ] keeps the True rows", fs=9.2, color=GRAY)
    fig.savefig(OUT / "fig5_boolean_mask.png")


# ---------------------------------------------------------------------- part 6
def fig_cleaning_pipeline():
    w, h = 24.0, 5.2
    fig, ax = canvas(w, h)
    steps = [("raw", '"Thanks @quiet-right,\nlet\'s keep it CIVIL."', ""),
             ("strip quotes", "Thanks @quiet-right,\nlet's keep it CIVIL.", ".str.strip('\" ')"),
             ("drop mentions", "Thanks ,\nlet's keep it CIVIL.", ".str.replace(regex)"),
             ("lowercase", "thanks ,\nlet's keep it civil.", ".str.lower()"),
             ("tidy spaces", "thanks , let's\nkeep it civil.", ".str.split().str.join(' ')")]
    bw, gap, x = 3.9, 0.9, 0.3
    for i, (title, ex, code) in enumerate(steps):
        fc = LORANGE if i == 0 else (LBLUE if i == len(steps) - 1 else "white")
        rect(ax, x, 1.3, bw, 2.4, fc=fc, ec=INK)
        text(ax, x + bw / 2, 4.2, title, fs=10, weight="bold")
        text(ax, x + bw / 2, 2.5, ex, fs=7.4, mono=True)
        if code:
            text(ax, x + bw / 2, 0.8, code, fs=6.8, mono=True, color=GRAY)
        if i < len(steps) - 1:
            arrow(ax, (x + bw + 0.1, 2.5), (x + bw + gap - 0.1, 2.5))
        x += bw + gap
    fig.savefig(OUT / "fig6_cleaning_pipeline.png")


# ---------------------------------------------------------------------- part 7
def fig_date_parts():
    w, h = 20.0, 5.6
    fig, ax = canvas(w, h)
    rect(ax, 5.5, 4.0, 9.0, 1.1, fc=LBLUE, ec=INK)
    text(ax, 10.0, 4.55, "2026-02-09 19:01:00", fs=14, mono=True, weight="bold")
    text(ax, 10.0, 5.35, 'df["timestamp"]  (datetime64)', fs=9, color=GRAY, mono=True)
    parts = [(".dt.year", "2026"), (".dt.month", "2"), (".dt.day", "9"), (".dt.hour", "19"),
             (".dt.minute", "1"), (".dt.day_name()", "Monday")]
    x0, bw, gap = 0.5, 2.7, 0.35
    for i, (code, val) in enumerate(parts):
        x = x0 + i * (bw + gap)
        arrow(ax, (10.0, 4.0), (x + bw / 2, 2.55), lw=1.0, color=GRAY)
        rect(ax, x, 1.2, bw, 1.3, fc="white", ec=INK)
        text(ax, x + bw / 2, 1.85, val, fs=12, weight="bold")
        text(ax, x + bw / 2, 0.7, code, fs=7.6, mono=True, color=GRAY)
    fig.savefig(OUT / "fig7_date_parts.png")


# ---------------------------------------------------------------------- part 8
def fig_groupby():
    w, h = 24.0, 6.6
    fig, ax = canvas(w, h)
    rows = [["llama8b", "4"], ["qwen7b", "2"], ["llama8b", "3"], ["qwen7b", "2"], ["llama8b", "5"]]
    grp = [0, 1, 0, 1, 0]
    text(ax, 2.6, 6.2, "df", fs=10.5, weight="bold", mono=True)
    table(ax, 0.3, 5.7, [2.2, 1.8], ["model", "gap_min"], rows, fs=8.4, rh=0.7, index=[0, 1, 2, 3, 4], iw=0.7,
          fills={(r, 0): (LBLUE if g == 0 else LORANGE) for r, g in enumerate(grp)})
    arrow(ax, (5.9, 3.7), (7.5, 3.7))
    text(ax, 6.7, 4.4, 'groupby("model")', fs=7.6, mono=True, color=GRAY)
    text(ax, 10.6, 6.2, "split: one small table per group", fs=10, weight="bold")
    table(ax, 7.8, 5.7, [1.6, 1.4], ["model", "gap_min"], [["llama8b", "4"], ["llama8b", "3"], ["llama8b", "5"]],
          fs=8, rh=0.65, hh=0.65, fills={(r, c): LBLUE for r in range(3) for c in (0, 1)},
          hfills={0: LBLUE, 1: LBLUE})
    table(ax, 7.8, 2.9, [1.6, 1.4], ["model", "gap_min"], [["qwen7b", "2"], ["qwen7b", "2"]],
          fs=8, rh=0.65, hh=0.65, fills={(r, c): LORANGE for r in range(2) for c in (0, 1)},
          hfills={0: LORANGE, 1: LORANGE})
    arrow(ax, (11.3, 3.7), (13.7, 3.7))
    text(ax, 12.5, 4.4, '["gap_min"]\n.median()', fs=7.6, mono=True, color=GRAY)
    text(ax, 16.4, 6.2, "apply + combine: one number per group", fs=10, weight="bold")
    table(ax, 14.0, 5.7, [1.6, 1.4], ["model", "gap_min"], [["llama8b", "4"], ["qwen7b", "2"]], fs=8, rh=0.65, hh=0.65,
          fills={(0, 0): LBLUE, (0, 1): LBLUE, (1, 0): LORANGE, (1, 1): LORANGE})
    fig.savefig(OUT / "fig8_groupby.png")


def fig_merge():
    w, h = 24.0, 6.0
    fig, ax = canvas(w, h)
    text(ax, 2.9, 5.6, "msgs", fs=10.5, weight="bold", mono=True)
    table(ax, 0.3, 5.1, [1.6, 2.4], ["conv_id", "text"], [["a1", "I agree..."], ["a1", "Thanks @..."], ["b7", "Hmm..."]],
          fs=8.4, rh=0.7, hfills={0: LBLUE}, fills={(r, 0): LBLUE for r in range(3)})
    text(ax, 2.9, 1.9, "one row per message", fs=8.5, color=GRAY)
    text(ax, 8.4, 5.6, "df", fs=10.5, weight="bold", mono=True)
    table(ax, 6.2, 5.1, [1.2, 2.2], ["id", "setting"], [["a1", "vanilla"], ["b7", "nomod"]],
          fs=8.4, rh=0.7, hfills={0: LBLUE}, fills={(r, 0): LBLUE for r in range(2)})
    text(ax, 7.9, 2.6, "one row per conversation", fs=8.5, color=GRAY)
    arrow(ax, (10.1, 3.6), (12.1, 3.6))
    text(ax, 11.1, 4.4, 'msgs.merge(df,\nleft_on="conv_id",\nright_on="id")', fs=7.2, mono=True, color=GRAY)
    text(ax, 17.0, 5.6, "result: every message gets the setting of its conversation", fs=10, weight="bold")
    table(ax, 12.4, 5.1, [1.6, 2.4, 1.2, 2.2], ["conv_id", "text", "id", "setting"],
          [["a1", "I agree...", "a1", "vanilla"], ["a1", "Thanks @...", "a1", "vanilla"], ["b7", "Hmm...", "b7", "nomod"]],
          fs=8.4, rh=0.7, hfills={0: LBLUE, 2: LBLUE, 3: LORANGE},
          fills={**{(r, 0): LBLUE for r in range(3)}, **{(r, 2): LBLUE for r in range(3)},
                 **{(r, 3): LORANGE for r in range(3)}})
    text(ax, 17.0, 1.9, "rows are matched by the key: same number of rows as msgs", fs=8.5, color=BLUE, weight="bold")
    ax.set_ylim(1.4, h)                                   # nothing is drawn below 1.4: crop the empty strip
    fig.set_size_inches(w * SCALE, (h - 1.4) * SCALE)
    fig.savefig(OUT / "fig8_merge.png")


def fig_join_types():
    w, h = 24.0, 9.4
    fig, ax = canvas(w, h)
    # the two input tables
    text(ax, 3.0, 9.0, "A: gap_table", fs=10.5, weight="bold", mono=True)
    table(ax, 0.8, 8.6, [2.2, 1.6], ["model", "gap_min"],
          [["qwen7b", "2"], ["llama8b", "4"], ["llama70b", "14"]], fs=8.4, rh=0.62, hh=0.62,
          fills={(0, 0): LORANGE, (0, 1): LORANGE, (1, 0): LBLUE, (1, 1): LBLUE, (2, 0): LBLUE, (2, 1): LBLUE},
          hfills={0: LBLUE})
    text(ax, 11.0, 9.0, "B: model_info", fs=10.5, weight="bold", mono=True)
    table(ax, 8.8, 8.6, [2.2, 1.8], ["model", "billions"],
          [["llama8b", "8"], ["llama70b", "70"], ["gemma9b", "9"]], fs=8.4, rh=0.62, hh=0.62,
          fills={(0, 0): LBLUE, (0, 1): LBLUE, (1, 0): LBLUE, (1, 1): LBLUE, (2, 0): LORANGE, (2, 1): LORANGE},
          hfills={0: LBLUE})
    text(ax, 17.5, 8.0, "the key is `model`:\nblue = found in both tables\norange = found in only one", fs=8.8, color=GRAY, ha="left")
    # the three results
    cols = ["model", "gap_min", "billions"]
    cw = [1.9, 1.4, 1.5]
    results = [
        ("how=\"inner\"", "only keys found in both", 0.4,
         [["llama8b", "4", "8"], ["llama70b", "14", "70"]], {}),
        ("how=\"left\"", "every row of A", 8.3,
         [["qwen7b", "2", "NaN"], ["llama8b", "4", "8"], ["llama70b", "14", "70"]], {(0, 2): LORANGE}),
        ("how=\"outer\"", "every row of A and of B", 16.2,
         [["qwen7b", "2", "NaN"], ["llama8b", "4", "8"], ["llama70b", "14", "70"], ["gemma9b", "NaN", "9"]],
         {(0, 2): LORANGE, (3, 1): LORANGE}),
    ]
    for title, sub, x, rows, fills in results:
        text(ax, x + 2.4, 5.2, title, fs=10.5, weight="bold", mono=True)
        text(ax, x + 2.4, 4.65, sub, fs=8.8, color=GRAY)
        table(ax, x, 4.2, cw, cols, rows, fs=8.4, rh=0.62, hh=0.62, fills=fills)
    fig.savefig(OUT / "fig8_join_types.png")


if __name__ == "__main__":
    zip_path = sys.argv[1] if len(sys.argv) > 1 else "online.zip"
    fig_json_to_row()
    fig_folders_to_table()
    fig_dataframe_anatomy()
    fig_missing_to_flag()
    fig_series_vs_frame()
    fig_loc_iloc()
    fig_explode()
    fig_boxplot(zip_path)
    fig_boolean_mask()
    fig_cleaning_pipeline()
    fig_date_parts()
    fig_groupby()
    fig_merge()
    fig_join_types()
    print("done")
