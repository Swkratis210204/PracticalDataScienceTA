# Lab 2: Annotation with SynDisco (1 hour)

A short preview of [Assignment 1](../../assignments/ass1/instructor/assignment1.md). In one notebook, students run the whole pipeline of the assignment on **5 texts**, with no analysis:

1. they **rate** the 5 texts themselves (1 fully civil to 5 very toxic), alone, in the notebook;
2. a model writes a short **conversation** about each text (3 random participants, 4 replies);
3. an **annotator** with no persona (the baseline) rates the same 5 texts, **without** and **with** the conversation;
4. they look at one table: their rating, the baseline without context, the baseline with context;
5. a last block gives the annotator a **persona** with one dimension and two values (gender: woman, man), runs it on the same 5 texts without context, and compares it with the baseline and with the student.

All the code is written. Students run the cells in order and type their 5 ratings. There are no gaps and no solutions notebook.

## Files

| File | What |
|---|---|
| `lab_annotation.ipynb` | the notebook, saved **without outputs** (it needs a GPU, run it on Colab) |
| `README.md` | this file |

The notebook writes four files next to itself, on the student's Colab disk: `my_ratings.csv` (their 5 ratings), `generated.jsonl` (the 5 conversations, the same name as in the assignment), `lab_results.csv` (you, baseline without and with context) and `lab_results_personas.csv` (you, baseline, woman, man).

## Run it

Open the notebook on Colab, then *Runtime → Change runtime type → T4 GPU*. The first code cell installs `syndisco` (about a minute); it brings `transformers` and `bitsandbytes`. The model is **`unsloth/Qwen2.5-3B-Instruct-bnb-4bit`** (2.1 GB download), the same one as the starting point of the assignment.

## Flow

| Min | Step | Notes |
|---|---|---|
| 0-8 | Intro, open Colab, T4 GPU, run the setup cells | what annotation is and why we compare a model with a person (the "idea" of the assignment); the install takes about a minute |
| 8-18 | **1. Rate the 5 texts** | alone, in silence; the texts go from civil to clearly hostile. Then compare two neighbours: they will disagree, and that is the point |
| 18-23 | **2. Load the model** | the download and load take 1-3 minutes: talk about `Actor` (persona, context, instructions) meanwhile |
| 23-38 | **3. Conversations** | about 1-2 minutes of generation on a T4. Ask them to read the 5 conversations: do they make sense? Show a bad one if there is one (cut off, repeats, refuses) |
| 38-46 | **4. The annotator** and **5. The table** | 10 short calls. An annotator is an `Actor` with `is_annotator=True`; the only difference between the two runs is the `context` |
| 46-54 | **6. A persona: one dimension, two values** | the same function with `persona={"gender": "woman"}` and `{"gender": "man"}`, no context, 10 short calls. Ask: do they differ from the baseline? Which is closest to you? Compare with a neighbour |
| 54-60 | Discuss, then Assignment 1 | show the bridge table at the end of the notebook: what is the same, and what is bigger in the assignment |

## What to say

- **The text is always rated alone.** The annotator's log has one entry, the text. The conversation goes in the annotator's `context`, so with and without context differ in one place only.
- **The baseline has no persona** (`persona=None`). In the conversations the personas only make the replies different. In step 6 a persona is *who the annotator is* (`{"gender": "woman"}`): it does not tell the model how to rate, the model decides. The grid of several dimensions is for the assignment.
- **Output limit.** The model is loaded with `max_out_tokens=80` for the conversations and the notebook sets it to 5 for the ratings. The same model object is used for both.
- The model is deterministic (greedy decoding): the same input gives the same output. The variety of the conversations comes from the random participants (`random.Random(0)`).

## Common problems

| Problem | What to do |
|---|---|
| No GPU, the model load is very slow or fails (`bitsandbytes`) | *Runtime → Change runtime type → T4 GPU*, then run again from the top |
| After `pip install`, an import error about `transformers` or `torch` | *Runtime → Restart session*, then run the cells from the second one |
| A conversation is cut off, repeated or refused | normal for a small model. Change the `0` in `random.Random(0)` and re-run the conversations cell; the assignment asks them to deal with this |
| The table shows `None` | the model did not answer with a number from 1 to 5 (the code looks for the first digit 1 to 5). Real, and a good talking point: the assignment asks to count these |
| `input()` does nothing | wait for the prompt below the cell; on Colab you type in the box and press Enter |

## Notes

- The 5 texts come from the Civil Comments dataset (CC0), chosen to run from civil to hostile, and they are **not** in the assignment's pool of 250.
- **Tested here, without a GPU:** the whole notebook, from top to bottom, with a stand-in model that answers by rule (it gives a different rating to a woman, a man and the baseline, so the personas, the parsing, the table and the four files are checked). An earlier version, before the persona block and the extra explanations, was also run with a tiny real model, `Qwen/Qwen2.5-0.5B-Instruct`. The expanded version could not be re-run with it (this machine ran out of memory), but its code is the same.
- **Not tested: the real model.** Qwen2.5-3B on a T4 was not run. The tiny model refused to reply to the hostile texts ("I'm sorry, but I can't assist") and repeated the same reply, and the 3B model may do the same on the harshest texts. The participants' prompt already says it is a role-play for a research study and never to refuse, to reduce this. **Run the notebook once on Colab before the lab**, and look at the 5 conversations.
- If a conversation is bad, it is a good moment to show why the assignment asks students to check and adjust their conversations (part C).
