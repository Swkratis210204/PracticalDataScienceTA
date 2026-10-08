# Lab 1 (pandas): next parts and open points

## Planned parts

- **Part 5:** filtering, slicing text, regex, deleting and popping.
- **Part 6:** operations between columns and Series (for example additions), strings, more preprocessing.
- **Part 7:** dates and datetimes.
- **Part 8:** group by, concat, group by with functions, joins, multiple group by.

## Hooks in the data for those parts

- **Empty messages.** 1,682 messages are just `""`, and about 83% of them are the moderator's (the instructions let it stay silent); the rest are users'. A natural filtering exercise for Part 5.
- **HTML entities.** Message texts contain `&gt;`, and some opening comments look cut off ("...the anti-establishment aspect of"). Good for regex and string cleaning.
- **Spike near 500 characters.** The message-length histogram has a second, smaller spike around 500 characters. Not investigated yet; it may be a length limit.
- **Dates (Part 7).** `timestamp` is already converted to a datetime in Part 2, so Part 7 can start from there: extract day and hour, differences between conversations. The runs span 2026-02-09 to 2026-02-22.
- **Joins and groups (Part 8).** `df` (one row per conversation, key `id`) and `msgs` (one row per message, key `conv_id`) are a natural pair for `merge`. `condition` gives the groups: compare message length by moderation setting and by model.
- **Not paired.** The 30 conversations of each condition start from different opening comments (no overlap between two conditions I checked, 690 distinct openings among 720 files), so conditions can only be compared on averages, not conversation by conversation.

## Notebook points to follow up

- Some cells change the table in place (dropping `moderator`; the `map` on `has_moderator` in Part 4, which turns every value into `NaN` if run twice). Idea: make the risky cells safe to re-run, or keep the warning in the README.
- Images are embedded in the notebook (about 1 MB), so it works on Colab; the PNGs and `figures/make_figures.py` are the source if one needs changing.
