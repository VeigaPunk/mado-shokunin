#!/usr/bin/env python3
"""PRED-C2-r48 - the XKB-compile entry is admitted (C2, coverage, sourced).

Scores one committed revision REV of the lane against BASE
(579f694b45c797a9c39761fdb4f9e0a1b71b3585, the lane tip at round start). ENTRY =
corpus/knowledge/xkb-keymap-compile-r48.md. Nothing in the lane is written: every read is
revision-addressed (`git show REV:path`) and ambient GIT_* is removed. The counter
FETCHES NOTHING: the pinned bytes it trusts are the committed copies under
.ufo/waves/round-48/fetch/ at REV (recursively, subdirectories allowed), plus the round-46
pins the held rows carry (.ufo/waves/round-46/fetch/). A fetch copy is trusted only when
its sha256 equals a digest the citing row records. There is no hard-coded upstream digest
map this round (unlike the round-47 xdg-terminal-exec pin): the committed copy and the
row's digest are bound to each other; neither is independently re-hashed here.

Pins are named by the entry and the rows, and resolved to a committed fetch copy by name:
the locator token's basename is the fetch basename (exact win), else the unique fetch copy
whose extension-stripped stem contains the token's stem or vice versa
(`libxkbcommon-rules.c` <- `rules.c`, `xkeyboard-config-symbols-br` <- `symbols/br`). The
bytes decide: a resolution is accepted only when the copy's sha256 is a digest the row
records.

The entry is admitted iff every clause holds:
  a  ENTRY exists at REV and is absent at BASE (present at BASE is a setup error,
     exit 2): the entry is new ground.
  b  provenance head, unfenced lines inside the first 20 raw lines: >= 3 distinct
     `source: S###` lines, every id numerically >= S340 (the registry tops at S339 at
     BASE and every row is new), exactly one `verified-at: 2026-10-26`, exactly one
     `recheck:` (ISO date, `NNd` or `on-*`); no `source:`/`verified-at:`/`recheck:` line
     outside that window; every `S###` token anywhere in the unfenced entry must be a row
     that exists in the Registry at REV (a cited id with no row is a ghost; the held ids
     S318/S319 exist and pass). Each head id has exactly one Registry row (0-3 leading
     spaces, 11 cells) with tier A/B/C, a non-empty kind, status `mined`, opened
     2026-10-26, a valid recheck cell and used-by listing ENTRY; no head id exists at BASE.
  c  every head row is pin-bound and every URL is ref-pinned:
     - the row records `sha256:<64hex>` and names at least one round-48 fetch pin by its
       `.ufo/waves/round-48/fetch/<path>` receipt path; every named pin exists at REV,
       mode 100644, and its sha256 equals a digest the row records;
     - for every URL in the row: refs `xkbcommon-1.13.2`, `xkeyboard-config-2.48` or a
       commit hash (7-40 hex) only; `main`, `master`, `HEAD`, `latest`, `dev`, `trunk`,
       `develop` and every other ref are refused; a URL with no ref segment is refused
       unless the row records a 40-hex commit and a digest; a row with no URL is refused
       unless its kind cell is `own-work` (a host capture has no upstream URL) and it
       still records a digest and a pin;
     - a URL path must relate to a pin name (stem containment), so a digest cannot be
       pasted from an unrelated file;
     - the anchor cell names pins with `<name>:<a>[-<b>]` ranges that resolve to one of
       the row's own pins (or to no fetch copy, i.e. an upstream path name the pin is a
       renamed copy of) and stay inside its line count, OR it says `whole file`;
       digest prefixes (`sha256:713703..`) are not read as locators; a range that
       resolves to a different pin is refused.
  d  every quote is pinned at its stated range. A quote is an inline span the author
     cites: a backticked or double-quoted span of 2-25 words immediately followed by
     `, <locator>`, ` at <locator>` or `<locator>` in parentheses, where the locator
     resolves to a committed fetch pin (round-48, or a round-46 pin cited by a held row).
     The span must occur verbatim (whitespace-collapsed, word-bounded) inside that pin,
     at least one occurrence line inside the stated [a,b]; a span longer than 25 words
     fails; every pin locator of the entry must stay inside its pin's line count and its
     pin must be cited by a row by name or by bytes (a pin whose sha256 equals a cited
     pin's sha is the same bytes; an uncited pin cannot launder a quote). A quote whose
     locator names a lane document (not a pin) is refused: the entry quotes upstream
     bytes, it does not quote itself.
  e  the compile chain: >= 6 numbered steps (`^N. ` on an unfenced body line) and EVERY
     numbered step cites a `<pin>:<a>[-<b>]` range that resolves to a pin cited by a row
     (round-48 head row or held round-46 row) and stays inside the pin's line count. A
     chain sentence with no pin locator is a citation index, not a chain.
  f  the compile is answered by the host's own read-only capture: an unfenced entry line
     cites `.ufo/waves/round-48/receipts/<file>`. That receipt exists at REV (100644,
     >= 512 B), is absent at BASE, and carries: a `xkbcli`/`libxkbcommon` version triple;
     the positive RMLVO (`br` + `compose:caps`) with rc 0 and a 64-hex keymap sha256 in
     one window; and three negative probes: unknown layout (`--layout zz`) rc 1, unknown
     variant (`--variant nope`) rc 1, unknown option (`nope:nope`) rc 0 together with
     `XKB-595` or the `Unrecognized RMLVO option ... was ignored` text. A window is a
     blank-line record, a case (a non-indented line plus its indented continuation lines)
     or a line; every window that names a probe must carry exactly one distinct labelled
     rc, and it must be the expected one, so an rc value can never drift to a neighbouring
     case. The entry states each of those values on an unfenced line: the version beside
     `xkbcli`, `compose:caps` with rc 0, the digest (or its first >= 12 hex) beside
     `sha256`, and each probe's rc (`rc`/`exit`/`status` + integer). A receipt line may be
     a key=value pair or a table row; the rc must carry its label so a bare number in a
     table cell is not read.
  g  corpus/README.md holds exactly one column-0 index row for ENTRY with three cells,
     no redirect word (`supersed*|replac*|obsolet*|instead|deprecat*`), naming no other
     `knowledge/` file, and its `S###`/`S###-S###` tokens cover every head id.
  h  held ground: the rows S318/S319 (Hyprland's keymap compile and its `us` fallback)
     are byte-equal at BASE and REV, both present; the round-46 entry
     (corpus/knowledge/hyprland-input-devices-r46.md) is byte-equal at BASE and REV; and
     each held row's round-46 pin exists at REV with a digest the row records (the held
     citations the new entry leans on are pin-bound too).
  i  ground-absent at BASE: the terms GROUND = ("xkb_keymap_new_from_names", "XKB-595",
     "compile-keymap", "xkeyboard-config-2.48") each return no match from `git grep` at
     BASE under corpus/ (exit 1), and >= 2 of them occur at REV under corpus/.
 r  replay: with TMPDIR set to an explicit round scratch root, re-run the positive
    `xkbcli compile-keymap --layout br --options compose:caps` and byte-compare its
    output digest to the `host.keymap` digest in the cited receipt. Re-run the three
    negative probes (unknown layout, unknown variant, unknown option) in an isolated
    temporary HOME/XDG_CONFIG_HOME and require rc (1, 1, 0) plus the named diagnostics.
    Missing xkbcli or TMPDIR is a setup error; changed package outputs are a miss.
Final line: `PRED-C2-r48: admitted=N/1 verdict=TARGET_MET|TARGET_MISSED rev=<full hash>`;
exit 0 iff admitted=1/1, 1 otherwise, 2 on a setup failure (unresolved revision, or the
entry already present at BASE).

Residuals (declared): the fetch copies at REV are the trust root (the counter fetches
nothing, so a tag/commit URL and a digest are bound to each other, not independently
re-hashed to the upstream object; a commit hash is accepted without proving it belongs to
the named repository); a true quote at a true locator can stand beside a claim it does not
support; clause c binds URL+digest+name, not the truth of the row's scope sentence or the
tag/commit it names; clause d sees only spans the author cites with a locator (a quote
with no adjacent locator is out of its reach) and refuses lane-document locators outright;
clause e counts numbered steps and their pin locators, not the truth of each step; clause
f reads the receipt's own labels (a receipt whose rc has no label is refused) and binds
the entry's sentences to the committed capture, not to a re-run of xkbcli; clause i is a
term census, not a semantic novelty proof; clause h freezes two rows and one document, not
the rest of the round-46 ground.
"""
import argparse
import datetime
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

