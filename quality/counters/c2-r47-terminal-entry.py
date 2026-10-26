#!/usr/bin/env python3
"""PRED-C2-r47 - the terminal-selection entry is admitted (C2, coverage, sourced).

Scores one committed revision REV of the lane against BASE
(60edb66e2f1cb90acc6e9442fc93ded0ca42d750, the lane tip at round start). ENTRY =
corpus/knowledge/xdg-terminal-selection-r47.md. Nothing in the lane is written: every
read is revision-addressed (`git show REV:path`) and ambient GIT_* is removed. The
counter FETCHES NOTHING: the pinned bytes it trusts are the committed copies under
.ufo/waves/round-47/fetch/ at REV (recursively, subdirectories allowed). A fetch copy is
trusted only when its sha256 equals the digest the citing row records, and - for a file
of the xdg-terminal-exec repository - when it also equals the digest of the real
v0.14.3 file, hard-coded in PIN_SHA from
https://codeload.github.com/Vladimir-csp/xdg-terminal-exec/tar.gz/refs/tags/v0.14.3
(tag commit 065925df9f419008159258ae169018bfd23df71b; the tarball's `xdg-terminal-exec`
is byte-equal to the host /usr/bin/xdg-terminal-exec, sha256 89f2be9a65deb8..).

Pins are named by the entry and the rows, and resolved to a committed fetch copy by
name: the locator token's basename is the fetch basename (exact win), else the unique
fetch copy whose extension-stripped stem contains the token's stem or vice versa
(`README-v0.14.3.md` -> `README.md`). The bytes decide: a resolution is accepted only
when the copy's sha256 is the row's digest.

The entry is admitted iff every clause holds:
  a  ENTRY exists at REV and is absent at BASE (present at BASE is a setup error,
     exit 2): the entry is new ground.
  b  provenance head, unfenced lines inside the first 20 raw lines: >= 2 distinct
     `source: S###` lines, every id numerically >= S326 (the registry tops at S325 at
     BASE and every ROW is now new), exactly one `verified-at: 2026-10-26`, exactly one
     `recheck:` (ISO date, `NNd` or `on-*`); no `source:`/`verified-at:`/`recheck:` line
     outside that window; every `S###` token anywhere in the unfenced entry must be a
     row that exists in the Registry at REV (a cited id with no row is a ghost; held ids
     S056-S060 exist and pass). Each head id has exactly one Registry
     row (0-3 leading spaces, 11 cells) with tier A/B/C, a non-empty kind, status
     `mined`, opened 2026-10-26, a valid recheck cell and used-by listing ENTRY; no head
     id exists at BASE.
  c  every cited row is pin-bound and every URL is ref-pinned:
     - the row records `sha256:<64hex>` and names exactly one fetch pin by its
       `.ufo/waves/round-47/fetch/<path>` receipt path;
     - that copy exists at REV, mode 100644, and its sha256 equals the row's digest;
     - for a URL on the xdg-terminal-exec repository the URL path must be a key of
       PIN_SHA, the row's digest must equal PIN_SHA[path] and the fetch copy must hash
       to it (real v0.14.3 bytes), and the fetch name's stem must relate to the path;
     - the anchor cell names the pin with `<name>:<a>[-<b>]` ranges that resolve to that
       copy (or to no fetch copy, i.e. an upstream path name the pin is a renamed copy
       of) and stay inside its line count, OR it says `whole file` (range = the file);
       digest prefixes (`sha256:713703..`) are not read as locators;
     - every URL in the row is ref-pinned: refs `v0.14.3` or a commit hash (7-40 hex)
       only; `main`, `master`, `HEAD`, `latest`, `dev`, `trunk`, `develop` and every
       other ref are refused; a URL with no ref segment (e.g. a merge_requests URL) is
       refused unless the row records a 40-hex commit; a row with no URL is refused.
  d  every quote is pinned at its stated range. A quote is an inline span the author
     cites: a backticked or double-quoted span of 2-25 words immediately followed by
     `, <locator>`, ` at <locator>` or `<locator>` in parentheses, where the locator
     resolves to a committed fetch pin. The span must occur verbatim
     (whitespace-collapsed, word-bounded) inside that pin, at least one occurrence line
     inside the stated [a,b]; a span longer than 25 words fails; every pin locator of
     the entry must stay inside its pin's line count and its pin must be cited by a row
     by name or by bytes (a pin whose sha256 equals a cited pin's sha is the same bytes,
     so `README-v0.14.3.md` is cited when a row cites `README.md`; an uncited pin cannot
     launder a quote).
  e  the selection chain: >= 6 numbered steps (`^N. ` on an unfenced body line, raw
     line >= 20) and EVERY numbered step cites a `<script pin>:<a>[-<b>]` range inside
     the script pin's line count, where the script pin is the fetch copy whose sha256
     equals PIN_SHA["xdg-terminal-exec"]. A chain sentence with no script locator is a
     citation index, not a chain.
  f  the round-17 [UNK] is answered by the resolver's own live capture: an unfenced entry line names
     `corpus/knowledge/terminal-route-r17.md:144` (the [UNK] at :144-145) and cites
     `.ufo/waves/round-47/receipts/<file>`. That receipt exists at REV (100644, >= 256 B), is absent at BASE,
     holds `resolver_sha256=<the v0.14.3 script digest>`, >= 3 XDG_* lines, and `observed=<path>`: a committed
     capture (absent at BASE) of the real resolver's `--print-id --print-path --print-cmd` stdout whose first line
     is a `.desktop` id and second an absolute path. The citing entry line states that id and that path (or the
     path with /home/<user>/ written as ~/). (L1 freeze change from the w1 draft: the draft re-ran the landed
     tools/mado-terminal.py here, which made C2 depend on C1; the tool's agreement is C1's evidence.)
  g  corpus/README.md holds exactly one column-0 index row for ENTRY with three cells,
     no redirect word (`supersed*|replac*|obsolet*|instead|deprecat*`), naming no other
     `knowledge/` file, and its `S###`/`S###-S###` tokens cover every head id.
  h  held ground: the rows S056-S060 (the documentary terminal route) are byte-equal at
     BASE and REV, all five present.
  i  ground-absent at BASE: the terms GROUND = ("read_config_paths", "check_entry_key",
     "find_entry_paths", "print-delimiter") each return no match from `git grep` at BASE
     under corpus/ (exit 1), and >= 2 of them occur at REV under corpus/.
Final line: `PRED-C2-r47: admitted=N/1 verdict=TARGET_MET|TARGET_MISSED rev=<full hash>`;
exit 0 iff admitted=1/1, 1 otherwise, 2 on a setup failure (unresolved revision, or the
entry already present at BASE).

Residuals (declared): the fetch copies at REV are the trust root for every non-
xdg-terminal-exec URL (the counter fetches nothing, so a pinned commit URL outside that
repository is bound to the row's digest, not independently re-hashed); a true quote at a
true locator can stand beside a claim it does not support; clause c binds URL+digest+name,
not the truth of the row's scope sentence; clause d sees only spans the author cites with
a locator (a quote with no adjacent locator, like a quote of another lane document, is out
of its reach); clause e counts numbered steps and their script locators, not the truth of
each step; clause f binds the entry's sentence to a committed capture, not to a re-run of the resolver; clause i is a term census, not a semantic novelty proof.
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

PRED = "PRED-C2-r47"
ENTRY = "corpus/knowledge/xdg-terminal-selection-r47.md"
REGISTRY = "corpus/SOURCES.md"
README = "corpus/README.md"
FETCH = ".ufo/waves/round-47/fetch/"
RECEIPTS = ".ufo/waves/round-47/receipts/"
BASE_DEFAULT = "60edb66e2f1cb90acc6e9442fc93ded0ca42d750"
OPENED = "2026-10-26"
MIN_ID = 326
MIN_SOURCES = 2
MIN_RECEIPT = 256
HELD = ("S056", "S057", "S058", "S059", "S060")
GROUND = ("read_config_paths", "check_entry_key", "find_entry_paths", "print-delimiter")
TAG = "v0.14.3"
TAG_COMMIT = "065925df9f419008159258ae169018bfd23df71b"
BRANCH_REFS = ("main", "master", "HEAD", "head", "latest", "dev", "trunk", "develop",
               "Main", "Master")
EXTS = (".md", ".bats", ".list", ".scd", ".py", ".xml", ".cpp", ".hpp", ".h",
        ".conf", ".txt", ".desktop", ".sh", ".json", ".toml")
# real v0.14.3 bytes: sha256(file) from the tag tarball
PIN_SHA = {
    "xdg-terminal-exec": "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac",
    "README.md": "c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40",
    "xdg-terminals.list": "a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034",
    "xdg-terminal-exec.1.scd": "3dba162f5502a3553bad9b2398ace10f7bc2456900c7c9ff62a436935876ec59",
    "test/tests.bats": "ce4b634257dd6c1ebddd96d88f00f1b324f054209be6c80737224b69e986b311",
    "Makefile": "20ac532456fd0abbd449b5cabf8f14a07379763597e4c1dfe9c2ddb1c0dca6ef",
}
SCRIPT_SHA = PIN_SHA["xdg-terminal-exec"]
XTE_REPOS = ("vladimir-csp/xdg-terminal-exec",)
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")
SHA_RE = re.compile(r"sha256:\s*([0-9a-f]{64})|(?<![0-9a-f])([0-9a-f]{64})(?![0-9a-f])")
HEX40_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
URL_RE = re.compile(r"https?://[^\s`)\]>\"'|]+")
LOC_RE = re.compile(r"(?<![\w./-])([A-Za-z0-9._/-]+):(\d+)(?:-(\d+))?(?!\d)")
QUOTE_RE = re.compile(
    r"(?:`([^`\n]{2,600})`|\"([^\"\n]{2,600})\")"
    r"\s*(?:,\s*| at\s+|,\s*\(|\(\s*)([A-Za-z0-9._/-]+:\d+(?:-\d+)?)")
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")
RAW_RE = re.compile(r"^https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)(/.*)$")
GH_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/(?:blob|tree|raw)/([^/]+)(/.*)$")
GL_RE = re.compile(r"^https://gitlab\.freedesktop\.org/(.+?)/-/(?:blob|raw)/([^/]+)(/.*)$")
MADO_RE = re.compile(r"^MADO_TERM: selected=(\S+) path=(\S+) verdict=([A-Z]+)\s*$")


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
    rows = {}
    for line in section((blob or b"").decode("utf-8", "replace"), "## Registry"):
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


def fetch_pins(repo, rev):
    """name -> bytes for every committed fetch pin at REV (recursive)."""
    out = {}
    listing = git(repo, "ls-tree", "-r", rev, FETCH)
    for line in (listing or b"").decode("utf-8", "replace").splitlines():
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        meta, path = parts[0].split(), parts[1]
        if not path.startswith(FETCH):
            continue
        name = path[len(FETCH):]
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
        if d not in out:
            out.append(d)
    return out


def row_receipts(cells):
    out = []
    for name in re.findall(r"\.ufo/waves/round-47/fetch/([A-Za-z0-9._/-]+)", row_text(cells)):
        if name not in out:
            out.append(name)
    return out


def scan_urls(cells):
    """Clause c: every URL is ref-pinned; >= 1 URL; xte paths are PIN_SHA keys."""
    urls = URL_RE.findall(row_text(cells))
    if not urls:
        return False, "no_url"
    hex40 = bool(HEX40_RE.search(row_text(cells)))
    for u in urls:
        repo, ref, path, u = url_ref_path(u)
        if ref is None:
            # a ref-less locator (merge request, latest doc): only with a recorded
            # 40-hex commit and a recorded digest
            if not hex40 or not sha_in_row(cells):
                return False, "url_ref_absent:%s" % u[:90]
            continue
        if ref in BRANCH_REFS:
            return False, "url_branch_ref:%s" % u[:90]
        if ref != TAG and not re.fullmatch(r"[0-9a-f]{7,40}", ref):
            return False, "url_ref_not_pinned:%s" % u[:90]
        if (repo or "").lower() in XTE_REPOS and path not in PIN_SHA:
            return False, "url_path_not_pinned:%s" % path[:90]
    return True, ""


def wants(pin, path):
    """name/stem relation between a fetch pin and the URL path it should carry."""
    return stem(path) in stem(pin) or stem(pin) in stem(path)


def clause_c(repo, rev, ids, reg_rev, pins, by_base, name):
    ok = True
    cited_pins = {}
    for i in ids:
        rows = reg_rev.get(i, [])
        if len(rows) != 1 or len(rows[0]) != 11:
            print("%s %s clause=c id=%s rows=%d" % (PRED, name, i, len(rows)))
            ok = False
            continue
        cells = rows[0]
        good, why = scan_urls(cells)
        if not good:
            print("%s %s clause=c id=%s %s" % (PRED, name, i, why))
            ok = False
        digests = sha_in_row(cells)
        names = row_receipts(cells)
        if not digests:
            print("%s %s clause=c id=%s no_sha256" % (PRED, name, i))
            ok = False
        if len(names) != 1:
            print("%s %s clause=c id=%s fetch_receipts=%s" % (PRED, name, i, names))
            ok = False
            continue
        fname = names[0]
        blob = pins.get(fname)
        if blob is None:
            print("%s %s clause=c id=%s pin_missing=%s" % (PRED, name, i, fname))
            ok = False
            continue
        digest = hashlib.sha256(blob).hexdigest()
        cited_pins[fname] = blob
        if digest not in digests:
            print("%s %s clause=c id=%s pin_sha_mismatch=%s" % (PRED, name, i, fname))
            ok = False
        xte_paths = []
        for u in URL_RE.findall(row_text(cells)):
            repo_n, ref, path, _ = url_ref_path(u)
            if (repo_n or "").lower() in XTE_REPOS and path in PIN_SHA:
                xte_paths.append(path)
        for path in xte_paths:
            if PIN_SHA[path] not in digests:
                print("%s %s clause=c id=%s pin_sha_not_v0143=%s" % (PRED, name, i, path))
                ok = False
            if digest != PIN_SHA[path]:
                print("%s %s clause=c id=%s pin_bytes_not_v0143=%s" % (PRED, name, i, fname))
                ok = False
            if not wants(fname, path):
                print("%s %s clause=c id=%s pin_name_unrelated=%s:%s" % (
                    PRED, name, i, fname, path))
                ok = False
        lines = len(blob.decode("utf-8", "replace").split("\n"))
        anchor = cells[5]
        whole = re.search(r"\bwhole file\b", anchor, re.I) is not None
        ranges = []
        for token, a, b in locators(anchor):
            r = resolve_pin(token, pins, by_base)
            # a range under a name that resolves to THIS pin, or under an upstream
            # path name that no fetch copy carries (the pin is a renamed copy of it)
            if r == fname or r is None:
                ranges.append((a, b))
        if not ranges and not whole:
            print("%s %s clause=c id=%s anchor_no_range=%s" % (PRED, name, i, fname))
            ok = False
        for a, b in ranges:
            if a < 1 or b < a or b > lines:
                print("%s %s clause=c id=%s range_out_of_pin=%s:%d-%d/%d" % (
                    PRED, name, i, fname, a, b, lines))
                ok = False
        print("%s %s clause=c id=%s pin=%s sha=%s ranges=%d" % (
            PRED, name, i, fname, digest[:12], len(ranges)))
    return ok, cited_pins


def clause_d(pins, all_pins, by_base, cited_names, cited_bytes, lines, name):
    ok = True
    quotes = 0
    for ln, line in enumerate(lines, 1):
        for n, a, b in locators(line):
            pint = resolve_pin(n, all_pins, by_base)
            if pint is None:
                continue
            plines = len(all_pins[pint].decode("utf-8", "replace").split("\n"))
            if a < 1 or b < a or b > plines:
                print("%s %s clause=d locator_out_of_pin=%s:%d-%d/%d line=%d" % (
                    PRED, name, n, a, b, plines, ln))
                ok = False
            if pint not in cited_names and all_pins[pint] not in cited_bytes:
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


def clause_e(pins, lines, name):
    scripts = sorted(pn for pn, blob in pins.items()
                     if hashlib.sha256(blob).hexdigest() == SCRIPT_SHA)
    if not scripts:
        print("%s %s clause=e script_pin_missing sha=%s" % (PRED, name, SCRIPT_SHA[:12]))
        return False
    nlines = len(pins[scripts[0]].decode("utf-8", "replace").split("\n"))
    steps = [(ln, l) for ln, l in enumerate(lines, 1) if re.match(r"^\d+\.\s", l)]
    ok = len(steps) >= 6
    if not ok:
        print("%s %s clause=e steps=%d <6" % (PRED, name, len(steps)))
    cited = 0
    for ln, l in steps:
        hit = False
        for token, a, b in locators(l):
            if resolve_pin(token, pins, pin_index(pins)) != scripts[0]:
                continue
            if 1 <= a <= b <= nlines:
                hit = True
        if hit:
            cited += 1
        else:
            print("%s %s clause=e step_without_script_range line=%d" % (PRED, name, ln))
            ok = False
    print("%s %s clause=e steps=%d script_cited=%d script=%s:%d" % (
        PRED, name, len(steps), cited, scripts[0], nlines))
    return ok


def read_env_lines(text):
    env = {}
    for line in text.splitlines():
        m = re.match(r"^(XDG_[A-Z_]+)=(.*)$", line.strip())
        if m:
            env[m.group(1)] = m.group(2).strip()
    return env


def clause_f(repo, rev, base, lines, name):
    """The round-17 [UNK] is answered by the resolver's own read-only capture (L1 freeze: no tool run here, so C2
    stays separable from C1)."""
    cand, cited_lines = [], {}
    for l in lines:
        if not re.search(r"terminal-route-r17\.md:144(?!\d)", l):
            continue
        for p in re.findall(r"(?<![\w./-])(\.ufo/waves/round-47/receipts/[A-Za-z0-9._-]+)", l):
            if p not in cand:
                cand.append(p)
            cited_lines.setdefault(p, []).append(l)
    if not cand:
        print("%s %s clause=f no_r17_receipt_line" % (PRED, name))
        return False
    full = 0
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
        if not re.search(r"^resolver_sha256=%s$" % SCRIPT_SHA, text, re.M):
            print("%s %s clause=f receipt_no_resolver_sha=%s" % (PRED, name, path))
            continue
        m = re.search(r"^observed=(\S+)$", text, re.M)
        if not m:
            print("%s %s clause=f receipt_no_observed=%s" % (PRED, name, path))
            continue
        obs = show(repo, rev, m.group(1))
        if obs is None or show(repo, base, m.group(1)) is not None:
            print("%s %s clause=f observed_missing_or_held=%s" % (PRED, name, m.group(1)))
            continue
        first = obs.decode("utf-8", "replace").split("\n")
        if len(first) < 3 or not first[0].strip().endswith(".desktop") or not first[1].startswith("/"):
            print("%s %s clause=f observed_not_a_print_capture=%s" % (PRED, name, m.group(1)))
            continue
        sel, pth = first[0].strip(), first[1].strip()
        env = read_env_lines(text)
        if len(env) < 3:
            print("%s %s clause=f env_lines=%d" % (PRED, name, len(env)))
            continue
        tilde = re.sub(r"^/home/[^/]+/", "~/", pth)
        said = any(sel in l and (pth in l or tilde in l) for l in cited_lines[path])
        if not said:
            print("%s %s clause=f entry_line_does_not_state=%s %s" % (PRED, name, sel, tilde))
            continue
        full += 1
        print("%s %s clause=f receipt=%s observed=%s selected=%s path=%s" % (PRED, name, path, m.group(1), sel, tilde))
    if full == 0:
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


def clause_h(reg_rev, reg_base, name):
    ok = True
    for i in HELD:
        a, b = reg_base.get(i), reg_rev.get(i)
        if not a or a != b:
            print("%s %s clause=h held_row_moved=%s" % (PRED, name, i))
            ok = False
    print("%s %s clause=h held=%s unchanged=%d" % (PRED, name, ",".join(HELD), int(ok)))
    return ok


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
    cl = dict.fromkeys("abcdefghi", 0)
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
    # a cited S### must be a row that exists at REV (held rows included); an invented
    # id or a row not yet opened is a ghost
    ghosts = cited - set(reg_rev)
    rows_ok = len(ids) >= MIN_SOURCES and not ghosts
    for i in ids:
        rows = reg_rev.get(i, [])
        if len(rows) != 1 or len(rows[0]) != 11:
            print("%s %s clause=b id=%s rows=%d" % (PRED, name, i, len(rows)))
            rows_ok = False
            continue
        cells = rows[0]
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
    pins = fetch_pins(repo, rev)
    if not pins:
        print("%s %s clause=c fetch_pins=0 under %s" % (PRED, name, FETCH))
        return 0
    by_base = pin_index(pins)
    c_ok, cited_pins = clause_c(repo, rev, ids, reg_rev, pins, by_base, name)
    cl["c"] = int(c_ok)
    cl["d"] = int(clause_d(pins, pins, by_base, set(cited_pins),
                           set(cited_pins.values()), lines, name))
    cl["e"] = int(clause_e(pins, lines, name))
    cl["f"] = int(clause_f(repo, rev, base, lines, name))
    readme = (show(repo, rev, README) or b"").decode("utf-8", "replace")
    cl["g"] = int(clause_g(readme, ids, name))
    cl["h"] = int(clause_h(reg_rev, reg_base, name))
    cl["i"] = int(clause_i(repo, rev, base, text, name))
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
