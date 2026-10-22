"""Fetch a web page as text. Stdlib urllib only, charset-aware."""
import re
import urllib.request

USER_AGENT = "web-to-markdown-agent/1.0 (+https://github.com/sina09185790374-design)"


def decode_body(raw, headers=None):
    """Decode bytes using the HTTP charset, then a <meta charset>, else UTF-8."""
    charset = None
    if headers is not None:
        try:
            charset = headers.get_content_charset()
        except Exception:
            charset = None
    if not charset:
        head = raw[:2048].decode("ascii", errors="ignore")
        m = re.search(r'charset=["\']?([\w-]+)', head, re.I)
        charset = m.group(1) if m else "utf-8"
    return raw.decode(charset, errors="replace")


def fetch_url(url, timeout=20):
    """GET a URL and return its HTML as text. Raises urllib errors on failure."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return decode_body(resp.read(), resp.headers)
