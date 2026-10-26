#!/usr/bin/env python3
"""PRED-C2-r41-v2 - the Hyprland focus-grab entry is admitted (C2, coverage, sourced).

v2 re-registers PRED-C2-r41-v1 (quality/counters/c2-r41-focus-entry.py, frozen
60c3914) after the round-41 wave w1 falsified it BEFORE any data commit: nine
forgeries (invented 512-byte receipts, an invented journal, ADMIT/REFUSE naming
absent files, a localized source behind a redirect, boilerplate quotes, a
one-character location, two new ids) were admitted, and 29 of 45 further
mutants survived (a ghost citation past line 20, lowercase ids, a symlink
receipt, an unvalidated `recheck`, a row with no location, a self-admit, fenced
header lines, a held row losing its used-by items, a journal with no boot line
or replayed sessions, a quote assembled across HTML blocks). v2 closes those
paths; v1 stays in the tree as the superseded predicate.

Scores one committed revision REV (revision-addressed git reads, every ambient
GIT_* variable removed; nothing in the lane is written). The entry is
corpus/knowledge/hyprland-focus-grab-r41.md. Fenced code blocks (``` ... ```) of
the entry, the README and the lesson are removed before any line is matched. It
is admitted iff every clause holds:

  a  the entry exists at REV and is absent at BASE (present at BASE is a
     setup error, exit 2);
  b  within its first 20 raw lines, outside fences: >= 4 distinct `source:
     S###` lines, exactly one `verified-at: 2026-10-25` and exactly one
     `recheck:` (an ISO calendar date, `NNd` or `on-*`); no `source:`,
     `verified-at:` or `recheck:` line outside that window (outside fences);
     and no `S###`/`s###` token anywhere in the entry (outside fences) that is
     not one of the cited ids;
  c  every cited id has exactly one `## Registry` row (0-3 leading spaces),
     11 cells, status `mined`, a valid `recheck` cell, and its used-by cell,
     split on `,` and `;` and trimmed, lists the entry's path as one item; ids
     absent from the BASE registry (at least 3) carry opened 2026-10-25 and a
     location (last whitespace token of cell 1) holding a `/` and a `.`; ids
     present at BASE keep cells 1-9 byte-equal to their BASE row and keep
     every BASE used-by item;
  d  corpus/lessons/round-41.md `## Gate` (outside fences) holds, per cited id,
     EXACTLY ONE line (starting in column 0) `GATE <id> receipt=<path>
     sha256=<64 hex> quote="<q>"`, and no `GATE S###` line sits outside that
     section; the receipt is a regular file (git mode 100644) committed at REV
     under .ufo/waves/round-41/fetch/ with exactly that sha256, >= 512 bytes,
     distinct per id (no two ids share a path, a sha256 or a whitespace-
     normalized quote); for a NEW id the receipt's file name and sha256 must be
     one of the PINS (the receipts the L1 fetched before the wave; the table
     below is part of this counter); the quote is 3-25 words and occurs in the
     receipt's normalized text (HTML receipts: tags replaced by a space, scripts
     and styles dropped, entities decoded; other receipts: whitespace collapsed
     only) and in no OTHER cited receipt;
  e  each new id's location, without its `#fragment`, occurs in no other
     registry row, and the location's last path component (query and fragment
     dropped, lower-cased) and the receipt's file name contain one another (one
     is a substring of the other);
  f  corpus/README.md holds exactly one column-zero index row for the entry
     outside fenced blocks;
  g  per cited id, one entry line (outside fences) names the id, names no other
     cited id, and carries its Gate quote, and that line is not the census line
     of h;
  h  exactly one new cited row has kind own-work; its Gate receipt is a saved
     journal (the output of `journalctl --user -u xdg-desktop-portal-hyprland
     --no-pager -o short-iso`, not a tool's report) of which this counter
     computes, with its own parser of the ADVERT/BOOT grammar below, S sessions,
     A adverts, D distinct names in the latest session and F adverts naming
     hyprland_focus_grab_manager_v1 in the latest session; the entry carries
     the line `journal sessions=S adverts=A interfaces=D focus_grab=F`
     verbatim as a line of its own (outside fences) exactly once, S >= 2,
     A >= 40, F >= 1, D >= 20, the journal holds >= 1 BOOT line, and the
     sessions' first timestamps are distinct and ascending. ADVERT = a line that
     fully matches `TS HOST xdg-desktop-portal-hyprland[PID]: [LOG]  | Got
     interface: NAME (ver N)` (ASCII digits; two spaces after `[LOG]`; NAME
     `[A-Za-z0-9_]{1,128}`); BOOT = `-- Boot <32 lowercase hex> --`; a session
     starts at an ADVERT when none is open, a BOOT line came since the previous
     ADVERT, or its PID differs from the open session's;
  i  the lesson's `## Gate` carries >= 1 line `ADMIT <staged path> as <this
     entry's path>` and >= 1 line `REFUSE <staged path> reason=<text of >= 4
     distinct words>` where each staged path names one of the 13 focus-theme
     package files in STAGED (below), the REFUSE target differs from every
     ADMIT target, and no cited row (any cell, lower-cased) contains a
     localized-documentation marker of BAD_LOC (the localized-documentation
     channel is outside PROVINCE.md).

Final line: `PRED-C2-r41-v2: admitted=N/1 verdict=TARGET_MET|TARGET_MISSED
rev=<full hash>`. TARGET_MET iff admitted=1/1 (exit 0), else exit 1.
Residual (declared): the pins are the trust root (a forged receipt committed
before the v2 freeze would be pinned as genuine); a real receipt can be cited
for a claim it does not support (the quote-to-claim binding is the non-author
closure's job); a held id's receipt is not pinned; BAD_LOC is a marker list, not
a language detector. The own-work journal receipt is parsed by C2's own parser
and C2 does not depend on C1's tool.
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

PRED = "PRED-C2-r41-v2"
BASE_DEFAULT = "ab2bfaab661c846d1de9d58c01651cd156a13949"
ENTRIES = ("corpus/knowledge/hyprland-focus-grab-r41.md",)
LESSON = "corpus/lessons/round-41.md"
FETCH = ".ufo/waves/round-41/fetch/"
OPENED = "2026-10-25"
MIN_RECEIPT = 512
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) '
                     r'quote="(.+)"\s*$')
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")
SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")
JOURNAL_RE = re.compile(r"^journal sessions=([0-9]+) adverts=([0-9]+) interfaces=([0-9]+) focus_grab=([0-9]+)$")
ADV_RE = re.compile(
    r"([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}) (\S+) "
    r"xdg-desktop-portal-hyprland\[([0-9]+)\]: (?:\[LOG\]|\[ERR\])  \| "
    r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver ([0-9]{1,6})\)")
BOOT_RE = re.compile(r"-- Boot ([0-9a-f]{32}) --")
ADMIT_RE = re.compile(r"^ADMIT (\S+\.md) as (\S+\.md)\s*$")
REFUSE_RE = re.compile(r"^REFUSE (\S+\.md) reason=(.{20,})$")
BAD_LOC = ("amgsk.dev", "zhihu", "/zh", "/ja", "zenn.dev", "qiita.com", "/jp/",
           "/cn/", "t.co/", "bit.ly", "\u65e5\u672c", "\u4e2d\u6587")
# the receipts the L1 fetched before the wave (fetch/ at the v2 freeze); a NEW
# cited id's receipt must be one of them, byte for byte
PINS = {
    "Hyprland-FocusGrab.cpp": "53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1",
    "Hyprland-FocusGrab.hpp": "dce47251853f8d95eeec0eb357665efdceccd52b111e633c56412e5c55103421",
    "focus-grab-v1.xml": "0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4",
    "input-capture-v1.xml": "fff89f6f9de622fefa1a62a6e6970f76683b6328454565583046abebcfe2c360",
    "issue-565.html": "148a9053e813a7d912c3c2e9fdb234ef42d20004438d33b41f1110d37679d1dc",
    "protocols-README.md": "3c7007636e13889860491d0c57f93c29d92122d17838ca1f6559e4aeb7aa6323",
    "quickshell-grab.cpp": "6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40",
    "xdph-PortalManager.cpp": "15c3e39cea5af1a92924ebc1ffe0f7825c86ac3c0b49e894aede86b2e091ea55",
    "xdph-journal.txt": "bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7",
}
# the staged package files of the focus theme (the only paths an ADMIT/REFUSE may name)
STAGED = {
    "focus-control-surfaces-r28.md",
    "focus-grab-focus-selection-r10.md",
    "focus-grab-has-no-client-here-r15.md",
    "focus-grab-keyboard-routing-r13.md",
    "focus-grab-mouse-target-r11.md",
    "focus-grab-observed-semantics-r9.md",
    "focus-grab-protocol-live-on-host-r14.md",
    "focus-grab-seat-semantics-r8.md",
    "focus-grab-whitelist-admission-r12.md",
    "privileged-client-surface-r29.md",
    "compositor-focus-manipulation-literature-r26.md",
    "wayland-input-security-literature-r8.md",
    "upstream-input-holds-and-the-lock-screen-r16.md",
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


def journal_counts(blob):
    """Sessions, adverts, distinct names and focus-grab adverts of the LATEST
    session of a saved journal, by this counter's own parser."""
    sessions, changed, cur, boots, firsts = [], False, None, 0, []
    for line in (blob or b"").decode("utf-8", "replace").split("\n"):
        if BOOT_RE.fullmatch(line):
            changed = True
            boots += 1
            continue
        m = ADV_RE.fullmatch(line)
        if not m:
            continue
        pid, name = m.group(3), m.group(4)
        if cur is None or changed or pid != cur[0]:
            cur = [pid, 0, {}]
            sessions.append(cur)
            firsts.append(m.group(1))
            changed = False
        cur[1] += 1
        cur[2][name] = cur[2].get(name, 0) + 1
    if not sessions:
        return None
    total = sum(x[1] for x in sessions)
    last = sessions[-1][2]
    return (len(sessions), total, len(last),
            last.get("hyprland_focus_grab_manager_v1", 0), boots > 0,
            len(set(firsts)) == len(firsts) and firsts == sorted(firsts))


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


