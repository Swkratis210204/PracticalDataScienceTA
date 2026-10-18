# Practical Data Science: Outside Labs

Six labs that support the 4-week annotation-distribution project, plus two QA sessions (not labs).

| # | Session | Supports |
|---|---|---|
| 1 | Processing (libraries) | Intro to the most basic stuff |
| 2 | Versioning (GitHub) | All parts |
| 3 | Agentic (install and quantize, HuggingFace) | Part of the project |
| 4 | Quantization | Part of the project |
| 5 | Scikit (ML tools) | Log experiments on MLflow |
| 6 | MLOps | Set up tests, runner, take previous models and deploy with FastAPI |

---

## Lab 1. Processing (libraries)

- Pandas basics: read, select, filter, missing data, text, dates, group by, joins
- Storing data as JSONL and Parquet
- Hands-on: a 1-hour pandas lab (data tour, quiz, build the query, broken queries)

## Lab 2. Versioning (GitHub)

- Git basics: commit, branch, pull request, merge conflicts
- What to keep out of git: API keys, large data, outputs (`.gitignore`)
- Secrets: `.env` files, environment variables, a committed `.env.example`, GitHub Actions secrets, what to do if a key leaks (rotate it)
- Environments: virtual environments (venv or conda), `requirements.txt` or `pyproject.toml`, pinned versions
- A good README and repo structure
- Hands-on: set up the project repo with a `.env` for the API key, a clean environment and one PR

## Lab 3. Agentic (install and quantize, HuggingFace)

- Installing the libraries from PyPI (`transformers`, `torch`) in a clean environment
- Taking a small model from Hugging Face: model card, size, license, loading it with `transformers`
- Explaining the inputs: tokenizer, chat template, system vs user message, context length
- Explaining the hyperparameters: `temperature`, `top_p`, `top_k`, `max_new_tokens`, seed; what each does to the output
- Giving the model instructions: a persona prompt that returns a label as JSON, with validation and retry
- Hands-on: annotate 10–20 texts with the model, once with different personas and once with different temperatures, and compare the labels (a small version of Part C of the project)

## Lab 4. Quantization

- What quantization is: FP32, FP16, 8-bit and 4-bit, and why models are big
- Loading a model in 8-bit or 4-bit (`bitsandbytes`, or GGUF with llama.cpp)
- What you gain and lose: memory, speed (tokens per second), output quality
- Hands-on: load the lab 3 model in 4-bit, rerun the same annotations and measure how much the labels change (e.g. Cohen's kappa between the full and the quantized run)

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