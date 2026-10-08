# Lab 1: Pandas

A hands-on introduction to pandas. Instead of a toy table, the lab works with a real, messy dataset: **SynDisco**, 720 *synthetic* online discussions in which seven simulated users debate a topic and an LLM moderator may or may not step in. The same setup was run with 6 language models and 4 moderation settings, 30 conversations each.

Along the way we answer simple questions about the data: how is it stored, how long are the conversations, who speaks, and what does the moderator change?

## Contents

| Part | Topic | Status |
|---|---|---|
| 1 | Loading data: nested JSON files into one table | ready |
| 2 | Simple exploration: `head`, `info`, `describe`, missing values | ready |
| 3 | Selecting rows and columns: `loc`, `iloc`, slices, labels | ready |
| 4 | Math and statistics: `mean`, `median`, `mode`, `value_counts`, changing values | ready |
| 5 | Filtering and text: boolean filters, slicing text, regex, `drop`, `pop` | planned |
| 6 | Operations between columns, strings, preprocessing | planned |
| 7 | Dates and times | planned |
| 8 | Groups and joins: `groupby`, `concat`, `merge` | planned |

Every part opens with its goals, explains each step in short markdown cells, and ends with a list of findings. Each part is a heading, so you can collapse the parts you are not working on.

## Run it

**On Colab:** upload `PandasLab.ipynb`, or, once the repository is on GitHub, open
`https://colab.research.google.com/github/<user>/<repo>/blob/<branch>/labs/lab01-pandas/PandasLab.ipynb`
(replace `<user>`, `<repo>` and `<branch>`). Run the first download cell.

**Locally:** install the requirements from the repository root (`pip install -r requirements.txt`), start `jupyter lab`, open `PandasLab.ipynb` and run the cells from top to bottom. The first two cells download the data: the first uses `wget` and `unzip` (Colab, Linux, Mac); the second is plain Python and works on any system, including Windows. Run one of them, not both.

The notebook was written and run with Python 3.13, pandas 3.0.6, numpy 2.5, matplotlib 3.10, seaborn 0.13 and scipy 1.18. It is meant to work on pandas 2.x as well, but that has not been tested.

Some cells change the table in place (for example the one that drops `moderator`), so run them once. If you get an error after running a cell twice, rerun from section 1.4 down.

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
