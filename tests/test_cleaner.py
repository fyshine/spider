import pytest

from novel_scraper.cleaner import clean_chapter_body, clean_text


def test_clean_text_removes_ads_and_controls():
    raw = "欢迎阅读，本章未完。\n\n点击进入广告页面。\n\n第一段小说内容。"
    cleaned = clean_text(raw)

    assert "本章未完" not in cleaned
    assert "点击进入广告页面" not in cleaned
    assert "第一段小说内容" in cleaned


def test_clean_chapter_body_deduplicates_paragraphs():
    raw = "第一段。\n\n第一段。\n\n第二段。"
    result = clean_chapter_body(raw)

    paragraphs = [p for p in result.split("\n\n") if p.strip()]
    assert paragraphs == ["第一段。", "第二段。"]


def test_clean_text_normalizes_whitespace_and_special_chars():
    raw = "第一段。\u00a0\u00a0  第二段。\n\n\u200b第三段。"
    result = clean_text(raw)

    assert "第一段。 第二段。" in result
    assert "第三段。" in result
