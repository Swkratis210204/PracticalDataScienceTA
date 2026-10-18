# Lab 2: Versioning with git and GitHub (about 50 min plus buffer)

Students receive a 20-line crawler (`template/`), put it under git, push it to a GitHub repo they create themselves, and then work through secrets, environments, branches, a merge and a pull request. Everyone follows the same steps live on their own repo, so the code and the history match the projector.

## Files

| File | What |
|---|---|
| `template/crawler.py` | the crawler: 2 pages of books.toscrape.com to `books.jsonl`, about 4 s; `API_KEY` starts empty, the teacher types a fake key into it during the secrets step |
| `template/README.md` | what students see: the files, and how to make the venv, install and run |
| `template/requirements.txt` | empty on purpose: students fill it in |
| `template/.env` | empty on purpose: students put the key in it |
| `teacher_guide.md` | the script for the lab: commands, timing, what to say, checks, common problems |
| `student_guide.md` | the students' step-by-step sheet with checkpoints and extra steps |
| `student_guide.pdf` | the student guide as a PDF, made from `student_guide.md` (regenerate it after editing the markdown) |
| `git-cheat-sheet-education.pdf` | GitHub's official cheat sheet, from their documentation |
| `template/test_quotes.py` | one test of `clean()` from `quotes.py`. In the repo from the first commit, but it fails with an import error until `quotes.py` is added in the PR step, so students should not run `pytest` before then |
| `template/.github/workflows/test.yml` | GitHub Actions: installs `requirements.txt` plus `pytest` and runs `pytest`. Runs only on pull requests (`on: pull_request`), never on a push, so nothing runs before the PR step |
| `big_change/quotes.py` | the **one** file students add in the pull request step: it crawls quotes.toscrape.com and has a small `clean()` function. Upload it as a loose file next to the zip |
| `lab2.zip` | the starting repo: `template/` zipped as a `book-crawler/` folder, plus `student_guide.pdf` **next to it, not inside it** (so it is not part of the first commit). **Upload** `lab2.zip` and `big_change/quotes.py`. If you change `template/` or the student guide, rebuild it |

The template deliberately has **no** `.gitignore`: students create it during the lab. The empty `.env` and `requirements.txt` are part of the initial commit.

## Libraries

`requests`, `beautifulsoup4`, `python-dotenv` (the last one is used from the secrets step). Measured on Windows: `venv` about 10 s, install about 7 s. `pip freeze` then lists 9 packages for the 3 installed, which is the "hand-written list vs full freeze" discussion.

## Flow

| Min | Step | Notes |
|---|---|---|
| 0-10 | Talk 1: why git and GitHub; download the template | |
| 10-15 | `git init`, **initial commit**, create an **empty** GitHub repo, `remote add`, `branch -M main`, `push`; start the venv and install | The empty `.env` is in this first commit on purpose. Do not tick README or .gitignore on GitHub, the push is rejected otherwise. |
| 15-30 | Talk 2 + hands-on: key in the code, move to `.env`, `git rm --cached`, `load_dotenv`, `.gitignore`, `requirements.txt`; commit **without pushing**; mention tests and CI | the story is in the next section |
| 30-35 | Change the site in `crawler.py` (e.g. `PAGES`), **commit**, then one **push** for both commits | one-line diff |
| 35-40 | **New branch**, change, commit | everyone types the same change (put it on a slide) |
| 40-43 | **Merge** the branch into `main` | local merge, no review |
| 43-45 | Commit again on `main` | |
| 45-57 | New branch, copy in the PR files, push, **pull request** on GitHub, watch the test run (green tick), merge, then `git pull` on `main` | you break the test on your repo to show the red cross; students open their own PR |
| rest | `log --graph`, hashes, other commands, tests (one function, one assertion) | cut freely |

## The secrets step (reference)

The story, in order (details in `teacher_guide.md`, step 3):

1. The initial commit has an empty `API_KEY` and an empty, **tracked** `.env`.
2. You type a fake key into the code and run it. Say: anyone who sees the repo sees the key.
3. Move it to `.env`. `git status` shows `.env` as modified: it is tracked, so the next commit would publish the key. `git rm --cached .env` stops tracking it (the file stays on disk). The key never enters the history.
4. Load it from the code: `load_dotenv()` and `API_KEY = os.getenv("API_KEY")` (needs `import os` and `from dotenv import load_dotenv`).
5. `git status` now shows `.env`, `.venv/` and `books.jsonl` as untracked, and `git add .` would take all of them (untracking does not stop git from adding a file again). `.gitignore` with those names, plus `__pycache__/`, fixes it.
6. `requirements.txt` with the three libraries (hand-written, then compare with `pip freeze`).
7. Commit, but do not push. The next step makes one more commit and one push sends both.

A `.env.example` with fake values is only an extra step, for repos that other people clone.

**Python 3.13 and newer** write a `.gitignore` containing `*` inside `.venv/`, so on those versions git never shows the venv. On 3.12 or older it appears as untracked and `git add .` adds about 1,200 files (19 MB). Do not build the lesson on the venv appearing; the `.venv/` line in `.gitignore` is good practice on any version.

## Watch for

- Empty repo on GitHub, `main` vs `master`, and the first push (login) are the usual blockers. Ask students to install git and try one push the day before.
- Different edits make different diffs. Put the exact change to type on a slide.
- If the site is slow, 2 pages is already small. The crawl sleeps 0.5 s between pages, keep it.
- A "big change" for the PR demo: point the crawler at `quotes.toscrape.com` (different selectors), so the diff is worth reviewing.
