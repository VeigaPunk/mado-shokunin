#!/usr/bin/env python3
"""PRED-C2-r49 - the Hyprland bind-key-match entry is admitted (C2, coverage, sourced).

Draft for the round-49 freeze (w1/ExecCounterC2), adapted from PRED-C2-r48-v2. Scores one
committed revision REV of the lane against BASE 03e4ae76aff7a4be59cb69970dd553baa319695a
(the lane tip at round start). ENTRY = corpus/knowledge/hyprland-bind-key-match-r49.md.
Nothing in the lane is written: every read is revision-addressed (`git show REV:path`) and
ambient GIT_* is removed. The counter FETCHES NOTHING: the pinned bytes it trusts are the
committed copies under .ufo/waves/round-49/fetch/ at REV (recursively, subdirectories
allowed), plus the round-46 pin the held row S319 carries
(.ufo/waves/round-46/fetch/). A fetch copy is trusted only when its sha256 equals a digest
the citing row records.

Pins are named by the entry and the rows, and resolved to a committed fetch copy by name:
the locator token's basename is the fetch basename (exact win), else the unique fetch copy
whose extension-stripped stem contains the token's stem or vice versa
(`Hyprland-legacy-ConfigManager.cpp` <- `Hyprland-legacy-ConfigManager.cpp`,
`xkbcommon-keysym.c` <- `xkbcommon-keysym.c`). The bytes decide: a resolution is accepted
only when the copy's sha256 is a digest the row records.

The entry is admitted iff every clause holds:
  a  ENTRY exists at REV and is absent at BASE (present at BASE is a setup error, exit 2):
     the entry is new ground.
  b  provenance head, unfenced lines inside the first 20 raw lines: >= 3 distinct
     `source: S###` lines, every id numerically >= S352 (the registry tops at S351 at BASE
     and every row is new), exactly one `verified-at: 2026-10-27`, exactly one `recheck:`
     (ISO date, `NNd` or `on-*`); no `source:`/`verified-at:`/`recheck:` line outside that
     window; every `S###` token anywhere in the unfenced entry must be a row that exists in
     the Registry at REV (a cited id with no row is a ghost; the held id S319 exists and
     passes). Each head id has exactly one Registry row (0-3 leading spaces, 11 cells) with
     tier A/B/C, a non-empty kind, status `mined`, opened 2026-10-27, a valid recheck cell and
     used-by listing ENTRY; no head id exists at BASE. Landing: corpus/README.md holds
     exactly one column-0 index row for ENTRY with three cells, no redirect word
     (`supersed*|replac*|obsolet*|instead|deprecat*`), naming no other `knowledge/` file, and
     its `S###`/`S###-S###` tokens cover every head id.
  c  every head row is pin-bound and every URL is ref-pinned:
     - the row records `sha256:<64hex>` and names at least one round-49 fetch pin by its
       `.ufo/waves/round-49/fetch/<path>` receipt path; every named pin exists at REV,
       mode 100644, and its sha256 equals a digest the row records;
     - for every URL in the row: refs `xkbcommon-1.13.2`, `v0.56.2`, `0.56.2` or a commit
       hash (7-40 hex) only; `main`, `master`, `HEAD`, `latest`, `dev`, `trunk`, `develop`
       and every other ref are refused; a URL with no ref segment is refused unless the row
       records a 40-hex commit and a digest; a row with no URL is refused unless its kind
       cell is `own-work` (a host capture has no upstream URL) and it still records a digest
       and a pin;
     - a URL path must relate to a pin name (stem containment), so a digest cannot be
       pasted from an unrelated file;
     - the anchor cell names pins with `<name>:<a>[-<b>]` ranges that resolve to one of the
       row's own pins (or to no fetch copy, i.e. an upstream path name the pin is a renamed
       copy of) and stay inside its line count, OR it says `whole file`; digest prefixes
       (`sha256:713703..`) are not read as locators; a range that resolves to a different
       pin is refused.
  d  every quote is pinned at its stated range. A quote is an inline span the author cites:
     a backticked or double-quoted span of 2-25 words immediately followed by `, <locator>`,
     ` at <locator>` or `<locator>` in parentheses, where the locator resolves to a committed
     fetch pin (round-49, or the round-46 pin cited by the held row). The span must occur
     verbatim (whitespace-collapsed, word-bounded) inside that pin, at least one occurrence
     line inside the stated [a,b]; a span longer than 25 words fails; every pin locator of
     the entry must stay inside its pin's line count and its pin must be cited by a row by
     name or by bytes (a pin whose sha256 equals a cited pin's sha is the same bytes; an
     uncited pin cannot launder a quote). A quote whose locator names a lane document (not a
     pin) is refused: the entry quotes upstream bytes, it does not quote itself.
  e  the chain: >= 6 numbered steps (`^N. ` on an unfenced body line) and EVERY numbered
     step carries at least one quote that clause d would verify: a backticked or
     double-quoted span of >= 2 words (and <= 25) immediately followed by a locator that
     resolves to a pin cited by a row (round-49 head row or the held round-46 row) and that
     occurs inside the pin at least once within the stated [a,b]. An in-range locator alone
     is not enough (a step locator pointed at the wrong line inside the pin was admitted in
     w1/ExecControlsC2 bundle 14): a step is grounded on bytes, not on a number.
  f  the live capture answers it: an unfenced entry line cites
     `.ufo/waves/round-49/receipts/<file>`. That receipt exists at REV (100644, >= 512 B,
     absent at BASE), is a shape file (it carries no raw binds JSON), names
     `hyprctl binds -j`, records the raw-JSON digest on a `sha256` line, states the bind
     total and the four key-form counts (the form rule is fixed and re-derived by clause r: a
     `key` starting `code:`/`mouse`/`switch:` is that form, a bind with an empty `key` and a
     non-zero `keycode` is `code` (the dump's only trace of a keycode bind), everything else
     is `named`; the four counts must sum to the total), carries `Hyprland 0.56.2` with the pinned commit
     `efb50993780079460b0cbed1363e2166a2de1d9f`, and states `input:resolve_binds_by_sym`
     with `int 0` (or `set false`). The entry repeats each of those values on unfenced
     lines: the version beside the commit, the bind total (`192 binds` or `binds=192`), each
     form count beside its label (`named`/`code`/`mouse`/`switch`), the digest (or its first
     >= 12 hex) beside `sha256`, and the resolve value beside the option name. The stated
     counts must sum to the stated total. A count or digest may not drift between the
     receipt and the entry.
  g  held ground, cited and not re-registered: row S319 (Hyprland's keyboard base) is
     byte-equal at BASE and REV, its round-46 pin exists at REV with a digest the row
     records, and the entry cites `S319` in its unfenced text. No new row (>= S352 at REV,
     absent at BASE) repeats the (repository, ref, path) of S319's URL: the keyboard base is
     cited, never re-registered under a new id (other held sources may be reopened with a
     new scope, as rows S162/S303/S317 already do for one file).
  h  the entry has a `## Limits` section with >= 3 bullet lines, at least two of which name
     a scoped limitation (`not`, `no `, `never`, `outside`, `held`, `inferred`, `[UNK]`):
     the compositor half that was not measured is stated, not implied.
  i  the lesson carries the gate and the ground is new: corpus/lessons/round-49.md exists
     at REV with a non-empty `## Gate` section holding a `**S### admit**` line for EVERY
     registry row new at REV (id >= S352, absent at BASE; C1 and C2 rows alike), and every
     such row is used (its used-by cell names ENTRY, or a path that exists at REV) so a row
     nobody cites cannot be minted to pad the Gate; and the terms GROUND =
     ("xkb_state_key_get_one_sym", "m_xkbSymState", "keysym_to_name", "xkb_keysym_get_name")
     each return no match from `git grep` at BASE under corpus/ (exit 1) while >= 2 occur at
     REV under corpus/; and the entry body is not a paste or a light paraphrase of held
     text: of its unfenced lines >= 60 characters, at most 5 occur verbatim anywhere under
     corpus/ at BASE (at least 8 such lines exist), and of the hashed 6-word shingles of its
     unfenced prose fewer than 15% already occur in the base tree's corpus/knowledge and
     corpus/lessons text (at least 150 shingles; a one-word-per-nine paraphrase of two held
     documents measures 0.23-0.56, a verbatim paste 1.0, new prose about 0.01).
  j  topic coverage, source-derived (freeze addition after w1/CritClaimSizing C2 rows 48-50: six easy steps
     could omit the question): for each of the seven TOPICS below the counter finds, in the named pin,
     the lines that carry the topic's code text (regex over the pinned bytes, never a typed line number),
     and requires at least one numbered step to carry a quote whose locator names that pin and whose
     range covers one of those lines, the quote verified there as in clause e. Topics: the state the
     pressed keysym is read from (resolve_binds_by_sym ternary); the case-insensitive second lookup;
     the exact modifier-mask comparison with the `i` escape; the `code:` key form; the zero-modifier
     sym-state update; the depressed-only bind mask; the per-device option read. This checks that the
     entry answers each question at the line that implements it, not that its sentence is true (the
     non-author reading's job; declared residual).
  r  replay: the live capture is re-run and byte-compared. TMPDIR is REQUIRED and a TMPDIR
     under /tmp is REFUSED (setup error; a /tmp work dir is not a runnable instrument). With
     a scratch HOME/XDG_* set (never the operator's), the counter runs the host's
     /usr/bin/hyprctl (never a PATH lookup): `binds -j` must hash to the receipt's raw-JSON
     digest and re-derive the receipt's total and form counts; `getoption
     input:resolve_binds_by_sym -j` must yield the receipt's resolve value. XDG_RUNTIME_DIR
     and HYPRLAND_INSTANCE_SIGNATURE are inherited (the read-only socket route); the
     compositor's JSON is never printed. A missing hyprctl, a missing socket variable or an
     unreachable compositor is a setup error.
Final line: `PRED-C2-r49: clauses=... admitted=N/1 verdict=TARGET_MET|TARGET_MISSED rev=<full hash>`;
exit 0 iff admitted=1/1, 1 otherwise, 2 on a setup failure (unresolved revision, the entry
already present at BASE, a /tmp or absent TMPDIR, a missing hyprctl/socket).

Residuals (declared): the fetch copies at REV are the trust root (the counter fetches
nothing, so a tag/commit URL and a digest are bound to each other, not independently
re-hashed to the upstream object); a true quote at a true locator can stand beside a claim
it does not support; clause c binds URL+digest+name, not the truth of the row's scope
sentence or the tag/commit it names; clause d sees only spans the author cites with a
locator (a quote with no adjacent locator is out of its reach) and refuses lane-document
locators outright; clause e counts numbered steps and their pin locators, not the truth of
each step; clause f reads the receipt's own labels and binds the entry's sentences to the
committed capture; clause g compares URL triples, so a held source quoted inline with no
new row is out of its reach; clause h reads section shape and scope words, not the truth of
a limit; clause i is a term census plus a duplicate-line sample, not a semantic novelty
proof; clause r trusts the live socket at scoring time (a bind changed between capture and
score is a miss by design).
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

PRED = "PRED-C2-r49"
ENTRY = "corpus/knowledge/hyprland-bind-key-match-r49.md"
REGISTRY = "corpus/SOURCES.md"
README = "corpus/README.md"
LESSON = "corpus/lessons/round-49.md"
FETCH = ".ufo/waves/round-49/fetch/"
HELD_FETCH = ".ufo/waves/round-46/fetch/"
RECEIPTS = ".ufo/waves/round-49/receipts/"
BASE_DEFAULT = "03e4ae76aff7a4be59cb69970dd553baa319695a"
OPENED = "2026-10-27"
MIN_ID = 352
MIN_SOURCES = 3
MIN_RECEIPT = 512
MAX_RECEIPT = 262144
HELD = ("S319",)
HYPRLAND_COMMIT = "efb50993780079460b0cbed1363e2166a2de1d9f"
HYPRLAND_VERSION = re.compile(r"Hyprland\s+0\.56\.2")
FORMS = ("named", "code", "mouse", "switch")
GROUND = ("xkb_state_key_get_one_sym", "m_xkbSymState", "keysym_to_name",
          "xkb_keysym_get_name")
TAGS = ("xkbcommon-1.13.2", "v0.56.2", "0.56.2")
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
    r"(?:`([^`\n]{2,})`|\"([^\"\n]{2,})\")"
    r"\s*(?:,\s*| at\s+|,\s*\(|\(\s*)([A-Za-z0-9._/-]+:\d+(?:-\d+)?)")
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")
RAW_RE = re.compile(r"^https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)(/.*)$")
GH_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/(?:blob|tree|raw)/([^/]+)(/.*)$")
GL_RE = re.compile(r"^https://gitlab\.freedesktop\.org/(.+?)/-/(?:blob|raw)/([^/]+)(/.*)$")
RECEIPT_RE = re.compile(re.escape(RECEIPTS) + r"([A-Za-z0-9._-]+)")
PROBE_CMD = re.compile(r"hyprctl\s+binds\s+-j")
SCOPE_WORD = re.compile(r"\b(not|no|never|outside|held|inferred|unknown|\[UNK\])\b", re.I)
RESOLVE_OPTION = "resolve_binds_by_sym"
CLAUSES = "a:0"


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
        d = (a or b).lower()
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
        if ref in BRANCH_REFS:
            return False, "url_branch_ref:%s" % u[:90]
        if ref not in TAGS and not re.fullmatch(r"[0-9a-f]{7,40}", ref):
            return False, "url_ref_not_pinned:%s" % u[:90]
    return True, ""


def wants(pin, path):
    """name/stem relation between a fetch pin and the URL path it should carry."""
    return stem(path) in stem(pin) or stem(pin) in stem(path)


def bound_pins(reg_rev, pins, held_pins):
    """fetch pins a registry row at REV actually binds (names the pin path and records its digest).

    A pin outside this set cannot launder a quote: the entry may lean on any row-bound ground,
    including held round-46 pins, but not on an unbound file that happens to sit in a fetch dir.
    """
    out = {}
    for rows in reg_rev.values():
        for _, cells in rows:
            digests = sha_in_row(cells)
            for fname in row_receipts(cells):
                blob = pins.get(fname)
                if blob is not None and hashlib.sha256(blob).hexdigest() in digests:
                    out[fname] = blob
            for fname in held_receipts(cells):
                blob = held_pins.get(fname)
                if blob is not None and hashlib.sha256(blob).hexdigest() in digests:
                    out[fname] = blob
    return out


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
            print("%s %s clause=c id=%s no_round49_pin" % (PRED, name, i))
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
            mode = ls_mode(repo, rev, FETCH + fname)
            if mode != "100644":
                print("%s %s clause=c id=%s pin_mode=%s:%s" % (PRED, name, i, fname, mode))
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
    """Every numbered step carries a quote that clause d verifies at its stated range.

    An in-range locator alone is not enough (w1/ExecControlsC2 bundle 14: a step locator
    pointed at the wrong line inside the pin and was admitted). A step is grounded when at
    least one backticked/double-quoted span of >= 2 words is immediately followed by a
    locator that resolves to a row-cited pin and the span occurs inside that pin at least
    once within [a,b].
    """
    by_base = pin_index(pins)
    steps = [(ln, l) for ln, l in enumerate(lines, 1) if re.match(r"^\d+\.\s", l)]
    ok = len(steps) >= 6
    if not ok:
        print("%s %s clause=e steps=%d <6" % (PRED, name, len(steps)))
    cited = 0
    for ln, l in steps:
        verified = 0
        uncited = []
        for m in QUOTE_RE.finditer(l):
            span = m.group(1) if m.group(1) is not None else m.group(2)
            token = m.group(3)
            q = norm_q(span)
            if len(q.split()) < 2:
                continue
            pint = resolve_pin(token.rsplit(":", 1)[0], pins, by_base)
            if pint is None:
                continue
            if pint not in cited_names:
                uncited.append(pint)
                continue
            rng = re.match(r".+:(\d+)(?:-(\d+))?$", token)
            a, b = int(rng.group(1)), int(rng.group(2) or rng.group(1))
            at = occurrences(pins[pint], q)
            if any(a <= x <= b for x in at):
                verified += 1
        if verified:
            cited += 1
        else:
            print("%s %s clause=e step_without_verified_quote line=%d uncited=%s" % (
                PRED, name, ln, uncited[:3]))
            ok = False
    print("%s %s clause=e steps=%d verified_steps=%d" % (PRED, name, len(steps), cited))
    return ok


def forms_in(text):
    """label -> set of ints stated next to the label.

    Both orders are read (`named=184` and `184 named`) but never mixed: the label-first
    reading wins when it states anything, so `binds=192 named=184` cannot also be read as
    `192 named`. A form whose two readings disagree in one order is a miss.
    """
    out = {}
    for label in FORMS:
        first = set()
        for m in re.finditer(r"(?<![A-Za-z0-9_])%s\s*[=:]\s*(\d+)\b" % label, text, re.I):
            first.add(int(m.group(1)))
        for m in re.finditer(r"(?<![A-Za-z0-9_])%s\s+(\d+)\b" % label, text, re.I):
            first.add(int(m.group(1)))
        last = set()
        for m in re.finditer(r"(?<![0-9])(\d+)\s+%s\b" % label, text, re.I):
            last.add(int(m.group(1)))
        out[label] = first if first else last
    return out


def total_in(text):
    """the bind total, only in an unambiguous form (`binds=<n>`, `binds (<n>)`, `<n> binds`)."""
    vals = set()
    for m in re.finditer(r"\bbinds\s*[=:]\s*(\d+)", text, re.I):
        vals.add(int(m.group(1)))
    for m in re.finditer(r"\bbinds\s*\(\s*(\d+)\s*\)", text, re.I):
        vals.add(int(m.group(1)))
    for m in re.finditer(r"(?<![0-9])(\d+)\s+binds\b", text, re.I):
        vals.add(int(m.group(1)))
    return vals


def digest_in(text):
    """raw-JSON digest stated on a sha256 line."""
    vals = set()
    for line in text.splitlines():
        if re.search(r"sha256", line, re.I):
            for d in HEX64_RE.findall(line):
                vals.add(d.lower())
    return vals


def resolve_in(text):
    """the quoted resolve_binds_by_sym value (int or set-bool)."""
    vals = set()
    for line in text.splitlines():
        if RESOLVE_OPTION not in line:
            continue
        m = re.search(r"\bint\s*[=:]?\s*(-?\d+)", line, re.I) \
            or re.search(r'"int"\s*:\s*(-?\d+)', line)
        if m:
            vals.add(int(m.group(1)))
            continue
        if re.search(r"\bset\s*[=:]?\s*(true|false)\b", line, re.I):
            vals.add(0 if re.search(r"false", line, re.I) else 1)
        elif re.search(r"\bfalse\b", line, re.I):
            vals.add(0)
        elif re.search(r"\btrue\b", line, re.I):
            vals.add(1)
    return vals


def version_ok(text):
    for line in text.splitlines():
        if HYPRLAND_VERSION.search(line) and HYPRLAND_COMMIT in line:
            return True
    return False


def clause_f(repo, rev, base, lines, name):
    """The live capture (hyprctl binds -j shape + getoption) answers the entry."""
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
        if len(blob) < MIN_RECEIPT or len(blob) > MAX_RECEIPT:
            print("%s %s clause=f receipt_size=%s:%d" % (PRED, name, path, len(blob)))
            continue
        text = blob.decode("utf-8", "replace")
        if not PROBE_CMD.search(text):
            print("%s %s clause=f receipt_no_hyprctl_binds=%s" % (PRED, name, path))
            continue
        if '"modmask"' in text or '"dispatcher"' in text:
            print("%s %s clause=f receipt_embeds_json=%s" % (PRED, name, path))
            continue
        if not version_ok(text):
            print("%s %s clause=f receipt_version_bad=%s" % (PRED, name, path))
            continue
        digests = digest_in(text)
        if len(digests) != 1:
            print("%s %s clause=f receipt_digest=%s:%s" % (PRED, name, path, sorted(digests)))
            continue
        digest = digests.pop()
        totals = total_in(text)
        if len(totals) != 1:
            print("%s %s clause=f receipt_total=%s:%s" % (PRED, name, path, sorted(totals)))
            continue
        total = totals.pop()
        fvals = forms_in(text)
        if any(len(v) != 1 for v in fvals.values()) or total <= 0:
            print("%s %s clause=f receipt_forms=%s:%s" % (
                PRED, name, path, {k: sorted(v) for k, v in fvals.items()}))
            continue
        if sum(next(iter(v)) for v in fvals.values()) != total:
            print("%s %s clause=f receipt_forms_sum=%s:%s!=%d" % (
                PRED, name, path, {k: next(iter(v)) for k, v in fvals.items()}, total))
            continue
        rvals = resolve_in(text)
        if rvals != {0}:
            print("%s %s clause=f receipt_resolve=%s:%s" % (PRED, name, path, sorted(rvals)))
            continue
        # the entry states the same values on unfenced lines; backticked spans are code (`code:10`,
        # `mouse:272` are key forms, not counts) and are blanked before the numbers are read (freeze fix:
        # the w1 draft read form labels inside code spans, so an entry quoting a bind form could not agree)
        prose = "\n".join(re.sub(r"`[^`\n]*`", " ", l) for l in lines)
        said_ver = version_ok("\n".join(lines))
        et = total_in(prose)
        said_total = et == {total}
        ef = forms_in(prose)
        said_forms = all(ef[k] == fvals[k] for k in FORMS)
        ed = digest_in("\n".join(lines))
        said_sha = any(d == digest or digest.startswith(d[:12])
                       for d in ed if len(d) >= 12)
        said_resolve = resolve_in(prose) == {0}
        if not (said_ver and said_total and said_forms and said_sha and said_resolve):
            print("%s %s clause=f entry_disagrees=%s ver=%d total=%s forms=%s sha=%d resolve=%d" % (
                PRED, name, path, said_ver, sorted(et), {k: sorted(ef[k]) for k in FORMS},
                said_sha, said_resolve))
            continue
        full_ok += 1
        print("%s %s clause=f receipt=%s binds=%d forms=%s sha=%s resolve=0" % (
            PRED, name, path, total, ",".join("%s:%d" % (k, next(iter(fvals[k]))) for k in FORMS),
            digest[:12]))
    if full_ok == 0:
        print("%s %s clause=f no_receipt_answers cited=%s" % (PRED, name, cand))
        return False
    return True


def clause_g(repo, rev, base, reg_rev, reg_base, held_pins, text, name):
    """Held S319 is cited and unchanged; no new row re-registers a held source."""
    ok = True
    cited = {}
    for i in HELD:
        a, b = reg_base.get(i), reg_rev.get(i)
        if not a or a != b:
            print("%s %s clause=g held_row_moved=%s" % (PRED, name, i))
            ok = False
            continue
        cells = b[0][1]
        digests = sha_in_row(cells)
        names = held_receipts(cells)
        if not names or not digests:
            print("%s %s clause=g held_row_unpinned=%s" % (PRED, name, i))
            ok = False
            continue
        for fname in names:
            blob = held_pins.get(fname)
            if blob is None:
                print("%s %s clause=g held_pin_missing=%s" % (PRED, name, fname))
                ok = False
                continue
            if hashlib.sha256(blob).hexdigest() not in digests:
                print("%s %s clause=g held_pin_sha_mismatch=%s" % (PRED, name, fname))
                ok = False
                continue
            cited[fname] = blob
    if not re.search(r"\b%s\b" % "|".join(HELD), text):
        print("%s %s clause=g held_not_cited=%s" % (PRED, name, ",".join(HELD)))
        ok = False
    held_urls = set()
    for i in HELD:
        for _, cells in reg_base.get(i, []):
            for u in URL_RE.findall(row_text(cells)):
                repo_n, ref, path, _ = url_ref_path(u)
                if repo_n and ref and path:
                    held_urls.add((repo_n, ref, path))
    if not held_urls:
        print("%s %s clause=g held_url_unreadable=%s" % (PRED, name, ",".join(HELD)))
        ok = False
    for i, rows in sorted(reg_rev.items()):
        if i in reg_base or int(i[1:]) < MIN_ID:
            continue
        for _, cells in rows:
            for u in URL_RE.findall(row_text(cells)):
                repo_n, ref, path, _ = url_ref_path(u)
                if (repo_n, ref, path) in held_urls:
                    print("%s %s clause=g re_registered_held_url=%s:%s" % (
                        PRED, name, i, u[:90]))
                    ok = False
    print("%s %s clause=g held=%s unchanged=%d pins=%d held_urls=%d" % (
        PRED, name, ",".join(HELD), int(ok), len(cited), len(held_urls)))
    return ok, cited


TOPICS = (
    ("state", "Hyprland-KeybindManager.cpp",
     r"m_resolveBindsBySym\s*\?\s*pKeyboard->m_xkbSymState\s*:\s*m_xkbTranslationState"),
    ("case", "Hyprland-KeybindManager.cpp", r"KBKEYLOWER\s*=\s*xkb_keysym_from_name\(.*XKB_KEYSYM_CASE_INSENSITIVE"),
    ("mask", "Hyprland-KeybindManager.cpp", r"modmask\s*!=\s*k->modmask\s*&&\s*!k->ignoreMods"),
    ("code-form", "Hyprland-legacy-ConfigManager.cpp", r"key\.starts_with\(\"code:\"\)"),
    ("zero-mod-sym-state", "Hyprland-IKeyboard.cpp",
     r"xkb_state_update_mask\(m_xkbSymState,\s*0,\s*0,\s*0,\s*0,\s*0,"),
    ("depressed-mask", "Hyprland-InputManager.cpp", r"m_lastMods\s*=\s*MODS\.depressed"),
    ("option-read", "Hyprland-InputManager.cpp",
     r"getDeviceInt\(devname,\s*\"resolve_binds_by_sym\",\s*\"input:resolve_binds_by_sym\"\)"),
)


def clause_j(pins, cited_names, lines, name):
    """Every TOPIC is answered by a numbered step quoting the pin at a line that carries it."""
    by_base = pin_index(pins)
    steps = [l for l in lines if re.match(r"^\d+\.\s", l)]
    ok = True
    for topic, pin_name, pattern in TOPICS:
        pint = resolve_pin(pin_name, pins, by_base)
        if pint is None or pint not in cited_names:
            print("%s %s clause=j topic=%s pin_missing=%s" % (PRED, name, topic, pin_name))
            ok = False
            continue
        text = pins[pint].decode("utf-8", "replace").splitlines()
        targets = {i for i, l in enumerate(text, 1) if re.search(pattern, l)}
        if not targets:
            print("%s %s clause=j topic=%s no_line_in_pin" % (PRED, name, topic))
            ok = False
            continue
        hit = None
        for l in steps:
            for m in QUOTE_RE.finditer(l):
                span = m.group(1) if m.group(1) is not None else m.group(2)
                token = m.group(3)
                q = norm_q(span)
                if len(q.split()) < 2 and len(q) < 8:
                    continue
                if resolve_pin(token.rsplit(":", 1)[0], pins, by_base) != pint:
                    continue
                rg = re.match(r".+:(\d+)(?:-(\d+))?$", token)
                a, b = int(rg.group(1)), int(rg.group(2) or rg.group(1))
                covered = [t for t in targets if a <= t <= b]
                if covered and any(a <= x <= b for x in occurrences(pins[pint], q)):
                    hit = covered[0]
                    break
            if hit:
                break
        if hit:
            print("%s %s clause=j topic=%s line=%d" % (PRED, name, topic, hit))
        else:
            print("%s %s clause=j topic=%s unanswered lines=%s" % (PRED, name, topic, sorted(targets)[:4]))
            ok = False
    return ok


def clause_h(lines, name):
    sec = section("\n".join(lines), "## Limits")
    bullets = [l for l in sec if re.match(r"^\s*[-*]\s+\S", l)]
    scoped = [l for l in bullets if SCOPE_WORD.search(l)]
    ok = len(bullets) >= 3 and len(scoped) >= 2
    if not ok:
        print("%s %s clause=h limits=%d bullets=%d scoped=%d" % (
            PRED, name, int(bool(sec)), len(bullets), len(scoped)))
    else:
        print("%s %s clause=h bullets=%d scoped=%d" % (PRED, name, len(bullets), len(scoped)))
    return ok


def shingles(text, n=6):
    """hashed word n-grams: the novelty probe's unit (order-preserving, cheap to compare)."""
    toks = re.findall(r"[a-z]{2,}", text.lower())
    return {hash(tuple(toks[k:k + n])) for k in range(len(toks) - n + 1)}


