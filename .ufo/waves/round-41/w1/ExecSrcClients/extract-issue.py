#!/usr/bin/env python3
"""Deterministic extraction of hyprwm/Hyprland issue #565 from the saved HTML page.

Reads the single `react-app.embeddedData` JSON payload GitHub ships in the page and
prints the issue's metadata, its body verbatim, and the ordered text nodes of the body.
No network, no HTML heuristics beyond the one script tag.
"""
import json
import re
import sys

HTML = sys.argv[1] if len(sys.argv) > 1 else "issue-565.html"
raw = open(HTML, encoding="utf-8").read()

m = re.search(
    r'<script type="application/json" data-target="react-app\.embeddedData">(.*?)</script>',
    raw,
    re.S,
)
if not m:
    sys.exit("no embeddedData script")
data = json.loads(m.group(1))


def walk(node, path=""):
    yield path, node
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, f"{path}[{i}]")


# The issue object: a dict with number+title+body.
issues = [(p, n) for p, n in walk(data) if isinstance(n, dict) and {"number", "title", "body"} <= set(n)]
if not issues:
    sys.exit("no issue object")
for p, n in issues:
    print(f"PATH {p}")
    print(f"NUMBER {n.get('number')}")
    print(f"TITLE {n.get('title')!r}")
    print(f"STATE {n.get('state')} stateReason={n.get('stateReason')}")
    print(f"CREATED {n.get('createdAt')} CLOSED {n.get('closedAt')}")
    print(f"AUTHOR {(n.get('author') or {}).get('login')}")
    print(f"URL {n.get('url') or n.get('resourcePath')}")
    print("BODY_VERBATIM_BEGIN")
    print(n.get("body"))
    print("BODY_VERBATIM_END")

# Ordered text nodes of the body, markdown links resolved to their text.
body = issues[0][1].get("body") or ""
text = re.sub(r"```[^\n]*\n(.*?)```", lambda mm: "\n".join(mm.group(1).splitlines()), body, flags=re.S)
text = re.sub(r"!?\[([^\]]*)\]\(([^)]*)\)", r"\1 (\2)", text)
print("TEXT_NODES_BEGIN")
for i, line in enumerate(text.splitlines()):
    s = line.strip()
    if s:
        print(f"{i:03d}| {s}")
print("TEXT_NODES_END")
