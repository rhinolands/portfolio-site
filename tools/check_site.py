"""Pre-publish gate for the portfolio site (stdlib only).

Checks site/index.html for:
  1. HTML well-formedness: every non-void tag is closed in order.
  2. AI tells in visible text: em dash, en dash, double hyphen, semicolon, curly quotes.
  3. Leak patterns anywhere in the file: private IPs, internal lab hostnames.
Exit code 1 on any finding, so CI fails loudly.
"""

import html
import re
import sys
from html.parser import HTMLParser

PATH = sys.argv[1] if len(sys.argv) > 1 else "site/index.html"
VOID = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "source",
    "track",
    "wbr",
}
AI_TELLS = re.compile("[—–“”;]|--")
LEAKS = re.compile(
    r"\b10\.\d+\.\d+\.\d+\b|\b192\.168\.\d+\.\d+\b|\b172\.(1[6-9]|2\d|3[01])\.\d+\.\d+\b|\.lab\.home\b|lab\.rhinojedi\.dev"
)


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.text, self.skip = [], [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            self.errors.append(f"unexpected </{tag}> at line {self.getpos()[0]}")
            return
        self.stack.pop()

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)


src = open(PATH, encoding="utf-8").read()
c = Checker()
c.feed(src)
problems = list(c.errors) + [f"unclosed <{t}> from line {p[0]}" for t, p in c.stack]

visible = re.sub(r"\s+", " ", html.unescape(" ".join(c.text)))
for m in AI_TELLS.finditer(visible):
    problems.append(
        f"AI tell {m.group(0)!r} in: ...{visible[max(0, m.start() - 40) : m.end() + 40]}..."
    )
for m in LEAKS.finditer(src):
    problems.append(f"leak pattern {m.group(0)!r}")

if problems:
    print(f"FAIL {PATH}: {len(problems)} finding(s)")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print(f"PASS {PATH}: well-formed, no AI tells in visible text, no leak patterns")
