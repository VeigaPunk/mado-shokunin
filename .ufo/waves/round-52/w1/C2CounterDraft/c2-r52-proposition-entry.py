#!/usr/bin/env python3
"""PRED-C2-r52 (DRAFT, seat C2CounterDraft) - a proposition-bound dispatcher knowledge entry.

Frozen claim (`.ufo/waves/round-52/claims-frozen.md`, C2) and registration
(`.ufo/waves/round-52/registration.md`, "C2 - coverage"), restated:

    one new indexed entry on a distinct Hyprland dispatcher-execution mechanism, holding at
    least four substantive propositions; each proposition maps to an opened-this-round `S###`
    registry row, a pin path/revision and an exact located quote of at most 25 words, with a
    written support rationale; every material factual proposition is mapped.

This counter checks the *structure* of that mapping and nothing else.  It does NOT decide whether
a quote entails the proposition it is attached to: entailment is a judgement for an outside
non-author reviewer, and the final line says so.  What it decides, mechanically:

    TMPDIR=<scratch> python3 -I c2-r52-proposition-entry.py --repo <lane> --rev <rev> \
        [--entry corpus/knowledge/<name>.md] [--fetch-root .ufo/waves/round-52] \
        [--work <scratch>]
    exits 0 with final line
        C2_R52: clauses=abcde clauses_met=5 admitted=1/1 verdict=TARGET_MET rev=<sha>
    iff at <rev>:
      (a) the target entry exists and an unfenced row of corpus/README.md indexes it;
      (b) it declares >=4 propositions, each with a claim, a source row, a pin locator, a quote
          and a written support rationale, with distinct ids and distinct claims;
      (c) every proposition's `S###` row exists in the corpus/SOURCES.md registry at <rev>, is
          `mined`, carries this round's access date, is absent from the registry at the frozen
          base (so it was opened this round), and its anchor cell names the proposition's pin
          under the round's fetch root together with a 40-hex revision, and its `used-by` cell
          names this entry;
      (d) every proposition's pin resolves to a file that exists at <rev> under the round's
          fetch root, and the proposition's quote (3..25 words) appears verbatim,
          whitespace-collapsed, inside the pin's *cited line span*; when the entry carries a
          pin manifest, the manifest must declare the pin and, if it names rows, the cited row;
      (e) the mapping is complete: every registry row this entry opened is mapped by a
          proposition, every proposition's row is cited by the entry, every proposition id is
          drawn on outside the map, no two propositions share a quote or a claim, and the
          propositions stand on at least two distinct rows.
    At the frozen base the target entry is absent and the command prints
    `admitted=0/1 verdict=TARGET_MISSED` and exits 1.

Citation grammar this counter accepts (documented so a draft entry can be written against it):

  proposition map - a markdown table with these columns, in any order and with any of these
      header spellings (a trailing parenthetical is ignored, so `quote (<=25 words)` is the
      quote column):
        id       - `id`, `prop`, `proposition id`       (optional; synthesized `P1..Pn` when
                                                            absent)
        claim    - `claim`, `proposition`, `statement`, `fact`
        row      - `row`, `source row`, `s-row`, `registry row`
        pin      - `pin`, `pin path`, `locator`, `source pin`, `pin:anchor`
        quote    - `quote`, `quoted`, `quoted text`
        support  - a rationale column (`why`, `why it supports`, `rationale`, `justification`,
                    `reason`) outranks a support-class column (`support`, `support class`);
                    the support-class column alone is too thin to be a rationale.
      One data row is one proposition; a header cell may not serve two roles.
      The alternative block form is also accepted: a line that is only a proposition id (`P1`),
      followed by `claim:`, `row:`, `pin:`, `quote:` and `support:` lines.
  pin cell         - `<pin-name>:<first>` or `<pin-name>:<first>-<last>`, optionally followed by
                      `@ <revision>`.  The name may be a bare file name or a path (only the
                      basename binds).  A bare `:123` cell continues the previous proposition's
                      pin, which is the house shorthand for "same file, other line".  A
                      shortened name (`legacy-DispatcherTranslator.cpp`) resolves to the staged
                      file when exactly one file under the fetch root ends with it.
  quote cell       - the quoted text; surrounding backticks or quotes are stripped and the text
                      is compared whitespace-collapsed against the pin's cited line span.  The
                      comparison policy is frozen and printed on every run
                      (`quote_policy=whitespace-collapsed`); the byte-exact count is reported
                      next to it (`quotes_raw=N/M`), so a reader can see how many quotes would
                      bind under the stricter reading and whether the verdict depends on it.
                      A `|` inside a cell must be written `\\|`, or the cell splits (a literal
                      backslash-pipe; markdown's own escape).
  cited rows       - the `S###` ids named on the entry's unfenced prose lines, except the
                      `held`/`ground`/`lane`/`recheck`/`verified-at` marker lines, which are
                      ground and housekeeping rather than claims of this entry.

Thresholds not named by the frozen sentence, and why: MIN_PROPS=4 is the sentence's "at least
four"; MAX_QUOTE_WORDS=25 is the sentence's quote cap; MIN_QUOTE_WORDS=3 (identifier tokens)
keeps a bare token from "binding" a pin line; MIN_DISTINCT_ROWS=2 keeps four propositions from
resting on one row; ACCESS_DATE is the round's access date; the fetch root and the frozen base
are the round's own.

Exit codes: 0 = 5/5 clauses; 1 = at least one clause missed; 2 = setup error (bad repo/rev, the
base commit missing, the base already holding the target entry, unusable scratch).  Scratch: the
`--work` directory, else a `mkdtemp` under `$TMPDIR`; a scratch path inside the scored repository
is refused before anything is created.  Nothing outside the scratch dir is written.

This file is a seat draft under `.ufo/waves/round-52/w1/C2CounterDraft/`; it is not committed and
has not been copied to `quality/counters/`.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

PRED = "PRED-C2-r52"
# The target slug this draft counter names.  Deliberately distinct from the round-51 entry
# `hyprland-dispatcher-dispatch-r51.md`; the entry seat's final path may be passed with
# `--entry`, and integration should set this constant to the landed path.
ENTRY_DEFAULT = "corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md"
R51_ENTRY_NAME = "hyprland-dispatcher-dispatch-r51.md"
REGISTRY = "corpus/SOURCES.md"
README = "corpus/README.md"
FETCH_ROOT_DEFAULT = ".ufo/waves/round-52"
BASE = "85d57a818c3707397e21c840b6498b105ba798aa"
ACCESS_DATE = "2026-10-27"
MIN_PROPS = 4
MIN_DISTINCT_ROWS = 2
MAX_QUOTE_WORDS = 25
MIN_QUOTE_WORDS = 3
# The one quote-comparison policy this counter freezes, printed on every run so a reader never
# has to guess which reading produced the verdict.  Whitespace-collapsed is the binding policy:
# a quote reflowed by markdown is still the same quote.  The raw, byte-exact count is reported
# alongside it as `quotes_raw=N/M`, because the choice is decision-relevant - a verdict that
# would flip on the policy must show both numbers rather than hide behind one.
QUOTE_POLICY = "whitespace-collapsed"

ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ROW_RE = re.compile(r"^S\d{3,}$")
ROW_IN_TEXT_RE = re.compile(r"\b(S\d{3,})\b")
HEX40_RE = re.compile(r"\b([0-9a-f]{40})\b")
ID_COLS = ("id", "prop", "proposition id", "proposition no")
CLAIM_COLS = ("claim", "proposition", "statement", "fact")
ROW_COLS = ("row", "source row", "s-row", "registry row", "registry-row")
PIN_COLS = ("pin", "pin path", "locator", "source pin", "pin:anchor", "pin anchor")
QUOTE_COLS = ("quote", "quoted", "quoted text")
# Two tiers: a rationale column ("why …") outranks a support-class column ("support", whose
# cells are one-word labels), so a table carrying both binds the rationale.
SUPPORT_TIER1 = ("why", "rationale", "justification", "reason", "support rationale",
                 "why it supports", "how it supports")
SUPPORT_TIER2 = ("support", "support class", "support rationale")
ROLES = ("id", "claim", "row", "pin", "quote", "support")
BLOCK_ID_RE = re.compile(r"^\**\s*(P\d+)\s*\**\s*:?\s*$")
BLOCK_KEY_RE = re.compile(r"^\s*([a-z][a-z \-]*)\s*:\s*(.+?)\s*$", re.I)
MARKER_RE = re.compile(r"^\s*(held|ground|lane|round|wave|base|verified-at|recheck|recheck)\b", re.I)


class Setup(Exception):
    pass


# ------------------------------------------------------------------ git helpers

def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV)
    return p.stdout if p.returncode == 0 else None


def git_rc(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          env=ENV).returncode


def show(repo, rev, path):
    return git(repo, "show", "%s:%s" % (rev, path))


def ls_files(repo, rev, path):
    out = git(repo, "ls-tree", "-r", "--name-only", rev, "--", path)
    return out.decode().splitlines() if out else []


def text_of(blob):
    return blob.decode("utf-8", "replace") if blob else ""


def resolve_rev(repo, rev):
    out = git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    if not out:
        raise Setup("rev does not resolve to a commit: %r" % rev)
    return out.decode().strip()


# ------------------------------------------------------------------ text helpers

def collapse(s):
    return re.sub(r"\s+", " ", s or "").strip()


def unfenced(lines):
    out, fenced = [], False
    for line in lines:
        s = line.strip()
        if s.startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return out


def cells_of(row):
    """Split a markdown table row on unescaped pipes; `\\|` stays inside its cell."""
    s = row.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    out, cur, esc = [], "", False
    for ch in s:
        if esc:
            cur += ch
            esc = False
            continue
        if ch == "\\":
            cur += ch
            esc = True
            continue
        if ch == "|":
            out.append(cur.strip())
            cur = ""
            continue
        cur += ch
    out.append(cur.strip())
    return out


def is_rule(cells):
    return all(re.fullmatch(r":?-{2,}:?", c or "") for c in cells) if cells else False


def tables(lines):
    """Consecutive markdown table blocks: [(header cells, [row cells, ...]), ...]."""
    out, cur = [], []
    for line in unfenced(lines):
        if line.strip().startswith("|"):
            cur.append(line.strip())
            continue
        if len(cur) >= 2:
            out.append(cur)
        cur = []
    if len(cur) >= 2:
        out.append(cur)
    for block in out:
        cells = [cells_of(r) for r in block]
        yield cells[0], [c for c in cells[1:] if not is_rule(c)]


def clean(cell):
    """Strip backticks, stars and whitespace from a cell but keep its case."""
    return re.sub(r"[`*\s]+", "", cell or "")


def strip_wrap(cell):
    """Strip wrapping backticks / quotes from a cell and unescape `\\|`."""
    s = (cell or "").strip()
    for _ in range(2):
        if len(s) >= 2 and s[0] == s[-1] and s[0] in "`\"'":
            s = s[1:-1].strip()
    return s.replace("\\|", "|")


def words(s):
    """Whitespace words: the plain reading of the sentence's "at most 25 words"."""
    return collapse(s).split()


