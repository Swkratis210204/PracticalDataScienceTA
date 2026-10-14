# Lab 1 (alternative): Pandas assessment (1 hour, open book, ungraded)

A standalone check-up on the pandas topics of `lectures/L1/intro_to_pandas.slides.html`. It does not depend on any other lab and does not build on the guided [lab01-pandas](../lab01-pandas/); it is an alternative to it, on the same **SynDisco** data (720 synthetic discussions, 20,340 messages). The data arrives pre-cleaned in two tables:

- `convs`: one row per conversation (720 x 7): `conv_id`, `started_at`, `experiment`, `model`, `setting`, `has_moderator`, `n_messages`.
- `msgs`: one row per message (18,658 x 9, empty messages already dropped): `conv_id`, `turn`, `speaker`, `written_by`, `text`, `is_mod`, `n_chars`, `n_words`, `addressed_to` (the only column with `NaN`).

## Files

| File | What |
|---|---|
| `lab_student.ipynb` | gaps (`___`), questions and `assert` checks, no solutions, no outputs |
| `lab_solutions.ipynb` | everything solved and executed, plus a "How I approach this" note per Block 3 task and Block 4 fix, and the quiz explanations |
| `README.md` | this file |
| `figures/` | `make_figures.py` redraws `toy_tables.png` (the picture of the toy tables in Block 2, embedded in both notebooks, so the notebooks are self-contained); the explode figure in Block 1 is copied from `../lab01-pandas/figures/fig4_explode.png` |
| `figures/merge_one_to_many.png` | embedded in both notebooks just before Broken 2: a neutral example (orders and e-mails) showing that a merge repeats a row when its key appears twice in the lookup table; it does not name Broken 2's tables or the fix (`make_merge_figure.py` redraws it) |

The first cell downloads `online.zip` from the SynDisco repository (`urllib`, works on Colab, Linux, Mac and Windows) and skips the download if `online/` or `online.zip` already exists. Needs only pandas and numpy.

## Timing and what each block tests

| Min | Block | Size | Tests | Checked by |
|---|---|---|---|---|
| 0-15 | 1. Get to know the data | 5 simple questions | reading the data, no queries: `shape`, `describe`, `value_counts`, `isna().sum()`, `min`/`max` on a date | `assert` on values |
| 15-30 | 2. Quiz | 7 predictions + 3 code reads (about 90 s each) | `loc` slice end, `&` with NaN, `&` precedence, `mean` skips NaN, `agg([...])` shape, inner and left merge row counts; code reads: filtered median, two-key `agg`, grouping a boolean Series | letters are compared to hashes, so the check cell does not reveal answers; code-read sentences must be non-empty |
| 30-50 | 3. Build the query | 5 queries, about 4 min each: 2½ to build, 1½ to discuss together, plus an optional Task 6 | the 5-step recipe (rows, groups, statistic, join, sort/limit). T1 filter + count (1 gap), T2 groupby + mean (2 gaps), T3 filter + groupby + `size` + sort + `head` (2 gaps), T4 two keys and a percentage as the mean of a True/False column (4 gaps), T5 merge with different key names then `agg(['count','mean'])` (plan as a string, then free code), T6 (extra, if time allows) `.str.len()` on the speaker name, then a filter and a count (2 gaps) | `assert` on shapes and values; the explanation is oral, in the 1½ minutes of discussion (the solutions notebook has a "how I approach this query" note per task) |
| 50-60 | 4. Broken queries | 3 snippets, about 3 min each | B1 `and` instead of `&` (ValueError), B2 duplicated key in a lookup table inflates 18,658 rows to 24,772 (silent), B3 `groupby` drops NaN keys, 15,199 of 18,658 counted (surprise) | `assert` on the fixed result; why each one went wrong is discussed orally (the solutions notebook explains each fix) |

