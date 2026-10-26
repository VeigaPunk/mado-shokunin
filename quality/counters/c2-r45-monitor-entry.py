#!/usr/bin/env python3
"""PRED-C2-r45 - the monitor-rule entry is admitted (C2, coverage, sourced).

Frozen before any round-45 data commit (.ufo/waves/round-45/registration.md). The code is the round-44 v2 counter
(quality/counters/c2-r44-gkeep-size-request-v2.py: clauses a-g and its T1-T4 tightenings) with round constants, a
monitor census for h, no assimilation clause (i keeps only the location and pin-coverage checks; this round admits
no staged package file), clause e allowing a held URL again only under a different scope cell (the census W04
case), and clause j given a range-width bound (round-44 closure D5: whole-file locator ranges satisfied it).

Scores one committed revision REV (revision-addressed git reads, ambient GIT_* removed; nothing in the lane is
written). ENTRY = corpus/knowledge/hyprland-monitor-rule-r45.md, LESSON = corpus/lessons/round-45.md,
FETCH = .ufo/waves/round-45/fetch/, BASE = 0c89478af821a6424c9ac922eafe02e39630cf4f, DATE = 2026-10-26. PINS
(file name -> sha256 and URL, tables below, part of the predicate): seven Hyprland files at efb50993 (Parser.cpp,
legacy ConfigManager.cpp, MonitorRuleManager.cpp, MonitorRule.hpp, Monitor.cpp, HyprCtl.cpp,
MonitorPositionController.cpp), hyprutils v0.14.2 String.cpp, and the hyprland-wiki Monitors page at ecc06f3b6605.
Fenced code blocks of the entry, README and lesson are removed before any line is matched. The entry is admitted
iff every clause holds:
  a  ENTRY exists at REV and is absent at BASE (present at BASE is a setup error, exit 2);
  b  within its first 20 raw lines, outside fences: >= 4 distinct `source: S###` lines, exactly one
     `verified-at: DATE` and exactly one `recheck:` (ISO date, `NNd` or `on-*`); no such line elsewhere; no
     `S###` token anywhere in the entry that is not a cited id;
  c  every cited id has exactly one Registry row (0-3 leading spaces), 11 cells, status `mined`, a valid recheck
     cell, and used-by listing ENTRY; ids absent at BASE (>= 3) carry opened DATE and a location (last token of
     cell 1) holding `/` and `.`; ids present at BASE keep cells 1-9 byte-equal and every BASE used-by item;
  d  LESSON `## Gate` holds per cited id exactly one column-0 line `GATE <id> receipt=<path> sha256=<hex>
     quote="<q>"` (none outside that section); the receipt is a 100644 file under FETCH at REV with that sha256,
     >= 256 bytes; distinct path, sha256 and quote per id; a receipt whose file name is one of PINS must be at
     FETCH/<name> with exactly the pinned sha256 - held ids included; a new id's receipt must be one of PINS; the
     quote is 3-25 words, occurs exactly once in its receipt's normalized text at word boundaries, also with
     comments removed (C/C++ `//`,`/* */`; `#` in .py/.conf), and in no other cited receipt;
  e  each new id's location occurs in no other row whose scope cell (cell 5) equals its own, and its last path
     component and the receipt name contain one another; a `Hyprland-` receipt's location starts with the
     efb50993 raw URL; for every cited id gated on a PINS receipt the location is exactly that pin's URL; a new
     row's anchor cell names the receipt with `<name>:<a>[-<b>]` ranges inside the receipt's line count;
  f  corpus/README.md holds exactly one column-0 index row for ENTRY;
  g  per cited id one entry line names that id and no other, carries its Gate quote and the computed locator
     `<receipt name>:<N>` (N = the receipt line where the quote starts); EVERY unfenced line naming a cited id
     (other than its `source:` line) carries that id's quote and locator; only the exact census line of h is
     exempt from these line checks;
  h  monitor census: from the pins the counter computes the rule's default refresh (MonitorRule.hpp
     `m_refreshRate = <R>;`), the requested-mode closeness bound (Monitor.cpp `!DELTALESSTHAN(bestMode->refreshRate
     / 1000.f, RULE->m_refreshRate, <T>)`), the scale step (Monitor.cpp `std::round(m_scale * <K>.0)`), the search
     length (the first `for (size_t i = 1; i < <N>; ++i)` loop after that line; steps = N - 1), the JSON refresh
     decimals (HyprCtl.cpp `"refreshRate": {:.<P>f}`) and the number of `ARGS[argno] == "` keys in handleMonitor
     (from its signature line to the first following line that is exactly `}`); the entry carries, verbatim,
     unfenced and exactly once, `hyprland monitor-rule default_refresh=<R> refresh_tolerance=<T> scale_step=1/<K>
     scale_search=<N-1> json_refresh_decimals=<P> line_keys=<n>`, and no other entry line carries one of those six
     `name=` tokens with another value;
  i  no cited row and no entry line holds a BAD_LOC marker; the Gate receipts of the cited ids cover every name in
     PINS;
  j  surface coverage: for each SURFACES item (pinned receipt, anchor text that occurs exactly once in it, keyword)
     the counter computes the anchor's line L, and some unfenced entry line outside the first 20 raw lines carries
     a locator `<receipt>:<a>[-<b>]` with a <= L <= b (b = a when absent) and b - a <= 30, and matches the keyword
     (case-insensitive). The seventeen surfaces: parseMode, parsePosition, parseScale (Parser.cpp); handleMonitor
     and its invalid-syntax return (legacy ConfigManager.cpp); add's erase and get's reverse search
     (MonitorRuleManager.cpp); the 60 Hz default (MonitorRule.hpp); matchesStaticSelector, the closeness bound and
     the 1/120 scale search (Monitor.cpp); the JSON refreshRate field and the `all` argument (HyprCtl.cpp); the
     explicit-position move (MonitorPositionController.cpp); isNumber2 (String.cpp); the wiki's line format and
     its `sdr_eotf` sentence (wiki-Monitors.md).
Final line: `PRED-C2-r45: admitted=N/1 verdict=TARGET_MET|TARGET_MISSED rev=<full hash>`; exit 0 iff admitted=1/1,
else 1; setup failure exit 2.
Residuals (declared): the pins are the trust root; a true quote at a true locator can stand beside a claim it does
not support, and a decision table naming no id is not bound (the non-author reading); registry cells 3-6 of a new
row are not read except the scope cell and the anchor ranges; clause j binds a locator and a keyword per surface,
not the truth of the sentence around them; the census line is bookkeeping of pinned bytes.
"""
import argparse
import collections
import datetime
import hashlib
import html
import json
import os
import re
import subprocess
import sys

