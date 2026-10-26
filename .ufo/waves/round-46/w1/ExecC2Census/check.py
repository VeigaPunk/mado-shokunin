#!/usr/bin/env python3
"""ExecC2Census independent derivation: census values, 28 surfaces, 10 gate quotes.

Does not import or run the frozen counter; reads the counter only to obtain the
frozen SURFACES spec table, then recomputes every anchor occurrence, locator and
quote count itself from .ufo/waves/round-46/fetch/ and the L1 draft entry.
"""
import ast
import json
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
F = os.path.join(LANE, ".ufo/waves/round-46/fetch")
ENTRY = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/entry.md")
CNT = os.path.join(LANE, "quality/counters/c2-r46-input-device-entry.py")
BUILD = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/build-pos.py")


def read(p):
    return open(p, encoding="utf-8", errors="replace").read()


def lit(path, name):
    """Extract a top-level literal assignment from a python file (no exec)."""
    tree = ast.parse(read(path))
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in n.targets):
            return ast.literal_eval(n.value)
    if name.startswith("QUOTES"):
        # dict built from string literals
        for n in tree.body:
            if isinstance(n, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == name for t in n.targets):
                return ast.literal_eval(n.value)
    raise SystemExit("missing literal " + name)


def strip_comments(text, ext):
    if ext != ".cpp":
        return text
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == '"':
                    j += 1
                    break
                j += 1
            out.append(text[i:j])
            i = j
        elif text.startswith("//", i):
            while i < n and text[i] != "\n":
                i += 1
        elif text.startswith("/*", i):
            k = text.find("*/", i + 2)
            i = n if k < 0 else k + 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def ws(s):
    return re.sub(r"\s+", " ", s)


SURFACES = lit(CNT, "SURFACES")
QUOTES = lit(BUILD, "QUOTES")

entry_raw = read(ENTRY).split("\n")
# body lines the way the counter sees them: non-fenced, k >= 20 (0-based)
body, fenced = [], False
for k, l in enumerate(entry_raw):
    if re.match(r"^\s{0,3}(```|~~~)", l):
        fenced = not fenced
        continue
    if not fenced and k >= 20:
        body.append((k + 1, l))

print("== census derivation ==")
cv = read(os.path.join(F, "Hyprland-ConfigValues.cpp"))
ik = read(os.path.join(F, "Hyprland-IKeyboard.cpp"))
cm = read(os.path.join(F, "Hyprland-ConfigManager.cpp"))
im = read(os.path.join(F, "Hyprland-InputManager.cpp"))
hc = read(os.path.join(F, "Hyprland-HyprCtl.cpp"))
vk = read(os.path.join(F, "Hyprland-protocols-VirtualKeyboard.cpp"))

d = re.search(r'MS<String>\("input:kb_layout", "([^"]*)", "([^"]*)"', cv)
f = re.findall(r'm_currentRules\.layout\s*=\s*"([^"]*)";', ik)
keys = re.findall(r'addSpecialConfigValue\("device", "([^"]*)"', cm)
m = re.search(r'getDeviceFloat\(devname, "scroll_factor", "input:scroll_factor"\), 0\.F, ([0-9]+)\.F\)', im)
p = re.search(r'"scrollFactor": \{:\.([0-9])f\}', hc)
v = re.findall(r'std::string name = "([^"]+)";', vk)
census = ("hyprland input-device default_layout=%s fallback_layout=%s device_keys=%d "
          "scroll_factor_max=%s json_scroll_decimals=%s virtual_prefix=%s") % (
    d.group(2), f[0], len(set(keys)), m.group(1), p.group(1), v[0])
print("kb_layout_line       : ConfigValues.cpp:%d  desc=%r default=%r" % (
    cv[:d.start()].count("\n") + 1, d.group(1), d.group(2)))
print("fallback_sites       : %r  (unique m_currentRules.layout assignment: %d)" % (f, len(f)))
print("other_us_fallbacks   : %r" % re.findall(r'rules\.layout = "([^"]*)";', ik))
print("device_key_count     : total=%d unique=%d" % (len(keys), len(set(keys))))
print("scroll_clamp         : InputManager.cpp:%d 0..%s.F" % (
    im[:m.start()].count("\n") + 1, m.group(1)))
print("json_decimals        : HyprCtl.cpp:%d {:.%sf}" % (
    hc[:p.start()].count("\n") + 1, p.group(1)))
