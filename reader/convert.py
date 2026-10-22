"""Convert HTML to clean, agent-ready Markdown."""
from .clean import MarkdownParser


def html_to_markdown(html):
    """Parse an HTML string and return Markdown text."""
    parser = MarkdownParser()
    parser.feed(html)
    parser.close()
    return parser.markdown()
