# Practical Data Science: Outside Labs

Six labs that support the 4-week annotation-distribution project, plus two QA sessions (not labs).

| # | Session | Supports |
|---|---|---|
| 1 | Processing (libraries) | Intro to the most basic stuff |
| 2 | Versioning (GitHub) + annotation with SynDisco | All parts; Assignment 1 (preview of the pipeline) |
| 3 | Local models (HuggingFace): summarize and filter texts | Part of the project |
| 4 | Quantization | Part of the project |
| 5 | Scikit (ML tools) | Log experiments on MLflow |
| 6 | MLOps | Set up tests, runner, take previous models and deploy with FastAPI |

---

## Lab 1. Processing (libraries)

- Pandas basics: read, select, filter, missing data, text, dates, group by, joins
- Storing data as JSONL and Parquet
- Hands-on: a 1-hour pandas lab (data tour, quiz, build the query, broken queries)

## Lab 2. Versioning (GitHub) and annotation with SynDisco

The lab has two parts.

### Part 1. Versioning (GitHub)

- Git basics: commit, branch, pull request, merge conflicts
- What to keep out of git: API keys, large data, outputs (`.gitignore`)
- Secrets: `.env` files, environment variables, a committed `.env.example`, GitHub Actions secrets, what to do if a key leaks (rotate it)
- Environments: virtual environments (venv or conda), `requirements.txt` or `pyproject.toml`, pinned versions
- A good README and repo structure
- Hands-on: set up the project repo with a `.env` for the API key, a clean environment and one PR

### Part 2. Annotation with SynDisco (1 hour)

- Hand annotation: rate 5 texts yourself, from 1 (fully civil) to 5 (very toxic), and see that two people disagree
- [SynDisco](https://dimits-ts.github.io/syndisco/): a framework to create conversations and annotate texts with model wrappers; an `Actor` has a persona, a context and instructions
- Mechanical annotation: a model writes a short conversation about each text, then an annotator (with no persona, the baseline) rates the same texts without and with that conversation as context
- A persona with one dimension and two values (gender: woman, man): does it differ from the baseline, and which is closest to you?
- Hands-on: run the lab notebook on Colab (T4 GPU) with `Qwen2.5-3B-Instruct` (4-bit); it is a preview of Assignment 1

## Lab 3. Local models (HuggingFace)

Under one hour, so there is time for questions.

**Scenario:** you have a pile of news articles and no time to read them all. Some topics are sensitive, so the texts should not be sent to an external service. A small model running on your own machine can do a first pass.

- Pick a small instruct model by hand on Hugging Face (model card, size, license, context length) and load it in a notebook with `transformers`
- Load 10-15 news articles (a small sample of CNN/DailyMail) and preprocess them: clean whitespace and leftovers, drop duplicates and empty texts, truncate to fit the context length
- The inputs: tokenizer (tokens are not words), chat template, system vs user message
- The hyperparameters, each seen in the output: `max_new_tokens` (a summary cut mid-sentence), `temperature` (0 for stable, high for invented details), `top_p`, `top_k`, seed (same seed, same output)
- **Case 1, read the summaries:** each article becomes 2 sentences, so you can skim all of them quickly
- **Case 2, keep only what matches:** the model answers whether the article is about a given topic, person or place, as JSON (`keep` and a short `reason`), with validation and one retry. Keep the articles that match, then read only those
- Hands-on: run both cases on the sample, change one hyperparameter and see what changes. Do the summaries still say what the article says? Does the filter keep what it should?

## Lab 4. Quantization

- What quantization is: FP32, FP16, 8-bit and 4-bit, and why models are big
- Loading a model in 8-bit or 4-bit (`bitsandbytes`, or GGUF with llama.cpp)
- What you gain and lose: memory, speed (tokens per second), output quality
- Hands-on: load the lab 3 model in 4-bit, rerun the same summaries and filter, and measure what changes (memory, speed, and how many articles are kept or dropped differently)

## Lab 5. Scikit (ML tools)

- Train/test split, pipelines, TF-IDF, logistic regression, random forest
- Metrics: accuracy, macro-F1, Cohen's kappa, Jensen–Shannon divergence
- At the end, log experiments in MLflow: params, metrics, artifacts, comparing runs in the UI
- Save the models with `mlflow.sklearn.log_model` so the next lab can load them
- Hands-on: train two models, log every run to MLflow and pick the best

## Lab 6. MLOps

- Tests with pytest and a single runner: `python run.py --config config.yaml`
- GitHub Actions: run tests and a small sample run on every push
- Take the models logged in lab 5 and load them from MLflow
- Serve the best model with FastAPI (Docker as an optional extra)
- Hands-on: push a change, watch CI pass, and call the deployed API

---

## QA sessions (not labs)

### QA (1st assignment)

- Open questions on parts A–C
- Common problems: broken generations, bad JSON from models, cost and caching
- Check of cleaning report and first annotation outputs

### QA (2nd assignment)

- Open questions on parts D–E (EDA and agreement) and the report
- Common problems: wrong kappa setup (Cohen's kappa needs two raters), misreading low agreement, plots without labels
- Check of final deliverables and presentation