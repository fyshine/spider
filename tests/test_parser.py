from novel_scraper.parser import parse_novel_page


def test_parse_novel_page_falls_back_to_title_and_body():
    html = """
    <html>
      <head><title>测试小说</title></head>
      <body>
        <div id=content>
          <h1>第一章 初始</h1>
          <p>这是小说的第一段。</p>
          <p>这是小说的第二段。</p>
        </div>
      </body>
    </html>
    """

    parsed = parse_novel_page(html)
    assert parsed["title"] == "测试小说"
    assert len(parsed["chapters"]) == 1
    assert parsed["chapters"][0]["heading"] == "第一章 初始"
    assert "这是小说的第一段" in parsed["chapters"][0]["body"]


def test_parse_novel_page_uses_content_selector_when_provided():
    html = """
    <html>
      <body>
        <div class="book-content">
          <h2>第二章 转折</h2>
          <p>转折段落。</p>
        </div>
      </body>
    </html>
    """

    parsed = parse_novel_page(html, selectors={"content": [".book-content"], "title": ["h2"]})
    assert parsed["title"] == "第二章 转折"
    assert parsed["chapters"]
    assert parsed["chapters"][0]["heading"] == "第二章 转折"
