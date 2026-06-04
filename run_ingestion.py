import os
from ingestion import scrape_groww_url
from vector_db import chunk_text, build_vector_store

urls = [
    "https://groww.in/mutual-funds/tata-small-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/tata-gold-etf-fof-direct-growth",
    "https://groww.in/mutual-funds/tata-digital-india-fund-direct-growth",
    "https://groww.in/mutual-funds/tata-silver-etf-fof-direct-growth",
    "https://groww.in/mutual-funds/tata-arbitrage-fund-direct-growth"
]

all_chunks = []

for url in urls:
    print(f"Scraping: {url}")
    text = scrape_groww_url(url)
    chunks = chunk_text(text, source_url=url)
    all_chunks.extend(chunks)

print(f"Total chunks extracted: {len(all_chunks)}")
print("Building Vector Store...")
build_vector_store(all_chunks)
print("Done!")
