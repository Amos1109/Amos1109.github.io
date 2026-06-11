"""Convert main.md to main.html with KaTeX support."""
import re
from pathlib import Path

MD_PATH = Path(__file__).parent / "main.md"
HTML_PATH = Path(__file__).parent / "main.html"

HTML_HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aerial Vision-Language Navigation - Yuting Hong</title>
  <meta name="author" content="Yuting Hong">
  <meta name="description" content="Notes on aerial vision-language navigation: end-to-end, modular, and trajectory-based approaches.">
  <link rel="shortcut icon" href="../../images/favicon/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
  <style>
    :root {
      --primary: #1a73e8;
      --bg: #f5f7fa;
      --card: #ffffff;
      --text: #333;
      --muted: #666;
      --border: #e8eaed;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      line-height: 1.75;
    }
    .post-container {
      max-width: 860px;
      margin: 0 auto;
      padding: 40px 20px 64px;
    }
    .back-link {
      display: inline-block;
      margin-bottom: 24px;
      color: var(--primary);
      text-decoration: none;
    }
    .back-link:hover { text-decoration: underline; }
    .post-header h1 {
      font-size: 2rem;
      margin: 0 0 8px;
      line-height: 1.25;
    }
    .post-meta {
      color: #888;
      font-size: 0.95rem;
      margin-bottom: 28px;
    }
    .summary-box {
      background: linear-gradient(135deg, #e8f0fe 0%, #f1f8ff 100%);
      border-left: 4px solid var(--primary);
      border-radius: 8px;
      padding: 20px 24px;
      margin-bottom: 28px;
      color: #444;
    }
    .summary-box strong { color: var(--primary); }
    .toc {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px 24px;
      margin-bottom: 32px;
    }
    .toc h2 {
      font-size: 1rem;
      margin: 0 0 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .toc ol {
      margin: 0;
      padding-left: 1.25rem;
    }
    .toc a {
      color: var(--primary);
      text-decoration: none;
    }
    .toc a:hover { text-decoration: underline; }
    .post-body section {
      background: var(--card);
      border-radius: 10px;
      padding: 28px 32px;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
      border: 1px solid var(--border);
    }
    .post-body h2 {
      font-size: 1.45rem;
      margin: 0 0 20px;
      padding-bottom: 10px;
      border-bottom: 2px solid var(--primary);
      color: var(--text);
    }
    .post-body h2:not(:first-child) { margin-top: 8px; }
    .post-body h3 {
      font-size: 1.15rem;
      margin: 28px 0 10px;
      color: #222;
      line-height: 1.4;
    }
    .post-body h4 {
      font-size: 1rem;
      margin: 20px 0 8px;
      color: var(--primary);
    }
    .post-body p { margin: 0 0 1em; }
    .post-body ul, .post-body ol {
      margin: 0 0 1em;
      padding-left: 1.5rem;
    }
    .post-body li { margin-bottom: 0.35em; }
    .post-body li > ul, .post-body li > ol { margin-top: 0.35em; }
    .paper-meta {
      font-style: italic;
      color: var(--muted);
      margin: -4px 0 14px;
      font-size: 0.95rem;
    }
    .paper-summary {
      background: #f8f9fb;
      border-left: 3px solid #90caf9;
      padding: 12px 16px;
      margin: 0 0 18px;
      border-radius: 0 6px 6px 0;
      color: #555;
      font-size: 0.98rem;
    }
    .post-body img {
      display: block;
      max-width: 100%;
      height: auto;
      margin: 16px auto 20px;
      border-radius: 6px;
      border: 1px solid var(--border);
    }
    .post-body hr {
      border: none;
      border-top: 1px solid var(--border);
      margin: 24px 0;
    }
    .katex-display {
      margin: 1em 0;
      overflow-x: auto;
      overflow-y: hidden;
    }
    @media (max-width: 640px) {
      .post-body section { padding: 20px 18px; }
      .post-header h1 { font-size: 1.6rem; }
    }
  </style>
</head>
<body>
  <div class="post-container">
    <a class="back-link" href="../index.html">&larr; Back to Blog</a>
    <header class="post-header">
      <h1>Aerial Vision-Language Navigation</h1>
      <p class="post-meta">Yuting Hong · 2026-06-11 · Paper Reading</p>
    </header>
"""

HTML_TAIL = """
  </div>
  <script>
    document.addEventListener("DOMContentLoaded", function () {
      renderMathInElement(document.body, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$", right: "$", display: false }
        ],
        throwOnError: false
      });
    });
  </script>