def base_grams(repo, base):
    """n-grams of the base tree's knowledge and lesson documents (bounded: 3 MiB, 256 KiB/file)."""
    out, total = set(), 0
    listing = git(repo, "ls-tree", "-r", "-l", base, "--", "corpus/knowledge", "corpus/lessons")
    for line in (listing or b"").decode("utf-8", "replace").splitlines():
        head, _, path = line.partition("\t")
        if not path.endswith(".md"):
            continue
        try:
            size = int(head.split()[3])
        except (IndexError, ValueError):
            continue
        if size > 262144:
            continue
        total += size
        if total > 3145728:
            break
        blob = show(repo, base, path)
        if blob:
            out |= shingles(blob.decode("utf-8", "replace"))
    return out


def body_text(lines):
    """unfenced prose for the novelty probe: no head provenance, no table rows."""
    return "\n".join(l for l in lines
                      if not l.startswith("|")
                      and not re.match(r"^(source|verified-at|recheck|ground):", l))


def clause_i(repo, rev, base, text, lines, reg_rev, reg_base, name):
    ok = True
    lesson = show(repo, rev, LESSON)
    new_ids = sorted(i for i in reg_rev if i not in reg_base and int(i[1:]) >= MIN_ID)
    if lesson is None:
        print("%s %s clause=i lesson_missing=%s" % (PRED, name, LESSON))
        ok = False
    else:
        gate = "\n".join(section(lesson.decode("utf-8", "replace"), "## Gate"))
        if not gate.strip():
            print("%s %s clause=i lesson_gate_empty" % (PRED, name))
            ok = False
        for i in new_ids:
            if not re.search(r"\*\*%s admit\*\*" % i, gate):
                print("%s %s clause=i gate_row_missing=%s" % (PRED, name, i))
                ok = False
    if not new_ids:
        print("%s %s clause=i no_new_rows" % (PRED, name))
        ok = False
    for i in new_ids:
        rows = reg_rev.get(i, [])
        if len(rows) != 1 or len(rows[0][1]) != 11:
            print("%s %s clause=i row_shape=%s:%d" % (PRED, name, i, len(rows)))
            ok = False
            continue
        used = rows[0][1][10]
        if ENTRY in used:
            continue
        paths = re.findall(r"[A-Za-z0-9._/-]+\.(?:md|py|json|txt|sh)", used)
        if not paths:
            print("%s %s clause=i row_unused=%s used_by=%r" % (PRED, name, i, used[:60]))
            ok = False
        elif not any(show(repo, rev, p) is not None and show(repo, base, p) is None
                     for p in paths):
            # ENTRY is new by clause a; a C1 tool or knowledge file is new this round. A row
            # whose only consumer is an already-held document is a minted row (w1 boundary 17).
            print("%s %s clause=i row_used_by_not_new=%s:%s" % (PRED, name, i, paths[:2]))
            ok = False
    present = 0
    for term in GROUND:
        rc = git_rc(repo, "grep", "-F", "-q", "-e", term, base, "--", "corpus")
        if rc != 1:
            print("%s %s clause=i ground_present_at_base=%s rc=%d" % (PRED, name, term, rc))
            ok = False
        if term in text or git_rc(repo, "grep", "-F", "-q", "-e", term, rev,
                                  "--", "corpus") == 0:
            present += 1
    if present < 2:
        print("%s %s clause=i ground_vacuous=%d/%d" % (PRED, name, present, len(GROUND)))
        ok = False
    body = [l.strip() for l in lines if len(l.strip()) >= 60 and not l.strip().startswith("|")]
    dup = 0
    for l in body[:40]:
        if git_rc(repo, "grep", "-F", "-q", "-e", l, base, "--", "corpus") == 0:
            dup += 1
    es = shingles(body_text(lines))
    bg = base_grams(repo, base)
    rate = len(es & bg) / len(es) if es else 1.0
    novel = len(es) >= 150 and rate < 0.15
    if len(body) < 8 or dup > 5 or not novel:
        print("%s %s clause=i novelty_body_lines=%d base_duplicates=%d grams=%d "
              "base_grams=%d overlap=%.3f" % (
                  PRED, name, len(body), dup, len(es), len(bg), rate))
        ok = False
    print("%s %s clause=i new_rows=%d gate=%d ground_present=%d/%d body=%d dup=%d "
          "overlap=%.3f" % (
              PRED, name, len(new_ids), int(lesson is not None), present, len(GROUND),
              len(body), dup, rate))
    return ok