def tokens(s):
    """Identifier/number tokens: the reading used for the minimum-quote-length floor, so a
    one-token code fragment cannot bind a pin line."""
    return re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+", s or "")


def key(s):
    """A comparison key for claim/quote identity: casefolded, punctuation-free."""
    return re.sub(r"[^a-z0-9]+", " ", collapse(s).lower()).strip()


# ------------------------------------------------------------------ registry

def registry(text):
    """S-id -> {column: value} for the SOURCES.md registry table."""
    rows, header = {}, None
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = cells_of(s)
        low = [c.lower() for c in cells]
        if header is None:
            if low and low[0] == "id" and "status" in low and "opened" in low:
                header = low
            continue
        if is_rule(cells) or not cells:
            continue
        m = ROW_RE.match(clean(cells[0]))
        if not m:
            continue
        row = dict(zip(header, cells))
        row["_cells"] = cells
        row["_line"] = s
        rows[m.group(0)] = row
    if header is None:
        raise Setup("registry header (id|source|...|status|opened|...) not found")
    return rows


# ------------------------------------------------------------------ proposition map

def norm(cell):
    """Normalise a table cell to a comparable key: no backticks, stars, case, spacing.

    A trailing parenthetical is dropped (`quote (<=25 words)` -> `quote`), so a header that
    documents its own constraint still names its role.
    """
    s = re.sub(r"\s+", " ", re.sub(r"[`*\s]", "", cell or "")).strip().lower()
    s = re.sub(r"\s*\([^)]*\)\s*$", "", s).strip()
    return s