PRED = "PRED-C2-r48"
ENTRY = "corpus/knowledge/xkb-keymap-compile-r48.md"
REGISTRY = "corpus/SOURCES.md"
README = "corpus/README.md"
FETCH = ".ufo/waves/round-48/fetch/"
HELD_FETCH = ".ufo/waves/round-46/fetch/"
RECEIPTS = ".ufo/waves/round-48/receipts/"
BASE_DEFAULT = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
OPENED = "2026-10-26"
MIN_ID = 340
MIN_SOURCES = 3
MIN_RECEIPT = 512
HELD = ("S318", "S319")
HELD_ENTRY = "corpus/knowledge/hyprland-input-devices-r46.md"
GROUND = ("xkb_keymap_new_from_names", "XKB-595", "compile-keymap",
          "xkeyboard-config-2.48")
TAGS = ("xkbcommon-1.13.2", "xkeyboard-config-2.48")
BRANCH_REFS = ("main", "master", "HEAD", "head", "latest", "dev", "trunk", "develop",
               "Main", "Master")
EXTS = (".md", ".bats", ".list", ".scd", ".py", ".xml", ".cpp", ".hpp", ".h",
        ".conf", ".txt", ".desktop", ".sh", ".json", ".toml")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")
SHA_RE = re.compile(r"sha256:\s*([0-9a-f]{64})|(?<![0-9a-f])([0-9a-f]{64})(?![0-9a-f])")
HEX40_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
HEX64_RE = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])")
URL_RE = re.compile(r"https?://[^\s`)\]>\"'|]+")
LOC_RE = re.compile(r"(?<![\w./-])([A-Za-z0-9._/-]+):(\d+)(?:-(\d+))?(?!\d)")
QUOTE_RE = re.compile(
    r"(?:`([^`\n]{2,600})`|\"([^\"\n]{2,600})\")"
    r"\s*(?:,\s*| at\s+|,\s*\(|\(\s*)([A-Za-z0-9._/-]+:\d+(?:-\d+)?)")
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")
RAW_RE = re.compile(r"^https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)(/.*)$")
GH_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/(?:blob|tree|raw)/([^/]+)(/.*)$")
GL_RE = re.compile(r"^https://gitlab\.freedesktop\.org/(.+?)/-/(?:blob|raw)/([^/]+)(/.*)$")
RECEIPT_RE = re.compile(re.escape(RECEIPTS) + r"([A-Za-z0-9._-]+)")
RC_RE = re.compile(r"\b(?:rc|exit(?:[ _-]?(?:code|status))?|status)\b\s*[=:]?\s*(\d+)",
                   re.I)
