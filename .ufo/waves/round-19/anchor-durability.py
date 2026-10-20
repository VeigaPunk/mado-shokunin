#!/usr/bin/env python3
"""Round-19 anchor-durability check for corpus/SOURCES.md (routed defects R18-V1, R18-V4).

Usage:
    anchor-durability.py REV [--rows S###,...] [--exclude-status ST[,ST]]

Reads committed bytes only: `git show REV:corpus/SOURCES.md` and the fetch
receipts committed at REV under `.ufo/waves/round-1[0-9]/fetch/*/receipts.jsonl`.
No network, no worktree reads, no row id is special-cased.

For every evaluated registry row, one line is printed:

    ROW <id> durable|PER_FETCH_DIGEST|UNPINNED_ALIAS — <reason>

Default evaluated set: status `mined` only. `--exclude-status` replaces that
filter with "every status not listed" (so `--exclude-status rejected,queued`
reproduces mined-only, and `--exclude-status rejected` adds `queued` rows).

Rules (structural; a row may hit more than one, the first status in the
precedence list is printed and the second is named after `also`):

  PER_FETCH_DIGEST — observed rotation only. Committed receipts at REV hold
    two or more distinct sha256 values among `http_status` 200 records for a
    URL the anchor credits, joined by either of:
      (i)  the exact http(s) URL appears in the source or anchor cell;
      (ii) a 64-hex digest in the anchor is one of that URL's recorded
           digests (the anchor credits the URL by its digest). A path mention
           alone, including a git tree object id under a path, credits no URL.

  UNPINNED_ALIAS
    a source-column http(s) URL whose path has a segment exactly `latest`,
    `main`, `master` or `HEAD`, and the anchor names no pin for it: a 40-hex
    commit, a version tag (`v?N(.N)*`), a revision date (publication,
    modification, release, archive — never an access/opened date), or a
    7-39 hex abbreviated commit within 40 characters before / 80 after an
    alias token in the anchor text.

  durable
    neither fired. A row that credits a 64-hex digest to an HTML/tree/blob
    page, an API listing or a docs site (clause tokens `tree`, `blob`,
    `html`, `listing`, `api.github.com`, `docs.rs`, or a source URL shaped
    github.com/<o>/<r>/(tree|blob)/..., api.github.com, docs.rs, *.html)
    whose receipts show fewer than two distinct digests prints that fact:
    `page digest, not shown to rotate (receipts: N records, M digests)`,
    with N=M=0 when no committed receipt covers the digest.

Exit: 0 = no row flagged, 1 = at least one flagged, 2 = usage or
could-not-evaluate (bad REV, no SOURCES.md at REV, absent `--rows` id, bad
`--exclude-status` value). `--rows` restricts the scan; an id absent from the
registry exits 2, an id present but outside the evaluated statuses is skipped
on stderr (status is reported there).

`MADO_LANE` overrides the lane root for hermetic fixtures (normally derived
from this file's location).
"""

import json
import os
import re
import subprocess
import sys
from urllib.parse import urlsplit

DERIVED_LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

SHA64 = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")
URL_RE = re.compile(r"https?://[^\s<>()\[\]`\"']+")
ROW_RE = re.compile(r"^\|[ \t]*S\d{3,}[ \t]*\|")
ALIAS_SEGMENTS = ("latest", "main", "master", "HEAD")
PAGE_TOKEN_RE = re.compile(r"\btree\b|\bblob\b|\bhtml\b|\blisting\b|api\.github\.com|docs\.rs",
                           re.IGNORECASE)
PAGE_URL_RE = re.compile(
    r"^https?://(?:api\.github\.com/|docs\.rs/|github\.com/[^/]+/[^/]+/(?:tree|blob)/)",
    re.IGNORECASE)
