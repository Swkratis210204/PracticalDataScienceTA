# Assignment (instructor version): Do Personas Annotate Like People, and Does Context Change Them?

The student version is `../student/assignment1_student.md`. This file is for us: the plan, the SynDisco mechanics, the decisions.

**Question:** when a language model is told to act as a person with a given identity, do its labels look like those of real people? And what changes when it first reads a conversation about the text?

## The plan

| | Step | Output |
|---|---|---|
| A (step 1) | The student runs `prepare_items.py --seed <their own seed>` on `data/pool.csv`: 250 short comments (60-400 characters) from Civil Comments (google/civil_comments, test split, CC0), built by `instructor/build_pool.py`. The pool has 5 bands of 50, cut by the crowd toxicity score and the subtype scores (band 1 score 0, band 2 0.1-0.3, band 3 0.4-0.6, band 4 0.7-0.89 with insult >= 0.6, band 5 >= 0.9 with strong subtype scores, then read by hand); the key is `instructor/pool_key.csv`. `pool.csv` holds only `id` and `text`, shuffled: no band, score or label. The band of every comment is packed (zlib + base64) in the `_MIX` line of `prepare_items.py`, which `build_pool.py` rewrites, so the script draws exactly 4 comments per band for every seed (tested on 41 seeds) while the data file stays clean. This is hidden, not secret: a student who decodes `_MIX` can recover the bands (coarse crowd groups, not the right answers). If you need real secrecy, run the script yourself for each student seed and give them only `items.csv` and `annotate.html`. Each student gets a different sample; the same seed gives the same sample. The crowd bands are targets, not truth: student ratings will differ. Writes `items/items.csv` and `items/annotate.html` | seed, items |
| A (step 2) | The student annotates the 20 items in `annotate.html` (guidelines start page; rating 1-5, plus, for 3-5 only, the toxic words selected in the text (evidence); Next is locked until there is a rating and, for 3-5, at least one selection; for ratings 1-2 evidence is not asked, and the CSV writes `not needed` in that cell; there is no free-text box; the download appears when all 20 are complete) and downloads `items_rated.csv` (`id, text, rating, label, evidence`; label = civil for 1-2, toxic for 3-5). Toxicity 1-5 (1-2 civil, 3-5 toxic). The guidelines are the start page of the page, not a separate document | seed, `items_rated.csv` |
| B | The student opens `items.csv` and `items_rated.csv` in the notebook and shows how they rated: a histogram and a boxplot of their ratings (optionally more), with one or two sentences on what they show | the figures, shown in the notebook |
| C | Branch 1: for each item, random participants generate one small conversation, with the item as their starting context | the conversations, shown in the notebook |
| D | Branch 1: every persona of the grid (a small starting grid that students must adapt), **plus a baseline with no persona**, annotates each item **with the generated conversation as context** (they label the item, not the conversation) | the table of ratings, shown in the notebook |
| E | Branch 2, in parallel: the same annotators, baseline included, annotate each item **without context** | the table of ratings, shown in the notebook |
| F | **Simple agreement** (share of the 20 items with the same answer), categorically (same civil/toxic label) and numerically (same exact 1-5 rating): human vs model (no context), human vs model (context), model no context vs model context (same identity), persona vs persona within each condition (pairwise table/heatmap and average); **key result: the identity closest to the student, named with all its attributes, with and without context**. No kappa, alpha or correlations | tables and figures in the notebook |
| G | Compare the two settings, tell the story | markdown cells inside the notebook (about 3-4 pages of text): a justification of every choice, the results and story (the largest part), the limits, and a short AI-use and sources section |

So per item and condition there are x labels for x identities, plus 1 from the baseline.

The pipeline figure (`../student/figures/pipeline.png`) shows it: A, then B, then the two branches (C then D, and E), merging in F, then G. Both branches start from the items; the human labels in B are made before any model output exists.

Everything is measured on the same 20 items, so human and model labels are directly comparable. The only things that vary are the persona and the context.

Calls: generation 20 conversations × the students' number of comments; annotation: (number of annotators) × 20 per condition, 180 with the starting grid of 8 personas + a baseline. All cheap, but it multiplies with every dimension students add.

## What to expect at hand-in

**Uploads: exactly two files.**