def tmp_root():
    """A scratch root from TMPDIR; /tmp and an absent TMPDIR are refused (SentScratch)."""
    t = os.environ.get("TMPDIR")
    if not t:
        raise Setup("TMPDIR required for replay scratch")
    rp = os.path.realpath(t)
    if rp == "/tmp" or rp.startswith("/tmp/"):
        raise Setup("TMPDIR under /tmp refused: %s" % rp)
    if not os.path.isdir(rp):
        raise Setup("TMPDIR is not a directory: %s" % rp)
    return rp


def live_binds(k):
    """(sha256, total, {form: n}, resolve-int) from a read-only hyprctl run."""
    env = {"PATH": "/usr/bin", "LANG": "C.UTF-8"}
    for keep in ("XDG_RUNTIME_DIR", "HYPRLAND_INSTANCE_SIGNATURE"):
        if not os.environ.get(keep):
            raise Setup("%s required for the live replay" % keep)
        env[keep] = os.environ[keep]
    S = tempfile.mkdtemp(dir=tmp_root(), prefix="c2r-")
    try:
        for key in ("HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_DATA_HOME",
                    "XDG_STATE_HOME"):
            env[key] = os.path.join(S, key.lower())
            os.makedirs(env[key])
        p = subprocess.run([k, "binds", "-j"], capture_output=True, env=env, timeout=60)
        if p.returncode != 0:
            raise Setup("hyprctl binds -j rc=%d" % p.returncode)
        raw = p.stdout
        try:
            import json
            binds = json.loads(raw.decode("utf-8"))
        except ValueError:
            raise Setup("hyprctl binds -j is not JSON")
        forms = dict.fromkeys(FORMS, 0)
        for b in binds:
            key = b.get("key") or ""
            kc = b.get("keycode") or 0
            if isinstance(key, str) and key.startswith("code:"):
                forms["code"] += 1
            elif isinstance(key, str) and key.startswith("mouse"):
                forms["mouse"] += 1
            elif isinstance(key, str) and key.startswith("switch:"):
                forms["switch"] += 1
            elif key == "" and kc:
                # the bind table prints a keycode bind with an empty key field, so the keycode
                # is the only trace of a `code:` bind in `hyprctl binds -j` (a `code:` prefix in
                # the key field is the bind-line form, not the dump form)
                forms["code"] += 1
            else:
                forms["named"] += 1
        q = subprocess.run([k, "getoption", "input:" + RESOLVE_OPTION, "-j"],
                           capture_output=True, env=env, timeout=60)
        if q.returncode != 0:
            raise Setup("hyprctl getoption rc=%d" % q.returncode)
        rv = None
        for line in q.stdout.decode("utf-8", "replace").splitlines():
            m = re.search(r'"int"\s*:\s*(-?\d+)', line)
            if m:
                rv = int(m.group(1))
        if rv is None:
            raise Setup("getoption reply carries no int")
        return hashlib.sha256(raw).hexdigest(), len(binds), forms, rv
    finally:
        shutil.rmtree(S, ignore_errors=True)