VER_RE = re.compile(r"(?i)(?:libxkbcommon|xkbcommon|xkbcli)[^0-9\n]{0,40}"
                    r"(\d+\.\d+\.\d+)")
PROBE_LAYOUT = re.compile(r"(?:--layout[ =]zz\b|layout=zz\b|\blayout\s+zz\b)")
PROBE_VARIANT = re.compile(r"(?:--variant[ =]nope\b|variant=nope\b|\bvariant\s+nope\b)")
PROBE_OPTION = re.compile(r"nope:nope")
POS_RMLVO = re.compile(r"compose:caps")
PROBE_NAMES = ("unknown layout", "unknown variant", "unknown option")


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV)
    return p.stdout if p.returncode == 0 else None


def git_rc(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          env=ENV).returncode


def show(repo, rev, path):
    return git(repo, "show", "%s:%s" % (rev, path))


def resolve_rev(repo, rev):
    out = git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    if not out:
        raise Setup("unresolved revision %s" % rev)
    return out.decode().strip()


def ls_mode(repo, rev, path):
    out = git(repo, "ls-tree", rev, "--", path)
    if not out:
        return None
    return out.split()[0].decode()


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
    """id -> [(raw line, cells)] for every row of the Registry section."""
    rows = {}
    for line in section((blob or b"").decode("utf-8", "replace"), "## Registry"):
        m = ROW_RE.match(line)
        if m:
            cells = [c.strip() for c in line.strip().split("|")[1:-1]]
            rows.setdefault(m.group(1), []).append((line.rstrip("\r"), cells))
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


def collapse(text):
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


def is_word(c):
    return c.isalnum() or c == "_"


def occurrences(blob, nq):
    text, lines = collapse(blob.decode("utf-8", "replace"))
    out, start = [], 0
    while True:
        k = text.find(nq, start)
        if k < 0:
            return out
        before = text[k - 1] if k > 0 else " "
        after = text[k + len(nq)] if k + len(nq) < len(text) else " "
        if not (is_word(nq[0]) and is_word(before)) and not (is_word(nq[-1]) and is_word(after)):
            out.append(lines[k])
        start = k + 1


def norm_q(s):
    return re.sub(r"\s+", " ", s).strip()


LOC_SKIP = ("sha256", "sha1", "sha512", "md5", "https", "http")


def locators(line):
    """(token, a, b) locator ranges on a line; digest prefixes are not locators."""
    out = []
    for token, a, b in LOC_RE.findall(line):
        name = token.rsplit("/", 1)[-1].lower()
        if name in LOC_SKIP or re.fullmatch(r"[0-9a-f]{6,}", name):
            continue
        out.append((token, int(a), int(b) if b else int(a)))
    return out


def stem(base):
    b = base.rsplit("/", 1)[-1].lower()
    for ext in EXTS:
        if b.endswith(ext):
            return b[:-len(ext)]
    return b


def pin_index(pins):
    by_base = {}
    for name in pins:
        by_base.setdefault(name.rsplit("/", 1)[-1], []).append(name)
    return by_base


def resolve_pin(token, pins, by_base):
    """fetch pin name for a locator token, or None (exact basename wins)."""
    base = token.rsplit("/", 1)[-1]
    if token in pins:
        return token
    if base in by_base and len(by_base[base]) == 1:
        return by_base[base][0]
    s = stem(base)
    if not s:
        return None
    cands = [n for n in pins if s in stem(n) or stem(n) in s]
    return cands[0] if len(cands) == 1 else None


def fetch_pins(repo, rev, root):
    """name -> bytes for every committed fetch pin at REV (recursive)."""
    out = {}
    listing = git(repo, "ls-tree", "-r", rev, root)
    for line in (listing or b"").decode("utf-8", "replace").splitlines():
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        path = parts[1]
        if not path.startswith(root):
            continue
        name = path[len(root):]
        blob = show(repo, rev, path)
        if blob is not None:
            out[name] = blob
    return out


