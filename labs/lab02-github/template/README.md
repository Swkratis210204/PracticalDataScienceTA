# Book crawler

A tiny crawler that reads the first pages of [books.toscrape.com](https://books.toscrape.com) (a site made for practising scraping) and saves the titles and prices to `books.jsonl`.

## Files

| File | What |
|---|---|
| `crawler.py` | the crawler |
| `requirements.txt` | the libraries it needs (empty for now, you fill it in) |
| `.env` | secrets, such as the API key (empty for now, you fill it in) |

## Run it

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install requests beautifulsoup4 python-dotenv
python crawler.py
```

It takes a few seconds and prints `saved 40 books to books.jsonl`.