def hkey(cell):
    """A header cell as a comparison key: no backticks or stars, casefolded, whitespace
    collapsed to nothing, and any trailing parenthetical dropped.

    `quote (<=25 words)` -> `quote`; `support class` -> `supportclass`; `why it supports` ->
    `whyitsupports`.
    """
    s = re.sub(r"[`*\s]+", "", cell or "").strip().lower()
    s = re.sub(r"\([^)]*\)$", "", s).strip()
    return s


def assign_columns(header):
    """Map role -> column index, no header cell serving two roles.

    `id` is optional; every other role is required.  The assignment is a small backtracking
    search so a header like `| proposition | claim | … |` does not collide on the word
    "proposition" - the id column takes it and the claim column takes `claim`.
    """
    low = [hkey(c) for c in header]
    names = {"id": ID_COLS, "claim": CLAIM_COLS, "row": ROW_COLS, "pin": PIN_COLS,
             "quote": QUOTE_COLS}
    squashed = {role: {hkey(a) for a in aliases} for role, aliases in names.items()}
    cands = {role: [i for i, c in enumerate(low) if c in squashed[role]] for role in ROLES
             if role != "support"}
    # The support role is two-tiered: a rationale column outranks a support-class column.
    t1 = {hkey(a) for a in SUPPORT_TIER1}
    t2 = {hkey(a) for a in SUPPORT_TIER2}
    cands["support"] = [i for i, c in enumerate(low) if c in t1]
    if not cands["support"]:
        cands["support"] = [i for i, c in enumerate(low) if c in t2]
    required = [r for r in ROLES if r != "id"]
    for role in required:
        if not cands[role]:
            return None, True
    order = required + ["id"]
    best = {}

    def solve(i, used, out):
        if i == len(order):
            best.clear()
            best.update(out)
            return True
        role = order[i]
        for c in cands[role]:
            if c in used:
                continue
            used.add(c)
            out[role] = c
            if solve(i + 1, used, out):
                return True
            used.discard(c)
            out.pop(role, None)
        return False

    if not solve(0, set(), {}):
        return None, True
    return best, False


