#!/usr/bin/env python3
"""Structural C2-r52-style checker over the Falsify38 fixture.

Implements exactly the counter-side checks the frozen C2 predicate assigns to
the counter (registration.md): proposition count, row/pin/quote bindings and
index; entry absence at base. Modeled line-for-line on the r51 counter's
clause-b algorithm (SRC_RE row collection, pin manifest, LOC_RE locators,
at_lines span match, words()<=25). It deliberately performs NO completeness
sweep over body prose: that is the point under test.
"""
import argparse
import os
import re
import subprocess
import sys

ENTRY = "corpus/knowledge/hyprland-dispatcher-execution-r52.md"
ENTRY_NAME = "hyprland-dispatcher-execution-r52.md"
REGISTRY = "corpus/SOURCES.md"
README = "corpus/README.md"
FETCH_ROOT = ".ufo/waves/round-52/fetch"
OPENED = "2026-10-27"
MIN_PROPS = 4
MAX_QUOTE_WORDS = 25

SRC_RE = re.compile(r"^\s*source\s*(?:\([^)]*\))?\s*:\s*(.+)$", re.I)
ROW_RE = re.compile(r"^(S\d{3,})$")
LOC_RE = re.compile(r"(?<![\w./-])([A-Za-z0-9._/-]+):(\d+)(?:-(\d+))?(?!\d)")
LOC_SKIP = re.compile(r"^(sha\d+|https?|www|file)$", re.I)
BACKTICK_RE = re.compile(r"`([^`\n]{2,300})`")
TOKEN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.:\-]{1,60}$")


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True)
    return p.stdout if p.returncode == 0 else None


def text_of(blob):
    return blob.decode("utf-8", "replace") if blob else ""


def show(repo, rev, path):
    return git(repo, "show", "%s:%s" % (rev, path))


def ls_files(repo, rev, path):
    out = git(repo, "ls-tree", "-r", "--name-only", rev, "--", path)
    return out.decode().splitlines() if out else []


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


def words(s):
    return collapse(s).split()


def at_lines(blob, first, last):
    lines = text_of(blob).splitlines()
    if first < 1 or first > len(lines):
        return None
    return "\n".join(lines[first - 1:min(last, len(lines))])


# ---------------- (a) entry + index

def index_row(readme_text, name):
    for header, rows in tables(readme_text.splitlines()):
        for cells in rows:
            for cell in cells:
                if name in cell and "knowledge/" in cell:
                    return collapse(cells[0] if cells else cell)
    return None


# ---------------- (b) registry + manifest + proposition map

def registry(text):
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
        rows[m.group(1)] = row
    if header is None:
        raise SystemExit("registry header not found")
    return rows


def pin_cell(cell):
    spans = BACKTICK_RE.findall(cell or "")
    if spans:
        return clean(spans[0])
    tok = re.split(r"[\s(,;]", (cell or "").strip(), maxsplit=1)[0]
    return clean(tok)


def manifest(text):
    out = {}
    for header, rows in tables(text.splitlines()):
        if not header:
            continue
        low = [clean(c).lower() for c in header]
        if not re.match(r"pin\b", low[0]):
            continue
        ridx = next((i for i, c in enumerate(low) if c in
                     ("row", "rows", "s-row", "srow", "source row", "registry row", "sid", "id")), None)
        for cells in rows:
            name = pin_cell(cells[0]) if cells else ""
            if not name:
                continue
            declared = clean(cells[ridx]) if ridx is not None and ridx < len(cells) else ""
            out[name] = {"row": declared if re.fullmatch(r"S\d{3,}", declared) else ""}
    return out


def resolve_pin(token, man):
    base = clean(token.rsplit("/", 1)[-1])
    if base in man:
        return base
    cands = [k for k in man if k.lower() == base.lower()]
    if len(cands) == 1:
        return cands[0]
    stem = base.rsplit(".", 1)[0].lower()
    cands = [k for k in man if k.rsplit(".", 1)[0].lower() == stem]
    if len(cands) == 1:
        return cands[0]
    cands = [k for k in man if k.rsplit(".", 1)[0].lower().endswith("-" + stem)]
    return cands[0] if len(cands) == 1 else None