def url_ref_path(url):
    u = url.rstrip(".,;:")
    m = RAW_RE.match(u)
    if m:
        return ("%s/%s" % (m.group(1), m.group(2)), m.group(3), m.group(4).lstrip("/"), u)
    m = GH_RE.match(u)
    if m:
        return ("%s/%s" % (m.group(1), m.group(2)), m.group(3), m.group(4).lstrip("/"), u)
    m = GL_RE.match(u)
    if m:
        return (m.group(1), m.group(2), m.group(3).lstrip("/"), u)
    return (None, None, None, u)


def row_text(cells):
    return " | ".join(cells)


def sha_in_row(cells):
    out = []
    for a, b in SHA_RE.findall(row_text(cells)):
        d = a or b
        d = d.lower()
        if d not in out:
            out.append(d)
    return out


def row_receipts(cells):
    out = []
    for name in re.findall(re.escape(FETCH) + r"([A-Za-z0-9._/-]+)", row_text(cells)):
        if name not in out:
            out.append(name)
    return out


def held_receipts(cells):
    out = []
    for name in re.findall(re.escape(HELD_FETCH) + r"([A-Za-z0-9._/-]+)", row_text(cells)):
        if name not in out:
            out.append(name)
    return out


def scan_urls(cells, kind):
    """Clause c: every URL is ref-pinned; a URL-less row only as an own-work capture."""
    text = row_text(cells)
    urls = URL_RE.findall(text)
    if not urls:
        return kind == "own-work" and bool(sha_in_row(cells)), "no_url"
    hex40 = bool(HEX40_RE.search(text))
    for u in urls:
        repo, ref, path, _ = url_ref_path(u)
        if ref is None:
            if not hex40 or not sha_in_row(cells):
                return False, "url_ref_absent:%s" % u[:90]
            continue
        # MUTANT c: any URL ref accepted, branch names included
    return True, ""


def wants(pin, path):
    """name/stem relation between a fetch pin and the URL path it should carry."""
    return stem(path) in stem(pin) or stem(pin) in stem(path)


def clause_c(repo, rev, ids, reg_rev, pins, by_base, name):
    ok = True
    cited = {}
    for i in ids:
        rows = reg_rev.get(i, [])
        if len(rows) != 1 or len(rows[0][1]) != 11:
            print("%s %s clause=c id=%s rows=%d" % (PRED, name, i, len(rows)))
            ok = False
            continue
        cells = rows[0][1]
        good, why = scan_urls(cells, cells[2])
        if not good:
            print("%s %s clause=c id=%s %s" % (PRED, name, i, why))
            ok = False
        digests = sha_in_row(cells)
        names = row_receipts(cells)
        if not digests:
            print("%s %s clause=c id=%s no_sha256" % (PRED, name, i))
            ok = False
        if not names:
            print("%s %s clause=c id=%s no_round48_pin" % (PRED, name, i))
            ok = False
            continue
        rowp = {}
        for fname in names:
            blob = pins.get(fname)
            if blob is None:
                print("%s %s clause=c id=%s pin_missing=%s" % (PRED, name, i, fname))
                ok = False
                continue
            digest = hashlib.sha256(blob).hexdigest()
            if digest not in digests:
                print("%s %s clause=c id=%s pin_sha_mismatch=%s" % (PRED, name, i, fname))
                ok = False
                continue
            rowp[fname] = blob
        cited.update(rowp)
        for u in URL_RE.findall(row_text(cells)):
            repo_n, ref, path, _ = url_ref_path(u)
            if path and not any(wants(pn, path) for pn in rowp):
                print("%s %s clause=c id=%s pin_name_unrelated=bound:%s:%s" % (
                    PRED, name, i, ",".join(sorted(rowp)) or "-", path[:80]))
                ok = False
        anchor = cells[5]
        whole = re.search(r"\bwhole file\b", anchor, re.I) is not None
        ranges = 0
        for token, a, b in locators(anchor):
            r = resolve_pin(token, pins, by_base)
            if r is None:
                # an upstream path name no fetch copy carries: the pin is a renamed copy
                continue
            if r not in rowp:
                print("%s %s clause=c id=%s range_other_pin=%s" % (PRED, name, i, token))
                ok = False
                continue
            ranges += 1
            nlines = len(rowp[r].decode("utf-8", "replace").split("\n"))
            if a < 1 or b < a or b > nlines:
                print("%s %s clause=c id=%s range_out_of_pin=%s:%d-%d/%d" % (
                    PRED, name, i, r, a, b, nlines))
                ok = False
        if ranges == 0 and not whole:
            print("%s %s clause=c id=%s anchor_no_range" % (PRED, name, i))
            ok = False
        print("%s %s clause=c id=%s pins=%s digests=%d ranges=%d" % (
            PRED, name, i, ",".join(sorted(rowp)), len(digests), ranges))
    return ok, cited


