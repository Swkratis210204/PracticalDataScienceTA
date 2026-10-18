# Lab 2: git and GitHub, step by step

You get a small crawler. You put it under git, push it to GitHub, keep its secret out of the repo, and work with branches, a merge and a pull request. Do each step together with the class and raise your hand when you reach the checkpoint.

All commands run in a terminal opened in the `book-crawler` folder.

## Step 0. Before we start

Set your name once (use any email, it appears in your commits):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Unzip `lab2.zip` and open a terminal inside the `book-crawler` folder.

## Step 1. Put it under git and push it

```bash
git init
git add .
git commit -m "initial commit"
git branch -M main
```

On github.com click **New repository**, give it a name, and **do not tick** README, .gitignore or license. Then copy its URL:

```bash
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

**Checkpoint:** refresh the GitHub page, you see your files. `git log --oneline` shows one commit.

Now create the environment and install the libraries (it runs while we talk):

```bash
python -m venv .venv
# Windows PowerShell:  .venv\Scripts\Activate.ps1
# Windows cmd:         .venv\Scripts\activate.bat
# Mac / Linux:         source .venv/bin/activate
pip install requests beautifulsoup4 python-dotenv
```

## Step 2. Keep secrets and junk out of git

1. Run `python crawler.py`. It should print `saved 40 books to books.jsonl`.
2. Run `git status`. Which files does git want to track that it should not?
3. Run `git log -p`, press `q` to leave. Find the API key. It is already in your history.
4. Move the key to `.env`:
   - In `.env` write `API_KEY=sk-demo-1234567890abcdef`
   - In `crawler.py` add `import os` and `from dotenv import load_dotenv`, call `load_dotenv()`, and replace the hardcoded key with `API_KEY = os.getenv("API_KEY")`
   - Run the crawler again, it must still work.
5. Create `.gitignore` with these lines:
   ```
   .env
   .venv/
   __pycache__/
   books.jsonl
   ```
6. Run `git status` again. If `.env` is still listed as modified, git is still tracking it. Run `git rm --cached .env`.
7. Create `.env.example` with `API_KEY=your-key-here`.
8. Write `requirements.txt` with one library per line: `requests`, `beautifulsoup4`, `python-dotenv`. Compare with `pip freeze`.
9. Check, then commit and push:
   ```bash
   git status
   git add .
   git status
   git commit -m "move key to .env, add .gitignore and requirements"
   git push
   ```

**Checkpoint:** `git status` showed no `.env`, no `.venv`, no `books.jsonl` to be committed. On GitHub there is no `.env` with a key in it.

## Step 3. Change something and commit

In `crawler.py` change `PAGES = 2` to `PAGES = 3`.

```bash
git diff
git add crawler.py
git commit -m "crawl 3 pages"
git push
git log --oneline
```

**Checkpoint:** `git diff` showed one changed line, and `git log` now has 3 commits.

## Step 4. A branch

```bash
git branch new-feature
git switch new-feature
```

Change the line that adds a book to also store the rating:

```python
        books.append({"title": item.h3.a["title"], "price": item.select_one(".price_color").text, "rating": item.select_one(".star-rating")["class"][1]})
```

Run the crawler and look at `books.jsonl`: each book has a rating. Then:

```bash
git add crawler.py
git commit -m "add rating"
git push -u origin new-feature
```

**Checkpoint:** `git branch` shows `* new-feature`, and GitHub lists two branches.

## Step 5. Merge it into main

```bash
git switch main
```

Open `crawler.py`: the rating is gone. It lives only on the branch. Now bring it in:

```bash
git merge new-feature
git log --oneline
git push
```

**Checkpoint:** the rating is back in `crawler.py` and `main` and `new-feature` end at the same commit.

## Step 6. A pull request

Get `quotes.py` from your teacher and put it in the folder.

```bash
git branch quotes
git switch quotes
python quotes.py
git add quotes.py
git commit -m "add quotes crawler"
git push -u origin quotes
```

On GitHub:

1. Click **Compare & pull request**.
2. Write a title and a short description (what you changed and why).
3. Open the **Files changed** tab and read the diff.
4. Click **Merge pull request**, then **Confirm merge**.

Back in the terminal, your laptop does not know about the merge yet:

```bash
git switch main
git pull
git log --oneline --graph
```

**Checkpoint:** `quotes.py` is on `main` and the graph shows the branch splitting off and joining back.

## Cheat sheet

| I want to | Command |
|---|---|
| see what changed | `git status`, `git diff` |
| save a snapshot | `git add <file>`, `git commit -m "message"` |
| see the history | `git log --oneline`, `git log --oneline --graph --all` |
| make or list branches | `git branch <name>`, `git branch` |
| move to a branch | `git switch <name>` |
| join a branch into the current one | `git merge <name>` |
| send my commits to GitHub | `git push` |
| get new commits from GitHub | `git pull` |
| stop tracking a file but keep it | `git rm --cached <file>` |

The full reference is on [docs.github.com](https://docs.github.com/en/get-started/using-git/about-git).

## Extra steps (if you finish early)

Do them in any order.

1. **Fresh clone test.** Clone your repo into a new folder, create a new venv, run `pip install -r requirements.txt`, copy `.env.example` to `.env`, put the key in it, and run the crawler. This is what a teammate would do.
2. **Look inside commits.** `git log -p`, `git show <id>`. Find your hashes: what do the first 7 characters stand for?
3. **Undo a change.** Edit a file and run `git restore <file>` to throw the change away. Then make a bad commit and undo it with `git revert <id>`.
4. **A conflict, on purpose.** Make two branches that change the same line of `crawler.py` differently, merge both into `main`, and resolve the markers that git leaves in the file (`<<<<<<<`, `=======`, `>>>>>>>`).
5. **Write a README.** Add a section to `README.md`: what the project does, how to set up the environment, how to run it.
6. **A test.** Write a small function that turns a price like `£51.77` into the number `51.77`, and one `assert` that checks it.
7. **Another PR.** Change the number of pages through a variable in `.env`, open a PR for it, and describe it so that someone else can review it.
