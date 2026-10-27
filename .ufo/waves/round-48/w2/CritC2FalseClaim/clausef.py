#!/usr/bin/env python3
"""Mechanical check of frozen clause f's window logic against the draft entry + committed receipt.
Reads only; no writes outside stdout. Mirrors quality/counters/c2-r48-xkb-entry.py clause f regexes."""
import re

RECEIPT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt"
ENTRY = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/l1-draft/xkb-keymap-compile-r48.md"

RC_RE = re.compile(r"\b(?:rc|exit(?:[ _-]?(?:code|status))?|status)\b\s*[=:]?\s*(\d+)", re.I)
VER_RE = re.compile(r"(?i)(?:libxkbcommon|xkbcommon|xkbcli)[^0-9\n]{0,40}(\d+\.\d+\.\d+)")
PROBE_LAYOUT = re.compile(r"(?:--layout[ =]zz\b|layout=zz\b|\blayout\s+zz\b)")
PROBE_VARIANT = re.compile(r"(?:--variant[ =]nope\b|variant=nope\b|\bvariant\s+nope\b)")
PROBE_OPTION = re.compile(r"nope:nope")
POS_RMLVO = re.compile(r"compose:caps")
HEX64_RE = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])")


def records(text):
    return [b for b in re.split(r"\n[ \t]*\n", text)]


def cases(text):
    lines = text.splitlines()
    out, i = [], 0
    while i < len(lines):
        if lines[i].strip() and not lines[i][:1].isspace():
            j = i + 1
            while j < len(lines) and lines[j].strip() and lines[j][:1].isspace():
                j += 1
            out.append("\n".join(lines[i:j]))
            i = j
        else:
            i += 1
    return out


def rc_values(window):
    return [int(x) for x in RC_RE.findall(window)]


def units(text, token_re):
    out = []
    for block in records(text) + cases(text):
        if not token_re.search(block):
            continue
        vals = set(rc_values(block))
        if len(vals) == 1:
            out.append(vals)
    for line in text.splitlines():
        if token_re.search(line):
            vals = set(rc_values(line))
            if len(vals) == 1:
                out.append(vals)
    return out


def probe_rc(text, token_re, want):
    us = units(text, token_re)
    if not us:
        return None, "no_labeled_rc"
    vals = set().union(*us)
    if vals != {want}:
        return None, "rc_values=%s" % sorted(vals)
    return us, ""


rec = open(RECEIPT, encoding="utf-8", errors="replace").read()
ent = open(ENTRY, encoding="utf-8", errors="replace").read()
print("receipt bytes:", len(rec.encode()))
m = VER_RE.search(rec)
print("version match:", m.group(1) if m else None)

for label, tre, want in (("layout", PROBE_LAYOUT, 1), ("variant", PROBE_VARIANT, 1),
                         ("option", PROBE_OPTION, 0), ("positive", POS_RMLVO, 0)):
    got, why = probe_rc(rec, tre, want)
    print("receipt probe %-8s -> %s %s" % (label, "ok" if got else "FAIL", why))

pos_br = [b for b in records(rec) + cases(rec) if POS_RMLVO.search(b) and re.search(r"\bbr\b", b)]
digests = []
for b in pos_br:
    for bl in b.splitlines():
        if re.search(r"keymap", bl, re.I) and not re.search(r"\.conf\b", bl):
            digests += [x.lower() for x in HEX64_RE.findall(bl)]
print("positive+br windows:", len(pos_br), "digests:", sorted(set(digests)))

lines = [l for l in ent.splitlines()]
said_ver = any(m.group(1) in l and re.search(r"xkbcli", l, re.I) for l in lines)
said_pos = any(POS_RMLVO.search(l) and re.search(r"\bbr\b", l) and rc_values(l) == [0] for l in lines)
said_sha = any(re.search(r"sha256", l, re.I) and any(d in l or re.search(r"(?<![0-9a-f])%s" % d[:12], l) for d in digests) for l in lines)
print("entry said_ver:", said_ver, "said_pos:", said_pos, "said_sha:", said_sha)
for label, tre, want, warn in (("layout", PROBE_LAYOUT, 1, False), ("variant", PROBE_VARIANT, 1, False),
                               ("option", PROBE_OPTION, 0, True)):
    ok = any(tre.search(l) and rc_values(l) == [want] and
             (not warn or re.search(r"XKB-595|ignored|warning", l, re.I)) for l in lines)
    print("entry said_neg %-8s %s" % (label, ok))

# where exactly does the entry state each value
for l in lines:
    if "silent at every level" in l or "only a WARNING" in l or "four rulesets" in l:
        print("ENTRY-NOTE:", l[:300])
