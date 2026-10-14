# Project: Annotation Distributions for Synthetic Conversations

**Goal:** build one pipeline that turns synthetic conversations into annotated data. Each conversation gets a majority label and a full label distribution, both produced by a crowd of persona-agents. Then explore the data and measure how much the annotators agree.

**Pipeline:** `generate → clean → annotate → eda → agreement`, run with `python run.py --config config.yaml`. Each stage reads the previous stage's file and writes its own.

---

## A) Take conversations

- Use the provided library to generate 200–500 conversations.
- Config controls topic, number of conversations, number of turns and seed.
- **Output:** `conversations.jsonl`

```json
{"conv_id": 1, "turns": [{"speaker": "A", "text": "..."}], "meta": {"topic": "...", "seed": 7}}
```

## B) Clean them

Required steps:

1. Drop empty or too-short conversations.
2. Remove duplicate conversations and duplicate consecutive turns.
3. Normalize speaker names and whitespace.
4. Remove broken output (truncated turns, model refusals, leaked prompt text).
5. Log counts, e.g. "started with 400, dropped 31 (12 duplicates, 9 empty, 10 broken), kept 369".

**Output:** `clean.jsonl` (same schema) and `clean_report.json`.

## C) Agentic annotation distribution (the core)

**Fixed for everyone (so groups are comparable):**

- **Label set:** pick one task, for example offensiveness with `not / mild / offensive`.
- **Persona schema:** `age_group, gender, ethnicity, education`.
- **Annotators per conversation:** N = 10.

**Pick one strategy (document why):**

| Strategy | How it works |
|---|---|
| Random identity | One model. Each annotation call samples a new random persona. |
| One model, fixed identities | One model, K fixed personas, every persona annotates every conversation. |
| Model pool | Several models, each given random personas. |

**Each annotator call returns** a JSON object with `label` and a one-sentence `rationale`. Validate it and retry on bad output. Cache all calls so reruns are free.

**Aggregate per conversation:**

- `distribution`: the share of each label
- `majority`: the most common label (define your tie-break rule)
- `entropy`: the disagreement level

**Output:** `annotations.jsonl`

```json
{
  "conv_id": 1,
  "distribution": {"not": 0.6, "mild": 0.3, "offensive": 0.1},
  "majority": "not",
  "entropy": 0.90,
  "annotators": [
    {"persona": {"age_group": "55+", "gender": "female", "ethnicity": "..."}, "model": "...", "label": "mild", "rationale": "..."}
  ]
}
```

## D) Exploratory data analysis (EDA)

Explore both the conversations and the annotations. Produce at least these, as figures or tables in a notebook or script:

- **Conversations:** number of turns and length distributions, topics, speakers.
- **Labels:** overall label distribution, and the distribution of majority labels.
- **Disagreement:** histogram of entropy, and how many conversations have a unanimous vote vs a split vote.
- **Examples:** the 5 highest-entropy and 5 lowest-entropy conversations, with a short comment on why.
- **Personas:** label rates by persona attribute (age, gender, ethnicity, education). If you used a model pool, also by model.
- **Quality:** share of invalid or retried annotator outputs.
- **Stereotyping check:** do the rationales lean on stereotypes for some groups?

**Output:** `eda/` folder with figures, and 5–8 sentences of findings in the report.

## E) Inter-annotator agreement

Measure how consistent the annotators are, for both targets.

**Majority label**

- **Cohen's kappa** between two independent sets of annotations. Pick one way to build the pair and document it:
  - Split-half: randomly split the N annotators into two groups, take each group's majority, compare.
  - Or compare two strategies or two models on the same conversations.
- Use **quadratic weighted kappa** if your labels are ordered (e.g. not < mild < offensive).
- **Fleiss' kappa** or **Krippendorff's alpha** across all N annotators.

Note: Cohen's kappa needs two raters. With random personas, annotators are not the same "rater" every time, which is why split-half is the simple option.

**Distribution**

- **Jensen–Shannon divergence** between the two split-half distributions of each conversation. Lower means more agreement. Report the mean and its spread.
- **Correlation of entropy** between the two halves (Spearman). Do the halves agree on *which* conversations are ambiguous?
- Optionally, **Krippendorff's alpha** as a single summary over all annotators.

**Also report**

- Agreement by persona group, if you used fixed identities (pairwise kappa between personas).
- A chance baseline, e.g. repeat the split-half after shuffling labels.
- A short interpretation: low agreement is not automatically a failure, because it is the signal this project studies.

**Output:** `agreement.json` and a results table.

---

## 4-week timeline

| Week | Work |
|---|---|
| 1 | Parts A and B working end to end |
| 2 | Part C: annotator call, personas, caching |
| 3 | Part C: aggregation and full run. Part D: EDA |
| 4 | Part E: agreement, README, report, short presentation |

## Deliverables

- Repo with `config.yaml`, `run.py` and one module per stage
- The output files (`conversations.jsonl`, `clean.jsonl`, `annotations.jsonl`, `agreement.json`) and the `eda/` folder
- README with run instructions
- 2-page report (choices, findings, limitations)

## Grading

| Part | Weight |
|---|---|
| A + B | 20% |
| C | 35% |
| D (EDA) | 15% |
| E (agreement) | 15% |
| Code, README, report | 15% |

## Provided starter

- Repo skeleton and config template
- Label definitions and persona schema
- Model wrapper with caching
- Tiny sample dataset for testing without API cost

**Limitations to state in the report:** personas are simulated, not real people. The results show what models imitate, not what real groups think.