PRED = "PRED-C2-r45"
BASE_DEFAULT = "0c89478af821a6424c9ac922eafe02e39630cf4f"
ENTRIES = ("corpus/knowledge/hyprland-monitor-rule-r45.md",)
LESSON = "corpus/lessons/round-45.md"
FETCH = ".ufo/waves/round-45/fetch/"
OPENED = "2026-10-26"
MIN_RECEIPT = 256
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) '
                     r'quote="(.+)"\s*$')
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")
SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")
JWIDTH = 30
BAD_LOC = ("amgsk.dev", "zhihu", "/zh", "/ja", "zenn.dev", "qiita.com", "/jp/",
           "/cn/", "t.co/", "bit.ly", "\u65e5\u672c", "\u4e2d\u6587")
# the receipts the L1 fetched before the wave (fetch/ at the freeze); a NEW
# cited id's receipt must be one of them, byte for byte
PINS = {
    "Hyprland-Parser.cpp": "616468fd0576d8b201ef00cd69289234f0ffb1c3137ae2a0ac954fabe37dd589",
    "Hyprland-legacy-ConfigManager.cpp": "9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b",
    "Hyprland-MonitorRuleManager.cpp": "17d46685c2623657f52e71b22a033c0a798cf3903f7bbeb64ceebce87527f016",
    "Hyprland-MonitorRule.hpp": "b01d31a16d5fb413ead28f46825381f36a70c29b86eceb58cd633dcbf031a2f5",
    "Hyprland-Monitor.cpp": "9cf88e154eb5dae676c79d37b5b055ca6134838857cecdbb89a3b747a6821927",
    "Hyprland-HyprCtl.cpp": "798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa",
    "Hyprland-MonitorPositionController.cpp": "3b705388fa53aef77c5e8c6f6307c94dab08b5dae9460bab427d648359b5ae49",
    "hyprutils-String.cpp": "a92c131a45f41918388eece78f225dbeab7791bb3cd2d3761d840aefa1527bac",
    "wiki-Monitors.md": "f2ac7025b7d7dd13b467ad52a5ca7b4da39e198f3ae4c6a675f92a38cd0304b9",
}
_HY = "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/"
PINS_URL = {
    "Hyprland-Parser.cpp": _HY + "config/shared/monitor/Parser.cpp",
    "Hyprland-legacy-ConfigManager.cpp": _HY + "config/legacy/ConfigManager.cpp",
    "Hyprland-MonitorRuleManager.cpp": _HY + "config/shared/monitor/MonitorRuleManager.cpp",
    "Hyprland-MonitorRule.hpp": _HY + "config/shared/monitor/MonitorRule.hpp",
    "Hyprland-Monitor.cpp": _HY + "output/Monitor.cpp",
    "Hyprland-HyprCtl.cpp": _HY + "debug/HyprCtl.cpp",
    "Hyprland-MonitorPositionController.cpp": _HY + "state/MonitorPositionController.cpp",
    "hyprutils-String.cpp": "https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/string/String.cpp",
    "wiki-Monitors.md": "https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605e453c0ad533d979fccbefff788ef/content/Configuring/Monitors.md",
}


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                       env=ENV)
    return p.stdout if p.returncode == 0 else None