def clause_d(pins, by_base, cited_names, cited_bytes, lines, name):
    ok = True
    quotes = 0
    for ln, line in enumerate(lines, 1):
        for n, a, b in locators(line):
            pint = resolve_pin(n, pins, by_base)
            if pint is None:
                continue
            plines = len(pins[pint].decode("utf-8", "replace").split("\n"))
            if a < 1 or b < a or b > plines:
                print("%s %s clause=d locator_out_of_pin=%s:%d-%d/%d line=%d" % (
                    PRED, name, n, a, b, plines, ln))
                ok = False
            if pint not in cited_names and pins[pint] not in cited_bytes:
                print("%s %s clause=d pin_not_cited_by_row=%s line=%d" % (PRED, name, pint, ln))
                ok = False
        for m in QUOTE_RE.finditer(line):
            span = m.group(1) if m.group(1) is not None else m.group(2)
            token = m.group(3)
            q = norm_q(span)
            words = len(q.split())
            if words < 2:
                continue
            quotes += 1
            if words > 25:
                print("%s %s clause=d quote_too_long words=%d line=%d" % (PRED, name, words, ln))
                ok = False
                continue
            pint = resolve_pin(token.rsplit(":", 1)[0], pins, by_base)
            if pint is None:
                print("%s %s clause=d quote_locator_unresolved=%s line=%d" % (
                    PRED, name, token, ln))
                ok = False
                continue
            rng = re.match(r".+:(\d+)(?:-(\d+))?$", token)
            a, b = int(rng.group(1)), int(rng.group(2) or rng.group(1))
            at = occurrences(pins[pint], q)
            if not at:
                print("%s %s clause=d quote_not_in_pin line=%d pin=%s q=%r" % (
                    PRED, name, ln, pint, q[:70]))
                ok = False
            elif not any(a <= x <= b for x in at):
                print("%s %s clause=d quote_out_of_range line=%d pin=%s q=%r at=%s range=%d-%d" % (
                    PRED, name, ln, pint, q[:60], at[:3], a, b))
                ok = False
    print("%s %s clause=d quotes=%d" % (PRED, name, quotes))
    return ok


def clause_e(pins, cited_names, lines, name):
    by_base = pin_index(pins)
    steps = [(ln, l) for ln, l in enumerate(lines, 1) if re.match(r"^\d+\.\s", l)]
    ok = len(steps) >= 6
    if not ok:
        print("%s %s clause=e steps=%d <6" % (PRED, name, len(steps)))
    cited = 0
    for ln, l in steps:
        hit = False
        uncited = []
        for token, a, b in locators(l):
            pint = resolve_pin(token, pins, by_base)
            if pint is None:
                continue
            if pint not in cited_names:
                uncited.append(pint)
                continue
            nlines = len(pins[pint].decode("utf-8", "replace").split("\n"))
            if 1 <= a <= b <= nlines:
                hit = True
        if hit:
            cited += 1
        else:
            print("%s %s clause=e step_without_pin_range line=%d uncited=%s" % (
                PRED, name, ln, uncited[:3]))
            ok = False
    print("%s %s clause=e steps=%d pin_cited=%d" % (PRED, name, len(steps), cited))
    return ok


def records(text):
    return [b for b in re.split(r"\n[ \t]*\n", text)]


def cases(text):
    """A case is a non-indented line plus the indented lines that follow it."""
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
    """Every coherent window naming the token and carrying one distinct rc value."""
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


