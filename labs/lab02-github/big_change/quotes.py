import json
import time

import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com/page/{}/"
PAGES = 2


def clean(text):
    # remove the curly quotation marks around a quote
    return text.strip("“”")


def crawl():
    quotes = []
    for page in range(1, PAGES + 1):
        r = requests.get(URL.format(page), timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        for item in soup.select("div.quote"):
            quotes.append({"text": clean(item.select_one("span.text").text), "author": item.select_one("small.author").text})
        time.sleep(0.5)  # be polite to the server
    return quotes


if __name__ == "__main__":  # runs only when you start this file, not when a test imports it
    quotes = crawl()
    with open("quotes.jsonl", "w", encoding="utf-8") as f:
        for quote in quotes:
            f.write(json.dumps(quote, ensure_ascii=False) + "\n")
    print(f"saved {len(quotes)} quotes to quotes.jsonl")