1. **The notebook**, which must run top to bottom, with the seed and the GitHub link in the first cell, and **all explanations in markdown cells** (no separate report). It must display: the 20 items and the student's ratings (the `items.csv` and `items_rated.csv` content, since those files are not uploaded), the 20 generated conversations, the final grid (dimensions, values, exact persona attributes), the model annotations with and without context (format of the human table plus `annotator` and `prompt`; every persona plus the baseline on all 20 items), the agreement results, and the explanations.
2. **A markdown file with the student's interactions with LLMs** (prompts and answers, or faithful summaries; tools named at the top; or a statement that no AI was used). This replaces the extra AI-use page.

The GitHub link (mandatory) goes in the notebook.

**Check these when marking (the hidden traps):**

- **The notebook explanations:** in English, with the link to the student's GitHub repository in the first cell (working with GitHub is mandatory). The LLM-interaction markdown file is present.

- **Counts:** every annotator of the student's grid plus the baseline appears in **both** conditions, on all 20 items. Count the annotators in the displayed tables: (personas + 1) per condition.
- **Same items, same instructions** in both conditions and for all personas. Only persona and context may differ. **Requirement, checked in the `prompt` column:** for the same annotator, the prompt in D and in E is identical except for the `context` field (the conversation in D, empty in E); instructions, persona and wording must not change.
- **Item, not conversation:** the label is of the item. Read the `prompt` column and check the context sits where the student says (the `context` field), and that the text labelled is the item.
- **Their sample:** run `prepare_items.py` with the seed they report and check that the texts match the items table shown in the notebook (same items, same ids). A different sample means a different seed, or tampering.
- **Human labels first:** the CSV ratings should not look tuned to the model (we cannot prove it; the evidence passages help, and the notebook should say when they were made).
- **Invalid answers** are counted per persona and condition, not dropped silently.
- **Constant annotators** (always the same label) get high simple agreement when most items share that label, and simple agreement ignores chance: the student should notice and say so.
- **Both views** of simple agreement, categorical and exact-rating, for all four comparisons.
- **Key result:** the identity closest to the student, named with **all** its attributes, with and without context, and whether it changes.
- **Personas are identity only:** read the `prompt` column for each persona: it says who the annotator is and does not tell it how to rate (no strict, lenient, harsh...); the label instructions are identical for all, and the model decides how such a person would rate. Differences between personas may be small or noisy: the report should say so.
- **Grid and wording:** the grid is changed or extended compared with the starting one (mandatory), and the dimensions, values and exact attributes of each persona (the persona dict in the saved prompt) are written down, with the reasons.

**The notebook explanations should contain:**

1. **Justification of every choice:** the seed, rating (guidelines followed, evidence), conversation settings (participants, comments, length), the model (which were tried, why this one), grid (dimensions, values, wording, why), where the context goes, handling of invalid answers.
2. **Results and story (the largest part of the explanations):** the agreement results of the four comparisons; simple agreement only; students must interpret the values; does context move labels and in which direction; which identity is closest to the student and whether it is the same with and without context; do the personas agree more or less with context; which identities move the most; whether the personas differ from the baseline at all and which dimension matters most.
3. **Limits:** the "closest identity is not the student's identity" statement, 20 items (noisy agreement percentages, no chance correction), a small model, one generated conversation per item (itself a bias), no sampling, personas that are only descriptions.
4. **AI use and sources:** a short section (for what, what the student checked, the sources used); the full record is in the LLM-interaction file.

**Weak work looks like:** explanations that only list numbers, a grid copied unchanged with no reasons, claims bigger than 20 items allow, agreement with no interpretation.

## SynDisco notes (read from the 2.2.1 source; not all run yet)