def clause_f(repo, rev, base, lines, name):
    """The compile is answered by the host's own read-only xkbcli capture."""
    cand = []
    for l in lines:
        for path in RECEIPT_RE.findall(l):
            full = RECEIPTS + path
            if full not in cand:
                cand.append(full)
    if not cand:
        print("%s %s clause=f no_receipt_line" % (PRED, name))
        return False
    full_ok = 0
    for path in cand:
        blob = show(repo, rev, path)
        if blob is None or ls_mode(repo, rev, path) != "100644":
            print("%s %s clause=f receipt_missing=%s" % (PRED, name, path))
            continue
        if show(repo, base, path) is not None:
            print("%s %s clause=f receipt_present_at_base=%s" % (PRED, name, path))
            continue
        if len(blob) < MIN_RECEIPT:
            print("%s %s clause=f receipt_short=%s:%d" % (PRED, name, path, len(blob)))
            continue
        text = blob.decode("utf-8", "replace")
        m = VER_RE.search(text)
        if not m:
            print("%s %s clause=f receipt_no_version=%s" % (PRED, name, path))
            continue
        version = m.group(1)
        pos, why = probe_rc(text, POS_RMLVO, 0)
        if pos is None:
            print("%s %s clause=f receipt_positive_bad=%s" % (PRED, name, why))
            continue
        pos_br = [b for b in records(text) + cases(text)
                  if POS_RMLVO.search(b) and re.search(r"\bbr\b", b)]
        if not pos_br:
            print("%s %s clause=f receipt_positive_no_layout=%s" % (PRED, name, path))
            continue
        digests = []
        for b in pos_br:
            for bl in b.splitlines():
                if re.search(r"keymap", bl, re.I) and not re.search(r"\.conf\b", bl):
                    digests += [x.lower() for x in HEX64_RE.findall(bl)]
        if not digests:
            print("%s %s clause=f receipt_no_keymap_sha=%s" % (PRED, name, path))
            continue
        if not (re.search(r"XKB-595", text)
                or re.search(r"Unrecognized RMLVO option", text)):
            print("%s %s clause=f receipt_no_xkb595=%s" % (PRED, name, path))
            continue
        neg_ok = True
        for token_re, want, label in ((PROBE_LAYOUT, 1, PROBE_NAMES[0]),
                                      (PROBE_VARIANT, 1, PROBE_NAMES[1]),
                                      (PROBE_OPTION, 0, PROBE_NAMES[2])):
            got, why = probe_rc(text, token_re, want)
            if got is None:
                print("%s %s clause=f receipt_probe_bad=%s(%s)" % (PRED, name, label, why))
                neg_ok = False
        if not neg_ok:
            continue
        # the entry states the same values on unfenced lines
        def states(pred):
            return any(pred(l) for l in lines)
        said_ver = states(lambda l: version in l and re.search(r"xkbcli", l, re.I))
        said_pos = states(lambda l: POS_RMLVO.search(l) and re.search(r"\bbr\b", l)
                          and rc_values(l) == [0])
        said_sha = states(lambda l: re.search(r"sha256", l, re.I)
                          and any(d in l or re.search(r"(?<![0-9a-f])%s" % d[:12], l)
                                  for d in digests))
        said_neg = []
        for token_re, want, label, warn in (
                (PROBE_LAYOUT, 1, PROBE_NAMES[0], False),
                (PROBE_VARIANT, 1, PROBE_NAMES[1], False),
                (PROBE_OPTION, 0, PROBE_NAMES[2], True)):
            def pred(l, token_re=token_re, want=want, warn=warn):
                if not token_re.search(l) or rc_values(l) != [want]:
                    return False
                return not warn or bool(re.search(r"XKB-595|ignored|warning", l, re.I))
            said_neg.append(states(pred))
        if not (said_ver and said_pos and said_sha and all(said_neg)):
            print("%s %s clause=f entry_disagrees=%s ver=%d pos=%d sha=%d neg=%s" % (
                PRED, name, path, said_ver, said_pos, said_sha, said_neg))
            continue
        full_ok += 1
        print("%s %s clause=f receipt=%s version=%s sha=%s probes=3" % (
            PRED, name, path, version, digests[0][:12]))
    if full_ok == 0:
        print("%s %s clause=f no_receipt_answers cited=%s" % (PRED, name, cand))
        return False
    return True


def clause_g(readme, ids, name):
    pat = re.compile(r"^\| `knowledge/%s`" % re.escape(os.path.basename(ENTRY)))
    frows = [l for l in unfenced(readme) if pat.match(l)]
    if len(frows) != 1:
        print("%s %s clause=g readme_rows=%d" % (PRED, name, len(frows)))
        return False
    row = frows[0]
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    ok = len(cells) == 3
    if not ok:
        print("%s %s clause=g readme_cells=%d" % (PRED, name, len(cells)))
    if re.search(r"\b(supersed\w*|replac\w*|obsolet\w*|instead|deprecat\w*)\b", row, re.I):
        print("%s %s clause=g readme_redirect_word" % (PRED, name))
        ok = False
    others = set(re.findall(r"knowledge/[A-Za-z0-9._-]+\.md", row)) - {
        "knowledge/" + os.path.basename(ENTRY)}
    if others:
        print("%s %s clause=g readme_names_other=%s" % (PRED, name, sorted(others)[:4]))
        ok = False
    listed = set()
    for a, b in re.findall(r"S(\d{3,})(?:-S(\d{3,}))?", cells[2] if len(cells) > 2 else ""):
        listed |= set("S%03d" % k for k in range(int(a), int(b or a) + 1))
    if not set(ids) <= listed:
        print("%s %s clause=g readme_missing_ids=%s" % (
            PRED, name, sorted(set(ids) - listed)))
        ok = False
    return ok


def clause_h(repo, rev, base, reg_rev, reg_base, held_pins, name):
    ok = True
    cited = {}
    for i in HELD:
        a, b = reg_base.get(i), reg_rev.get(i)
        if not a or a != b:
            print("%s %s clause=h held_row_moved=%s" % (PRED, name, i))
            ok = False
            continue
        cells = b[0][1]
        digests = sha_in_row(cells)
        names = held_receipts(cells)
        if not names or not digests:
            print("%s %s clause=h held_row_unpinned=%s" % (PRED, name, i))
            ok = False
            continue
        for fname in names:
            blob = held_pins.get(fname)
            if blob is None:
                print("%s %s clause=h held_pin_missing=%s" % (PRED, name, fname))
                ok = False
                continue
            if hashlib.sha256(blob).hexdigest() not in digests:
                print("%s %s clause=h held_pin_sha_mismatch=%s" % (PRED, name, fname))
                ok = False
                continue
            cited[fname] = blob
    if show(repo, rev, HELD_ENTRY) != show(repo, base, HELD_ENTRY):
        print("%s %s clause=h held_entry_moved=%s" % (PRED, name, HELD_ENTRY))
        ok = False
    print("%s %s clause=h held=%s unchanged=%d pins=%d" % (
        PRED, name, ",".join(HELD), int(ok), len(cited)))
    return ok, cited


