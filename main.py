#!/usr/bin/env python3
"""CLI: fetch a web page (or a local file) and print clean Markdown.

Usage:
  python3 main.py --demo                 # convert the bundled sample.html
  python3 main.py --url https://example.com/page
  python3 main.py --file page.html
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reader.convert import html_to_markdown
from reader.fetch import fetch_url

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser(description="Web page -> clean Markdown")
    ap.add_argument("--demo", action="store_true", help="convert sample.html")
    ap.add_argument("--url", help="fetch and convert this URL")
    ap.add_argument("--file", help="convert a local HTML file")
    args = ap.parse_args()
    if args.demo:
        html = open(os.path.join(HERE, "sample.html"), encoding="utf-8").read()
    elif args.url:
        html = fetch_url(args.url)
    elif args.file:
        html = open(args.file, encoding="utf-8").read()
    else:
        ap.print_help()
        return 2
    print(html_to_markdown(html))
    return 0


if __name__ == "__main__":
    sys.exit(main())
