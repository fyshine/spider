import argparse
import json
import sys
from typing import Dict, Optional

from .cleaner import clean_chapters
from .fetcher import fetch_url
from .optimizer import optimize_chapters
from .parser import load_selectors_from_json, parse_novel_page


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch and clean novel content from a web page."
    )
    parser.add_argument("url", help="URL of the novel chapter page to scrape")
    parser.add_argument(
        "--selectors",
        help="Optional JSON file with custom CSS selectors for title and content",
        default=None,
    )
    parser.add_argument(
        "--output",
        help="Optional output file path. If omitted, prints to stdout.",
        default=None,
    )
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Output structured JSON containing title and chapters.",
    )
    return parser


def render_output(data: Dict[str, object], as_json: bool = False) -> str:
    if as_json:
        return json.dumps(data, ensure_ascii=False, indent=2)

    lines = [f"Title: {data.get('title', '')}".strip(), ""]
    for chapter in data.get("chapters", []):
        heading = chapter.get("heading", "")
        if heading:
            lines.append(heading)
            lines.append("-")
        lines.append(chapter.get("body", ""))
        lines.append("")
    return "\n".join(lines).strip()


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    selectors = None
    if args.selectors:
        selectors = load_selectors_from_json(args.selectors)

    try:
        html = fetch_url(args.url)
    except Exception as exc:
        print(f"Error fetching URL: {exc}", file=sys.stderr)
        return 2

    parsed = parse_novel_page(html, selectors=selectors)
    cleaned = clean_chapters(parsed.get("chapters", []))
    optimized = optimize_chapters(cleaned)

    result = {
        "title": parsed.get("title", ""),
        "chapters": optimized,
    }
    output_text = render_output(result, as_json=args.as_json)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output_text)
    else:
        print(output_text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
