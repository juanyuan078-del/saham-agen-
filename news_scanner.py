# news_scanner.py
# Scan RSS feed berita, cari judul yang relevan sama kode saham tertentu
# dan mengandung kata kunci "cerita korporasi" (akuisisi, merger, dll).

import feedparser
from config import NEWS_RSS_FEEDS, NEWS_KEYWORDS


def _fetch_all_entries():
    entries = []
    for feed_url in NEWS_RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            entries.extend(feed.entries)
        except Exception as e:
            print(f"Gagal ambil RSS {feed_url}: {e}")
    return entries


def get_news_signal(kode_saham: str, entries: list = None) -> str | None:
    """
    Cari judul berita yang menyebut kode saham (tanpa .JK) DAN
    mengandung salah satu kata kunci akuisisi/korporasi.
    Return judul berita pertama yang cocok, atau None kalau gak ada.
    """
    ticker_short = kode_saham.replace(".JK", "")
    if entries is None:
        entries = _fetch_all_entries()

    for entry in entries:
        title = getattr(entry, "title", "")
        title_lower = title.lower()

        if ticker_short.lower() not in title_lower:
            continue

        for kw in NEWS_KEYWORDS:
            if kw.lower() in title_lower:
                return title

    return None