def proposition_table(lines):
    """(records, notes): the proposition map from the table form or the block form."""
    out, notes = [], []
    for header, rows in tables(lines):
        idx, conflict = assign_columns(header)
        if conflict or any(r not in idx for r in ("claim", "row", "pin", "quote", "support")):
            continue
        for n, cells in enumerate(rows, 1):
            rec = {"_form": "table"}
            for role in ROLES:
                i = idx.get(role)
                rec[role] = strip_wrap(cells[i]) if i is not None and i < len(cells) else ""
            if not rec["id"]:
                rec["id"] = "P%d" % n
            out.append(rec)
    if out:
        return out, notes
    cur, block = None, {}
    for line in unfenced(lines):
        m = BLOCK_ID_RE.match(line.strip())
        if m:
            if cur:
                cur.update(block)
                out.append(cur)
            cur, block = {"id": m.group(1), "_form": "block"}, {}
            continue
        if cur is None:
            continue
        km = BLOCK_KEY_RE.match(line)
        if km:
            k = hkey(km.group(1))
            for role, aliases in (("claim", CLAIM_COLS), ("row", ROW_COLS), ("pin", PIN_COLS),
                                  ("quote", QUOTE_COLS), ("support", SUPPORT_TIER1),
                                  ("support", SUPPORT_TIER2)):
                if k in {hkey(a) for a in aliases}:
                    block[role] = strip_wrap(km.group(2))
                    break
    if cur:
        cur.update(block)
        out.append(cur)
    return out, notes


def pin_manifest(lines):
    """pin name -> {"file": ..., "row": ...}, from every table whose first header cell starts
    with `pin`.  Names are kept as written and lower-cased, so a lookup never depends on case."""
    out = {}
    for header, rows in tables(lines):
        if not header or not norm(header[0]).startswith("pin"):
            continue
        fidx = next((i for i, c in enumerate(header)
                     if norm(c) in ("file", "upstream file", "path")), None)
        ridx = next((i for i, c in enumerate(header)
                     if norm(c) in ("row", "rows", "s-row", "srow", "source row",
                                    "registry row", "sid")), None)
        for cells in rows:
            if not cells:
                continue
            name = strip_wrap(cells[0])
            if not name:
                continue
            out[name] = {
                "file": strip_wrap(cells[fidx]) if fidx is not None and fidx < len(cells) else "",
                "row": strip_wrap(cells[ridx]) if ridx is not None and ridx < len(cells) else "",
            }
            out[name.lower()] = out[name]
    return out


def parse_pin_cell(cell, prev_pin=None):
    """(pin name, first, last, revision) from `<pin>:<first>[-<last>][@ rev]`.

    The pin cell may carry a full path (`…/fetch/Hyprland-KeybindManager.cpp:113`); only the
    basename is the pin name.  A bare `:123` cell continues the previous proposition's pin,
    which is the house shorthand for "same file, other line".
    """
    s = collapse(cell)
    rev = ""
    m = HEX40_RE.search(s)
    if m:
        rev = m.group(1)
        s = (s[:m.start()] + " " + s[m.end():])
    m = re.search(r"([A-Za-z0-9._/-]*[A-Za-z0-9._-]+)?:(\d+)(?:-(\d+))?", s)
    if not m:
        return None
    name = (m.group(1) or "").rsplit("/", 1)[-1]
    if not name:
        # a bare `:123` continues the previous proposition's pin
        if prev_pin is None:
            return None
        name = prev_pin
    first = int(m.group(2))
    last = int(m.group(3)) if m.group(3) else first
    return name, first, last, rev


# ------------------------------------------------------------------ clause (a)

def index_row(readme_text, name):
    """The README index row that names the entry, or None.

    The row may sit in any table of the README (the coverage map, the round-notes table), so
    every table row of every table block is scanned, not just the first column.
    """
    needle = "knowledge/%s" % name
    for header, rows in tables(readme_text.splitlines()):
        for cells in rows:
            if any(needle in (cell or "") for cell in cells):
                return collapse(cells[0] if cells else "")
    for line in readme_text.splitlines():
        s = line.strip()
        if s.startswith("|") and needle in s:
            return collapse(cells_of(s)[0] if cells_of(s) else "")
    return None


def clause_a(repo, rev, entry_path, entry_name):
    entry = show(repo, rev, entry_path)
    if entry is None:
        return 0, "entry=absent"
    readme = show(repo, rev, README)
    if readme is None:
        return 0, "readme=absent"
    row = index_row(text_of(readme), entry_name)
    if not row:
        return 0, "index_row=absent"
    return 1, "index_row=%s" % (row[:57] + "..." if len(row) > 60 else row)


# ------------------------------------------------------------------ clause (b)

