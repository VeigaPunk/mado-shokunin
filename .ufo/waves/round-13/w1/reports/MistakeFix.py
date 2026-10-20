#!/usr/bin/env python3
"""MistakeFix.py - narrow active-URL collision check for corpus/SOURCES.md.

Purpose
-------
The round-12 outside spot-check rejected S030 because it re-registered S017's
URL without an opening ``supersedes S0NN -`` link.  The fleet census keys a
duplicate on the exact (URL, scope-string) pair
(``scripts/sources-census.sh`` W04/E04), so S030's differing scope string
produced only a non-failing warning.  This merge check is intentionally
stricter and narrower: among ACTIVE rows (status queued or mined), any shared
canonical source URL is a collision unless the later row's ``teaches`` OPENS
with ``supersedes S<id> -`` naming the earlier row.

It does not compute scope overlap, semantic similarity, or a "distinct
anchor" judgment.  A differing scope string is not an exemption; the collision
is the merge gate's request for human review or an explicit supersedes link.
A ``rejected`` row is retained history and is ignored by the collision check
(it may still be named as a supersedes target).

Policy implemented (deliberately narrow)
----------------------------------------
Rows
  Only markdown registry rows matching ``^| S<3+ digits> |`` are read.  The
  table must have 11 cells (a split on ``|`` yields 13 fields), the id must
  be unique, and ``status`` must be exactly queued|mined|rejected.  Tier,
  kind, scope, anchor revision, dates, recheck cadence, used-by path
  existence and append-only history are NOT validated here.  In particular,
  no row is examined for scope text or scope overlap.

Canonical URL
  The first bare ``http(s)://`` token in the ``source`` cell is used.  Scheme
  and host are case-folded; a default port (80/443), a fragment and one
  trailing slash on a non-root path are removed; path and query are otherwise
  preserved.  A trailing `.,;` on the token is stripped before parsing.  Userinfo (credential
  material) is a policy error.  There is no aliasing of ``www.``, http vs https, or query order;
  Markdown link wrappers are not parsed and redirects/canonical-link tags are not resolved (the
  first bare token is used).

Collision rule
  Rows are ordered as written (append-only).  For each pair of ACTIVE rows
  (queued/mined) with the same canonical URL, the later row must open its
  ``teaches`` with ``supersedes S<id> -`` naming that earlier row; otherwise
  the pair is a collision and the merge stops for human review.  The link
  must resolve to an existing earlier row, forgives only the named row, and
  is not transitive.

Rejected rows
  A ``rejected`` row never creates a collision, even when its URL equals an
  active row's URL (that pair is the S017/S030 shape at HEAD).  Rejected rows
  that share a URL with active rows are reported once as REJECTED_HISTORY,
  informationally; they do not affect the exit code.  A new rejected row may
  supersede an earlier rejected row, e.g. ``supersedes S030 - REJECTED: ...``,
  without editing the earlier row's immutable cells.

Rows without a URL
  A row whose ``source`` has no URL (own-work/code paths; 10 rows at round-12
  HEAD) is outside URL-collision scope.  The summary prints ``no_url=N`` so
  the limit is visible; it is not a pass claim for those rows.

Exit map
  0  no live collision (rejected history is ignored)
  1  at least one active-row collision requiring review or a supersedes link
  2  usage, read, parse or policy error (bad row, duplicate id, bad status,
     bad URL, credential URL, empty registry, unknown/self/forward supersedes)

Read-only: no network, no writes.  ``--selftest`` uses in-memory fixtures only
and reads no registry (including this script's own directory).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple
from urllib.parse import urlsplit


ROW_RE = re.compile(r"^\|\s*(S\d{3,})\s*\|")
URL_RE = re.compile(r"https?://[^\s<>`\"']+", re.IGNORECASE)
SUPERSEDES_RE = re.compile(
    r"^\s*supersedes\s+(S\d{3,})(?=\s|[—–:-]|$)", re.IGNORECASE
)
STATUSES = ("queued", "mined", "rejected")
ACTIVE_STATUSES = ("queued", "mined")


class UrlPolicyError(ValueError):
    """A URL-cell policy failure with the report kind attached."""

    def __init__(self, kind: str, message: str):
        super().__init__(message)
        self.kind = kind


@dataclass(frozen=True)
class Row:
    id: str
    line: int
    url: Optional[str]
    status: str
    supersedes: Optional[str]


@dataclass(frozen=True)
class Problem:
    kind: str
    where: str
    detail: str


@dataclass
class Report:
    rows: List[Row]
    problems: List[Problem]
    collisions: List[Tuple[Row, Row, str]]
    rejected_history: List[Tuple[Row, Tuple[str, ...]]]
    supersedes_ok: List[Tuple[Row, Row]]

    def exit_code(self) -> int:
        if self.problems:
            return 2
        if self.collisions:
            return 1
        return 0


def _extract_url(source: str) -> Optional[str]:
    match = URL_RE.search(source)
    if match is None:
        return None
    return match.group(0).rstrip(".,;")


def _canonical_url(raw: str) -> str:
    candidate = raw.strip().strip("`<>").rstrip(".,;")
    try:
        parts = urlsplit(candidate)
        host = parts.hostname
        port = parts.port
    except ValueError as exc:
        raise UrlPolicyError("BAD_URL", "unparseable URL: %s" % exc) from exc
    scheme = (parts.scheme or "").lower()
    if scheme not in ("http", "https"):
        raise UrlPolicyError(
            "BAD_URL", "unsupported scheme %r (only http/https are compared)" % scheme
        )
    if not host:
        raise UrlPolicyError("BAD_URL", "URL has no host")
    if parts.username is not None or parts.password is not None:
        raise UrlPolicyError(
            "CREDENTIAL_URL",
            "credential material in URL is forbidden (contract rule 6)",
        )
    host = host.lower()
    if ":" in host:
        host = "[%s]" % host  # IPv6 literal
    if port is None or (scheme == "http" and port == 80) or (
        scheme == "https" and port == 443
    ):
        netloc = host
    else:
        netloc = "%s:%d" % (host, port)
    path = parts.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]
    query = "?%s" % parts.query if parts.query else ""
    return "%s://%s%s%s" % (scheme, netloc, path, query)


def _parse_supersedes(teaches: str) -> Optional[str]:
    match = SUPERSEDES_RE.match(teaches)
    return match.group(1) if match else None


def parse_registry(text: str) -> Tuple[List[Row], List[Problem]]:
    """Parse only the cells the merge policy needs; collect problems."""
    problems: List[Problem] = []
    rows: List[Row] = []
    seen = {}  # id -> first line number
    saw_row = False

    for lineno, line in enumerate(text.splitlines(), 1):
        if not ROW_RE.match(line):
            continue
        saw_row = True
        parts = line.split("|")
        if len(parts) != 13:
            problems.append(
                Problem(
                    "BAD_ROW",
                    "line %d" % lineno,
                    "expected 11 cells (13 split fields), got %d" % len(parts),
                )
            )
            continue
        cells = [cell.strip() for cell in parts[1:-1]]
        (
            row_id,
            source,
            _kind,
            _tier,
            _scope,
            _anchor,
            teaches,
            status,
            _opened,
            _recheck,
            _used_by,
        ) = cells
        if row_id in seen:
            problems.append(
                Problem(
                    "DUP_ID",
                    row_id,
                    "line %d repeats line %d" % (lineno, seen[row_id]),
                )
            )
            continue
        seen[row_id] = lineno
        if status not in STATUSES:
            problems.append(
                Problem(
                    "BAD_STATUS",
                    row_id,
                    "line %d has %r; expected %s"
                    % (lineno, status, "|".join(STATUSES)),
                )
            )
            continue
        url = None
        raw_url = _extract_url(source)
        if raw_url is not None:
            try:
                url = _canonical_url(raw_url)
            except UrlPolicyError as exc:
                problems.append(
                    Problem(exc.kind, row_id, "line %d: %s" % (lineno, exc))
                )
        rows.append(
            Row(
                id=row_id,
                line=lineno,
                url=url,
                status=status,
                supersedes=_parse_supersedes(teaches),
            )
        )

    by_id = {row.id: row for row in rows}
    if not saw_row:
        problems.append(
            Problem(
                "NO_ROWS",
                "registry",
                "no registry rows found (check the path and the 11-cell table shape)",
            )
        )
    for row in rows:
        if row.supersedes is None:
            continue
        target = by_id.get(row.supersedes)
        if row.supersedes == row.id:
            problems.append(
                Problem("SUPERSEDES_SELF", row.id, "line %d names itself" % row.line)
            )
        elif target is None:
            problems.append(
                Problem(
                    "SUPERSEDES_UNKNOWN",
                    row.id,
                    "line %d names missing row %s" % (row.line, row.supersedes),
                )
            )
        elif target.line > row.line:
            problems.append(
                Problem(
                    "SUPERSEDES_FORWARD",
                    row.id,
                    "line %d names later row %s (line %d); corrections point backward"
                    % (row.line, row.supersedes, target.line),
                )
            )
    return rows, problems


def collision_scan(rows: Sequence[Row]) -> List[Tuple[Row, Row, str]]:
    """Active-row URL collisions; rejected rows never collide."""
    collisions: List[Tuple[Row, Row, str]] = []
    for index in range(len(rows)):
        earlier = rows[index]
        if earlier.status not in ACTIVE_STATUSES:
            continue
        for later_index in range(index + 1, len(rows)):
            later = rows[later_index]
            if later.status not in ACTIVE_STATUSES:
                continue
            if earlier.url is None or later.url is None:
                continue  # own-work/path rows are outside URL collision scope
            if earlier.url != later.url:
                continue
            if later.supersedes == earlier.id:
                continue
            detail = (
                "same canonical URL among active rows; add an opening "
                "'supersedes %s —' link or route to human review; differing "
                "scope text is not an exemption" % earlier.id
            )
            collisions.append((earlier, later, detail))
    return collisions


def valid_supersedes(rows: Sequence[Row]) -> List[Tuple[Row, Row]]:
    """Resolved, backward opening links; one entry per link."""
    by_id = {row.id: row for row in rows}
    links: List[Tuple[Row, Row]] = []
    for row in rows:
        if row.supersedes is None:
            continue
        target = by_id.get(row.supersedes)
        if target is None:
            continue
        if target.line >= row.line:
            continue
        links.append((target, row))
    return links


def rejected_history(rows: Sequence[Row]) -> List[Tuple[Row, Tuple[str, ...]]]:
    """Rejected rows sharing a canonical URL with active rows; informational."""
    active_ids_by_url = {}
    for row in rows:
        if row.status in ACTIVE_STATUSES and row.url is not None:
            active_ids_by_url.setdefault(row.url, []).append(row.id)
    notes: List[Tuple[Row, Tuple[str, ...]]] = []
    for row in rows:
        if row.status != "rejected" or row.url is None:
            continue
        if row.url in active_ids_by_url:
            notes.append((row, tuple(active_ids_by_url[row.url])))
    return notes


def _default_registry_path() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "corpus" / "SOURCES.md"
        if candidate.is_file():
            return candidate
    return Path("corpus") / "SOURCES.md"


def _evaluate(text: str) -> Report:
    rows, problems = parse_registry(text)
    return Report(
        rows=rows,
        problems=problems,
        collisions=collision_scan(rows),
        rejected_history=rejected_history(rows),
        supersedes_ok=valid_supersedes(rows),
    )


def format_report(report: Report, registry: str) -> str:
    lines: List[str] = []
    for problem in report.problems:
        lines.append(
            "MISTAKE_FIX: ERROR %s %s :: %s"
            % (problem.kind, problem.where, problem.detail)
        )
    for earlier, later, detail in report.collisions:
        lines.append(
            "MISTAKE_FIX: COLLISION %s -> %s :: %s [url %s]"
            % (earlier.id, later.id, detail, later.url)
        )
    for row, active_ids in report.rejected_history:
        lines.append(
            "MISTAKE_FIX: REJECTED_HISTORY %s :: same canonical URL as active "
            "%s; ignored by the collision check (retained rejection record)"
            % (row.id, ", ".join(active_ids))
        )
    verdict = "ERROR" if report.problems else "FAIL" if report.collisions else "PASS"
    urls = len({row.url for row in report.rows if row.url is not None})
    no_url = len([row for row in report.rows if row.url is None])
    lines.append(
        "MISTAKE_FIX: %s registry=%s rows=%d urls=%d no_url=%d collisions=%d "
        "rejected_history=%d supersedes=%d errors=%d"
        % (
            verdict,
            registry,
            len(report.rows),
            urls,
            no_url,
            len(report.collisions),
            len(report.rejected_history),
            len(report.supersedes_ok),
            len(report.problems),
        )
    )
    return "\n".join(lines)


def _row(
    row_id: str,
    source: str,
    scope: str,
    status: str = "mined",
    teaches: str = "One bounded learner benefit.",
    used_by: str = "—",
) -> List[str]:
    """Build one 11-cell registry row for the selftest fixtures."""
    return [
        row_id,
        source,
        "docs",
        "A",
        scope,
        "§Syntax; 2026-08-26",
        teaches,
        status,
        "2026-10-19",
        "90d",
        used_by,
    ]


def _table(rows: Sequence[Sequence[str]]) -> str:
    header = (
        "| id | source | kind | tier | scope | anchor | teaches | status | "
        "opened | recheck | used-by |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
    )
    return header + "".join("| " + " | ".join(row) + " |\n" for row in rows)


def _pair_ids(pairs: Sequence[Sequence[Row]]) -> Tuple[Tuple[str, str], ...]:
    return tuple(sorted((pair[0].id, pair[1].id) for pair in pairs))


def run_selftest() -> int:
    """Exercise the policy with in-memory fixtures; read no file."""
    url_rules = "https://wiki.hypr.land/Configuring/Basics/Window-Rules/"
    url_start = "https://wiki.hypr.land/Configuring/Start/"
    scope_s017 = (
        "Current latest-git Lua-era syntax and documented effect semantics, "
        "scoped to that wiki era"
    )
    scope_s030 = "Current Lua window-rule syntax"

    fixtures: List[dict] = []

    def add(
        name,
        rows,
        collisions=0,
        problems=0,
        supersedes=0,
        rejected_ids=(),
        collision_pairs=(),
        problem_kinds=(),
    ):
        fixtures.append(
            {
                "name": name,
                "text": _table(rows),
                "collisions": collisions,
                "problems": problems,
                "supersedes": supersedes,
                "rejected_ids": tuple(rejected_ids),
                "collision_pairs": tuple(collision_pairs),
                "problem_kinds": tuple(problem_kinds),
            }
        )

    add(
        "unique-urls",
        [_row("S001", url_rules, scope_s030), _row("S002", url_start, scope_s030)],
    )
    add(
        "same-url-same-scope-collision",
        [_row("S001", url_rules, scope_s030), _row("S002", url_rules, scope_s030)],
        collisions=1,
        collision_pairs=(("S001", "S002"),),
    )
    # Required discriminator: differing scope strings are STILL a collision.
    # This is the 5174e15 shape, where S030 was mined and S017 was mined.
    add(
        "same-url-different-scope-still-collision",
        [
            _row("S017", url_rules, scope_s017),
            _row("S030", url_rules, scope_s030),
        ],
        collisions=1,
        collision_pairs=(("S017", "S030"),),
    )
    # Required: rejected history is tolerated (HEAD shape, immutable teaches).
    add(
        "rejected-history-tolerated",
        [
            _row("S017", url_rules, scope_s017),
            _row("S030", url_rules, scope_s030, status="rejected"),
        ],
        rejected_ids=("S030",),
    )
    # Required: a valid opening supersedes link permits the later active row.
    add(
        "valid-supersedes-permitted",
        [
            _row("S001", url_rules, scope_s030),
            _row(
                "S002",
                url_rules,
                scope_s030,
                teaches="supersedes S001 — distinct anchor at a pinned revision.",
            ),
        ],
        supersedes=1,
    )
    add(
        "mined-supersedes-queued",
        [
            _row("S006", url_rules, scope_s030, status="queued"),
            _row(
                "S042",
                url_rules,
                scope_s030,
                teaches="supersedes S006 — revision-anchored correction.",
            ),
        ],
        supersedes=1,
    )
    # Required: an unknown supersedes target is a policy error.
    add(
        "unknown-supersedes-rejected",
        [
            _row("S001", url_rules, scope_s030),
            _row(
                "S002",
                url_start,
                scope_s030,
                teaches="supersedes S099 — missing row.",
            ),
        ],
        problems=1,
        problem_kinds=("SUPERSEDES_UNKNOWN",),
    )
    # Required: a new rejected row may supersede rejected S030 with a
    # REJECTED reason, leaving S030's immutable teaches cell untouched.
    add(
        "new-rejected-row-supersedes-rejected-s030",
        [
            _row("S017", url_rules, scope_s017),
            _row("S030", url_rules, scope_s030, status="rejected"),
            _row(
                "S045",
                url_rules,
                scope_s030,
                status="rejected",
                teaches=(
                    "supersedes S030 — REJECTED: duplicate of S017; flip: a "
                    "distinct anchor at a pinned revision S017 does not cover."
                ),
            ),
        ],
        supersedes=1,
        rejected_ids=("S030", "S045"),
    )
    add(
        "supersedes-not-opening",
        [
            _row("S001", url_rules, scope_s030),
            _row(
                "S002",
                url_rules,
                scope_s030,
                teaches="Corrects the anchor; supersedes S001 — later text.",
            ),
        ],
        collisions=1,
        collision_pairs=(("S001", "S002"),),
    )
    add(
        "supersedes-other-id",
        [
            _row("S001", url_rules, scope_s030),
            _row("S002", url_start, scope_s030),
            _row(
                "S003",
                url_rules,
                scope_s030,
                teaches="supersedes S002 — unrelated URL.",
            ),
        ],
        collisions=1,
        supersedes=1,
        collision_pairs=(("S001", "S003"),),
    )
    add(
        "supersedes-forward",
        [
            _row("S001", url_rules, scope_s030),
            _row(
                "S002",
                url_rules,
                scope_s030,
                teaches="supersedes S003 — forward.",
            ),
            _row("S003", url_start, scope_s030),
        ],
        collisions=1,
        problems=1,
        collision_pairs=(("S001", "S002"),),
        problem_kinds=("SUPERSEDES_FORWARD",),
    )
    add(
        "supersedes-chain-not-transitive",
        [
            _row("S001", url_rules, scope_s030),
            _row(
                "S002",
                url_rules,
                scope_s030,
                teaches="supersedes S001 — first correction.",
            ),
            _row(
                "S003",
                url_rules,
                scope_s030,
                teaches="supersedes S002 — second correction.",
            ),
        ],
        collisions=1,
        supersedes=2,
        collision_pairs=(("S001", "S003"),),
    )
    add(
        "active-row-superseding-rejected-still-collides-with-active",
        [
            _row("S017", url_rules, scope_s017),
            _row("S030", url_rules, scope_s030, status="rejected"),
            _row(
                "S045",
                url_rules,
                scope_s030,
                teaches="supersedes S030 — corrected rejection record.",
            ),
        ],
        collisions=1,
        supersedes=1,
        rejected_ids=("S030",),
        collision_pairs=(("S017", "S045"),),
    )
    add(
        "url-normalization",
        [
            _row("S001", "https://Example.ORG:443/Path/", scope_s030),
            _row("S002", "https://example.org/Path#frag", scope_s030),
        ],
        collisions=1,
        collision_pairs=(("S001", "S002"),),
    )
    add(
        "url-query-distinct",
        [
            _row("S001", "https://example.org/page?a=1", scope_s030),
            _row("S002", "https://example.org/page?a=2", scope_s030),
        ],
    )
    add(
        "url-scheme-distinct",
        [
            _row("S001", "http://example.org/page", scope_s030),
            _row("S002", "https://example.org/page", scope_s030),
        ],
    )
    add(
        "own-work-no-url",
        [
            _row("S001", "corpus/knowledge/one.md", scope_s030),
            _row("S002", "corpus/knowledge/two.md", scope_s030),
        ],
    )
    add(
        "mined-over-rejected-tolerated",
        [
            _row("S001", url_rules, scope_s030, status="rejected"),
            _row("S002", url_rules, scope_s030),
        ],
        rejected_ids=("S001",),
    )
    add(
        "rejected-later-with-used-by-tolerated",
        [
            _row("S001", url_rules, scope_s030),
            _row(
                "S002",
                url_rules,
                scope_s030,
                status="rejected",
                used_by="corpus/knowledge/x.md",
            ),
        ],
        rejected_ids=("S002",),
    )
    add(
        "three-row-chain",
        [
            _row("S017", url_rules, scope_s017),
            _row("S030", url_rules, scope_s030, status="rejected"),
            _row("S031", url_rules, scope_s030),
        ],
        collisions=1,
        rejected_ids=("S030",),
        collision_pairs=(("S017", "S031"),),
    )
    add(
        "empty-registry",
        [],
        problems=1,
        problem_kinds=("NO_ROWS",),
    )
    add(
        "duplicate-id",
        [_row("S001", url_rules, scope_s030), _row("S001", url_start, scope_s030)],
        problems=1,
        problem_kinds=("DUP_ID",),
    )
    add(
        "malformed-row",
        [_row("S001", url_rules, scope_s030)[:-1]],
        problems=1,
        problem_kinds=("BAD_ROW",),
    )
    add(
        "bad-status",
        [_row("S001", url_rules, scope_s030, status="done")],
        problems=1,
        problem_kinds=("BAD_STATUS",),
    )
    add(
        "credentials-url",
        [_row("S001", "https://user:redacted@example.org/page", scope_s030)],
        problems=1,
        problem_kinds=("CREDENTIAL_URL",),
    )

    failures = []
    for fixture in fixtures:
        report = _evaluate(fixture["text"])
        errors = []
        counts = {
            "collisions": len(report.collisions),
            "problems": len(report.problems),
            "supersedes": len(report.supersedes_ok),
        }
        for key in ("collisions", "problems", "supersedes"):
            if counts[key] != fixture[key]:
                errors.append(
                    "%s=%d expected %d" % (key, counts[key], fixture[key])
                )
        got_collision_pairs = _pair_ids(report.collisions)
        if got_collision_pairs != tuple(sorted(fixture["collision_pairs"])):
            errors.append(
                "collision_pairs=%r expected %r"
                % (got_collision_pairs, tuple(sorted(fixture["collision_pairs"])))
            )
        got_rejected_ids = tuple(
            sorted(row.id for row, _active_ids in report.rejected_history)
        )
        if got_rejected_ids != tuple(sorted(fixture["rejected_ids"])):
            errors.append(
                "rejected_ids=%r expected %r"
                % (got_rejected_ids, tuple(sorted(fixture["rejected_ids"])))
            )
        got_problem_kinds = tuple(sorted(problem.kind for problem in report.problems))
        if got_problem_kinds != tuple(sorted(fixture["problem_kinds"])):
            errors.append(
                "problem_kinds=%r expected %r"
                % (got_problem_kinds, tuple(sorted(fixture["problem_kinds"])))
            )
        expected_exit = 2 if fixture["problems"] else 1 if fixture["collisions"] else 0
        if report.exit_code() != expected_exit:
            errors.append(
                "exit=%d expected %d" % (report.exit_code(), expected_exit)
            )
        if errors:
            failures.append((fixture["name"], errors))

    total = len(fixtures)
    if failures:
        print("MISTAKE_FIX_SELFTEST: FAIL %d/%d" % (len(failures), total))
        for name, errors in failures:
            print("  - %s: %s" % (name, "; ".join(errors)))
        return 1
    print("MISTAKE_FIX_SELFTEST: PASS %d/%d" % (total, total))
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="MistakeFix.py",
        description=(
            "Narrow active-URL collision check for corpus/SOURCES.md "
            "(read-only; see module docstring for the exact policy)."
        ),
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="run in-memory fixtures only; reads no registry file",
    )
    parser.add_argument(
        "--registry",
        metavar="PATH",
        default=None,
        help="registry markdown path (default: nearest corpus/SOURCES.md)",
    )
    args = parser.parse_args(argv)
    if args.selftest:
        return run_selftest()
    registry = Path(args.registry) if args.registry else _default_registry_path()
    try:
        text = registry.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print("MISTAKE_FIX: ERROR READ %s :: %s" % (registry, exc))
        return 2
    report = _evaluate(text)
    print(format_report(report, str(registry)))
    return report.exit_code()


if __name__ == "__main__":
    sys.exit(main())
