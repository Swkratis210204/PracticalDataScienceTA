# Assignment (instructor version): Do Personas Annotate Like People, and Does Context Change Them?

The student version is `assignment1_student.md`. This file is for us: the plan, the SynDisco mechanics, the decisions.

**Question:** when a language model is told to act as a person with a given identity, do its labels look like those of real people? And what changes when it first reads a conversation about the text?

## The plan

| | Step | Output |
|---|---|---|
| A | Load the 20 conversations of the file and clean them, nothing more | the clean items |
| B | Annotate the 20 items by hand in the CSV we give (id, text, empty rating and explanation columns): the student writes the rating and a one-sentence reason beside each text, saves, then loads the file into the code. Toxicity 1-5 (1-2 civil, 3-5 toxic). No separate guidelines document | the CSV with the ratings and explanations |
| C | Branch 1: for each item, random participants generate one small conversation, with the item as their starting context | `generated.jsonl` |
| D | Branch 1: every persona of the grid (a small starting grid that students must adapt), **plus a baseline with no persona**, annotates each item **with the generated conversation as context** (they label the item, not the conversation) | `annotations_context.jsonl` |
| E | Branch 2, in parallel: the same annotators, baseline included, annotate each item **without context** | `annotations_no_context.jsonl` |
| F | Agreement across everything, categorically and numerically: human vs model (no context), human vs model (context), model no context vs model context (same identity), persona vs persona within each condition; **key result: the identity closest to the student, named with all its attributes, with and without context** | `agreement.json` |
| G | Compare the two settings, tell the story | a 2-3 page report: a justification of every choice, the story, AI use |

So per item and condition there are x labels for x identities, plus 1 from the baseline.

The pipeline figure (`figures/pipeline.png`) shows it: A, then B, then the two branches (C then D, and E), merging in F, then G. Both branches start from the items; the human labels in B are made before any model output exists.

Everything is measured on the same 20 items, so human and model labels are directly comparable. The only things that vary are the persona and the context.

Calls: generation 20 conversations × about 5 comments; annotation: (number of annotators) × 20 per condition, 260 with the starting grid of 12 personas + a baseline. All cheap, but it multiplies with every dimension students add.

## What to expect at hand-in

**Uploads (four things):**

1. **The notebook**, which must run top to bottom, with the seed written down.
2. **The CSV** with the 20 ratings and one-sentence explanations, made before any model output.
3. **The outputs:** `generated.jsonl` (20 conversations), the annotation files of both conditions (one per annotator, baseline included), `agreement.json` and the figures (at least a persona-vs-persona heatmap).
4. **The report** (2-3 pages).

**Check these when marking (the hidden traps):**

- **Counts:** every annotator of the student's grid plus the baseline appears in **both** conditions, on all 20 items. Count the annotation files: (personas + 1) per condition.
- **Same items, same instructions** in both conditions and for all personas. Only persona and context may differ.
- **Item, not conversation:** the label is of the item. Open one saved `prompt` and check the context sits where the student says.
- **Human labels first:** the CSV ratings should not look tuned to the model (we cannot prove it; the explanations help, and the report should say when they were made).
- **Invalid answers** are counted per persona and condition, not dropped silently.
- **Constant annotators** (always the same label) break kappa: the student should notice.
- **Both views** of agreement, categorical and numeric, for all four comparisons.
- **Key result:** the identity closest to the student, named with **all** its attributes, with and without context, and whether it changes.
- **Sanity check:** strict rates higher than lenient. If not, the report must discuss prompts or parsing.
- **Grid and wording:** dimensions, values and the exact prompt wording of each persona are written down, with the reasons.

**The report should contain:**