def show(repo, rev, path):
    return git(repo, "show", "%s:%s" % (rev, path))


def resolve(repo, rev):
    out = git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    if not out:
        raise Setup("unresolved revision %s" % rev)
    return out.decode().strip()


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


def registry(blob):
    rows = {}
    for line in section((blob or b"").decode("utf-8", "replace"),
                        "## Registry"):
        m = ROW_RE.match(line)
        if m:
            cells = [c.strip() for c in line.strip().split("|")[1:-1]]
            rows.setdefault(m.group(1), []).append(cells)
    return rows


def valid_date(s):
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if not m:
        return False
    try:
        datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return False
    return True


def recheck_ok(rc):
    m = RECHECK_RE.match(rc or "")
    if not m:
        return False
    tok = m.group(1)
    return valid_date(tok) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", tok) else True


def ls_mode(repo, rev, path):
    out = git(repo, "ls-tree", rev, "--", path)
    if not out:
        return None
    return out.split()[0].decode()


def looks_html(blob):
    return re.search(rb"<(!doctype|html|body|div|p)\b", blob[:4096], re.I) \
        is not None


def norm_receipt(blob):
    text = blob.decode("utf-8", "replace")
    if looks_html(blob):
        return norm(text)
    return re.sub(r"\s+", " ", text).strip()


def collapse_with_lines(text):
    """(collapsed text, 1-based line number of each collapsed character)."""
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


def quote_at(blob, nq):
    """Line of the first word-bounded occurrence of the normalized quote in a
    non-HTML receipt, 0 for an HTML receipt that holds it word-bounded, None."""
    isw = lambda c: c.isalnum() or c == "_"
    if looks_html(blob):
        text = norm(blob.decode("utf-8", "replace"))
        lines = None
    else:
        text, lines = collapse_with_lines(blob.decode("utf-8", "replace"))
    start = 0
    while True:
        k = text.find(nq, start)
        if k < 0:
            return None
        before = text[k - 1] if k > 0 else " "
        after = text[k + len(nq)] if k + len(nq) < len(text) else " "
        if not (isw(nq[0]) and isw(before)) and not (isw(nq[-1]) and isw(after)):
            return lines[k] if lines else 0
        start = k + 1