def clause_b(entry_text):
    recs, _notes = proposition_table(entry_text.splitlines())
    if len(recs) < MIN_PROPS:
        return 0, "propositions=%d<%d" % (len(recs), MIN_PROPS), recs
    ids, bad, claims = [], [], []
    for rec in recs:
        pid = collapse(rec.get("id", ""))
        ids.append(pid)
        missing = [k for k in ("claim", "row", "pin", "quote", "support")
                   if not collapse(rec.get(k, ""))]
        if missing:
            bad.append("%s:empty(%s)" % (pid or "?", ",".join(missing)))
        rowid = collapse(rec.get("row", ""))
        if not ROW_RE.match(rowid):
            bad.append("%s:row_malformed(%s)" % (pid or "?", rowid))
        if len(tokens(rec.get("support", ""))) < 4:
            bad.append("%s:support_thin" % (pid or "?"))
        claims.append(key(rec.get("claim", "")))
    for value, label in ((ids, "id"), (claims, "claim")):
        dupes = sorted({v for v in value if v and value.count(v) > 1})
        if dupes:
            bad.append("duplicate_%s:%s" % (label, ",".join(dupes[:3])))
    detail = "propositions=%d ids=%d forms=%s" % (
        len(recs), len(set(ids)), ",".join(sorted({r.get("_form", "?") for r in recs})))
    if bad:
        detail += " miss=" + ",".join(bad[:4])
    return (1 if not bad else 0), detail, recs


# ------------------------------------------------------------------ clause (c)

def clause_c(repo, rev, entry_name, recs, fetch_root):
    """Each proposition's row: exists, mined, opened this round, pin path, revision, used-by."""
    reg_text = show(repo, rev, REGISTRY)
    if reg_text is None:
        return 0, "registry=absent"
    rows = registry(text_of(reg_text))
    base_text = show(repo, BASE, REGISTRY)
    base_rows = registry(text_of(base_text)) if base_text else {}
    notes, ok_rows = [], set()
    prev_pin = None
    for rec in recs:
        pid = collapse(rec.get("id", ""))
        rowid = collapse(rec.get("row", ""))
        parsed = parse_pin_cell(rec.get("pin", ""), prev_pin)
        pin = parsed[0] if parsed else ""
        if parsed:
            prev_pin = parsed[0]
        row = rows.get(rowid)
        if row is None:
            notes.append("%s:row_absent(%s)" % (pid, rowid))
            continue
        status = norm(row.get("status", ""))
        if status != "mined":
            notes.append("%s:status(%s)" % (pid, status or "-"))
            continue
        opened = norm(row.get("opened", ""))
        if opened != ACCESS_DATE:
            notes.append("%s:opened(%s)" % (pid, opened or "-"))
            continue
        if rowid in base_rows:
            notes.append("%s:row_not_new(%s)" % (pid, rowid))
            continue
        anchor = row.get("anchor", "") or row.get("_line", "")
        if fetch_root not in anchor:
            notes.append("%s:anchor_no_fetch_root" % pid)
            continue
        if pin and not (pin in anchor or any(pin in a for a in anchor.split())):
            notes.append("%s:anchor_no_pin(%s)" % (pid, pin))
            continue
        if not HEX40_RE.search(anchor):
            notes.append("%s:anchor_no_revision" % pid)
            continue
        used = norm(row.get("used-by", "")) + " " + norm(row.get("used by", ""))
        if entry_name not in used:
            notes.append("%s:used_by(%s)" % (pid, used or "-"))
            continue
        ok_rows.add(rowid)
    detail = "rows_bound=%d/%d distinct_rows=%d" % (len(ok_rows), len(recs), len(ok_rows))
    if notes:
        detail += " miss=" + ",".join(notes[:4])
    return (1 if not notes and ok_rows else 0), detail


# ------------------------------------------------------------------ clause (d)

def pin_index(repo, rev, fetch_root):
    """Basename -> repo path, for every file under the round's fetch root.

    The root is a prefix, not a fixed directory: a seat may stage its pins under
    `.ufo/waves/round-52/w1/<seat>/fetch/`.  A basename that appears more than once is
    dropped, so an ambiguous name can never be silently bound to one of several files.
    """
    out = {}
    for path in ls_files(repo, rev, fetch_root):
        base = path.rsplit("/", 1)[-1]
        if base in out:
            out[base] = None          # ambiguous: two files with the same basename
        else:
            out[base] = path
    return out


def resolve_pin_file(pin, index):
    """The repo path of the pinned file: exact basename, else a unique suffix match.

    A shortened pin name (`legacy-DispatcherTranslator.cpp`) resolves to the staged file
    (`Hyprland-legacy-DispatcherTranslator.cpp`) when exactly one file's basename ends with it.
    """
    if pin in index:
        return index[pin]
    hits = [p for base, p in index.items() if p and base.endswith(pin)]
    if len(hits) == 1:
        return hits[0]
    return None