1. **Justification of every choice:** cleaning (what was changed), rating (why), conversation settings, grid (dimensions, values, wording, why), where the context goes, handling of invalid answers.
2. **The story:** does context move labels and in which direction; which identity is closest to the student and whether it is the same with and without context; do the personas agree more or less with context; which identities move the most; strict vs lenient.
3. **Limits:** the "closest identity is not the student's identity" statement, 20 items (noisy kappas), a small model, one generated conversation per item (itself a bias), no sampling, personas that are only descriptions.
4. **AI use:** for what, and what the student checked.

**Weak work looks like:** a report that only lists numbers, a grid copied unchanged with no reasons, claims bigger than 20 items allow, agreement with no interpretation.

## SynDisco notes (read from the 2.2.1 source; not all run yet)

- **Discussion, per item.** `DiscussionExperiment` picks the seed segment at random for each discussion, so one experiment per item (`num_discussions=1`), with its own participants. The item goes in the participants' shared `context` string (it ends up in the system prompt). `seed_opinions=None` is allowed: the discussion then starts empty.
- **Annotation.** An `Annotation` labels **every entry** of a log, with the previous `history_ctx_len` entries as context (default 3 in `AnnotationExperiment`). With one entry per log (the item), the label is of the item alone. For the context condition the clean option is to put the generated conversation in the annotator's `context` and keep the log identical to the no-context run, so only the context changes. Putting the conversation into the log as earlier entries also works but labels those entries too.
- **One experiment per item and condition**, since `AnnotationExperiment` takes one `Logs` object. One output file per annotator. The saved `prompt` of each entry holds the system prompt, so persona and context can be recovered from it.
- **Output limit.** `TransformersModel` reads `max_out_tokens` on every call, so the same loaded model can generate long and then answer with one number if the attribute is changed. It decodes greedily (`do_sample=False`), so the same input gives the same output.
- **What went wrong in our test with Qwen2.5-3B (4-bit):** with `max_out_tokens=10` every comment was cut in the middle of a sentence. Beyond that, the model refused ("I'm sorry, but I can't assist with..."), wrote about the text in the third person instead of as a commenter, and copied the previous comment (greedy decoding, repeated history). Students will hit the same things, and the student file tells them to read the first conversations before the full run. Likely fixes: a proper output limit, clearer first-person instructions, a `repetition_penalty` through `generation_kwargs`, a larger model. We have not yet tested a generation recipe that works.

## Decided

- **Data and size:** 20 items from an external file, nothing generated before part C.
- **Label:** toxicity 1-5, compared categorically (1-2 civil, 3-5 toxic) and numerically.
- **Grid:** a small starting grid is given as an example: gender (female, male) × politics (left, right) × annotation style (strict, moderate, lenient) = 12 personas, plus a baseline with no persona. A persona therefore combines several attributes of two kinds: **who it is** (identity: here gender and politics) and **how it annotates** (a disposition: here the style). **Students must adapt the grid and explain why** (more dimensions such as gender, age, race, education; more values; more styles; rewording how each is written in the prompt). The style dimension doubles as a sanity check: a strict persona should rate higher than a lenient one. The no-persona **baseline is required and runs in both conditions**.
- **Grid values are placeholders:** the earlier gender × race × politics grid (2 × 4 × 3) is gone from the student file. Which dimensions and values are the starting grid is still our choice.
- **Where the context goes** is a hint for students, not specified.
- **Reproducibility:** a working pipeline with sensible results, not identical runs. Fixed seeds are asked for.

## Open

1. **The data file:** where it comes from. The student file says it is a CSV with an id, the text, and empty rating and explanation columns (text | rating 1-5 | explanation); we must produce it that way.
2. **The grid values** (female, male; Black, White, Asian, Hispanic; left, center, right are my choice).
3. **The grading weights** in the student file (10 / 15 / 20 / 20 / 20 / 15 are my proposal) and the deadline.
4. **Generation settings:** participants per conversation and number of comments (the student file only says short).
5. **Noise:** with 20 items, kappas are very noisy. The student file says so; do you want a chance baseline or a bootstrap as a requirement?
