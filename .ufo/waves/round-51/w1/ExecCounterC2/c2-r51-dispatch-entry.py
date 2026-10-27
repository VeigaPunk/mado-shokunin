#!/usr/bin/env python3
"""PRED-C2-r51 - the dispatcher-dispatch entry is admitted (C2, coverage, sourced).

Frozen contract (`.ufo/waves/round-51/claims.md`, sentence PRED-C2-r51):

    TMPDIR=<scratch> python3 -I quality/counters/c2-r51-dispatch-entry.py --repo <lane> --rev <rev>
    exits 0 with final line
        C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=<rev>
    iff at <rev>:
      (a) corpus/knowledge/hyprland-dispatcher-dispatch-r51.md exists and is indexed in
          corpus/README.md;
      (b) its `source:` block cites >=2 rows S364-S379 of corpus/SOURCES.md with status `mined`,
          opened 2026-10-27, each bound to a pin under .ufo/waves/round-51/fetch/ named in the
          entry's pin manifest whose cited line contains the row's quote verbatim (<=25 words);
      (c) the entry's maximum word-8-gram shingle overlap against every corpus/knowledge/*.md at
          base 6ca8c559a4a3d6d361101592116eea2bc7452437 and every file under
          .ufo/waves/round-*/candidate/ (recursive) is <=30% per file;
      (d) >=3 distinct `held:` citations each name corpus/knowledge/<file>:<line> at base and the
          named line contains every pinned key token of that citation.
    At base the entry is absent and the command prints admitted=0/1 verdict=TARGET_MISSED exit 1.

Citation grammar this counter checks (the only accepted shapes; documented so a draft can be
written against it):

  source line  - a line beginning `source:` that names one registry row, e.g.
                 `source: S364 - <title> - <what it teaches> `quoted text`(Pin-Name:123) ...`
                 A row is scored when some unfenced prose line names it (the `source:` line or any
                 `**OBS** S364: ...` line) and that line carries a locator whose basename resolves
                 to a pin named in the entry's pin manifest plus a quoted span (backticks, "..."
                 or smart quotes, or an explicit `quote=`) whose text appears verbatim, whitespace
                 collapsed, in the pin's cited line span. A quote written immediately before its
                 locator (the house `quote`(Pin:123) shape) is tried first; other quoted spans on
                 the same line are accepted too. A manifest that carries a row column binds that
                 pin to that row, and a declared row must match the cited row.
  pin manifest - a markdown table whose first header cell starts with `pin`; each row names a pin
                 file. The pin file itself must exist at `.ufo/waves/round-51/fetch/<pin name>` at
                 <rev>.
  held line    - a line beginning `held` that cites `corpus/knowledge/<file>.md:<line>` and pins
                 its key tokens with `keys=TOK[,TOK...]` (or, absent keys=, the backticked
                 identifier spans on the same line), e.g.
                 `held: corpus/knowledge/keybind-rule-semantics.md:108 keys=dispatcher,submap`.
                 Every pinned token must appear verbatim in that base line.

Exit codes: 0 = 4/4 clauses; 1 = at least one clause missed; 2 = setup error (bad repo/rev/base,
unusable scratch). Scratch: `--work DIR` or a mkdtemp under $TMPDIR; a scratch root inside the
scored repository is refused. No file outside the scratch dir is written.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

PRED = "PRED-C2-r51"
ENTRY = "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md"
ENTRY_NAME = "hyprland-dispatcher-dispatch-r51.md"
REGISTRY = "corpus/SOURCES.md"
README = "corpus/README.md"
FETCH_ROOT = ".ufo/waves/round-51/fetch"
WAVES = ".ufo/waves"
# Frozen constants: the base commit every novelty/held comparison is scored against, the row
# window the source block must cite, and the round's access date.
BASE = "6ca8c559a4a3d6d361101592116eea2bc7452437"
ROW_MIN, ROW_MAX = 364, 379
OPENED = "2026-10-27"
MIN_ROWS = 2
MIN_HELD = 3
MAX_QUOTE_WORDS = 25
NGRAM = 8
MAX_OVERLAP = 0.30
MIN_BODY_SHINGLES = 300

ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ROW_RE = re.compile(r"^(S\d{3,})$")
SRC_RE = re.compile(r"^\s*source\s*(?:\([^)]*\))?\s*:\s*(.+)$", re.I)
HELD_RE = re.compile(r"^\s*held\b", re.I)
KLOC_RE = re.compile(r"(?:corpus/)?knowledge/([A-Za-z0-9._-]+\.md):(\d+)")
KEYS_RE = re.compile(r"\bkeys?\s*[=:]\s*(.+)$", re.I)
LOC_RE = re.compile(r"(?<![\w./-])([A-Za-z0-9._/-]+):(\d+)(?:-(\d+))?(?!\d)")
LOC_SKIP = re.compile(r"^(sha\d+|https?|www|file)$", re.I)
BACKTICK_RE = re.compile(r"`([^`\n]{2,300})`")
DQUOTE_RE = re.compile(r"(?<![\w`])\"([^\"\n]{2,300})\"")
SQUOTE_RE = re.compile(r"[\u201c]([^\u201d\n]{2,300})[\u201d]")
QASSIGN_RE = re.compile(r"\bquot(?:e|ed)\s*[=:]\s*(.+)$", re.I)
SHA_RE = re.compile(r"^[0-9a-fA-F]{32,64}$")
TOKEN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.:\-]{1,60}$")
CAND_RE = re.compile(r"^\.ufo/waves/round-[^/]+/candidate/.+")
KNOW_RE = re.compile(r"^corpus/knowledge/[^/]+\.md$")


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


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


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


def cells_of(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def is_rule(cells):
    return all(re.fullmatch(r":?-{2,}:?", c or "") for c in cells) if cells else False


def clean(cell):
    return re.sub(r"[`*\s]+", "", cell or "")


# ---------------------------------------------------------------- (a) entry + index row

def index_row(readme_text, name):
    """The README index row that names the entry, or None."""
    for header, rows in tables(readme_text.splitlines()):
        for cells in rows:
            for cell in cells:
                if name in cell and "knowledge/" in cell:
                    return collapse(cells[0] if cells else cell)
    return None


def clause_a(repo, rev):
    entry = show(repo, rev, ENTRY)
    if entry is None:
        return 0, None, "entry=absent"
    readme = show(repo, rev, README)
    if readme is None:
        return 0, entry, "readme=absent"
    row = index_row(text_of(readme), ENTRY_NAME)
    if not row:
        return 0, entry, "index_row=absent"
    return 1, entry, "index_row=%s" % (len(row) > 60 and row[:57] + "..." or row)


# ---------------------------------------------------------------- (b) source block

def registry(text):
    """S-id -> {column: value} for the SOURCES.md registry table at REV."""
    rows, header = {}, None
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = cells_of(s)
        if header is None:
            low = [c.lower() for c in cells]
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
        rows[m.group(1)] = row
    if header is None:
        raise Setup("registry header (id|source|...|status|opened|...) not found")
    return rows


def pin_cell(cell):
    """The pin name inside a manifest cell: first backticked span, else the leading token."""
    spans = BACKTICK_RE.findall(cell or "")
    if spans:
        return pin_name(spans[0])
    tok = re.split(r"[\s(,;]", (cell or "").strip(), maxsplit=1)[0]
    return pin_name(tok)


def manifest(text):
    """pin -> {row, file} from every entry table whose first header cell is a pin column.

    The frozen sentence needs the pin *named* in the manifest; a manifest that also carries a
    row/source column binds that pin to that row, and a declared row must match the cited row.
    """
    rowkeys = ("row", "rows", "s-row", "srow", "source row", "registry row", "sid", "id")
    out = {}
    for header, rows in tables(text.splitlines()):
        if not header:
            continue
        low = [clean(c).lower() for c in header]
        if not re.match(r"pin\b", low[0]):
            continue
        ridx = next((i for i, c in enumerate(low) if c in rowkeys), None)
        fidx = next((i for i, c in enumerate(low) if c in ("file", "upstream file")), None)
        for cells in rows:
            name = pin_cell(cells[0]) if cells else ""
            if not name:
                continue
            declared = clean(cells[ridx]) if ridx is not None and ridx < len(cells) else ""
            out[name] = {
                "row": declared if re.fullmatch(r"S\d{3,}", declared) else "",
                "file": clean(cells[fidx]) if fidx is not None and fidx < len(cells) else "",
            }
    return out


def pin_name(n):
    return re.sub(r"[`*\s]+", "", n or "")


def resolve_pin(token, man):
    """manifest pin whose name the locator token names (exact, then case, then suffix stem)."""
    base = pin_name(token.rsplit("/", 1)[-1])
    if base in man:
        return base
    cands = [k for k in man if k.lower() == base.lower()]
    if len(cands) == 1:
        return cands[0]
    stem = base.rsplit(".", 1)[0].lower()
    cands = [k for k in man if k.rsplit(".", 1)[0].lower() == stem]
    if len(cands) == 1:
        return cands[0]
    # a shortened prose name (`DispatcherTranslator.cpp`) still names the pinned file
    cands = [k for k in man if k.rsplit(".", 1)[0].lower().endswith("-" + stem)]
    return cands[0] if len(cands) == 1 else None


def quote_candidates(line):
    """Quoted spans on a source line; an explicit `quote=`/`quoted:` scope is tried first."""
    texts = []
    m = QASSIGN_RE.search(line)
    if m:
        texts.append(m.group(1))
    texts.append(line)
    out = []
    for text in texts:
        for rx in (BACKTICK_RE, SQUOTE_RE, DQUOTE_RE):
            out.extend(x.group(1) for x in rx.finditer(text))
    seen, uniq = set(), []
    for q in out:
        q = q.strip()
        if len(q) < 4 or q in seen:
            continue
        if " " not in q and (SHA_RE.match(q) or "/" in q or q.startswith("http")
                             or q.endswith(".md")):
            continue
        seen.add(q)
        uniq.append(q)
    return uniq


def words(s):
    return collapse(s).split()


def at_lines(blob, first, last):
    lines = text_of(blob).splitlines()
    if first < 1 or first > len(lines):
        return None
    return "\n".join(lines[first - 1:min(last, len(lines))])


def paired_quote(line, start):
    """The quoted span that ends just before `start` (house style `quote`(Pin:123)), or None."""
    head = line[:start]
    for rx in (BACKTICK_RE, SQUOTE_RE, DQUOTE_RE):
        spans = [m for m in rx.finditer(head) if head[m.end():].strip(" ,;") == ""]
        if spans:
            return spans[-1].group(1).strip()
    return None


def bind_row(rowid, lines, man, pins_at_rev, loader):
    """(pin, first, last, quote, line) for a row bound to a pin at rev, or (None, reason).

    Each candidate line names ROWID; a locator on it must resolve to a pin the manifest names
    (a manifest row column, when present, must name this same row) and the quote paired with that
    locator - or failing a pairing, any quote on the line - must appear verbatim in the pin's
    cited line span.
    """
    reason = "no_locator"
    for line in lines:
        locs = [m for m in LOC_RE.finditer(line) if not LOC_SKIP.match(m.group(1))]
        quotes = quote_candidates(line)
        if not locs:
            continue
        if not quotes:
            reason = "no_quote"
            continue
        for m in locs:
            token, first = m.group(1), int(m.group(2))
            last = int(m.group(3)) if m.group(3) else first
            name = resolve_pin(token, man)
            if not name:
                reason = "pin_unmapped:%s" % token.rsplit("/", 1)[-1]
                continue
            if man[name]["row"] and man[name]["row"] != rowid:
                reason = "pin_row_mismatch:%s=%s" % (name, man[name]["row"])
                continue
            if name not in pins_at_rev:
                reason = "pin_file_absent:%s" % name
                continue
            blob = loader(name)
            if blob is None:
                reason = "pin_file_absent:%s" % name
                continue
            span = at_lines(blob, first, last)
            if span is None:
                reason = "pin_line_out_of_range:%s:%d" % (name, first)
                continue
            hay = collapse(span)
            paired = paired_quote(line, m.start())
            for q in ([paired] if paired else []) + quotes:
                if len(words(q)) > MAX_QUOTE_WORDS:
                    continue
                if collapse(q) and collapse(q) in hay:
                    return (name, first, last, collapse(q), line), ""
            reason = "quote_not_at_pin"
    return None, reason


def clause_b(repo, rev, entry_text):
    """Rows S364-S379 cited by the entry, each bound to a manifest pin at a verifying quote."""
    prose = [l for l in unfenced(entry_text.splitlines()) if not l.strip().startswith("|")]
    rowids = []
    for line in prose:
        m = SRC_RE.match(line)
        if not m:
            continue
        for k in re.findall(r"\bS(\d{3,})\b", m.group(1)):
            rowid = "S" + k
            if ROW_MIN <= int(k) <= ROW_MAX and rowid not in rowids:
                rowids.append(rowid)
    if not rowids:
        return 0, "source_rows=0"
    reg_text = show(repo, rev, REGISTRY)
    if reg_text is None:
        return 0, "registry=absent"
    rows = registry(text_of(reg_text))
    man = manifest(entry_text)
    if not man:
        return 0, "pin_manifest=absent"
    pins_at_rev = {p.rsplit("/", 1)[-1] for p in ls_files(repo, rev, FETCH_ROOT)}
    pin_blobs, verified, notes = {}, {}, []

    def loader(name):
        if name not in pin_blobs:
            pin_blobs[name] = show(repo, rev, FETCH_ROOT + "/" + name)
        return pin_blobs[name]

    for rowid in rowids:
        row = rows.get(rowid)
        if row is None:
            notes.append("%s=absent" % rowid)
            continue
        if clean(row.get("status", "")).lower() != "mined":
            notes.append("%s=status:%s" % (rowid, clean(row.get("status", "")) or "-"))
            continue
        if clean(row.get("opened", "")) != OPENED:
            notes.append("%s=opened:%s" % (rowid, clean(row.get("opened", "")) or "-"))
            continue
        anchored = [l for l in prose if re.search(r"\b%s\b" % rowid, l)]
        bound, why = bind_row(rowid, anchored, man, pins_at_rev, loader)
        if bound is None:
            notes.append("%s=%s" % (rowid, why))
            continue
        verified[rowid] = bound
    ok = len(verified) >= MIN_ROWS
    detail = "rows=%d/%d pins=%d" % (len(verified), MIN_ROWS,
                                     len({v[0] for v in verified.values()}))
    if notes:
        detail += " miss=" + ",".join(notes[:4])
    return (1 if ok else 0), detail


# ---------------------------------------------------------------- (c) novelty

def body_text(entry_text):
    out, fenced = [], False
    for line in entry_text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            fenced = not fenced
            continue
        if fenced or not s or s.startswith("|"):
            continue
        if re.match(r"^(source|ground|held|verified-at|recheck|lane|pin)\b", s, re.I):
            continue
        out.append(s)
    return "\n".join(out)


def shingles(text, n=NGRAM):
    toks = re.findall(r"[a-z0-9]{2,}", text.lower())
    if len(toks) < n:
        return set()
    return {tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)}


def clause_c(repo, rev, base, entry_text):
    body = shingles(body_text(entry_text))
    if len(body) < MIN_BODY_SHINGLES:
        return 0, "body_shingles=%d<%d" % (len(body), MIN_BODY_SHINGLES), []
    refs = []
    for path in ls_files(repo, base, "corpus/knowledge"):
        if KNOW_RE.match(path):
            blob = show(repo, base, path)
            if blob is not None:
                refs.append((path, blob))
    n_cand = 0
    for path in ls_files(repo, rev, WAVES):
        if not CAND_RE.match(path):
            continue
        blob = show(repo, rev, path)
        if blob is None or not blob:
            continue
        n_cand += 1
        refs.append((path, blob))
    scored = []
    for path, blob in refs:
        other = shingles(text_of(blob))
        hits = len(body & other)
        scored.append((hits / float(len(body)), hits, path))
    scored.sort(reverse=True)
    top = scored[:3]
    worst = top[0][0] if top else 0.0
    detail = ("body_shingles=%d files=%d+cand%d max=%.1f%% "
              "top=[%s]" % (len(body), len(refs) - n_cand, n_cand, worst * 100.0,
                            ", ".join("%.1f%%:%s" % (r * 100.0, p) for r, _, p in top)))
    return (1 if worst <= MAX_OVERLAP else 0), detail, top


# ---------------------------------------------------------------- (d) held citations

def held_tokens(line):
    m = KEYS_RE.search(line)
    toks = []
    if m:
        for part in re.split(r"[,\s;]+", m.group(1)):
            tok = part.strip("`*'\"()[]")
            if TOKEN_RE.match(tok):
                toks.append(tok)
    if not toks:
        for span in BACKTICK_RE.findall(line):
            tok = span.strip()
            if TOKEN_RE.match(tok) and "/" not in tok and not tok.endswith(".md"):
                toks.append(tok)
    seen, out = set(), []
    for t in toks:
        if t not in seen and t.lower() not in ("keys", "key"):
            seen.add(t)
            out.append(t)
    return out


def clause_d(repo, base, entry_text, base_kn):
    cites, seen, notes = {}, set(), []
    lines_seen, untargeted = 0, 0
    for line in unfenced(entry_text.splitlines()):
        if not HELD_RE.match(line):
            continue
        lines_seen += 1
        locs = KLOC_RE.findall(line)
        if not locs:
            # a `held (cited, not re-registered): S### - ...` line cites a registry row, not a
            # corpus line; only `corpus/knowledge/<file>:<line>` citations score clause (d)
            untargeted += 1
            continue
        toks = held_tokens(line)
        if not toks:
            notes.append("no_tokens:%s:%s" % locs[0])
            continue
        for name, num in locs:
            key = (name, int(num))
            if key in seen:
                continue
            seen.add(key)
            path = "corpus/knowledge/" + name
            if path not in base_kn:
                notes.append("file_absent:%s" % path)
                continue
            lines = base_kn[path]
            n = int(num)
            if n < 1 or n > len(lines):
                notes.append("line_out_of_range:%s:%d" % (name, n))
                continue
            missing = [t for t in toks if t not in lines[n - 1]]
            if missing:
                notes.append("token_missing:%s:%d:%s" % (name, n, missing[0]))
                continue
            cites[key] = toks
    detail = "held=%d/%d lines=%d untargeted=%d tokens=%d" % (
        len(cites), MIN_HELD, lines_seen, untargeted,
        sum(len(v) for v in cites.values()))
    if notes:
        detail += " miss=" + ",".join(notes[:4])
    return (1 if len(cites) >= MIN_HELD else 0), detail, sorted(cites)


# ---------------------------------------------------------------- driver

def knowledge_at_base(repo, base):
    out = {}
    for path in ls_files(repo, base, "corpus/knowledge"):
        if not KNOW_RE.match(path):
            continue
        blob = show(repo, base, path)
        if blob is not None:
            out[path] = text_of(blob).splitlines()
    return out


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
    return os.path.realpath(tempfile.mkdtemp(prefix="c2-r51-", dir=tmp))


def score(repo, rev, base, work):
    entry = show(repo, rev, ENTRY)
    entry_text = text_of(entry) if entry is not None else None
    met, results = 0, {}
    record = {"pred": PRED, "rev": rev, "base": base, "entry": ENTRY}

    a, _, adet = clause_a(repo, rev)
    results["a"] = a
    print("C2_R51: a ok=%d %s" % (a, adet))

    if entry_text is None:
        print("C2_R51: b ok=0 skipped=entry-absent")
        print("C2_R51: c ok=0 skipped=entry-absent")
        print("C2_R51: d ok=0 skipped=entry-absent")
        record.update({"a": a, "b": 0, "c": 0, "d": 0})
    else:
        try:
            b, bdet = clause_b(repo, rev, entry_text)
        except Setup as exc:
            b, bdet = 0, "setup:%s" % exc
        results["b"] = b
        print("C2_R51: b ok=%d %s" % (b, bdet))

        c, cdet, top = clause_c(repo, rev, base, entry_text)
        results["c"] = c
        print("C2_R51: c ok=%d %s" % (c, cdet))
        record["c_top"] = [{"file": p, "overlap": round(r, 4), "hits": h} for r, h, p in top]

        base_kn = knowledge_at_base(repo, base)
        d, ddet, cites = clause_d(repo, base, entry_text, base_kn)
        results["d"] = d
        print("C2_R51: d ok=%d %s" % (d, ddet))
        record.update({"a": a, "b": b, "c": c, "d": d,
                       "held": ["corpus/knowledge/%s:%d" % k for k in cites]})

    met = sum(results.get(k, 0) for k in "abcd")
    admitted = 1 if met == 4 else 0
    record.update({"clauses_met": met, "admitted": admitted})
    try:
        with open(os.path.join(work, "c2-r51-probe.json"), "w") as fh:
            json.dump(record, fh, indent=1, sort_keys=True)
        print("C2_R51: work=%s probe=written" % work)
    except OSError as exc:
        print("C2_R51: work=%s probe=degraded(%s)" % (work, exc))
    print("C2_R51: clauses=abcd clauses_met=%d admitted=%d/1 verdict=%s rev=%s"
          % (met, admitted, "TARGET_MET" if admitted else "TARGET_MISSED", rev))
    return admitted


def main(argv):
    ap = argparse.ArgumentParser(description=PRED)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
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
        rev = resolve_rev(repo, args.rev)
        if git_rc(repo, "cat-file", "-e", BASE + "^{commit}") != 0:
            raise Setup("base commit %s is not in %s" % (BASE, root))
        if show(repo, BASE, ENTRY) is not None:
            raise Setup("base %s already holds %s: the base is not the round-51 base"
                        % (BASE[:12], ENTRY))
        work = scratch_dir(args.work, root)
        print("C2_R51: meta rev=%s base=%s work=%s" % (rev, BASE[:12], work))
    except Setup as exc:
        print("C2_R51: setup error: %s" % exc)
        return 2
    return 0 if score(repo, rev, BASE, work) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
