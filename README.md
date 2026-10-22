# Web-to-Markdown Agent 🌐➡️📝

Fetch any web page and convert it to **clean, agent-ready Markdown** — the Crawl4AI pattern, re-implemented from scratch in ~150 lines of stdlib-only Python. No dependencies, no API keys, no headless browser.

Agents are only as good as their web context. This strips the chrome (nav, footer, sidebars, scripts, styles) and keeps the content: headings, lists, links, emphasis, quotes, images.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB) ![License](https://img.shields.io/badge/license-MIT-green) ![Deps](https://img.shields.io/badge/deps-stdlib%20only-brightgreen)

## Quick start
```bash
python3 main.py --demo                          # convert the bundled sample.html
python3 main.py --url https://example.com/page  # fetch + convert a live page
python3 main.py --file page.html                # convert a local file
```

## As a library
```python
from reader.convert import html_to_markdown
from reader.fetch import fetch_url

md = html_to_markdown(fetch_url("https://example.com"))
```

## What survives the clean-up
| HTML | Markdown |
|---|---|
| `h1`–`h6` | `#`–`######` |
| `a href` | `[text](url)` |
| `ul/ol li` | `- item` / `1. item` |
| `strong/em/code` | `**bold**` / `*italic*` / `` `code` `` |
| `blockquote`, `img` | `> quote`, `![alt](src)` |
| `script/style/nav/footer/aside/form` | **dropped** |

Persian/RTL pages work out of the box (charset detected from headers or `<meta>`), which is exactly what our shop's price-watch and trend-radar pipelines need.

## Tests
```bash
python3 -m unittest discover -s tests -v   # 12 tests
python3 main.py --demo
```

## فارسی 🇮🇷
هر صفحه وبی رو می‌خونه و به مارک‌داون تمیز و آماده ایجنت تبدیل می‌کنه — بدون ناوبری و فوتر و اسکریپت و تبلیغات کناری. الگوی Crawl4AI، ولی پیاده‌سازی اصل و سبک خودمون با کتابخانه استاندارد پایتون. صفحات فارسی و راست‌چین هم کامل پشتیبانی می‌شن. تو خط لوله رادار ترند و چک قیمت مغازه‌مون استفاده می‌شه.

ساخته‌شده در «خدمات کامپیوتری سینا» — اراک. تلگرام: [@sarzamin_game11](https://t.me/sarzamin_game11)

## License
MIT