def prior_equal_pins(repo, rev, pin_names, fetch_root):
    """The bound pins whose bytes are byte-identical to a pin staged in an earlier round.

    A new registry row can still point at bytes that were already on disk; this reports how
    many of the bound pins are byte-equal to a prior round's copy, so a reviewer can see it.
    It is a diagnostic, not a gate: reopening a pinned file under a new row is legitimate when
    the scope is new, and the row's own freshness is checked by clause (c).
    """
    if not pin_names:
        return set()
    import hashlib
    base_files = [p for p in ls_files(repo, BASE, ".ufo/waves")
                  if "/fetch/" in p and p.rsplit("/", 1)[-1] in pin_names]
    if not base_files:
        return set()
    prior = {}
    for path in base_files:
        blob = show(repo, BASE, path)
        if blob is None:
            continue
        prior.setdefault(path.rsplit("/", 1)[-1], set()).add(
            hashlib.sha256(blob).hexdigest())
    index = pin_index(repo, rev, fetch_root)
    out = set()
    for name in pin_names:
        path = resolve_pin_file(name, index)
        if path is None:
            continue
        blob = show(repo, rev, path)
        if blob is None:
            continue
        if hashlib.sha256(blob).hexdigest() in prior.get(name, ()):
            out.add(name)
    return out


def clause_d(repo, rev, entry_text, recs, fetch_root):
    """Each proposition's pinned file, and verbatim quote at the cited line.

    The pin manifest is optional: when the entry carries one (`| pin | … |`), the manifest
    must declare the proposition's pin and, if it names rows, the cited row must be among
    them.  When the entry carries none, the pin is bound to the file alone.
    """
    man = pin_manifest(entry_text.splitlines())
    index = pin_index(repo, rev, fetch_root)
    notes, bound, raw_ok = [], {}, {}
    prev_pin = None
    for rec in recs:
        pid = collapse(rec.get("id", ""))
        parsed = parse_pin_cell(rec.get("pin", ""), prev_pin)
        if parsed is None:
            notes.append("%s:pin_malformed(%s)" % (pid, collapse(rec.get("pin", ""))))
            continue
        pin, first, last, rev_tok = parsed
        prev_pin = pin
        if man:
            if pin.lower() not in man:
                notes.append("%s:pin_not_manifested(%s)" % (pid, pin))
                continue
            man_rows = {m.group(1)
                        for m in ROW_IN_TEXT_RE.finditer(man[pin.lower()].get("row", ""))}
            prop_row = collapse(rec.get("row", ""))
            if man_rows and prop_row and prop_row not in man_rows:
                notes.append("%s:manifest_row_mismatch(%s!=%s)"
                             % (pid, prop_row, ",".join(sorted(man_rows))))
        path = resolve_pin_file(pin, index)
        if path is None:
            notes.append("%s:pin_file_absent(%s)" % (pid, pin))
            continue
        blob = show(repo, rev, path)
        if blob is None:
            notes.append("%s:pin_file_absent(%s)" % (pid, pin))
            continue
        lines = text_of(blob).splitlines()
        if first < 1 or first > len(lines):
            notes.append("%s:pin_line_out_of_range(%s:%d)" % (pid, pin, first))
            continue
        span = "\n".join(lines[first - 1:min(last, len(lines))])
        quote = strip_wrap(rec.get("quote", ""))
        if not quote:
            notes.append("%s:quote_empty" % pid)
            continue
        nw = len(words(quote))
        if nw > MAX_QUOTE_WORDS:
            notes.append("%s:quote_too_long(%d)" % (pid, nw))
            continue
        nt = len(tokens(quote))
        if nt < MIN_QUOTE_WORDS:
            notes.append("%s:quote_too_short(%d)" % (pid, nt))
            continue
        if collapse(quote) not in collapse(span):
            notes.append("%s:quote_not_at_pin(%s:%d)" % (pid, pin, first))
            continue
        if quote.strip() not in span:
            raw_ok[pid] = False
        bound[pid] = (pin, first, last, quote)
    detail = "quotes_bound=%d/%d quotes_raw=%d/%d pins=%d policy=%s" % (
        len(bound), len(recs), len(bound) - len(raw_ok), len(bound),
        len({v[0] for v in bound.values()}), QUOTE_POLICY)
    prior = prior_equal_pins(repo, rev, {v[0] for v in bound.values()}, fetch_root)
    if prior:
        detail += " pins_prior_equal=%d/%d" % (len(prior), len(bound))
    if notes:
        detail += " miss=" + ",".join(notes[:4])
    return (1 if not notes and bound else 0), detail, bound


# ------------------------------------------------------------------ clause (e)

def prose_text(entry_text):
    """The entry's prose, with the proposition map and the pin manifest removed: the sentences
    that carry the claims, as opposed to the tables that index them."""
    out = []
    for line in unfenced(entry_text.splitlines()):
        s = line.strip()
        if s.startswith("|"):
            continue
        out.append(s)
    return collapse(" ".join(out))


