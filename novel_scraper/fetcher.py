import time
from typing import Dict, Optional

import requests

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_url(url: str, timeout: int = 10, retries: int = 3, backoff: float = 1.0, headers: Optional[Dict[str, str]] = None) -> str:
    """Fetch a URL and return the HTML response text."""
    session = requests.Session()
    request_headers = {**DEFAULT_HEADERS, **(headers or {})}

    last_exception = None
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=timeout, headers=request_headers)
            response.raise_for_status()
            response.encoding = response.encoding or "utf-8"
            return response.text
        except requests.RequestException as exc:
            last_exception = exc
            if attempt == retries:
                raise
            time.sleep(backoff * attempt)

    if last_exception is not None:
        raise last_exception
    return ""
