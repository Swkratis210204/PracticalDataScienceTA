import json
import time

import requests
from bs4 import BeautifulSoup

API_KEY = ""  # the key that is sent to the server with every request
URL = "https://books.toscrape.com/catalogue/page-{}.html"  # {} becomes the page number
PAGES = 2  # how many pages to crawl

books = []
for page in range(1, PAGES + 1):
    # download one page, sending the key in a header
    r = requests.get(URL.format(page), headers={"X-API-Key": API_KEY}, timeout=10)
    soup = BeautifulSoup(r.content, "html.parser")  # turn the HTML into something we can search
    # every book on the page is an <article class="product_pod">
    for item in soup.select("article.product_pod"):
        books.append({"title": item.h3.a["title"], "price": item.select_one(".price_color").text})
    time.sleep(0.5)  # be polite to the server

# save one book per line (JSON Lines)
with open("books.jsonl", "w", encoding="utf-8") as f:
    for book in books:
        f.write(json.dumps(book, ensure_ascii=False) + "\n")

print(f"saved {len(books)} books to books.jsonl")