def referenced_ids(entry_text):
    """The proposition ids the entry draws on outside the proposition map itself.

    An id that appears only in its own map row is not drawn on.  A range (`P08-P11`) counts
    for every id inside it.  The scan covers the whole entry, tables included: the "what the
    evidence licenses" table is where an entry names the propositions its sentences rest on.
    """
    from collections import Counter
    text = collapse(entry_text)
    counts = Counter(re.findall(r"\bP\d+\b", text))
    out = {p for p, n in counts.items() if n >= 2}
    for lo, hi in re.findall(r"\bP(\d+)\s*-\s*P(\d+)\b", text):
        width = max(len(lo), len(hi))
        for n in range(int(lo), int(hi) + 1):
            out.add("P" + str(n).zfill(width))
    return out


def cited_rows(entry_text, man):
    """S-ids the entry claims on prose lines, plus the rows its pin manifest declares."""
    prose, table = set(), set()
    for line in unfenced(entry_text.splitlines()):
        s = line.strip()
        if s.startswith("|"):
            continue
        if MARKER_RE.match(s):
            continue
        for m in ROW_IN_TEXT_RE.finditer(line):
            prose.add(m.group(1))
    for spec in man.values():
        for m in ROW_IN_TEXT_RE.finditer(spec.get("row", "")):
            table.add(m.group(1))
    return prose, table


def registry_state(repo, rev):
    """(rows at rev, rows at the frozen base, rows opened this round)."""
    reg_text = show(repo, rev, REGISTRY)
    if reg_text is None:
        raise Setup("registry=absent")
    rows = registry(text_of(reg_text))
    base_text = show(repo, BASE, REGISTRY)
    base_rows = registry(text_of(base_text)) if base_text else {}
    fresh = set()
    for rowid, row in rows.items():
        if rowid in base_rows:
            continue
        if norm(row.get("status", "")) != "mined":
            continue
        if norm(row.get("opened", "")) != ACCESS_DATE:
            continue
        fresh.add(rowid)
    return rows, base_rows, fresh


def clause_e(entry_text, recs, bound, man, rows, fresh):
    """Completeness of the mapping: no unmapped claim row, no orphan proposition, no padding.

    `fresh` is the set of registry rows opened this round.  Only those are the entry's own
    claims: a prose mention of a pre-existing (held) row is not a proposition this entry has
    to map, so the unmapped-row check is scoped to the rows this entry opened.  A prose row
    that names no registry row at all is a defect of any kind.
    """
    prose, manifest_rows = cited_rows(entry_text, man)
    prop_rows = {collapse(r.get("row", "")) for r in recs}
    notes = []
    for rowid in sorted(prose - set(rows)):
        notes.append("row_not_in_registry:%s" % rowid)
    for rowid in sorted((prose & fresh) - prop_rows):
        notes.append("row_unmapped:%s" % rowid)
    for rowid in sorted(prop_rows - prose):
        notes.append("row_uncited:%s" % rowid)
    if len(prop_rows) < MIN_DISTINCT_ROWS:
        notes.append("rows_too_few:%d" % len(prop_rows))
    quotes = [key(r.get("quote", "")) for r in recs]
    dupq = sorted({q for q in quotes if q and quotes.count(q) > 1})
    if dupq:
        notes.append("duplicate_quote:%s" % ",".join(dupq[:2]))
    claims = [key(r.get("claim", "")) for r in recs]
    dupc = sorted({c for c in claims if c and claims.count(c) > 1})
    if dupc:
        notes.append("duplicate_claim:%s" % ",".join(dupc[:2]))
    # Every proposition must be drawn on by the entry's prose.  The body names propositions by
    # their id (the "what the evidence licenses" table cites them, and the chain steps do), so
    # a map row no sentence points at is padding rather than a claim.
    referenced = referenced_ids(entry_text)
    for rec in recs:
        pid = collapse(rec.get("id", ""))
        if pid and pid not in referenced:
            notes.append("%s:id_not_referenced" % pid)
    detail = "prose_rows=%d prop_rows=%d manifest_rows=%d" % (
        len(prose), len(prop_rows), len(manifest_rows))
    if notes:
        detail += " miss=" + ",".join(notes[:4])
    return (1 if not notes else 0), detail


# ------------------------------------------------------------------ driver

def scratch_dir(arg, repo_root):
    root = os.path.realpath(repo_root)
    if arg:
        path = os.path.abspath(arg)
        real = os.path.realpath(path)
        if real == root or real.startswith(root + os.sep):
            raise Setup("scratch dir inside the scored repository: %s" % arg)
        if not os.path.isdir(real):
            try:
                os.makedirs(real)
            except OSError as exc:
                raise Setup("--work cannot be created: %s (%s)" % (arg, exc))
        return real
    tmp = os.environ.get("TMPDIR") or tempfile.gettempdir()
    if not os.path.isdir(tmp):
        raise Setup("TMPDIR is not a directory: %s" % tmp)
    return os.path.realpath(tempfile.mkdtemp(prefix="c2-r52-", dir=tmp))


