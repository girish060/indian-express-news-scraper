import time
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

TARGET_COUNT = 25
MIN_DELAY    = 1.5
MAX_DELAY    = 3.0
OUTPUT_FILE  = "Indian_Express_News_Girish_Kumar.csv"

RSS_FEEDS = [
    "https://indianexpress.com/feed/",
    "https://indianexpress.com/section/india/feed/",
    "https://indianexpress.com/section/politics/feed/",
    "https://indianexpress.com/section/business/feed/",
    "https://indianexpress.com/section/technology/feed/",
    "https://indianexpress.com/section/sports/feed/",
    "https://indianexpress.com/section/world/feed/",
    "https://indianexpress.com/section/cities/feed/",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


def get_links_from_rss():
    seen  = set()
    items = []

    for feed_url in RSS_FEEDS:
        if len(items) >= TARGET_COUNT + 15:
            break

        print(f"  Reading feed: {feed_url} ...")
        try:
            resp = requests.get(feed_url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)

            for item in root.iter("item"):
                title_el = item.find("title")
                link_el  = item.find("link")

                title = title_el.text.strip() if title_el is not None else ""
                link  = link_el.text.strip()  if link_el  is not None else ""

                if link and link not in seen and len(title) > 10:
                    seen.add(link)
                    items.append({"title": title, "link": link})

        except Exception as e:
            print(f"  [Error] {feed_url}: {e}")

        time.sleep(random.uniform(1.0, 2.0))

    print(f"  Found {len(items)} unique article links.")
    return items


def get_article_text(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for selector in ["div.full-details", "div#pcl-full-content", "div.story_details", "div.article-body"]:
            container = soup.select_one(selector)
            if container:
                paras = [p.get_text(strip=True) for p in container.find_all("p") if len(p.get_text(strip=True)) > 40]
                if paras:
                    return " ".join(paras)

        paras = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 60]
        return " ".join(paras[:30])

    except Exception as e:
        print(f"  [Error fetching article] {e}")
        return ""


def main():
    print("=" * 60)
    print("Indian Express News Scraper - Girish Kumar")
    print("=" * 60)

    print("\n[1] Collecting article links from RSS feeds ...")
    articles = get_links_from_rss()

    if not articles:
        print("ERROR: No article links found.")
        return

    print(f"\n[2] Scraping up to {TARGET_COUNT} articles ...")
    records = []

    for idx, article in enumerate(articles):
        if len(records) >= TARGET_COUNT:
            break

        print(f"  [{idx + 1}] {article['title'][:70]} ...")
        time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

        full_text = get_article_text(article["link"])

        if full_text:
            records.append({
                "NEWS_TITLE_Girish Kumar": article["title"],
                "NEWS_LINK":               article["link"],
                "FULL_SCRAPED_TEXT":        full_text,
            })
            print(f"    OK {len(full_text)} chars scraped")
        else:
            print("    SKIP No text found.")

    print(f"\n[3] Building DataFrame with {len(records)} articles ...")
    df = pd.DataFrame(records, columns=[
        "NEWS_TITLE_Girish Kumar",
        "NEWS_LINK",
        "FULL_SCRAPED_TEXT",
    ])

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"\n[4] Saved -> {OUTPUT_FILE}")
    print(f"    Rows: {len(df)}  |  Columns: {list(df.columns)}")
    print("\nDone!")


if __name__ == "__main__":
    main()