# Good alternatives to the standard tools

The standard tools are the ones you will meet most often. But for many steps there is another tool that is **faster, simpler, or better for a different situation**. This page lists the ones worth knowing about, in the order of a data science project.

> **How to read it:** each row says which standard tool the new one replaces or sits next to. "Better" depends on the problem: choose by your data size, your team and your deadline.

---

## 1. Processing data

| Replaces / next to | Try | Why |
|---|---|---|
| pandas | **Polars** | Much faster and lighter on memory, with *lazy* queries that are planned before they run |
| pandas | **DuckDB** | Write SQL directly on CSV, Parquet or a DataFrame, with no server |
| looking at tables in a notebook | **DBeaver** | A free app to browse and query data with SQL |
| pandas | **PySpark** | The same ideas on a cluster, for data too big for one machine |

## 2. Versioning and environments

| Replaces / next to | Try | Why |
|---|---|---|
| GitHub | **GitLab, Codeberg** | Other hosts for the same git repository |
| Git (for big files) | **DVC** | Git for **data and models**: git keeps a small pointer, the big file lives in storage |
| GitHub + MLflow | **DagsHub** | Code, data and experiments in one place |
| pip + venv | **uv** | Very fast, creates the environment and locks exact versions |

## 3. Language models

| Replaces / next to | Try | Why |
|---|---|---|
| `transformers` (running a model) | **Ollama, LM Studio** | Run a model on your own computer with one command |
| `transformers` (many requests) | **vLLM** | A server that answers many requests quickly |
| bitsandbytes (quantization) | **llama.cpp (GGUF), AWQ, GPTQ** | Other ways to shrink a model, from laptop CPUs to GPUs |
| parsing the model's text by hand | **Pydantic, Instructor** | Force **valid, structured** output, such as a label as JSON |
| Hugging Face (finding models) | **Ollama library, Kaggle, OpenRouter** | Other places to get or call models |

## 4. Classical machine learning

| Replaces / next to | Try | Why |
|---|---|---|
| scikit-learn (random forest) | **XGBoost, LightGBM** | Gradient boosting, usually stronger on table data |
| scikit-learn (big data) | **Spark MLlib** | The same kind of tools on a cluster |
| scikit-learn (grid search) | **Optuna** | Smarter search for hyperparameters |

## 5. Tracking experiments

| Replaces / next to | Try | Why |
|---|---|---|
| MLflow | **Weights & Biases** | Polished dashboards, popular in research |
| MLflow | **TensorBoard** | Simple and free, built into PyTorch and TensorFlow |
| MLflow | **DVC experiments** | Tracks experiments inside git, with no server |

## 6. Tests, deployment and automation

| Replaces / next to | Try | Why |
|---|---|---|
| pytest (tests of the code) | **pandera, Great Expectations** | Tests for the **data**: columns, types and ranges |
| running checks by hand | **Ruff, pre-commit** | Check and format the code before every commit |
| FastAPI (a quick demo) | **Streamlit, Gradio** | A web demo of your model in a few lines |
| GitHub Actions (a pipeline) | **Prefect, Airflow** | Run the steps of a pipeline in order, on a schedule |

## 7. Notebooks and annotation

| Replaces / next to | Try | Why |
|---|---|---|
| Jupyter | **Marimo** | A notebook that is a plain Python file and updates what depends on a change |
| a spreadsheet for annotation | **Label Studio** | A tool made for annotation, with several annotators |

---

**One rule to remember:** a newer tool is not automatically a better one. Choose by the size of the problem, by what your team already knows, and by how well the tool is maintained.