HEX40 = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
HEX7_39 = re.compile(r"(?<![0-9a-f])[0-9a-f]{7,39}(?![0-9a-f])")
TAG_RE = re.compile(r"(?<![\w.])v?\d+\.\d+(?:\.\d+)*(?![\w.])")
DATE_RE = re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)")
ALIAS_IN_ANCHOR = re.compile(r"(?<![\w/])(?:latest|main|master|HEAD)(?![\w])")
RECEIPT_PATH_RE = re.compile(r"^\.ufo/waves/round-1[0-9]/fetch/[^/]+/receipts\.jsonl$")
STATUS_ORDER = ("UNPINNED_ALIAS", "PER_FETCH_DIGEST")
STATUS_ENUM = ("queued", "mined", "rejected")


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], capture_output=True)


def clean_url(u):
    return u.rstrip(".,;:)]}'\"")


def urls_in(text):
    out = []
    for raw in URL_RE.findall(text):
        u = clean_url(raw)
        if u not in out:
            out.append(u)
    return out


def segments(u):
    return [s for s in urlsplit(u).path.split("/") if s]


def alias_segments(u):
    return [s for s in segments(u) if s in ALIAS_SEGMENTS]


def pin_token(anchor):
    """The first pin the anchor names, or None.

    A dated version is a date attached to the source revision (modified,
    published, released, dated, archived); an access/opened date dates the
    observation, never the source, and is not a pin.
    """
    m = HEX40.search(anchor)
    if m:
        return f"40-hex commit {m.group(0)}"
    for d in DATE_RE.finditer(anchor):
        lead = anchor[max(0, d.start() - 24):d.start()]
        if re.search(r"(?:accessed|opened|read|fetched)\s*$", lead, re.IGNORECASE):
            continue
        return f"date {d.group(0)}"
    m = TAG_RE.search(anchor)
    if m:
        return f"version {m.group(0)}"
    for a in ALIAS_IN_ANCHOR.finditer(anchor):
        window = anchor[max(0, a.start() - 40):a.end() + 80]
        m = HEX7_39.search(window)
        if m:
            return f"abbreviated commit {m.group(0)}"
    return None


def ref_segment(u):
    """Last path segment that looks like a ref: a 40-hex commit or a version tag."""
    ref = None
    for s in segments(u):
        if HEX40.fullmatch(s) or TAG_RE.fullmatch(s):
            ref = s
    return ref


def page_clause_digest(anchor):
    """b1: (digest, clause) for a digest whose own clause names a page."""
    for m in SHA64.finditer(anchor):
        lead = anchor[:m.start()]
        cut = lead.rfind(";")
        clause = lead[cut + 1:] if cut >= 0 else lead
        if PAGE_TOKEN_RE.search(clause[-60:]):
            return m.group(0), clause.strip()[-60:]
    return None


def page_source_digest(source, anchor):
    """b2: (url, digest) when the source URL is a page and the anchor digests bytes."""
    m = SHA64.search(anchor)
    if not m:
        return None
    for u in urls_in(source):
        path = urlsplit(u).path
        if PAGE_URL_RE.search(u) or path.lower().endswith(".html"):
            return u, m.group(0)
    return None