def clause_r(repo, rev, lines, name):
    """Replay: re-run the receipted read-only hyprctl capture and compare (see docstring)."""
    k = "/usr/bin/hyprctl" if os.path.isfile("/usr/bin/hyprctl") else None
    if not k:
        raise Setup("hyprctl missing for replay")
    cand = []
    for l in lines:
        for path in RECEIPT_RE.findall(l):
            full = RECEIPTS + path
            if full not in cand:
                cand.append(full)
    for full in cand:
        blob = show(repo, rev, full)
        if blob is None or len(blob) < MIN_RECEIPT:
            continue
        text = blob.decode("utf-8", "replace")
        digests = digest_in(text)
        totals = total_in(text)
        fvals = forms_in(text)
        rvals = resolve_in(text)
        if len(digests) != 1 or len(totals) != 1 or rvals != {0} \
                or any(len(v) != 1 for v in fvals.values()):
            print("%s %s clause=r receipt_unparseable=%s" % (PRED, name, full))
            return False
        digest = digests.pop()
        total = totals.pop()
        want_forms = {k2: next(iter(v)) for k2, v in fvals.items()}
        got_digest, got_total, got_forms, got_resolve = live_binds(k)
        if got_digest != digest or got_total != total or got_forms != want_forms \
                or got_resolve != 0:
            print("%s %s clause=r replay_mismatch sha=%s/%s total=%d/%d forms=%s/%s resolve=%d" % (
                PRED, name, got_digest[:12], digest[:12], got_total, total,
                got_forms, want_forms, got_resolve))
            return False
        print("%s %s clause=r replay=ok sha=%s binds=%d forms=%s resolve=%d" % (
            PRED, name, digest[:12], total,
            ",".join("%s:%d" % (k2, want_forms[k2]) for k2 in FORMS), got_resolve))
        return True
    print("%s %s clause=r no_receipt_found" % (PRED, name))
    return False