Block 1 is deliberately light: it is a warm-up to get a feel for the data before the queries. If a class is slow, the cuts that hurt least are the discussion of Tasks 1-2 and Task 5 (do it together on the board).

## Common mistakes to expect

- **Block 1:** `shape` read as `(columns, rows)`; reading the `50%` row of `describe` as the mean; forgetting that `describe` skips text columns; reading `isna().sum()` as an error report when the NaN in `addressed_to` just mean "no @name"; `min`/`max` on `started_at` returning a Timestamp (compare the date part).
- **Quiz:** `loc[11:13]` as 2 rows (end excluded, like `iloc`); expecting a `ValueError` for the missing parentheses in Q3 (it is a `TypeError`); `mean` dividing by 5 instead of 3; counting the merge in Q6 as 3 (forgetting that duplicate keys multiply); R2 read as "one row per writer" (forgetting that two keys give one row per pair).
- **Task 1:** `>=` instead of `>`; forgetting `~` or the parentheses around each comparison.
- **Task 2:** forgetting to filter the user messages first; `.mean()` without picking `n_chars` first gives a wide table or an error on the text columns.
- **Task 3:** `sort_values()` without `ascending=False` gives the 3 *smallest*; grouping by `written_by` instead of `conv_id`; `head` vs `tail`.
- **Task 4:** forgetting `.round`, or using `notna()` (gives the opposite share); `sum()` instead of `mean()` (counts, not percentages); grouping by one key only.
- **Task 6:** `len(msgs["speaker"])` instead of `.str.len()` (gives the number of rows, not one length per name); forgetting `~msgs["is_mod"]`; `>= 15` instead of `> 15`.
- **Task 5:** merging with `on="model"` (the column does not exist in `msgs`); using a `left` join and leaving the real comments in as `NaN` (the count is then 11,948 instead of 10,508); skipping the plan.
- **Broken 1:** adding only `&` and no parentheses (gives the same TypeError as Q3).
- **Broken 2:** fixing the symptom (dropping rows after the merge) and not the key; students who only look at the final counts miss it, which is the point.
- **Broken 3:** `fillna` on the whole table instead of the key; `dropna=False` placed in the wrong call.

## What is assumed known (from the slides) and what is extra

From the slides: `read_csv`, `head`/`describe`, `loc`/`iloc` (label slices include the end), boolean filtering, `isna`/`dropna`/`fillna`, vector operations and alignment, `del`/`pop`, `.str` with regex, `.dt`, `groupby` with a list of keys and `agg(['mean','std'])`, `size`, `concat`, `merge(on=, how='left')`, `rename`, `apply`.

Not in the slides, so used only in the provided cleaning cell, in hints, or in the solutions: `&`/`~` (the brief asks for `&` vs `and`), `explode`, `np.where`, `groupby(..., dropna=False)` (Broken 3 fix), `drop_duplicates` (Broken 2 fix), `left_on`/`right_on` (hinted in Task 5, can be avoided with `rename`), `validate=` and `transform` (solutions only). The lab is open book, so students can look these up; trim them if you prefer a stricter slides-only lab.

## Notes for you

- Auto-checks are plain `assert`s with a hint message. They compare your answer with a short hash of the right one (helper `ok(...)` in the cell after the loading cell), so the expected values are not readable in the notebook and the hints do not contain numbers. The checks compare exact values, so a student who modifies `msgs` in place (for example dropping columns) can break later checks. The notebook tells them to work on copies; "Run all" from the top repairs it.
- Hashes make the answers non-obvious, not secret: a letter answer can be brute-forced, and a motivated student can read the helper. Fine for an ungraded, open-book session. If you prefer, you can also announce the results in class and let students confirm them against the check.
- Tested with Python 3.12, pandas 2.3.3, numpy 2.4.2 and the SynDisco `online.zip` as of February 2026. `lab_solutions.ipynb` runs top to bottom with every assert passing. In `lab_student.ipynb` the cells before the first gap run without errors and every check cell fails until it is filled in.