def occurrences(blob, nq):
    isw = lambda c: c.isalnum() or c == "_"
    if looks_html(blob):
        text = norm(blob.decode("utf-8", "replace"))
    else:
        text = collapse_with_lines(blob.decode("utf-8", "replace"))[0]
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


def strip_comments(text, path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".cpp", ".hpp", ".h", ".cc"):
        text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
        return re.sub(r"//[^\n]*", " ", text)
    if ext in (".py", ".conf"):
        return re.sub(r"#[^\n]*", " ", text)
    return text


def quote_in_code(blob, nq, path):
    flat = re.sub(r"\s+", " ", strip_comments(blob.decode("utf-8", "replace"), path))
    return nq in flat


def all_body_lines_bound(ids, entry_lines, gates, receipts_raw):
    for i in ids:
        gl = gates.get(i, [])
        if len(gl) != 1 or i not in receipts_raw:
            return False
        path, digest, quote = gl[0]
        q = re.sub(r"\s+", " ", quote)
        at = quote_at(receipts_raw[i], q)
        bn = os.path.basename(path)
        for l in entry_lines:
            if not re.search(r"\b%s\b" % i, l):
                continue
            if l.startswith("source:"):
                continue
            if q not in l:
                return False
            if at and ("%s:%d" % (bn, at)) not in l:
                return False
    return True


def norm(text):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


CENSUS_KEYS = ("default_refresh", "refresh_tolerance", "scale_step", "scale_search",
               "json_refresh_decimals", "line_keys")


def host_census(new_ids, reg_rev, gates, receipts_raw, lines):
    """Clause h (round 45): recompute the monitor census line from the pinned receipts."""
    byname = {}
    for i, gl in gates.items():
        if i in receipts_raw and gl and gl[0] is not None and len(gl) == 1:
            byname[os.path.basename(gl[0][0])] = receipts_raw[i].decode("utf-8", "replace")
    need = ("Hyprland-MonitorRule.hpp", "Hyprland-Monitor.cpp", "Hyprland-HyprCtl.cpp",
            "Hyprland-legacy-ConfigManager.cpp")
    if not all(n in byname for n in need):
        return False, []
    r = re.findall(r"float\s+m_refreshRate\s*=\s*([0-9]+(?:\.[0-9]+)?);", byname["Hyprland-MonitorRule.hpp"])
    mon = byname["Hyprland-Monitor.cpp"]
    t = re.findall(r"!DELTALESSTHAN\(bestMode->refreshRate / 1000\.f, RULE->m_refreshRate, ([0-9]+)\)", mon)
    k = re.findall(r"std::round\(m_scale \* ([0-9]+)\.0\)", mon)
    p = re.findall(r'"refreshRate": \{:\.([0-9])f\}', byname["Hyprland-HyprCtl.cpp"])
    if len(r) != 1 or len(t) != 1 or len(k) != 1 or len(p) != 1:
        return False, []
    after = mon[mon.index("std::round(m_scale * %s.0)" % k[0]):]
    n = re.search(r"for \(size_t i = 1; i < ([0-9]+); \+\+i\)", after)
    src = byname["Hyprland-legacy-ConfigManager.cpp"].split("\n")
    sig = "std::optional<std::string> CConfigManager::handleMonitor(const std::string& command, const std::string& args) {"
    if n is None or src.count(sig) != 1:
        return False, []
    s = src.index(sig)
    try:
        e = src.index("}", s + 1)
    except ValueError:
        return False, []
    nkeys = "\n".join(src[s:e + 1]).count('ARGS[argno] == "')
    want = ["hyprland monitor-rule default_refresh=%s refresh_tolerance=%s scale_step=1/%s scale_search=%d "
            "json_refresh_decimals=%s line_keys=%d" % (r[0], t[0], k[0], int(n.group(1)) - 1, p[0], nkeys)]
    ok = all(sum(1 for l in lines if l == w) == 1 for w in want)
    return ok, want


