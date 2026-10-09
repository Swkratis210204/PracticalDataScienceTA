# Lab 1: Pandas

A hands-on introduction to pandas. Instead of a toy table, the lab works with a real, messy dataset: **SynDisco**, 720 *synthetic* online discussions in which seven simulated users debate a topic and an LLM moderator may or may not step in. The same setup was run with 6 language models and 4 moderation settings, 30 conversations each.

Along the way we answer simple questions about the data: how is it stored, how long are the conversations, who speaks, and what does the moderator change?

## Contents

| Part | Topic | Status |
|---|---|---|
| 1 | Loading and a first look: nested JSON files into one table, `head`, `info`, `describe`, missing values | ready |
| 2 | Selecting and summarising: `loc`, `iloc`, `explode`, `mean`, `median`, `value_counts`, `replace`, `map`, `clip` | ready |
| 3 | Filtering and cleaning text: boolean masks, `.str`, regex, `drop`, `pop`, arithmetic between columns | ready |
| 4 | Dates and times: `.dt`, differences between dates | ready |
| 5 | Groups and joins: `groupby`, `concat`, `merge` | ready |

Every part opens with its goal, explains each step in short markdown cells, and ends with a **Your turn** exercise (an empty cell to write in, and the solution folded below it) and a list of findings. Each part is a heading, so you can collapse the parts you are not working on.

## Run it

**On Colab:** upload `PandasLab.ipynb`, or, once the repository is on GitHub, open
`https://colab.research.google.com/github/<user>/<repo>/blob/<branch>/labs/lab01-pandas/PandasLab.ipynb`
(replace `<user>`, `<repo>` and `<branch>`). Run the first download cell.

**Locally:** install the requirements from the repository root (`pip install -r requirements.txt`), start `jupyter lab`, open `PandasLab.ipynb` and run the cells from top to bottom. The first two cells download the data: the first uses `wget` and `unzip` (Colab, Linux, Mac); the second is plain Python and works on any system, including Windows. Run one of them, not both.

The notebook needs only pandas and matplotlib. It was run top to bottom with Python 3.14, pandas 2.3.3 and matplotlib 3.11.

Some cells change the table in place (for example the one that drops `moderator` in Part 1, the one that drops the empty messages in Part 3, or the merge in Part 5), so run them once. If you get an error after running a cell twice, rerun from Part 1 down.

## Data

The data is **not** stored in this repository. The notebook downloads it from the SynDisco project:
<https://github.com/dimits-ts/syndisco> (`viewer_datasets/online.zip`).
It is unpacked into an `online/` folder next to the notebook, which is ignored by git. The dataset belongs to its authors: see their repository for the terms of use and how to cite it.

## Files

```
PandasLab.ipynb        the lab
figures/               explanatory figures used in the notebook
  make_figures.py      redraws them
  *.png
```

The figures are embedded in the notebook, so it is self-contained. To redraw them, run `python figures/make_figures.py online.zip` from this folder (only the box plot reads the data).
