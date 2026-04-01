"""Generic novel scraper package."""

from .fetcher import fetch_url
from .parser import parse_novel_page
from .cleaner import clean_text, clean_chapter_body
from .optimizer import optimize_chapters

__all__ = [
    "fetch_url",
    "parse_novel_page",
    "clean_text",
    "clean_chapter_body",
    "optimize_chapters",
]