</body>
</html>
"""


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_]+", "-", text.strip())


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    html_parts = []
    i = 0
    in_list = False
    list_type = None
    in_section = False
    section_open = False
    skip_until_content = True

    def close_list():
        nonlocal in_list, list_type
        if in_list:
            html_parts.append(f"</{list_type}>")
            in_list = False
            list_type = None

    def close_section():
        nonlocal section_open
        if section_open:
            html_parts.append("</section>")
            section_open = False

    def open_section_if_needed():
        nonlocal in_section
        if not in_section:
            html_parts.append('<article class="post-body">')
            in_section = True

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            close_list()
            i += 1
            continue

        if stripped == "---":
            close_list()
            i += 1
            continue

        if stripped.startswith("# "):
            close_list()
            i += 1
            continue

        if stripped.startswith("> **总结**"):
            summary_lines = []
            i += 1
            while i < len(lines) and lines[i].strip().startswith(">"):
                summary_lines.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            html_parts.append(
                '<div class="summary-box"><strong>总结</strong><br>'
                + format_inline("<br>".join(summary_lines))
                + "</div>"
            )
            continue

        if stripped.startswith("## 目录"):
            toc_items = []
            i += 1
            while i < len(lines):
                item = lines[i].strip()
                if not item:
                    i += 1
                    continue
                m = re.match(r"^\d+\.\s+\[(.+?)\]\(#(.+?)\)", item)
                if not m:
                    break
                toc_items.append((m.group(1), m.group(2)))
                i += 1
            if toc_items:
                items = "".join(f'<li><a href="#{slug}">{title}</a></li>' for title, slug in toc_items)
                html_parts.append(f'<nav class="toc"><h2>目录</h2><ol>{items}</ol></nav>')
            continue

        if stripped.startswith("## "):
            close_list()
            open_section_if_needed()
            close_section()
            title = stripped[3:].strip()
            sid = slugify(title)
            html_parts.append(f'<section id="{sid}"><h2>{title}</h2>')
            section_open = True
            i += 1
            continue

        if stripped.startswith("### "):
            close_list()
            open_section_if_needed()
            html_parts.append(f"<h3>{stripped[4:].strip()}</h3>")
            i += 1
            continue

        if stripped.startswith("#### "):
            close_list()
            open_section_if_needed()
            html_parts.append(f"<h4>{stripped[5:].strip()}</h4>")
            i += 1
            continue

        if stripped.startswith("*") and stripped.endswith("*") and not stripped.startswith("**"):
            close_list()
            open_section_if_needed()
            html_parts.append(f'<p class="paper-meta">{stripped.strip("*")}</p>')
            i += 1
            continue

        if stripped.startswith("> ") and not stripped.startswith("> **总结**"):
            close_list()
            open_section_if_needed()
            html_parts.append(f'<p class="paper-summary">{stripped[2:].strip()}</p>')
            i += 1
            continue

        if re.match(r"^!\[.*\]\(.*\)$", stripped):
            close_list()
            open_section_if_needed()
            m = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
            alt, src = m.group(1), m.group(2)
            html_parts.append(f'<img src="{src}" alt="{alt}">')
            i += 1
            continue

        if re.match(r"^[-*]\s+", stripped):
            open_section_if_needed()
            if not in_list or list_type != "ul":
                close_list()
                html_parts.append("<ul>")
                in_list = True
                list_type = "ul"
            html_parts.append(f"<li>{format_inline(stripped[2:].strip())}</li>")
            i += 1
            continue

        if re.match(r"^\d+\.\s+", stripped):
            open_section_if_needed()
            if not in_list or list_type != "ol":
                close_list()
                html_parts.append("<ol>")
                in_list = True
                list_type = "ol"
            content = re.sub(r"^\d+\.\s+", "", stripped)
            html_parts.append(f"<li>{format_inline(content)}</li>")
            i += 1
            continue

        if stripped.startswith("$$"):
            close_list()
            open_section_if_needed()
            math_lines = [stripped[2:]]
            if not stripped.endswith("$$") or stripped == "$$":
                i += 1
                while i < len(lines) and not lines[i].strip().endswith("$$"):
                    math_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    math_lines.append(lines[i].strip()[:-2])
                    i += 1
            else:
                math_lines = [stripped[2:-2]]
                i += 1
            html_parts.append(f'<p>$${" ".join(math_lines).strip()}$$</p>')
            continue

        close_list()
        open_section_if_needed()
        html_parts.append(f"<p>{format_inline(stripped)}</p>")
        i += 1

    close_list()
    close_section()
    if in_section:
        html_parts.append("</article>")

    return "\n".join(html_parts)


def format_inline(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def main():
    md = MD_PATH.read_text(encoding="utf-8")
    body = md_to_html(md)
    HTML_PATH.write_text(HTML_HEAD + body + HTML_TAIL, encoding="utf-8")
    print(f"Wrote {HTML_PATH}")


if __name__ == "__main__":
    main()
