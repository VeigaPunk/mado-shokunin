#!/usr/bin/env python3
"""PRED-C2-r43 - the Hyprland gkeep-geometry entry is admitted (C2, coverage, sourced).

Round-43 re-registration of PRED-C2-r42 (quality/counters/c2-r42-gkeep-entry.py, frozen at
809dc2caef09d9cbf15a496e55a1b208803a3561 and never scored by a seat: round 42 stopped before its
wave). Only the round constants differ: BASE, the entry/lesson/fetch paths, the opened and
verified-at date 2026-10-26, the host-clients receipt name and the pins of the two re-captured
own-work receipts (host-clients-r43.json, gkeep-ui-excerpt.py); every clause is unchanged.

Built from PRED-C2-r41-v2 (quality/counters/c2-r41-focus-entry-v2.py) with the two
holes its round-41 closure routed: a quote may begin or end in the middle of a word
(clause d now requires word boundaries at both ends) and a claim line may cite a real
receipt for a sentence that is not at the cited place (clause g now requires the
locator `<receipt file name>:<line>` of the quote, computed by this counter, in the
line). The own-work census clause h is rebuilt for this round's host facts.

Scores one committed revision REV (revision-addressed git reads, every ambient GIT_*
variable removed; nothing in the lane is written). The entry is
corpus/knowledge/hyprland-gkeep-geometry-r43.md. Fenced code blocks (``` ... ```) of the
entry, the README and the lesson are removed before any line is matched. It is admitted
iff every clause holds:

  a  the entry exists at REV and is absent at BASE (present at BASE is a setup error,
     exit 2);
  b  within its first 20 raw lines, outside fences: >= 4 distinct `source: S###` lines,
     exactly one `verified-at: 2026-10-26` and exactly one `recheck:` (an ISO calendar
     date, `NNd` or `on-*`); no `source:`, `verified-at:` or `recheck:` line outside that
     window (outside fences); and no `S###`/`s###` token anywhere in the entry (outside
     fences) that is not one of the cited ids;
  c  every cited id has exactly one `## Registry` row (0-3 leading spaces), 11 cells,
     status `mined`, a valid `recheck` cell, and its used-by cell, split on `,` and `;`
     and trimmed, lists the entry's path as one item; ids absent from the BASE registry
     (at least 3) carry opened 2026-10-26 and a location (last whitespace token of cell
     1) holding a `/` and a `.`; ids present at BASE keep cells 1-9 byte-equal to their
     BASE row and keep every BASE used-by item;
  d  corpus/lessons/round-43.md `## Gate` (outside fences) holds, per cited id, EXACTLY
     ONE line (starting in column 0) `GATE <id> receipt=<path> sha256=<64 hex>
     quote="<q>"`, and no `GATE S###` line sits outside that section; the receipt is a
     regular file (git mode 100644) committed at REV under .ufo/waves/round-43/fetch/
     with exactly that sha256, >= 256 bytes, distinct per id (no two ids share a path, a
     sha256 or a whitespace-normalized quote); for a NEW id the receipt's file name and
     sha256 must be one of the PINS (the receipts the L1 fetched before the wave; the
     table below is part of this counter); the quote is 3-25 words and occurs in the
     receipt's normalized text (HTML receipts: tags replaced by a space, scripts and
     styles dropped, entities decoded; other receipts: whitespace collapsed only) AT WORD
     BOUNDARIES (a quote that starts with a word character is not preceded by one, and
     one that ends with a word character is not followed by one) and in no OTHER cited
     receipt;
  e  each new id's location, without its `#fragment`, occurs in no other registry row,
     and the location's last path component (query and fragment dropped, lower-cased) and
     the receipt's file name contain one another (one is a substring of the other);
  f  corpus/README.md holds exactly one column-zero index row for the entry outside
     fenced blocks;
  g  per cited id, one entry line (outside fences) names the id, names no other cited id,
     carries its Gate quote and, for a non-HTML receipt, the locator
     `<receipt file name>:<N>` where N is the 1-based line of the receipt on which the
     quote starts (computed here), and that line is not one of the census lines of h;
  h  the host census: exactly three new cited rows have kind own-work and their
     receipts are host-gkeep.conf, host-clients-r43.json and gkeep-ui-excerpt.py (the
     PINS); this counter computes from them, by its own parsers, (1) from the config
     copy the lines `windowrule = size W H, match:class RX`, `windowrule = float V,
     match:class RX` and `windowrule = center V, match:class RX` (exactly one of each,
     the same RX, W and H ASCII digits) and the entry carries the line
     `host rules size=<W>x<H> float=<V> center=<V> class=<RX>`; (2) from the clients
     JSON (a list of objects) T mapped-or-unspecified clients, F of them floating true
     and G of them whose class matches RX under `re.fullmatch` and the entry carries
     `host clients total=<T> floating=<F> gkeep=<G>`; (3) from the excerpt the single
     call `set_default_size(W, H)` and the single `application_id="<ID>"` and the entry
     carries `gkeep request default_size=<W>x<H> application_id=<ID>`; each line verbatim
     as a line of its own (outside fences) exactly once; the rule's size equals the
     request's size and ID fully matches RX;
  i  the lesson's `## Gate` carries >= 1 line `ADMIT <staged path> as <this entry's
     path>` and >= 1 line `REFUSE <staged path> reason=<text of >= 4 distinct words>`
     where each staged path names one of the 11 gkeep-theme package files in STAGED
     (below), the REFUSE target differs from every ADMIT target, and no cited row (any
     cell, lower-cased) contains a localized-documentation marker of BAD_LOC (the
     localized-documentation channel is outside PROVINCE.md).

Final line: `PRED-C2-r43: admitted=N/1 verdict=TARGET_MET|TARGET_MISSED rev=<full hash>`.
TARGET_MET iff admitted=1/1 (exit 0), else exit 1.
Residual (declared): the pins are the trust root (a forged receipt committed before the
freeze would be pinned as genuine); a real receipt can be cited for a claim it does not
support, at a true locator, with a word-bounded quote (the quote-to-claim binding is the
non-author closure's job); a held id's receipt is not pinned; BAD_LOC is a marker list, not
a language detector. The census lines are recomputed from pinned receipts by this
counter's own parsers and C2 does not depend on C1's tool.
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

PRED = "PRED-C2-r43"
BASE_DEFAULT = "a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f"
ENTRIES = ("corpus/knowledge/hyprland-gkeep-geometry-r43.md",)
LESSON = "corpus/lessons/round-43.md"
FETCH = ".ufo/waves/round-43/fetch/"
OPENED = "2026-10-26"
MIN_RECEIPT = 256
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) '
                     r'quote="(.+)"\s*$')
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")
SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")
ADMIT_RE = re.compile(r"^ADMIT (\S+\.md) as (\S+\.md)\s*$")
REFUSE_RE = re.compile(r"^REFUSE (\S+\.md) reason=(.{20,})$")
BAD_LOC = ("amgsk.dev", "zhihu", "/zh", "/ja", "zenn.dev", "qiita.com", "/jp/",
           "/cn/", "t.co/", "bit.ly", "\u65e5\u672c", "\u4e2d\u6587")
# the receipts the L1 fetched before the wave (fetch/ at the v2 freeze); a NEW
# cited id's receipt must be one of them, byte for byte
PINS = {
    "gkeep-ui-excerpt.py": "3695b788c6d766b8e87c01916a6594158a26c2cf816f991ccf30b72d9c5d1713",
    "host-clients-r43.json": "21db902e1f1234b9f52411cf7885097a18d67b00b9dd0110f9bbd2b36fb442ad",
    "host-gkeep.conf": "3726e488c0bf93028f1bba11017cf02d26da6dc3604362815bc4f3738b8e9949",
    "Hyprland-DefaultFloatingAlgorithm.cpp": "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91",
    "Hyprland-GeometricMovableAnimated.cpp": "649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d",
    "Hyprland-HyprCtl.cpp": "798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa",
    "Hyprland-RegexMatchEngine.cpp": "8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282",
    "Hyprland-Target.cpp": "49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06",
    "Hyprland-WindowRuleApplicator.cpp": "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b",
    "Hyprland-WindowTarget.cpp": "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d",
}
# the staged package files of the focus theme (the only paths an ADMIT/REFUSE may name)
STAGED = {
    "gkeep-geometry-unobservable-r8.md",
    "gkeep-rendered-geometry-chain-r9.md",
    "gkeep-size-rule-application-r10.md",
    "gkeep-size-to-real-size-r11.md",
    "gkeep-observation-route-r11.md",
    "gkeep-client-size-request-r12.md",
    "gkeep-rendered-geometry-record-r13.md",
    "gkeep-rendered-geometry-record-r14.md",
    "gkeep-geometry-never-recorded-r15.md",
    "glyph-and-geometry-r31.md",
    "gkeep-element-rules-r30.md",
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


def host_census(new_ids, reg_rev, gates, receipts_raw, lines):
    """Clause h: recompute the three host census lines from the pinned own-work receipts."""
    own = [i for i in new_ids if reg_rev[i][0][2] == "own-work"]
    byname = {}
    for i in own:
        gl = gates.get(i, [])
        if len(gl) == 1 and i in receipts_raw:
            byname[os.path.basename(gl[0][0])] = receipts_raw[i]
    if len(own) != 3 or set(byname) != {"host-gkeep.conf", "host-clients-r43.json",
                                        "gkeep-ui-excerpt.py"}:
        return False, []
    conf = byname["host-gkeep.conf"].decode("utf-8", "replace")
    sizes, floats, centers = [], [], []
    for ln in conf.split("\n"):
        m = re.fullmatch(r"windowrule = (size|float|center) ([^,]+), match:class (\S+)", ln.strip())
        if not m:
            continue
        {"size": sizes, "float": floats, "center": centers}[m.group(1)].append((m.group(2), m.group(3)))
    if len(sizes) != 1 or len(floats) != 1 or len(centers) != 1:
        return False, []
    rx = sizes[0][1]
    if floats[0][1] != rx or centers[0][1] != rx:
        return False, []
    wh = re.fullmatch(r"([0-9]+) ([0-9]+)", sizes[0][0])
    if not wh or floats[0][0] not in ("on", "off") or centers[0][0] not in ("on", "off"):
        return False, []
    rules_line = "host rules size=%sx%s float=%s center=%s class=%s" % (
        wh.group(1), wh.group(2), floats[0][0], centers[0][0], rx)
    try:
        doc = json.loads(byname["host-clients-r43.json"].decode("utf-8"))
        assert isinstance(doc, list) and all(isinstance(c, dict) for c in doc)
        rxc = re.compile(rx)
    except (ValueError, AssertionError, re.error):
        return False, []
    live = [c for c in doc if c.get("mapped") is not False]
    g = sum(1 for c in live if isinstance(c.get("class"), str) and rxc.fullmatch(c["class"]))
    fl = sum(1 for c in live if c.get("floating") is True)
    clients_line = "host clients total=%d floating=%d gkeep=%d" % (len(live), fl, g)
    ui = byname["gkeep-ui-excerpt.py"].decode("utf-8", "replace")
    sd = re.findall(r"set_default_size\(([0-9]+), ([0-9]+)\)", ui)
    ai = re.findall(r'application_id="([^"]+)"', ui)
    if len(sd) != 1 or len(ai) != 1 or sd[0] != (wh.group(1), wh.group(2)) or not rxc.fullmatch(ai[0]):
        return False, []
    ui_line = "gkeep request default_size=%sx%s application_id=%s" % (sd[0][0], sd[0][1], ai[0])
    want = [rules_line, clients_line, ui_line]
    ok = all(sum(1 for l in lines if l == w) == 1 for w in want)
    return ok, want


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
                    and quote_at(blob, nq) is not None
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

    h_ok, census_lines = host_census(new_ids, reg_rev, gates, receipts_raw, lines)
    cl["h"] = int(h_ok)
    census_lines = set(census_lines)

    entry_lines = [re.sub(r"\s+", " ", l) for l in lines
                   if l not in census_lines
                   and not l.startswith("host ") and not l.startswith("gkeep request")]
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