SURFACES = [
    ("Hyprland-Parser.cpp", "bool CMonitorRuleParser::parseMode(const std::string& value) {", r"mode|resolution", "parse-mode"),
    ("Hyprland-Parser.cpp", "bool CMonitorRuleParser::parsePosition(const std::string& value, bool isFirst) {", r"position|auto", "parse-position"),
    ("Hyprland-Parser.cpp", "bool CMonitorRuleParser::parseScale(const std::string& value) {", r"scale", "parse-scale"),
    ("Hyprland-legacy-ConfigManager.cpp", "std::optional<std::string> CConfigManager::handleMonitor(const std::string& command, const std::string& args) {", r"handleMonitor|monitor line", "handle-monitor"),
    ("Hyprland-legacy-ConfigManager.cpp", 'return "invalid syntax at \\"" + std::string(ARGS[argno]) + "\\"";', r"invalid syntax|unknown key|dropped", "invalid-syntax"),
    ("Hyprland-MonitorRuleManager.cpp", "std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });", r"erase|same selector", "add-erase"),
    ("Hyprland-MonitorRuleManager.cpp", "for (auto const& r : m_rules | std::views::reverse) {", r"last|reverse", "get-reverse"),
    ("Hyprland-MonitorRule.hpp", "m_refreshRate   = 60; // Hz", r"\b60\b", "default-60"),
    ("Hyprland-Monitor.cpp", "bool CMonitor::matchesStaticSelector(std::string_view selector) const {", r"desc:|selector", "selector"),
    ("Hyprland-Monitor.cpp", "!DELTALESSTHAN(bestMode->refreshRate / 1000.f, RULE->m_refreshRate, 1))", r"refresh|Hz", "closeness"),
    ("Hyprland-Monitor.cpp", "float    searchScale = std::round(m_scale * 120.0);", r"120|scale", "scale-search"),
    ("Hyprland-HyprCtl.cpp", '"refreshRate": {:.5f},', r"refreshRate", "json-refresh"),
    ("Hyprland-HyprCtl.cpp", 'if (vars.size() == 2 && vars[1] == "all")', r"\ball\b", "monitors-all"),
    ("Hyprland-MonitorPositionController.cpp", "m->moveTo(*POS);", r"explicit|position", "explicit-position"),
    ("hyprutils-String.cpp", "bool Hyprutils::String::isNumber2(const std::string_view& str, bool allowfloat) {", r"isNumber|number", "is-number"),
    ("wiki-Monitors.md", "monitor = name, resolution, position, scale", r"wiki|document", "wiki-format"),
    ("wiki-Monitors.md", "The default transfer function assumed to be in use on an SDR display", r"sdr_eotf", "wiki-sdr-eotf"),
]


def surfaces_ok(repo, rev, text, name):
    """Clause j: every surface's computed line is cited, with its keyword, outside the header window."""
    raw_lines = text.splitlines()
    body_lines, fenced = [], False
    for k, l in enumerate(raw_lines):
        if re.match(r"^\s{0,3}(```|~~~)", l):
            fenced = not fenced
            continue
        if not fenced and k >= 20:
            body_lines.append(l)
    ok = True
    for rname, anchor, kw, label in SURFACES:
        blob = show(repo, rev, FETCH + rname)
        if blob is None:
            print("%s %s clause=j surface=%s receipt_missing" % (PRED, name, label))
            ok = False
            continue
        rl = blob.decode("utf-8", "replace").split("\n")
        hits = [n for n, l in enumerate(rl, 1) if anchor in l]
        if len(hits) != 1:
            print("%s %s clause=j surface=%s anchor_count=%d" % (PRED, name, label, len(hits)))
            ok = False
            continue
        L = hits[0]
        pat = re.compile(r"(?<![\w.-])%s:(\d+)(?:-(\d+))?(?!\d)" % re.escape(rname))
        found = False
        for l in body_lines:
            if not re.search(kw, l, re.I):
                continue
            for a, b in pat.findall(l):
                if int(a) <= L <= int(b or a) and int(b or a) - int(a) <= JWIDTH:
                    found = True
        ok &= found
        print("%s %s clause=j surface=%s line=%d cited=%d" % (PRED, name, label, L, found))
    return ok


