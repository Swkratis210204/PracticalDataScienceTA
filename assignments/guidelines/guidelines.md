# Exercise: Reading Annotation Guidelines

> Find real annotation tasks, read the guidelines their annotators received, rate how good the instructions are, and check whether they say **whom the annotator is judging**.

| Step | What you do | You hand in |
|:---:|---|---|
| **Task** | Find 4 annotation tasks and their guidelines | The datasets and links |
| **1** | Rate the instructions | A score from 1 to 4 for each task |
| **2** | Author or reader? | A label and a quote for each task |
| **3** | Explain | Short written answers |

---

## Task

Find **4 annotation tasks**:

- **2 on sentiment**
- **2 on toxicity** (or offensiveness)

Look in papers or dataset documentation. For each one, **find the guidelines** the annotators received.

---

## Step 1: Rate the instructions

Give each task **one score from 1 to 4**. Each level includes everything in the levels below it.

| Score | Label | What the guidelines contain | How to recognize it |
|:---:|---|---|---|
| **1** | Bare | Only the task name, or a question and a scale. Nothing explains the labels. | You could not tell what the annotator should do in a doubtful case. |
| **2** | Defined | Level 1, plus a written definition of the label or of each scale point. | You can say what "toxic" or "positive" means for this task, but you have not seen it applied. |
| **3** | Illustrated | Level 2, plus example texts for the labels or scale points. | You can see which texts get which label. |
| **4** | Comprehensive | Level 3, plus rules for hard cases (sarcasm, quotes, mixed sentiment) and a described procedure (annotator training, how disagreements were resolved). | A new annotator could label a tricky text without guessing. |

> **Skipped a level?** If a task would skip a level, for example it has examples but no definitions, give it the highest level it fully reaches.

---

## Step 2: Author or reader?

For each task, decide whether the guidelines say what the annotator is judging:

| Answer | Meaning |
|---|---|
| **Author** | The annotator judges what the writer meant or felt. |
| **Reader** | The annotator judges how the text comes across, or how they react to it. |
| **Not stated** | The guidelines do not say. |

Write the sentence that **shows or implies** it. If you cannot quote one, the answer is "not stated".

---

## Fill in one row per task

> **Which columns belong to which step?**
> The **first 5 columns** (Dataset to Why this score) are for **Step 1**.
> The **last 2 columns** (Author, reader or not stated, and Quote) are for **Step 2**.

> **The first row is a fake example.** It only shows the format. It is not a real dataset, and its link and guidelines do not exist. Do not include it in your answer.

| Dataset | Task | Link to guidelines | Score (1–4) | Why this score | Author, reader or not stated | Quote |
|---|---|---|:---:|---|:---:|---|
| *FAKE EXAMPLE:* ExampleSet-X | Toxicity | https://example.com/guidelines | 3 | Defines "toxic" and gives example comments, but has no rules for hard cases | Reader | "Rate how toxic this comment feels to you as a reader." |

**Report one number.** Count the rows where you answered **author** or **reader** (not "not stated"), and write it as a number out of 4, for example "1 of 4". This is how many of your guidelines say or imply whom the annotator should judge.

---

## Step 3: Explain

Answer each question in two or three sentences.

1. **Weakest guidelines.** Which of your 4 tasks got the lowest score, and what exactly is missing from its guidelines (definitions, examples, hard cases or procedure)?
2. **Whose feeling?** In a sentiment dataset of Iliad verses, take a verse where a warrior dies in battle. The character in the scene may feel rage, the narrator may sound calm, and the reader may feel sadness. Explain how three annotators could give this verse three different sentiment labels, and say which of your 4 tasks, if any, would have prevented this.
3. **Write the fix.** Write one or two sentences of instruction for annotating the sentiment of literary verses, so that every annotator judges the same thing. Say whom they should judge: the character, the narrator or the reader.

---

## What is required

> Everything above needs a **simple, to-the-point explanation**: your score, your author/reader choice and your answers to questions 1 and 2 each come with a short reason of one to three sentences.
>
> The only exception is question 3, where the instruction you write is the answer.