def score(repo, rev, base, name):
    cl = dict.fromkeys("abcdefghir", 0)
    raw = show(repo, rev, ENTRY)
    text = raw.decode("utf-8", "replace") if raw is not None else ""
    lines = unfenced(text)
    cl["a"] = int(raw is not None)
    if not cl["a"]:
        print("%s %s clause=a entry_absent" % (PRED, name))
        global CLAUSES
        CLAUSES = "a:0"
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
    readme = (show(repo, rev, README) or b"").decode("utf-8", "replace")
    pat = re.compile(r"^\| `knowledge/%s`" % re.escape(os.path.basename(ENTRY)))
    frows = [l for l in unfenced(readme) if pat.match(l)]
    readme_ok = len(frows) == 1
    if readme_ok:
        row = frows[0]
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        readme_ok = len(cells) == 3
        if re.search(r"\b(supersed\w*|replac\w*|obsolet\w*|instead|deprecat\w*)\b", row, re.I):
            print("%s %s clause=b readme_redirect_word" % (PRED, name))
            readme_ok = False
        others = set(re.findall(r"knowledge/[A-Za-z0-9._-]+\.md", row)) - {
            "knowledge/" + os.path.basename(ENTRY)}
        if others:
            print("%s %s clause=b readme_names_other=%s" % (PRED, name, sorted(others)[:4]))
            readme_ok = False
        listed = set()
        for a, b in re.findall(r"S(\d{3,})(?:-S(\d{3,}))?",
                               cells[2] if len(cells) > 2 else ""):
            listed |= set("S%03d" % k for k in range(int(a), int(b or a) + 1))
        if not set(ids) <= listed:
            print("%s %s clause=b readme_missing_ids=%s" % (
                PRED, name, sorted(set(ids) - listed)))
            readme_ok = False
    else:
        print("%s %s clause=b readme_rows=%d" % (PRED, name, len(frows)))
    cl["b"] = int(rows_ok and len(ids) >= MIN_SOURCES and va == OPENED
                  and recheck_ok(rc) and outside == 0 and readme_ok)
    print("%s %s clause=b ids=%d outside_head=%d verified=%s recheck=%s readme=%d ok=%d" % (
        PRED, name, len(ids), outside, va, (rc or "")[:10], int(readme_ok), cl["b"]))
    pins = fetch_pins(repo, rev, FETCH)
    if not pins:
        print("%s %s clause=c fetch_pins=0 under %s" % (PRED, name, FETCH))
        CLAUSES = "a:1 c:0"
        return 0
    held_pins = fetch_pins(repo, rev, HELD_FETCH)
    all_pins = dict(held_pins)
    all_pins.update(pins)
    by_base = pin_index(all_pins)
    c_ok, head_pins = clause_c(repo, rev, ids, reg_rev, pins, pin_index(pins), name)
    cl["c"] = int(c_ok)
    g_ok, held_cited = clause_g(repo, rev, base, reg_rev, reg_base, held_pins, text, name)
    cl["g"] = int(g_ok)
    bound = bound_pins(reg_rev, pins, held_pins)
    cited_names = set(head_pins) | set(held_cited) | set(bound)
    cl["d"] = int(clause_d(all_pins, by_base, cited_names,
                           set(head_pins.values()) | set(held_cited.values())
                           | set(bound.values()), lines, name))
    print("%s %s clause=d ground_pins=%d bound_extra=%d" % (
        PRED, name, len(cited_names), len(set(bound) - set(head_pins) - set(held_cited))))
    cl["e"] = int(clause_e(all_pins, cited_names, lines, name))
    cl["j"] = int(clause_j(all_pins, cited_names, lines, name))
    cl["f"] = int(clause_f(repo, rev, base, lines, name))
    cl["h"] = int(clause_h(lines, name))
    cl["i"] = int(clause_i(repo, rev, base, text, lines, reg_rev, reg_base, name))
    cl["r"] = int(clause_r(repo, rev, lines, name))
    admitted = int(all(cl.values()))
    CLAUSES = " ".join("%s:%d" % kv for kv in sorted(cl.items()))
    print("%s %s clauses=%s admitted=%d" % (PRED, name, CLAUSES, admitted))
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
    print("%s: clauses=%s admitted=%d/1 verdict=%s rev=%s" % (
        PRED, CLAUSES, n, "TARGET_MET" if met else "TARGET_MISSED", rev))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as exc:
        print("%s SETUP %s" % (PRED, exc))
        sys.exit(2)