def norm(text):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def score(repo, rev, base, entry, reg_rev, reg_base, lesson, readme):
    name = os.path.basename(entry)
    cl = dict.fromkeys("abcdefghi", 0)
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
            pin_ok = True
            if i in new_ids:
                pin_ok = PINS.get(os.path.basename(path)) == digest \
                    and path == FETCH + os.path.basename(path)
            nq = re.sub(r"\s+", " ", quote)
            if (blob is not None and len(blob) >= MIN_RECEIPT and pin_ok
                    and ls_mode(repo, rev, path) == "100644"
                    and hashlib.sha256(blob).hexdigest() == digest
                    and 3 <= len(quote.split()) <= 25
                    and path not in seen_paths and digest not in seen_sha
                    and nq not in seen_quote
                    and nq in norm_receipt(blob)):
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
        cells = reg_rev[i][0] if len(reg_rev.get(i, [[]])[0]) == 11 else None
        if cells is None:
            e_ok = False
            continue
        loc = cells[1].split()[-1] if cells[1].split() else ""
        key = loc.split("#")[0]
        same = [j for j, rr in reg_rev.items() for r in rr
                if len(r) == 11 and r[1].split()
                and r[1].split()[-1].split("#")[0] == key]
        e_ok &= bool(loc) and same == [i]
    cl["e"] = int(e_ok and bool(new_ids))

    own = [i for i in new_ids if reg_rev[i][0][2] == "own-work"]
    h_ok = False
    census_lines = set()
    if len(own) == 1 and own[0] in receipts_raw:
        jc = journal_counts(receipts_raw[own[0]])
        jm = [m for m in map(JOURNAL_RE.match, lines) if m]
        if jc is not None and len(jm) == 1:
            got = tuple(int(x) for x in jm[0].groups())
            census_lines = {jm[0].group(0)}
            h_ok = (got == jc[:4] and jc[0] >= 2 and jc[1] >= 40 and jc[2] >= 20
                    and jc[3] >= 1 and jc[4] and jc[5])
    cl["h"] = int(h_ok)

    entry_lines = [re.sub(r"\s+", " ", l) for l in lines
                   if l not in census_lines
                   and not l.startswith("journal ")]
    for i in ids:
        quote = None
        for path, digest, q in gates.get(i, []):
            quote = q
        if i not in receipts or quote is None:
            g_ok = False
            continue
        q = re.sub(r"\s+", " ", quote)
        hit = any(re.search(r"\b%s\b" % i, l) and q in l
                  and len(set(re.findall(r"\bS\d{3,}\b", l))) == 1
                  for l in entry_lines)
        g_ok &= hit
        print("%s %s clause=g id=%s obs=%d" % (PRED, name, i, hit))
    cl["g"] = int(g_ok)

    pat = re.compile(r"^\| `knowledge/%s`" % re.escape(name))
    cl["f"] = int(sum(1 for l in unfenced(readme) if pat.match(l)) == 1)
    admits = [m for m in map(ADMIT_RE.match, glines) if m]
    refuses = [m for m in map(REFUSE_RE.match, glines) if m]
    staged_ok = lambda p: os.path.basename(p) in STAGED
    adm = [m for m in admits if m.group(2) == entry and staged_ok(m.group(1))]
    ref = [m for m in refuses if staged_ok(m.group(1))
           and len(set(m.group(2).lower().split())) >= 4
           and all(m.group(1) != a.group(1) for a in adm)]
    bad = False
    for i in ids:
        rows = reg_rev.get(i, [])
        if rows and len(rows[0]) == 11:
            row_text = " ".join(rows[0]).lower()
            bad |= any(b_ in row_text for b_ in BAD_LOC)
    cl["i"] = int(bool(adm) and bool(ref) and not bad)
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
