# Novel Scraper

A generic Python novel crawler and cleaner for extracting novel chapters, removing ads and noise, and normalizing text.

## Features

- Fetch page HTML from a URL using `requests`
- Parse title and content with generic heuristics
- Clean ads, repeated content, and abnormal characters
- Normalize whitespace and paragraph structure
- Provide a CLI interface for scraping and export

## Quick start

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Or install from the project with:

```bash
python -m pip install .
```

Run the scraper:

```bash
python -m novel_scraper.cli https://example.com/novel/chapter-1
```

Use optional selector configuration for custom sites:

```bash
python -m novel_scraper.cli https://example.com/novel/chapter-1 --selectors selectors.json
```

## Modules

- `novel_scraper.fetcher` — fetch HTML safely
- `novel_scraper.parser` — parse generic novel pages
- `novel_scraper.cleaner` — clean advertisements and duplicates
- `novel_scraper.optimizer` — optimize chapter structure
- `novel_scraper.cli` — command line interface