def score(repo, rev, base, entry, reg_rev, reg_base, lesson, readme):
    name = os.path.basename(entry)
    cl = dict.fromkeys("abcdefghij", 0)
    raw = show(repo, rev, entry)
    text = raw.decode("utf-8", "replace") if raw is not None else ""
    lines = unfenced(text)
    cl["a"] = int(raw is not None)
    # header: only unfenced lines inside the first 20 raw lines count; every
    # source:/verified-at:/recheck: line of the whole entry must sit there
    head, fenced_state, window = [], False, 0
    for k, l in enumerate(text.splitlines()):
        if re.match(r"^\s{0,3}(```|~~~)", l):
            fenced_state = not fenced_state
            continue
        if not fenced_state:
            if k < 20:
                head.append(l)
            elif re.match(r"^(source|verified-at|recheck):", l):
                window += 1
    ids = []
    for line in head:
        m = SRC_RE.match(line)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    cited = set(re.findall(r"\b[Ss]\d{3,}\b", "\n".join(lines)))
    ghosts = cited - set(ids)

    def hv(key):
        vals = [l[len(key) + 1:].strip() for l in head
                if l.startswith(key + ":")]
        return vals[0] if len(vals) == 1 else None
    va, rc = hv("verified-at"), hv("recheck")
    cl["b"] = int(len(ids) >= 4 and va == OPENED and recheck_ok(rc)
                  and window == 0 and not ghosts)

    rows_ok = bool(ids)
    new_ids = []
    for i in ids:
        rows = reg_rev.get(i, [])
        if len(rows) != 1 or len(rows[0]) != 11:
            rows_ok = False
            print("%s %s clause=c id=%s rows=%d" % (PRED, name, i, len(rows)))
            continue
        cells = rows[0]
        items = [x.strip() for x in re.split(r"[,;]", cells[10])]
        good = cells[7] == "mined" and entry in items \
            and recheck_ok(cells[9])
        if i in reg_base:
            old = reg_base[i]
            good &= len(old) == 1 and len(old[0]) == 11 \
                and old[0][:9] == cells[:9] and recheck_ok(cells[9]) is not None
            good &= set(x.strip() for x in re.split(r"[,;]", old[0][10])
                        if x.strip() not in ("", "\u2014")) <= set(items)
        else:
            new_ids.append(i)
            loc = cells[1].split()[-1] if cells[1].split() else ""
            good &= cells[8] == OPENED and ("/" in loc and "." in loc)
        rows_ok &= good
        print("%s %s clause=c id=%s new=%d status=%s used=%d ok=%d" % (
            PRED, name, i, i not in reg_base, cells[7], entry in items, good))
    cl["c"] = int(rows_ok and len(new_ids) >= 3)

    glines = unfenced("\n".join(section(lesson, "## Gate")))
    gates = collections.defaultdict(list)
    for line in glines:
        m = GATE_RE.match(line.rstrip("\n"))
        if m:
            gates[m.group(1)].append(m.groups()[1:])
        elif re.match(r"^\s+GATE S\d", line):
            gates["<indented>"].append(None)
    outside = 0
    in_gate = set(glines)
    for line in unfenced(lesson):
        if re.match(r"^GATE S\d", line) and line not in in_gate:
            outside += 1
    d_ok, g_ok = bool(ids), bool(ids)
    receipts, receipts_raw = {}, {}
    seen_paths, seen_sha, seen_quote = set(), set(), set()
    for i in ids:
        good = None
        gl = gates.get(i, [])
        if len(gl) == 1:
            path, digest, quote = gl[0]
            blob = show(repo, rev, path) if path.startswith(FETCH) else None
            pin_ok = PINS.get(os.path.basename(path)) in (None, digest) \
                and (os.path.basename(path) not in PINS
                     or path == FETCH + os.path.basename(path))
            nq = re.sub(r"\s+", " ", quote)
            if (blob is not None and len(blob) >= MIN_RECEIPT and pin_ok
                    and ls_mode(repo, rev, path) == "100644"
                    and hashlib.sha256(blob).hexdigest() == digest
                    and 3 <= len(quote.split()) <= 25
                    and path not in seen_paths and digest not in seen_sha
                    and nq not in seen_quote
                    and quote_at(blob, nq) is not None
                    and len(occurrences(blob, nq)) == 1
                    and quote_in_code(blob, nq, path)):
                good = quote
                receipts[i] = blob.decode("utf-8", "replace")
                receipts_raw[i] = blob
                seen_paths.add(path)
                seen_sha.add(digest)
                seen_quote.add(nq)
        print("%s %s clause=d id=%s gates=%d bound=%d" % (
            PRED, name, i, len(gl), good is not None))
        if good is None:
            d_ok = g_ok = False
    # a quote occurs in its own receipt and in no other cited receipt
    for i in receipts:
        q = re.sub(r"\s+", " ", gates[i][0][2])
        for j in receipts:
            if j != i and q in norm_receipt(receipts_raw[j]):
                d_ok = False
                print("%s %s clause=d quote of %s also in receipt of %s" % (
                    PRED, name, i, j))
    cl["d"] = int(d_ok and not gates.get("<indented>") and outside == 0)

    e_ok = True
    for i in new_ids:
        gl_ = gates.get(i, [])
        cells_ = reg_rev[i][0] if len(reg_rev.get(i, [[]])[0]) == 11 else None
        if cells_ is None or len(gl_) != 1:
            e_ok = False
            continue
        comp = re.split(r"[?#]", cells_[1].split()[-1])[0].rstrip("/") \
            .rsplit("/", 1)[-1].lower()
        rb = os.path.basename(gl_[0][0]).lower()
        e_ok &= bool(comp) and (comp in rb or rb in comp)
        if rb.startswith('hyprland-') and not cells_[1].split()[-1].startswith(
                'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/'):
            e_ok = False
        cells = reg_rev[i][0] if len(reg_rev.get(i, [[]])[0]) == 11 else None
        if cells is None:
            e_ok = False
            continue
        loc = cells[1].split()[-1] if cells[1].split() else ""
        key = loc.split("#")[0]
        same = [j for j, rr in reg_rev.items() for r in rr
                if len(r) == 11 and r[1].split()
                and r[1].split()[-1].split("#")[0] == key and r[4] == cells[4]]
        e_ok &= bool(loc) and same == [i]
    for i in ids:
        gl_ = gates.get(i, [])
        row_ = reg_rev.get(i, [])
        if len(gl_) == 1 and row_ and len(row_[0]) == 11:
            loc_ = row_[0][1].split()[-1].split("#")[0] if row_[0][1].split() else ""
            pin_url = PINS_URL.get(os.path.basename(gl_[0][0]))
            if pin_url is not None and pin_url.split("#")[0] != loc_:
                e_ok = False
                print("%s %s clause=e+ id=%s location=%s pin=%s" % (
                    PRED, name, i, loc_, pin_url))
    # T4: a new row's anchor must name the receipt it is gated on and stay inside it
    for i in new_ids:
        row_ = reg_rev.get(i, [])
        gl_ = gates.get(i, [])
        if not row_ or len(row_[0]) != 11 or len(gl_) != 1 or i not in receipts_raw:
            e_ok = False
            continue
        rb_ = os.path.basename(gl_[0][0])
        nlines_ = len(receipts_raw[i].decode("utf-8", "replace").splitlines())
        anchor_ = row_[0][5]
        rng = re.findall(r"%s:(\d+)(?:-(\d+))?" % re.escape(rb_), anchor_)
        if not rng or any(int(b or a) > nlines_ for a, b in rng):
            e_ok = False
            print("%s %s clause=e/4 id=%s anchor=%s receipt_lines=%d" % (
                PRED, name, i, anchor_[:70], nlines_))
    cl["e"] = int(e_ok and bool(new_ids))

    h_ok, census_lines = host_census(new_ids, reg_rev, gates, receipts_raw, lines)
    census_lines = set(census_lines)

    entry_lines = [re.sub(r"\s+", " ", l) for l in lines
                   if l not in census_lines
]
    if h_ok:
        want = dict(re.findall(r"(\w+)=(\S+)", next(iter(census_lines))))
        for l in entry_lines:
            for key, v in re.findall(r"\b(%s)=(\S+)" % "|".join(CENSUS_KEYS), l):
                if v.rstrip(".,;:)`") != want.get(key):
                    h_ok = False
                    print("%s %s clause=h prose %s=%s != %s" % (PRED, name, key, v, want.get(key)))
    cl["h"] = int(h_ok)
    for i in ids:
        quote = None
        for path, digest, q in gates.get(i, []):
            quote = q
        if i not in receipts or quote is None:
            g_ok = False
            continue
        q = re.sub(r"\s+", " ", quote)
        at = quote_at(receipts_raw[i], q)
        base_name = os.path.basename(gates[i][0][0])
        loc_ok = True if at == 0 else (at is not None and
                                       re.search(r"(?<![\w.-])%s:%d(?!\d)" % (re.escape(base_name), at), "\n".join(entry_lines)) is not None)
        hit = any(re.search(r"\b%s\b" % i, l) and q in l
                  and len(set(re.findall(r"\bS\d{3,}\b", l))) == 1
                  and (at == 0 or (at is not None and ("%s:%d" % (base_name, at)) in l
                                   and re.search(r"(?<![\w.-])%s:%d(?!\d)" % (re.escape(base_name), at), l)))
                  for l in entry_lines)
        g_ok &= hit
        print("%s %s clause=g id=%s obs=%d locator_line=%s" % (PRED, name, i, hit, at))
    cl["g"] = int(g_ok and all_body_lines_bound(ids, entry_lines, gates, receipts_raw))

    pat = re.compile(r"^\| `knowledge/%s`" % re.escape(name))
    cl["f"] = int(sum(1 for l in unfenced(readme) if pat.match(l)) == 1)
    # clause i (round 45): no assimilation part; location markers and pin coverage only
    bad = False
    for i in ids:
        rows = reg_rev.get(i, [])
        if rows and len(rows[0]) == 11:
            row_text = " ".join(rows[0]).lower()
            bad |= any(b_ in row_text for b_ in BAD_LOC)
    used = set(os.path.basename(gates[i][0][0]) for i in receipts)
    bad |= not set(PINS) <= used
    bad |= any(b_ in l.lower() for l in lines for b_ in BAD_LOC)
    cl["i"] = int(not bad)
    cl["j"] = int(raw is not None and surfaces_ok(repo, rev, text, name))
    admitted = int(all(cl.values()))
    print("%s %s clauses=%s admitted=%d" % (
        PRED, name, " ".join("%s:%d" % kv for kv in sorted(cl.items())),
        admitted))
    return admitted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    rev = resolve(repo, args.rev)
    base = resolve(repo, args.base)
    for e in ENTRIES:
        if show(repo, base, e) is not None:
            raise Setup("precondition_failed entry_present_at_base %s" % e)
    reg_rev = registry(show(repo, rev, "corpus/SOURCES.md"))
    reg_base = registry(show(repo, base, "corpus/SOURCES.md"))
    lesson = (show(repo, rev, LESSON) or b"").decode("utf-8", "replace")
    readme = (show(repo, rev, "corpus/README.md") or b"").decode(
        "utf-8", "replace")
    n = sum(score(repo, rev, base, e, reg_rev, reg_base, lesson, readme)
            for e in ENTRIES)
    met = n == 1
    print("%s: admitted=%d/1 verdict=%s rev=%s" % (
        PRED, n, "TARGET_MET" if met else "TARGET_MISSED", rev))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as exc:
        print("%s SETUP %s" % (PRED, exc))
        sys.exit(2)
