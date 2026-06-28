# Indian Express News Scraper

A Python web scraper that collects full-text news articles from **Indian Express** using RSS feeds and BeautifulSoup.

## Features
- Scrapes **25 articles** across 8 sections: India, Politics, Business, Technology, Sports, World, Cities
- Extracts full article body text using BeautifulSoup CSS selectors
- Deduplicates articles across feeds
- Adds polite random delays (1.5–3s) to avoid rate-limiting
- Exports results to a clean **CSV file**

## Tech Stack
- Python 3
- `requests` — HTTP fetching
- `beautifulsoup4` — HTML parsing
- `pandas` — CSV export
- `xml.etree.ElementTree` — RSS feed parsing

## Installation

```bash
pip install requests beautifulsoup4 pandas
```

## Usage

```bash
python scrape_indian_express_Girish_Kumar.py
```

Output is saved to `Indian_Express_News_Girish_Kumar.csv` with columns:

| Column | Description |
|---|---|
| `NEWS_TITLE_Girish Kumar` | Article headline |
| `NEWS_LINK` | URL of the article |
| `FULL_SCRAPED_TEXT` | Full body text scraped from the page |

## Project Structure

```
indian-express-scraper/
├── scrape_indian_express_Girish_Kumar.py   # Main scraper script
├── README.md
└── .gitignore
```

## Author
**Girish Kumar**  
B.Tech Computer Science, D.Y. Patil Pratishthan's College of Engineering, Pune
