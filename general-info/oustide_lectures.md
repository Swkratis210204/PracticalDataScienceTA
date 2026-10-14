# Practical Data Science: Outside Labs

Eight sessions that support the 4-week annotation-distribution project.

| # | Session | Supports |
|---|---|---|
| 1 | Processing (libraries) | Intro to the most basic stuff |
| 2 | Versioning (GitHub) | All parts |
| 3 | Agentic (install and quantize, HuggingFace) | Part of the project |
| 4 | Quantization | Part of the project |
| 5 | Scikit (ML tools) | Log experiments on MLflow |
| 6 | MLOps | Set up tests, runner, take previous models and deploy with FastAPI |
| 7 | QA (1st assignment) | 
| 8 | QA (2nd assignment) |

---

## 1. Processing (libraries)

- Pandas basics: read, select, filter, missing data, text, dates, group by, joins
- Storing data as JSONL and Parquet
- Hands-on: a 1-hour pandas lab (data tour, quiz, build the query, broken queries)

## 2. Literature (search)

- Finding papers: Google Scholar, Semantic Scholar, arXiv, citation chasing
- Reading a paper fast: abstract, figures, method, limitations
- Keywords for this project: annotator disagreement, perspectivism, persona prompting, LLM-as-annotator, inter-annotator agreement
- Hands-on: find 5 relevant papers and write a 1-page related-work summary

## 3. Versioning (GitHub)

- Git basics: commit, branch, pull request, merge conflicts
- What to keep out of git: API keys, large data, outputs (`.gitignore`)
- Secrets: `.env` files, environment variables, a committed `.env.example`, GitHub Actions secrets, what to do if a key leaks (rotate it)
- Environments: virtual environments (venv or conda), `requirements.txt` or `pyproject.toml`, pinned versions
- A good README and repo structure
- Hands-on: set up the project repo with a `.env` for the API key, a clean environment and one PR

## 4. Agentic (install and quantize, PyPI)

- Installing the libraries from PyPI (`transformers`, `torch`, `bitsandbytes` or similar) in a clean environment
- Taking a small model from Hugging Face: model card, size, license, loading it with `transformers`
- Changing things: load in 8-bit or 4-bit (quantization), compare memory, speed and output quality
- Explaining the inputs: tokenizer, chat template, system vs user message, context length
- Explaining the hyperparameters: `temperature`, `top_p`, `top_k`, `max_new_tokens`, seed; what each does to the output
- Giving the model instructions: a persona prompt that returns a label as JSON, with validation and retry
- Hands-on: annotate 10–20 texts with the model, once with different personas and once with different temperatures, and compare the labels (a small version of Part C of the project)

## 5. Scikit (ML tools)

- Train/test split, pipelines, TF-IDF, logistic regression, random forest
- Metrics: accuracy, macro-F1, Cohen's kappa, Jensen–Shannon divergence
- Log experiments in MLflow: params, metrics, artifacts, comparing runs in the UI
- Hands-on: train two models, log every run to MLflow and pick the best

## 6. MLOps

- Tests with pytest and a single runner: `python run.py --config config.yaml`
- GitHub Actions: run tests and a small sample run on every push
- Take the models logged in session 5 and load them from MLflow
- Serve the best model with FastAPI and package it with Docker
- Hands-on: push a change, watch CI pass, and call the deployed API

## 7. QA (1st assignment)

- Open questions on parts A–C
- Common problems: broken generations, bad JSON from models, cost and caching
- Check of cleaning report and first annotation outputs

## 8. QA (2nd assignment)

- Open questions on parts D–E (EDA and agreement) and the report
- Common problems: wrong kappa setup (Cohen's kappa needs two raters), misreading low agreement, plots without labels
- Check of final deliverables and presentation