def receipt_groups(lane, rev):
    """{url: {'digests': {sha}, 'records': n}}, per requested URL, over 200 records at REV."""
    tree = git(lane, "ls-tree", "-r", "--name-only", rev)
    if tree.returncode != 0:
        return None, 0, 0
    groups, files, bad = {}, 0, 0
    for path in tree.stdout.decode(errors="replace").splitlines():
        if not RECEIPT_PATH_RE.match(path):
            continue
        files += 1
        body = git(lane, "show", f"{rev}:{path}")
        if body.returncode != 0:
            return None, files, bad
        for line in body.stdout.decode(errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            try:
                status = int(rec.get("http_status"))
            except (TypeError, ValueError):
                bad += 1
                continue
            digest = rec.get("sha256")
            url = rec.get("url")
            if status != 200 or not isinstance(digest, str) or not isinstance(url, str):
                continue
            if not SHA64.fullmatch(digest):
                continue
            groups.setdefault(url, {"digests": set(), "records": 0})
            groups[url]["digests"].add(digest)
            groups[url]["records"] += 1
    return groups, files, bad


def digest_coverage(digest, groups):
    """(url, count of 200 records, distinct digests for that url) for a credited digest."""
    for u in sorted(groups):
        g = groups[u]
        if digest in g["digests"]:
            return u, g["records"], len(g["digests"])
    return None


def rotation_match(text, anchor, groups):
    """Observed rotation for a URL the anchor credits, or None.

    Returns (url, sorted digests, how). The anchor credits a URL when the
    exact URL appears in the row, or when a 64-hex digest in the anchor is one
    of that URL's recorded digests. A row that merely names a path segment
    (e.g. a git tree *object* id under `themes/x`) credits no URL and is not
    joined.
    """
    urls = urls_in(text)
    for u in urls:
        if u in groups and len(groups[u]["digests"]) >= 2:
            return u, sorted(groups[u]["digests"]), "exact URL"
    for d in SHA64.findall(anchor):
        hit = digest_coverage(d, groups)
        if hit and hit[2] >= 2:
            u = hit[0]
            return u, sorted(groups[u]["digests"]), f"credited digest {d[:8]}…"
    return None


def page_digest_note(digest, groups):
    """`durable` reason text for a page-credited digest with no observed rotation."""
    hit = digest_coverage(digest, groups)
    recs, k = (hit[1], hit[2]) if hit else (0, 0)
    return (f"sha256 {digest[:8]}… is a page digest, not shown to rotate "
            f"(receipts: {recs} records, {k} digests)")


def evaluate(row, groups):
    rid, source, anchor = row[0], row[1], row[5]
    text = source + " " + anchor
    flags = []
    notes = []
    groups = groups or {}

    aliases = []
    for u in urls_in(source):
        aliases.extend(alias_segments(u))
    if aliases:
        pin = pin_token(anchor)
        if pin is None:
            flags.append(("UNPINNED_ALIAS", "alias",
                          f"source path segment {aliases[0]} and anchor names no "
                          f"40-hex commit, tag or dated version"))

    page_digests = []
    page = page_clause_digest(anchor)
    if page:
        page_digests.append(page[0])
    page_source = page_source_digest(source, anchor)
    if page_source:
        page_digests.append(page_source[1])

    variance = rotation_match(text, anchor, groups)
    if variance:
        u, digs, how = variance
        flags.append(("PER_FETCH_DIGEST", "receipt variance",
                      f"{len(digs)} distinct 200 digests for {u} "
                      f"({digs[0][:8]}… ≠ {digs[1][:8]}…; matched by {how})"))
    else:
        for d in dict.fromkeys(page_digests):
            notes.append(page_digest_note(d, groups))

    if flags:
        primary = next(s for s in STATUS_ORDER if any(f[0] == s for f in flags))
        reasons = [r for s, _, r in flags if s == primary]
        other = [f"{k}: {r}" for s, k, r in flags if s != primary]
        reason = "; ".join(reasons)
        if other:
            reason += "; also " + "; ".join(other)
        if notes:
            reason += "; also " + "; ".join(notes)
        return rid, primary, reason

    if notes:
        hit = "; ".join(notes)
        if aliases:
            hit = f"alias segment {aliases[0]} pinned by {pin_token(anchor)}; " + hit
        return rid, "durable", hit
    if not urls_in(source):
        hit = "no source URL (local path or host bytes)"
    elif aliases:
        hit = f"alias segment {aliases[0]} pinned by {pin_token(anchor)}"
    elif SHA64.search(anchor) and ref_segment(urls_in(source)[0]):
        hit = f"sha256 over raw bytes at ref {ref_segment(urls_in(source)[0])}"
    elif pin_token(anchor):
        hit = f"no page digest; anchor pins {pin_token(anchor)}"
    elif SHA64.search(anchor):
        hit = "sha256 with no enumerated page class or pinned ref"
    elif DATE_RE.search(anchor):
        hit = "no assigned class fired; anchor dates the access, not a revision"
    else:
        hit = "no alias segment and no digest credited"
    return rid, "durable", hit


def parse_rows(doc):
    rows, malformed = [], []
    for n, line in enumerate(doc.splitlines(), 1):
        if not ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 11:
            malformed.append((n, cells[0] if cells else "?"))
            continue
        rows.append(cells)
    return rows, malformed


def main(argv):
    if not argv or argv[0].startswith("-"):
        print("usage: anchor-durability.py REV [--rows S###,...] "
              "[--exclude-status ST[,ST]]", file=sys.stderr)
        return 2
    rev = argv[0]
    keep = None
    exclude = None
    rest = argv[1:]
    i = 0
    while i < len(rest):
        if rest[i] == "--rows":
            if i + 1 >= len(rest):
                print("usage: --rows needs S###,S###", file=sys.stderr)
                return 2
            want = [x.strip() for x in rest[i + 1].split(",") if x.strip()]
            bad = [x for x in want if not re.fullmatch(r"S\d{3,}", x)]
            if bad:
                print(f"usage: bad row id {bad[0]}", file=sys.stderr)
                return 2
            keep = set(want)
            i += 2
            continue
        if rest[i] == "--exclude-status":
            if i + 1 >= len(rest):
                print("usage: --exclude-status needs ST[,ST]", file=sys.stderr)
                return 2
            vals = [x.strip() for x in rest[i + 1].split(",") if x.strip()]
            bad = [x for x in vals if x not in STATUS_ENUM]
            if bad:
                print(f"usage: bad status {bad[0]}", file=sys.stderr)
                return 2
            exclude = set(vals)
            i += 2
            continue
        print(f"usage: unknown argument {rest[i]}", file=sys.stderr)
        return 2

    def evaluated(status):
        if exclude is None:
            return status == "mined"
        return status not in exclude

    lane = os.environ.get("MADO_LANE") or DERIVED_LANE
    c = git(lane, "rev-parse", "--verify", rev + "^{commit}")
    if c.returncode != 0:
        print(f"could_not_evaluate: rev {rev}", file=sys.stderr)
        return 2
    commit = c.stdout.decode().strip()
    doc = git(lane, "show", f"{commit}:corpus/SOURCES.md")
    if doc.returncode != 0:
        print(f"could_not_evaluate: {commit}:corpus/SOURCES.md", file=sys.stderr)
        return 2

    rows, malformed = parse_rows(doc.stdout.decode(errors="replace"))
    if not rows:
        print(f"could_not_evaluate: no registry rows at {commit}", file=sys.stderr)
        return 2
    for n, rid in malformed:
        print(f"malformed: line {n} {rid} (not 11 columns)", file=sys.stderr)

    by_id = {r[0]: r for r in rows}
    if keep is not None:
        absent = sorted(x for x in keep if x not in by_id)
        if absent:
            print(f"could_not_evaluate: absent row {absent[0]}", file=sys.stderr)
            return 2
        for rid in sorted(keep):
            status = by_id[rid][7]
            if not evaluated(status):
                print(f"skipped: {rid} status={status}", file=sys.stderr)
        rows = [r for r in rows if r[0] in keep and evaluated(r[7])]
        if not rows:
            print("could_not_evaluate: --rows names no evaluated row", file=sys.stderr)
            return 2
    else:
        rows = [r for r in rows if evaluated(r[7])]

    groups, receipt_files, bad_receipts = receipt_groups(lane, commit)
    if groups is None:
        print(f"could_not_evaluate: receipts at {commit}", file=sys.stderr)
        return 2

    counts = {"durable": 0, "PER_FETCH_DIGEST": 0, "UNPINNED_ALIAS": 0}
    flagged = []
    for row in rows:
        rid, status, reason = evaluate(row, groups)
        counts[status] += 1
        if status != "durable":
            flagged.append(rid)
        print(f"ROW {rid} {status} — {reason}")

    scope = (f"mined={len(rows)}" if exclude is None
             else f"rows={len(rows)} statuses=not:"
                  f"{','.join(sorted(exclude))}")
    print(f"SUMMARY rev={commit} {scope} durable={counts['durable']} "
          f"per_fetch_digest={counts['PER_FETCH_DIGEST']} "
          f"unpinned_alias={counts['UNPINNED_ALIAS']} flagged={len(flagged)} "
          f"receipt_files={receipt_files} bad_receipt_lines={bad_receipts}")
    if flagged:
        print(f"FLAGGED {' '.join(flagged)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
