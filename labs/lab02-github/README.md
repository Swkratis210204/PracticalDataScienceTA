# Lab 2: Versioning with git and GitHub (about 50 min plus buffer)

Students receive a 20-line crawler (`template/`), put it under git, push it to a GitHub repo they create themselves, and then work through secrets, environments, branches, a merge and a pull request. Everyone follows the same steps live on their own repo, so the code and the history match the projector.

## Files

| File | What |
|---|---|
| `template/crawler.py` | the crawler: 2 pages of books.toscrape.com to `books.jsonl`, about 4 s; a fake API key is hardcoded on purpose |
| `template/README.md` | what students see: the files, and how to make the venv, install and run |
| `template/requirements.txt` | empty on purpose: students fill it in |
| `template/.env` | empty on purpose: students put the key in it |
| `teacher_guide.md` | the script for the lab: commands, timing, what to say, checks, common problems |
| `student_guide.md` | the students' step-by-step sheet with checkpoints, a cheat sheet and extra steps; share it as a separate file, not inside the zip (it would end up in their first commit) |
| `big_change/quotes.py` | the file students add in the pull request step (crawls quotes.toscrape.com); not in the zip |
| `lab2.zip` | `template/` zipped as a `book-crawler/` folder, to hand out |

The template deliberately has **no** `.gitignore` and no `.env.example`: students create them during the lab. The empty `.env` and `requirements.txt` are part of the initial commit.

## Libraries

`requests`, `beautifulsoup4`, `python-dotenv` (the last one is used from the secrets step). Measured on Windows: `venv` about 10 s, install about 7 s. `pip freeze` then lists 9 packages for the 3 installed, which is the "hand-written list vs full freeze" discussion.

## Flow

| Min | Step | Notes |
|---|---|---|
| 0-10 | Talk 1: why git and GitHub; download the template | |
| 10-15 | `git init`, **initial commit**, create an **empty** GitHub repo, `remote add`, `branch -M main`, `push`; start the venv and install | The key is in this first commit on purpose. Do not tick README or .gitignore on GitHub, the push is rejected otherwise. |
| 15-30 | Talk 2 + hands-on: secrets, `.env`, `.gitignore`, `requirements.txt`; mention tests and CI | `git status` shows `.venv/` and `books.jsonl` as untracked, that is the reason for `.gitignore`. `git log -p` shows the key is still in the history: rotate it. |
| 30-35 | Change the site in `crawler.py` (e.g. `PAGES`), **commit** | one-line diff |
| 35-40 | **New branch**, change, commit | everyone types the same change (put it on a slide) |
| 40-43 | **Merge** the branch into `main` | local merge, no review |
| 43-45 | Commit again on `main` | |
| 45-55 | New branch, bigger change, push, **pull request** on GitHub, merge, then `git pull` on `main` | you do the review demo on the projector; students open their own PR |
| rest | `log --graph`, hashes, other commands, tests (one function, one assertion) | cut freely |

## The secrets step (reference)

The fix, shown after the talk: `API_KEY = os.getenv("API_KEY")` with `load_dotenv()` at the top, a `.env` file holding `API_KEY=...`, `.env` and `.venv/` and `books.jsonl` and `__pycache__/` in `.gitignore`, and a `.env.example` with a placeholder. Needs `import os` and `from dotenv import load_dotenv`. `requirements.txt` gets the three libraries (hand-written, then compare with `pip freeze`).

**Trap, on purpose:** `.env` is already tracked (empty, in the initial commit). Adding it to `.gitignore` does nothing for a tracked file, so after the key goes in, `git status` still shows `.env` as modified and `git add .` would commit the secret. The fix is `git rm --cached .env`, then commit. Say it as: *`.gitignore` only affects files git does not track yet.* If you are short on time, tell them to write `.gitignore` before filling `.env`, and demo the trap on your own screen.

## Watch for

- Empty repo on GitHub, `main` vs `master`, and the first push (login) are the usual blockers. Ask students to install git and try one push the day before.
- Different edits make different diffs. Put the exact change to type on a slide.
- If the site is slow, 2 pages is already small. The crawl sleeps 0.5 s between pages, keep it.
- A "big change" for the PR demo: point the crawler at `quotes.toscrape.com` (different selectors), so the diff is worth reviewing.
