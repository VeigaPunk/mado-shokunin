#!/usr/bin/env python3
"""Check the `## Gate` section of the round-46 lesson draft against PRED-C2-r46 clause d (read-only).

Mirrors quality/counters/c2-r46-input-device-entry.py:505-560 on the draft instead of a revision: the Gate section is
taken by heading, fenced blocks removed, exactly one column-0 GATE line per cited id, no GATE line outside the section,
no indented GATE line, one receipt per id under .ufo/waves/round-46/fetch/ at the pinned sha256, quote 3-25 words and
word-bounded exactly once in the receipt (also with comments removed).
"""
import hashlib
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
DRAFT = os.path.join(LANE, ".ufo/waves/round-46/w1/ScrLessonGate/round-46.md")
FETCH = ".ufo/waves/round-46/fetch/"
GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) quote="(.+)"\s*$')
PINS = {
    "Hyprland-InputManager.cpp": "feedf32e2e3d23aeaed7a02ef4ab94be2d66f4b22873b3166026da1e9ece4765",
    "Hyprland-ConfigManager.cpp": "9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b",
    "Hyprland-ConfigValues.cpp": "a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754",
    "Hyprland-IKeyboard.cpp": "8a800efe9baa7f375a3781744372eecd98a88be2c4bedaae96c90a1102a1aa3d",
    "Hyprland-HyprCtl.cpp": "798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa",
    "Hyprland-MiscFunctions.cpp": "065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9",
    "Hyprland-VirtualKeyboard.cpp": "bc6d984a4c9e62313501c1cdb4ace3659c16d3b77e029a3c082a77f21500ed86",
    "Hyprland-protocols-VirtualKeyboard.cpp": "43cbf7b39bf0910df6d933cef95f029fa336d5b432b0202280e6fc40d8db2f50",
    "hyprlang-config.cpp": "fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e",
    "wiki-Keywords.md": "11c0842cb31ddbfd55298c772bc44d9ad8d29c0c91c69bef6010e39b3ebaf51e",
}
IDS = ["S%d" % n for n in range(316, 326)]


def section(text, title):
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == title
            continue
        if inside:
            out.append(line)
    return out


def unfenced(text):
    out, fenced = [], False
    for line in text.splitlines():
        if re.match(r"^\s{0,3}(```|~~~)", line):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return out


def strip_comments(text, name):
    if name.endswith((".cpp", ".hpp", ".h", ".cc")):
        text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
        return re.sub(r"//[^\n]*", " ", text)
    if name.endswith((".py", ".conf")):
        return re.sub(r"#[^\n]*", " ", text)
    return text


def isw(c):
    return c.isalnum() or c == "_"


def occurrences(text, nq):
    out, start = [], 0
    while True:
        k = text.find(nq, start)
        if k < 0:
            return out
        before = text[k - 1] if k > 0 else " "
        after = text[k + len(nq)] if k + len(nq) < len(text) else " "
        if not (isw(nq[0]) and isw(before)) and not (isw(nq[-1]) and isw(after)):
            out.append(k)
        start = k + 1


text = open(DRAFT, encoding="utf-8").read()
glines = unfenced("\n".join(section(text, "## Gate")))
gates, indented = {}, 0
for line in glines:
    m = GATE_RE.match(line.rstrip("\n"))
    if m:
        gates.setdefault(m.group(1), []).append(m.groups()[1:])
    elif re.match(r"^\s+GATE S\d", line):
        indented += 1
outside = sum(1 for line in unfenced(text)
              if re.match(r"^GATE S\d", line) and line not in set(glines))

bad = 0
if indented:
    print("FAIL indented GATE lines:", indented)
    bad += 1
if outside:
    print("FAIL GATE lines outside the Gate section:", outside)
    bad += 1
if list(gates) != IDS:
    print("FAIL gate ids:", list(gates))
    bad += 1
seen_path, seen_sha, seen_quote = set(), set(), set()
for sid in IDS:
    gl = gates.get(sid, [])
    if len(gl) != 1:
        print("%s FAIL gates=%d" % (sid, len(gl)))
        bad += 1
        continue
    path, digest, quote = gl[0]
    pin = os.path.basename(path)
    blob = open(os.path.join(LANE, path), "rb").read()
    body = blob.decode("utf-8", "replace")
    nq = re.sub(r"\s+", " ", quote)
    occ = occurrences(re.sub(r"\s+", " ", body), nq)
    code = re.sub(r"\s+", " ", strip_comments(body, pin))
    ok = (path.startswith(FETCH) and PINS.get(pin) == digest
          and hashlib.sha256(blob).hexdigest() == digest and len(blob) >= 256
          and 3 <= len(quote.split()) <= 25 and len(occ) == 1 and nq in code
          and path not in seen_path and digest not in seen_sha and nq not in seen_quote)
    seen_path.add(path)
    seen_sha.add(digest)
    seen_quote.add(nq)
    bad += 0 if ok else 1
    print("%s %-40s words=%2d occ=%d code=%d pin=%d %s"
          % (sid, pin, len(quote.split()), len(occ), int(nq in code),
             int(PINS.get(pin) == digest), "OK" if ok else "FAIL"))
print("GATE_CHECK: ids=%d failed=%d indented=%d outside=%d" % (len(IDS), bad, indented, outside))
sys.exit(0 if bad == 0 else 1)