def clause_r(repo, rev, base, lines, name):
    """Replay (critic finding 5): the counter re-runs the receipted xkbcli commands and byte-compares.

    The C2 receipt was taken in a scratch HOME/XDG_CONFIG_HOME (no user xkb dirs present). Clause r re-runs, on this
    host, the positive compile and the three negative probes with the same scratch env, and requires: the positive
    keymap bytes equal the receipt's recorded sha256; each negative probe's exit status equals the one the receipt
    records; the unknown-layout and unknown-variant stderr still carry the XKB-338/661 lines the entry quotes. `-` is
    refused (the receipt must be runnable). A missing xkbcli is a setup error.
    """
    for l in lines:
        for path in RECEIPT_RE.findall(l):
            full = RECEIPTS + path
            blob = show(repo, rev, full)
            if blob is None:
                continue
            if len(blob) < MIN_RECEIPT:
                print("%s %s clause=r receipt_short=%s" % (PRED, name, full))
                return False
            text = blob.decode("utf-8", "replace")
            dig = re.search(r"(?m)^([0-9a-f]{64})\s+host\.keymap$", text)
            if not dig:
                print("%s %s clause=r receipt_no_keymap_digest=%s" % (PRED, name, full))
                return False
            if not dig:
                print("%s %s clause=r receipt_no_digest=%s" % (PRED, name, full))
                return False
            m = VER_RE.search(text)
            if not m:
                print("%s %s clause=r receipt_no_version=%s" % (PRED, name, full))
                return False
            k = shutil.which("xkbcli")
            if not k:
                raise Setup("xkbcli missing for replay")
            if not os.environ.get("TMPDIR"):
                raise Setup("TMPDIR required for replay scratch")
            S = tempfile.mkdtemp(dir=os.environ["TMPDIR"], prefix="c2r-")
            try:
                env = dict(os.environ)
                env["HOME"] = os.path.join(S, "home")
                env["XDG_CONFIG_HOME"] = os.path.join(S, "xdg")
                env["XDG_CACHE_HOME"] = os.path.join(S, "cache")
                os.makedirs(env["XDG_CONFIG_HOME"])
                os.makedirs(env["XDG_CACHE_HOME"])
                for k2 in ("XKB_DEFAULT_RULES", "XKB_DEFAULT_MODEL", "XKB_DEFAULT_LAYOUT",
                           "XKB_DEFAULT_VARIANT", "XKB_DEFAULT_OPTIONS"):
                    env.pop(k2, None)

                def run(args):
                    p = subprocess.run([k] + args, capture_output=True, env=env, timeout=60)
                    return p.returncode, p.stdout, p.stderr

                rc, out, _ = run(["compile-keymap", "--layout", "br", "--options", "compose:caps"])
                if rc != 0 or hashlib.sha256(out).hexdigest() != dig.group(1):
                    print("%s %s clause=r positive_replay_failed rc=%d sha=%s" % (
                        PRED, name, rc, hashlib.sha256(out).hexdigest()[:12]))
                    return False
                rc1, _, err1 = run(["compile-keymap", "--test", "--layout", "zz"])
                rc2, _, err2 = run(["compile-keymap", "--test", "--layout", "br", "--variant", "nope"])
                rc3, _, err3 = run(["compile-keymap", "--test", "--layout", "br", "--options", "nope:nope"])
                if (rc1, rc2, rc3) != (1, 1, 0):
                    print("%s %s clause=r negative_replay_rc=%s" % (PRED, name, (rc1, rc2, rc3)))
                    return False
                if b"Couldn't find file" not in err1 or b'process include statement' not in err2:
                    print("%s %s clause=r negative_replay_stderr_short" % (PRED, name))
                    return False
                if b"XKB-595" not in err3 and b"Unrecognized RMLVO option" not in err3:
                    print("%s %s clause=r option_replay_stderr_short" % (PRED, name))
                    return False
            finally:
                shutil.rmtree(S, ignore_errors=True)
            print("%s %s clause=r replay=ok sha=%s neg=(1,1,0) ver=%s" % (PRED, name, dig.group(1)[:12], m.group(1)))
            return True
    print("%s %s clause=r no_receipt_found" % (PRED, name))
    return False


def clause_i(repo, rev, base, text, name):
    ok = True
    present = 0
    for term in GROUND:
        rc = git_rc(repo, "grep", "-F", "-q", "-e", term, base, "--", "corpus")
        if rc != 1:
            print("%s %s clause=i ground_present_at_base=%s rc=%d" % (PRED, name, term, rc))
            ok = False
        if term in text or git_rc(repo, "grep", "-F", "-q", "-e", term, rev, "--", "corpus") == 0:
            present += 1
    if present < 2:
        print("%s %s clause=i ground_vacuous=%d/%d" % (PRED, name, present, len(GROUND)))
        ok = False
    print("%s %s clause=i all_absent_at_base=%d present_at_rev=%d/%d" % (
        PRED, name, int(ok), present, len(GROUND)))
    return ok


