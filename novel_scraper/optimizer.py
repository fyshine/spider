from typing import List, Dict


def _join_short_lines(body: str, min_length: int = 40) -> str:
    paragraphs = [line.strip() for line in body.split("\n\n") if line.strip()]
    merged: List[str] = []

    for paragraph in paragraphs:
        if merged and len(paragraph) < min_length and not paragraph.endswith(("。", "！", "？", ".", "!", "?")):
            merged[-1] = merged[-1] + " " + paragraph
        else:
            merged.append(paragraph)

    return "\n\n".join(merged)


def _normalize_heading(heading: str, index: int) -> str:
    heading = heading.strip()
    if heading:
        return heading
    return f"Chapter {index + 1}"


def optimize_chapters(chapters: List[Dict[str, str]]) -> List[Dict[str, str]]:
    optimized = []
    for index, item in enumerate(chapters):
        heading = _normalize_heading(item.get("heading", ""), index)
        body = _join_short_lines(item.get("body", ""))
        optimized.append({"heading": heading, "body": body})
    return optimized
