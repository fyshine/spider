from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

DEFAULT_SELECTORS = {
    "title": ["title", "h1", ".chapter-title", ".book-title"],
    "content": ["#content", ".content", ".chapter-content", ".read-content", ".novel-content"],
}


def _normalize_selector(value: str) -> str:
    return value.strip()


def _find_first_text(soup: BeautifulSoup, selectors: List[str]) -> Optional[str]:
    for selector in selectors:
        tag = soup.select_one(selector)
        if tag and tag.get_text(strip=True):
            return tag.get_text(separator=" ", strip=True)
    return None


def _choose_content_block(soup: BeautifulSoup, selectors: List[str]) -> Optional[Tag]:
    for selector in selectors:
        tag = soup.select_one(selector)
        if isinstance(tag, Tag):
            return tag

    content_candidates = [
        tag for tag in soup.find_all(True) if tag.name in {"article", "section", "div"}
        and (tag.get("id", "").lower().find("content") >= 0 or tag.get("class", []) and any("content" in c.lower() or "chapter" in c.lower() for c in tag.get("class", [])))
    ]
    if content_candidates:
        return max(content_candidates, key=lambda element: len(element.get_text(strip=True)))
    return None


def _split_chapters(block: Tag) -> List[Dict[str, Any]]:
    chapters: List[Dict[str, Any]] = []
    current_heading = None
    current_paragraphs: List[str] = []

    for element in block.find_all(recursive=False):
        if element.name and element.name.startswith("h") and element.get_text(strip=True):
            if current_paragraphs:
                chapters.append({
                    "heading": current_heading or "",
                    "body": "\n\n".join(current_paragraphs).strip(),
                })
                current_paragraphs = []
            current_heading = element.get_text(separator=" ", strip=True)
            continue

        if element.name == "p":
            text = element.get_text(separator=" ", strip=True)
            if text:
                current_paragraphs.append(text)
            continue

        if element.name in {"div", "span"}:
            text = element.get_text(separator=" ", strip=True)
            if text:
                current_paragraphs.append(text)

    if current_paragraphs:
        chapters.append({
            "heading": current_heading or "",
            "body": "\n\n".join(current_paragraphs).strip(),
        })

    if not chapters:
        body_text = block.get_text(separator="\n\n", strip=True)
        if body_text:
            chapters.append({"heading": "", "body": body_text})

    return chapters


def parse_novel_page(html: str, selectors: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Parse HTML and return the novel title and chapter bodies."""
    soup = BeautifulSoup(html, "html.parser")
    selectors = selectors or {}

    title_selectors = selectors.get("title") if selectors.get("title") else DEFAULT_SELECTORS["title"]
    content_selectors = selectors.get("content") if selectors.get("content") else DEFAULT_SELECTORS["content"]

    title = _find_first_text(soup, [ _normalize_selector(item) for item in title_selectors ]) or ""
    content_block = _choose_content_block(soup, [ _normalize_selector(item) for item in content_selectors ])

    chapters: List[Dict[str, Any]] = []
    if content_block is not None:
        chapters = _split_chapters(content_block)
    else:
        body_text = soup.get_text(separator="\n\n", strip=True)
        chapters.append({"heading": title or "", "body": body_text})

    return {"title": title, "chapters": chapters}


def load_selectors_from_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        selectors = json.load(handle)
    if not isinstance(selectors, dict):
        raise ValueError("Selector configuration must be a JSON object.")
    return selectors
