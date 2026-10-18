import json
import time

import requests
from bs4 import BeautifulSoup

API_KEY = "sk-demo-1234567890abcdef"  # fake key, for the lab only
URL = "https://books.toscrape.com/catalogue/page-{}.html"
PAGES = 2

books = []
for page in range(1, PAGES + 1):
    r = requests.get(URL.format(page), headers={"X-API-Key": API_KEY}, timeout=10)
    soup = BeautifulSoup(r.content, "html.parser")
    for item in soup.select("article.product_pod"):
        books.append({"title": item.h3.a["title"], "price": item.select_one(".price_color").text})
    time.sleep(0.5)  # be polite to the server

with open("books.jsonl", "w", encoding="utf-8") as f:
    for book in books:
        f.write(json.dumps(book, ensure_ascii=False) + "\n")

print(f"saved {len(books)} books to books.jsonl")
