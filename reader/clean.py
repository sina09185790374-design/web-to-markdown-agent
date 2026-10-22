"""HTML -> clean Markdown, html.parser based (stdlib only).

Drops script/style/nav/footer/aside/form chrome; keeps headings, paragraphs,
lists, links, emphasis, blockquotes and images as Markdown.
"""
from html.parser import HTMLParser

DROP_TAGS = {"script", "style", "nav", "footer", "aside", "form", "iframe",
             "noscript", "svg", "button", "select", "textarea", "input",
             "head", "title"}
VOID_DROP = {"input"}
HEADINGS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}
BLOCK_END = {"p", "div", "section", "article", "tr", "blockquote", "pre",
             "table", "ul", "ol", "figure", "figcaption"}


class MarkdownParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []          # finished lines
        self.buf = []          # current inline text pieces
        self.drop_depth = 0
        self.list_stack = []   # True = ordered list
        self.link_href = None
        self.link_text = []
        self.in_pre = False

    # -- helpers ---------------------------------------------------------
    def _flush(self):
        text = " ".join("".join(self.buf).split())
        self.buf = []
        if text:
            self.out.append(text)

    def _emit_raw(self, line):
        self._flush()
        if line.strip():
            self.out.append(line)

    # -- tags ------------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in DROP_TAGS:
            if tag not in VOID_DROP:
                self.drop_depth += 1
            return
        if self.drop_depth:
            return
        if tag in HEADINGS:
            self._flush()
            self.buf.append("#" * HEADINGS[tag] + " ")
        elif tag == "a":
            self.link_href = attrs.get("href")
            self.link_text = []
        elif tag in ("strong", "b"):
            (self.link_text if self.link_href is not None else self.buf).append("**")
        elif tag in ("em", "i"):
            (self.link_text if self.link_href is not None else self.buf).append("*")
        elif tag == "code" and not self.in_pre:
            self.buf.append("`")
        elif tag == "pre":
            self.in_pre = True
            self._emit_raw("```")
        elif tag in ("ul", "ol"):
            self._flush()
            self.list_stack.append([tag == "ol", 0])
        elif tag == "li":
            self._flush()
            if self.list_stack and self.list_stack[-1][0]:
                self.list_stack[-1][1] += 1
                self.buf.append(f"{self.list_stack[-1][1]}. ")
            else:
                self.buf.append("- ")
        elif tag == "blockquote":
            self._flush()
            self.buf.append("> ")
        elif tag == "img":
            alt = attrs.get("alt", "")
            src = attrs.get("src", "")
            if src:
                self.buf.append(f"![{alt}]({src})")
        elif tag == "br":
            self.buf.append("\n")
        elif tag == "hr":
            self._emit_raw("---")

    def handle_endtag(self, tag):
        if tag in DROP_TAGS:
            if tag not in VOID_DROP and self.drop_depth:
                self.drop_depth -= 1
            return
        if self.drop_depth:
            return
        if tag == "a" and self.link_href is not None:
            text = "".join(self.link_text).strip() or self.link_href
            self.buf.append(f"[{text}]({self.link_href})")
            self.link_href = None
            self.link_text = []
        elif tag in ("strong", "b"):
            (self.link_text if self.link_href is not None else self.buf).append("**")
        elif tag in ("em", "i"):
            (self.link_text if self.link_href is not None else self.buf).append("*")
        elif tag == "code" and not self.in_pre:
            self.buf.append("`")
        elif tag == "pre":
            self.in_pre = False
            self._emit_raw("```")
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
            self._flush()
        elif tag in HEADINGS or tag in BLOCK_END or tag == "li":
            self._flush()

    def handle_data(self, data):
        if self.drop_depth:
            return
        if self.link_href is not None:
            self.link_text.append(data)
        else:
            self.buf.append(data)

    def markdown(self):
        self._flush()
        lines, blank = [], False
        for line in self.out:
            if line.strip():
                lines.append(line)
                blank = False
            elif not blank:
                lines.append("")
                blank = True
        return "\n\n".join(l for l in lines if l.strip()).strip() + "\n"
