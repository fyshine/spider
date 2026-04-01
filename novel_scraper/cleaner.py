import re
from typing import Iterable, List

AD_PATTERN = re.compile(
    r"(?:广告|点击|推荐|免费阅读|本章未完|本章完|【.*?】|\(.*?\)|〖.*?〗|阅读提示|充值|打赏|VIP|首发|点击进入|扫描二维码|关注公众号)",
    flags=re.IGNORECASE,
)

INVALID_CHAR_PATTERN = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\u200b\u200c\u200d\ufeff]")
MULTI_SPACE_PATTERN = re.compile(r"[ \t\u3000]+")
MULTI_NEWLINE_PATTERN = re.compile(r"\n{3,}")


def _clean_paragraph(text: str) -> str:
    text = INVALID_CHAR_PATTERN.sub("", text)
    text = AD_PATTERN.sub("", text)
    text = text.replace("\u00a0", " ")
    text = MULTI_SPACE_PATTERN.sub(" ", text)
    text = text.strip()
    return text


def clean_text(text: str) -> str:
    """Clean a full novel text block."""
    if not text:
        return ""

    paragraphs: List[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        cleaned = _clean_paragraph(paragraph)
        if cleaned:
            paragraphs.append(cleaned)

    normalized = "\n\n".join(paragraphs)
    normalized = MULTI_NEWLINE_PATTERN.sub("\n\n", normalized)
    return normalized.strip()


def clean_chapter_body(body: str) -> str:
    """Clean a chapter body and remove duplicate lines."""
    cleaned = clean_text(body)
    paragraphs = [para.strip() for para in cleaned.split("\n\n") if para.strip()]

    seen = set()
    unique_paragraphs: List[str] = []
    for paragraph in paragraphs:
        if paragraph in seen:
            continue
        seen.add(paragraph)
        unique_paragraphs.append(paragraph)

    return "\n\n".join(unique_paragraphs)


def clean_chapters(chapters: Iterable[dict]) -> List[dict]:
    cleaned = []
    for item in chapters:
        body = item.get("body", "")
        cleaned_body = clean_chapter_body(body)
        cleaned.append({"heading": item.get("heading", ""), "body": cleaned_body})
    return cleaned
