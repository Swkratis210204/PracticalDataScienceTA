# Practical Data Science (PDS)

Teaching assistant repository for the Practical Data Science course: labs, assignments, lecture material, general information and ideas, all in one place.

## Layout

| Folder | What goes in it |
|---|---|
| [`labs/`](labs/) | One folder per lab, each with its notebook, figures and README |
| [`assignments/`](assignments/) | Assignment briefs, grading notes, one folder per assignment |
| [`lectures/`](lectures/) | Slides and notes, one folder per week or topic |
| [`general-info/`](general-info/) | Syllabus, schedule, policies, contacts, anything about the course itself |
| [`ideas/`](ideas/) | Ideas for labs, exercises and improvements, and notes to follow up |

## Labs

| Lab | Topic | Status |
|---|---|---|
| [Lab 1](labs/lab01-pandas/) | Introduction to pandas, on the SynDisco discussion dataset | parts 1 to 4 of 8 ready |

## Running the labs

```bash
pip install -r requirements.txt
jupyter lab
```

Then open the notebook of the lab you want, or open it on Colab (each lab README has the link pattern). Data is never stored in the repository: every notebook downloads what it needs, and the downloaded files are ignored by git.

## Conventions

- A lab lives in `labs/labNN-topic/` and has its own `README.md` (goals, files, how to run), its notebook, and a `figures/` folder if it has any.
- Notebooks are saved with their outputs, so they can be read without running them.
- Keep large or downloaded data out of git. Add its folder to `.gitignore`.
- If this repository becomes public, do not commit assignment briefs or solutions. The assignment brief currently in `assignments/` is already excluded in `.gitignore`.