- **Discussion, per item.** `DiscussionExperiment` picks the seed segment at random for each discussion, so one experiment per item (`num_discussions=1`), with its own participants. The item goes in the participants' shared `context` string (it ends up in the system prompt). `seed_opinions=None` is allowed: the discussion then starts empty.
- **Annotation.** An `Annotation` labels **every entry** of a log, with the previous `history_ctx_len` entries as context (default 3 in `AnnotationExperiment`). With one entry per log (the item), the label is of the item alone. For the context condition the clean option is to put the generated conversation in the annotator's `context` and keep the log identical to the no-context run, so only the context changes. Putting the conversation into the log as earlier entries also works but labels those entries too.
- **System prompt.** `Actor.get_system_prompt()` returns a JSON string with `context`, `instructions`, `type` ("annotator" or "user") and `persona` (a dict attribute: value, empty for the baseline). The annotator's user prompt is "Comments so far: {last history_ctx_len entries}.
Your annotation:". So persona wording is the attribute names and values, not a free sentence, and the context condition is exactly the `context` field: D passes the generated conversation, E leaves it empty. `Annotation` labels every entry of the log (default `history_ctx_len` 2 in `Annotation`, 3 in `AnnotationExperiment`).
- **One experiment per item and condition**, since `AnnotationExperiment` takes one `Logs` object. One output file per annotator. The saved `prompt` of each entry holds the system prompt, so persona and context can be recovered from it.
- **Output limit.** `TransformersModel` reads `max_out_tokens` on every call, so the same loaded model can generate long and then answer with one number if the attribute is changed. It decodes greedily (`do_sample=False`), so the same input gives the same output.
- **What went wrong in our test with Qwen2.5-3B (4-bit):** with `max_out_tokens=10` every comment was cut in the middle of a sentence. Beyond that, the model refused ("I'm sorry, but I can't assist with..."), wrote about the text in the third person instead of as a commenter, and copied the previous comment (greedy decoding, repeated history). Students will hit the same things, and the student file tells them to read the first conversations before the full run. Likely fixes: a proper output limit, clearer first-person instructions, a `repetition_penalty` through `generation_kwargs`, a larger model. We have not tested a generation recipe that works. We do not prescribe one: students hand in 20 conversations that make sense, shown in the notebook, and how they get there is theirs (limit, instructions, repetition penalty, a larger model on Colab).

## Models (student choice)

Students may use any model their computer or Colab can run; the list below is only a suggestion.

Suggested starting point: `unsloth/Qwen2.5-3B-Instruct-bnb-4bit`. There is no starting notebook any more: students write their own. Alternatives listed in the student file, all checked on Hugging Face as existing, ungated and 2-6 GB: `unsloth/Qwen2.5-7B-Instruct-bnb-4bit` (size), `unsloth/Llama-3.1-8B-Instruct-bnb-4bit` (another family), `unsloth/Phi-4-mini-instruct-bnb-4bit` (small, MIT). Gemma and Mistral were left out on purpose: their chat templates are the likeliest to reject a system prompt. **We do not test them: students choose one and run their final notebook with it. Trying a few models first is recommended as good practice, to get the best result, but it is not required; the report must say which model was used and why.** Known risks: some chat templates reject or ignore a system prompt, which matters because SynDisco puts the persona and the context in the system prompt; Qwen3 is a reasoning model and is excluded; Llama has its own licence.

## Decided

- **Data and size:** 20 comments per student, drawn by a seeded script from a pool of 250 Civil Comments comments (5 toxicity bands of 50, hidden from students); nothing generated before part C.
- **Label:** toxicity 1-5, compared categorically (1-2 civil, 3-5 toxic) and numerically.
- **Grid:** a small starting grid is given as an example: gender (woman, man) × politics (left, right) × age (under 30, over 50) = 8 personas, plus a baseline with no persona. **A persona says only who the annotator is, never how to rate** (no strict/lenient style): the label instructions are identical for every annotator in both conditions, so only the identity and the context can change a label. In part C (generating the conversation) the participants may be guided, since the conversation is only context. **Students must adapt the grid and explain why** (more dimensions such as education, religion, origin; more values; rewording). The no-persona **baseline is required and runs in both conditions**. The grid is also drawn in `persona_grid.png`; the key-result example in the student file uses these dimensions. There is no strict-vs-lenient sanity check any more: the check is that persona prompts contain no rating guidance.
- **Generation settings** (participants, number of comments, length limit) are the students' choice: moderate, not very big and not very small, and justified in the notebook. What we check is the result: 20 conversations that make sense.
- **Where the context goes** is a hint for students, not specified.
- **Reproducibility:** a working pipeline with sensible results, not identical runs. Fixed seeds are asked for.
- **Noise with 20 items:** students are told that the values are noisy and must take it into account when interpreting; no uncertainty measure is asked or suggested.

## Hand out

Give students the whole `student/` folder: `assignment1_student.md`, `prepare_items.py`, `data/pool.csv` and `figures/`. Keep the `instructor/` folder to yourself: it holds `pool_key.csv` (the real toxicity scores and bands), `build_pool.py` (which rebuilds the key), `make_figures.py`, the downloaded `civil_comments_test.parquet` (not in git) and `unused/pefk-sample.csv` (the first, dropped data file).