def score(repo, rev, entry_path, fetch_root, work):
    entry_name = entry_path.rsplit("/", 1)[-1]
    entry = show(repo, rev, entry_path)
    entry_text = text_of(entry) if entry is not None else None
    results, record = {}, {"pred": PRED, "rev": rev, "base": BASE, "entry": entry_path}

    a, adet = clause_a(repo, rev, entry_path, entry_name)
    results["a"] = a
    print("C2_R52: a ok=%d %s" % (a, adet))

    if entry_text is None:
        for key_ in "bcde":
            results[key_] = 0
            print("C2_R52: %s ok=0 skipped=entry-absent" % key_)
    else:
        try:
            b, bdet, recs = clause_b(entry_text)
        except Setup as exc:
            b, bdet, recs = 0, "setup:%s" % exc, []
        results["b"] = b
        print("C2_R52: b ok=%d %s" % (b, bdet))

        try:
            c, cdet = clause_c(repo, rev, entry_name, recs, fetch_root)
        except Setup as exc:
            c, cdet = 0, "setup:%s" % exc
        results["c"] = c
        print("C2_R52: c ok=%d %s" % (c, cdet))

        try:
            d, ddet, bound = clause_d(repo, rev, entry_text, recs, fetch_root)
        except Setup as exc:
            d, ddet, bound = 0, "setup:%s" % exc, {}
        results["d"] = d
        print("C2_R52: d ok=%d %s" % (d, ddet))

        try:
            reg_rows, _base_rows, fresh = registry_state(repo, rev)
            e, edet = clause_e(entry_text, recs, bound, pin_manifest(entry_text.splitlines()),
                               reg_rows, fresh)
        except Setup as exc:
            e, edet = 0, "setup:%s" % exc
        results["e"] = e
        print("C2_R52: e ok=%d %s" % (e, edet))
        record["propositions"] = [
            {"id": collapse(r.get("id", "")), "row": collapse(r.get("row", "")),
             "pin": collapse(r.get("pin", "")),
             "quote_words": len(words(r.get("quote", ""))),
             "support_words": len(words(r.get("support", "")))}
            for r in recs]

    met = sum(results.get(k, 0) for k in "abcde")
    admitted = 1 if met == 5 else 0
    record.update({"clauses_met": met, "admitted": admitted,
                   "entailment": "outside-review-required"})
    try:
        with open(os.path.join(work, "c2-r52-probe.json"), "w") as fh:
            json.dump(record, fh, indent=1, sort_keys=True)
        print("C2_R52: work=%s probe=written" % work)
    except OSError as exc:
        print("C2_R52: work=%s probe=degraded(%s)" % (work, exc))
    print("C2_R52: entailment=not-checked (outside non-author review)")
    print("C2_R52: clauses=abcde clauses_met=%d admitted=%d/1 verdict=%s rev=%s"
          % (met, admitted, "TARGET_MET" if admitted else "TARGET_MISSED", rev))
    return admitted


def main(argv):
    ap = argparse.ArgumentParser(description=PRED)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--entry", default=ENTRY_DEFAULT,
                    help="repo-relative path of the target entry")
    ap.add_argument("--fetch-root", default=FETCH_ROOT_DEFAULT,
                    help="repo-relative pin root for this round")
    ap.add_argument("--work", default=None, help="scratch dir (default: mkdtemp under $TMPDIR)")
    args = ap.parse_args(argv)
    try:
        repo = os.path.abspath(args.repo)
        if not os.path.isdir(repo):
            raise Setup("--repo is not a directory: %s" % repo)
        top = git(repo, "rev-parse", "--show-toplevel")
        if not top:
            raise Setup("--repo is not a git work tree: %s" % repo)
        root = top.decode().strip()
        entry_path = args.entry.lstrip("/")
        entry_name = entry_path.rsplit("/", 1)[-1]
        if entry_name == R51_ENTRY_NAME:
            raise Setup("target entry must differ from the round-51 entry: %s" % entry_name)
        rev = resolve_rev(repo, args.rev)
        if git_rc(repo, "cat-file", "-e", BASE + "^{commit}") != 0:
            raise Setup("base commit %s is not in %s" % (BASE, root))
        if show(repo, BASE, entry_path) is not None:
            raise Setup("base %s already holds %s: the base is not the round-52 base"
                        % (BASE[:12], entry_path))
        work = scratch_dir(args.work, root)
        print("C2_R52: meta rev=%s base=%s entry=%s work=%s quote_policy=%s"
              % (rev, BASE[:12], entry_path, work, QUOTE_POLICY))
    except Setup as exc:
        print("C2_R52: setup error: %s" % exc)
        return 2
    return 0 if score(repo, rev, entry_path, args.fetch_root, work) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