print("virtual_prefix       : protocols/VirtualKeyboard.cpp:%d %r" % (
    vk[:vk.index(v[0])].count("\n") + 1, v[0]))
print("CENSUS               : %s" % census)
frozen = "hyprland input-device default_layout=us fallback_layout=us device_keys=47 scroll_factor_max=100 json_scroll_decimals=2 virtual_prefix=hl-virtual-keyboard"
print("FROZEN_MATCH         : %s" % (census == frozen))
print("entry_census_lines   : %s" % [l for l in entry_raw if l.strip() == census])

print("\n== 28 surfaces ==")
bad = 0
for rname, anchor, kw, label in SURFACES:
    rl = read(os.path.join(F, rname)).split("\n")
    hits = [n for n, l in enumerate(rl, 1) if anchor in l]
    st = {"label": label, "receipt": rname, "anchor_line": hits,
          "anchor_count": len(hits), "cited": False, "kw_ok": False}
    if len(hits) == 1:
        L = hits[0]
        pat = re.compile(r"(?<![\w.-])%s:(\d+)(?:-(\d+))?(?!\d)" % re.escape(rname))
        for k, l in body:
            if not re.search(kw, l, re.I):
                continue
            for a, b in pat.findall(l):
                if int(a) <= L <= int(b or a) and int(b or a) - int(a) <= 30:
                    st.update(cited=True, kw_ok=True, entry_line=k, span=[a, b],
                              entry_text=l[:400])
    else:
        for k, l in body:
            if re.search(kw, l, re.I) and re.search(re.escape(rname) + r":\d", l):
                st.update(entry_line=k, entry_text=l[:400])
    st["ok"] = st["cited"] and st["kw_ok"]
    bad += 0 if st["ok"] else 1
    print("%-2s %-14s %-32s anchor=%s cited=%s entry_line=%s span=%s" % (
        "OK" if st["ok"] else "FAIL", label, rname, hits, st["cited"],
        st.get("entry_line"), st.get("span")))
    if hits:
        lo = max(1, hits[0] - 2)
        hi = min(len(rl), hits[0] + 2)
        print("     pin[%d..%d]: %s" % (lo, hi, " | ".join(x.strip() for x in rl[lo-1:hi] if x.strip())))
    if st.get("entry_text"):
        print("     entry[%d]: %s" % (st["entry_line"], st["entry_text"]))
print("surfaces_not_ok      : %d" % bad)

def collapse(text):
    """single-spaced text + 1-based line number of every collapsed character"""
    out, lines, prev = [], [], True
    for ln, line in enumerate(text.split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    out.append(" ")
                    lines.append(ln)
                    prev = True
            else:
                out.append(ch)
                lines.append(ln)
                prev = False
    return "".join(out), lines


def isw(c):
    return c.isalnum() or c == "_"


def find_all(text, nq):
    """word-boundary-aware occurrence offsets"""
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


print("\n== 10 gate quotes ==")
qbad = 0
for sid, (rname, quote) in QUOTES.items():
    raw = read(os.path.join(F, rname))
    nq = ws(quote)
    flat, lnmap = collapse(raw)
    hits = find_all(flat, nq)
    at = lnmap[hits[0]] if hits else None
    stripped, _ = collapse(strip_comments(raw, os.path.splitext(rname)[1]))
    shits = find_all(stripped, nq)
    locs = [k for k, l in body if re.search(r"\b%s\b" % sid, l) and nq in ws(l)]
    loc_ok = bool(locs) and at is not None and any(
        re.search(r"(?<![\w.-])%s:%d(?!\d)" % (re.escape(rname), at), l) for k, l in body)
    ok = len(hits) == 1 and len(shits) == 1 and loc_ok
    qbad += 0 if ok else 1
    print("%-2s %s %-36s occ_raw=%d occ_nocomment=%d quote_line=%s obs_line=%s locator_ok=%s" % (
        "OK" if ok else "FAIL", sid, rname, len(hits), len(shits), at, locs, loc_ok))
    if locs:
        print("     obs: %s" % dict(body)[locs[0]][:300])
    if at:
        rl = raw.split("\n")
        hi = at + nq.count(" ") // 3
        print("     pin[%d..%d]: %s" % (at, min(len(rl), hi + 1),
              " | ".join(x.strip() for x in rl[at-1:hi+1] if x.strip())[:300]))
print("quotes_not_ok        : %d" % qbad)