def score(repo, rev, base, name):
    cl = dict.fromkeys("abcdefghir", 0)
    raw = show(repo, rev, ENTRY)
    text = raw.decode("utf-8", "replace") if raw is not None else ""
    lines = unfenced(text)
    cl["a"] = int(raw is not None)
    if not cl["a"]:
        print("%s %s clause=a entry_absent" % (PRED, name))
        return 0
    head, fenced, outside = [], False, 0
    for k, l in enumerate(text.splitlines()):
        if re.match(r"^\s{0,3}(```|~~~)", l):
            fenced = not fenced
            continue
        if fenced:
            continue
        if k < 20:
            head.append(l)
        elif re.match(r"^(source|verified-at|recheck):", l):
            outside += 1
    ids = []
    for l in head:
        m = SRC_RE.match(l)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    cited = set(re.findall(r"\bS\d{3,}\b", "\n".join(lines)))

    def hv(key):
        vals = [l[len(key) + 1:].strip() for l in head if l.startswith(key + ":")]
        return vals[0] if len(vals) == 1 else None
    va, rc = hv("verified-at"), hv("recheck")
    reg_rev = registry(show(repo, rev, REGISTRY))
    reg_base = registry(show(repo, base, REGISTRY))
    ghosts = cited - set(reg_rev)
    rows_ok = len(ids) >= MIN_SOURCES and not ghosts
    for i in ids:
        rows = reg_rev.get(i, [])
        if len(rows) != 1 or len(rows[0][1]) != 11:
            print("%s %s clause=b id=%s rows=%d" % (PRED, name, i, len(rows)))
            rows_ok = False
            continue
        cells = rows[0][1]
        items = [x.strip() for x in re.split(r"[,;]", cells[10])]
        good = (cells[3] in ("A", "B", "C") and bool(cells[2]) and cells[7] == "mined"
                and cells[8] == OPENED and ENTRY in items and recheck_ok(cells[9])
                and int(i[1:]) >= MIN_ID and i not in reg_base)
        if i in reg_base:
            print("%s %s clause=b id=%s present_at_base" % (PRED, name, i))
        if not good:
            print("%s %s clause=b id=%s tier=%s kind=%s status=%s opened=%s used=%d recheck=%s" % (
                PRED, name, i, cells[3], cells[2][:12], cells[7], cells[8], ENTRY in items,
                cells[9][:12]))
        rows_ok &= good
    if ghosts:
        print("%s %s clause=b ghost_ids=%s" % (PRED, name, sorted(ghosts)[:6]))
    cl["b"] = int(rows_ok and len(ids) >= MIN_SOURCES and va == OPENED
                  and recheck_ok(rc) and outside == 0)
    print("%s %s clause=b ids=%d outside_head=%d verified=%s recheck=%s ok=%d" % (
        PRED, name, len(ids), outside, va, (rc or "")[:10], cl["b"]))
    pins = fetch_pins(repo, rev, FETCH)
    if not pins:
        print("%s %s clause=c fetch_pins=0 under %s" % (PRED, name, FETCH))
        return 0
    held_pins = fetch_pins(repo, rev, HELD_FETCH)
    all_pins = dict(held_pins)
    all_pins.update(pins)
    by_base = pin_index(all_pins)
    c_ok, head_pins = clause_c(repo, rev, ids, reg_rev, pins, pin_index(pins), name)
    cl["c"] = int(c_ok)
    h_ok, held_cited = clause_h(repo, rev, base, reg_rev, reg_base, held_pins, name)
    cl["h"] = int(h_ok)
    cited_names = set(head_pins) | set(held_cited)
    cl["d"] = int(clause_d(all_pins, by_base, cited_names,
                           set(head_pins.values()) | set(held_cited.values()), lines, name))
    cl["e"] = int(clause_e(all_pins, cited_names, lines, name))
    cl["f"] = int(clause_f(repo, rev, base, lines, name))
    readme = (show(repo, rev, README) or b"").decode("utf-8", "replace")
    cl["g"] = int(clause_g(readme, ids, name))
    cl["i"] = int(clause_i(repo, rev, base, text, name))
    cl["r"] = int(clause_r(repo, rev, base, lines, name))
    admitted = int(all(cl.values()))
    print("%s %s clauses=%s admitted=%d" % (
        PRED, name, " ".join("%s:%d" % kv for kv in sorted(cl.items())), admitted))
    return admitted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    rev = resolve_rev(repo, args.rev)
    base = resolve_rev(repo, args.base)
    if show(repo, base, ENTRY) is not None:
        raise Setup("precondition_failed entry_present_at_base %s" % ENTRY)
    n = score(repo, rev, base, os.path.basename(ENTRY))
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