def quote_candidates(line):
    out = []
    for rx in (BACKTICK_RE,):
        out.extend(x.group(1) for x in rx.finditer(line))
    seen, uniq = set(), []
    for q in out:
        q = q.strip()
        if len(q) < 4 or q in seen:
            continue
        seen.add(q)
        uniq.append(q)
    return uniq


def proposition_map(text):
    """Declared propositions: the table whose header starts with `proposition`."""
    for header, rows in tables(text.splitlines()):
        if not header:
            continue
        low = [clean(c).lower() for c in header]
        if not low[0].startswith("proposition"):
            continue
        out = []
        for cells in rows:
            if len(cells) < 5:
                continue
            m = re.match(r"\s*(P\d+)\s*:", cells[0])
            out.append({
                "id": m.group(1) if m else cells[0][:12],
                "row": clean(cells[1]),
                "pin": pin_cell(cells[2]),
                "quote": cells[3].strip().strip("`"),
                "rationale": cells[4].strip(),
            })
        return out
    return []


def score(repo, rev, base):
    entry = text_of(show(repo, rev, ENTRY))
    if not entry:
        print("CHECK: a ok=0 entry=absent")
        print("CHECK: verdict=TARGET_MISSED")
        return 1
    readme = text_of(show(repo, rev, README))
    a = 1 if index_row(readme, ENTRY_NAME) else 0
    print("CHECK: a ok=%d index_row=%s" % (a, "present" if a else "absent"))

    reg = registry(text_of(show(repo, rev, REGISTRY)))
    man = manifest(entry)
    props = proposition_map(entry)
    pins_at_rev = {p.rsplit("/", 1)[-1] for p in ls_files(repo, rev, FETCH_ROOT)}
    blob_cache = {}

    def loader(name):
        if name not in blob_cache:
            blob_cache[name] = show(repo, rev, FETCH_ROOT + "/" + name)
        return blob_cache[name]

    bound, notes = [], []
    for p in props:
        row = reg.get(p["row"])
        if row is None:
            notes.append("%s=row_absent" % p["id"]); continue
        if clean(row.get("status", "")).lower() != "mined":
            notes.append("%s=status" % p["id"]); continue
        if clean(row.get("opened", "")) != OPENED:
            notes.append("%s=opened" % p["id"]); continue
        name = resolve_pin(p["pin"], man)
        if not name:
            notes.append("%s=pin_unmapped" % p["id"]); continue
        if man[name]["row"] and man[name]["row"] != p["row"]:
            notes.append("%s=pin_row_mismatch" % p["id"]); continue
        if name not in pins_at_rev:
            notes.append("%s=pin_absent" % p["id"]); continue
        m = LOC_RE.search(p["pin"] + " ")  # proposition carries pin name only; use source line locators
        # locate the locator on the source line for this row
        anchored = [l for l in unfenced(entry.splitlines())
                    if re.search(r"\b%s\b" % p["row"], l) and l.strip().startswith("source")]
        span = None
        for line in anchored:
            for lm in LOC_RE.finditer(line):
                nm = resolve_pin(lm.group(1), man)
                if nm != name:
                    continue
                first = int(lm.group(2)); last = int(lm.group(3)) if lm.group(3) else first
                blob = loader(name)
                if blob is None:
                    continue
                span = at_lines(blob, first, last)
                if span is not None and collapse(p["quote"]) in collapse(span):
                    break
                span = None
        if span is None:
            notes.append("%s=quote_not_at_pin" % p["id"]); continue
        if len(words(p["quote"])) > MAX_QUOTE_WORDS:
            notes.append("%s=quote_overlong" % p["id"]); continue
        if not p["rationale"]:
            notes.append("%s=no_rationale" % p["id"]); continue
        bound.append(p["id"])
    b = 1 if len(bound) >= MIN_PROPS and not notes else 0
    print("CHECK: b ok=%d propositions=%d bound=%s notes=%s"
          % (b, len(props), ",".join(bound) or "-", ";".join(notes) or "-"))

    met = a + b
    verdict = "TARGET_MET" if met == 2 else "TARGET_MISSED"
    print("CHECK: clauses_met=%d/2 verdict=%s rev=%s" % (met, verdict, rev))
    return 0 if met == 2 else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    args = ap.parse_args(argv)
    if show(args.repo, args.base, ENTRY) is not None:
        print("CHECK: setup error: base already holds the entry")
        return 2
    return score(args.repo, args.rev, args.base)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
