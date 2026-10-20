# MistakeFix — round 13 / w1 — S030 duplicate admission, criterion comparison, and merge check

Seat: `MadoR13.MistakeFix` (executor, leaf; no subagent dispatch, no background jobs).
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Status: **draft; no shared file edited; no check run by this seat.** The merge check is
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/MistakeFix.py`
(sibling of the report); L1 runs it.

Working-tree observation (2026-10-20): `corpus/QUALITY.md` and `corpus/SOURCES.md` are modified by
other seats. `corpus/QUALITY.md:32-39` already carries criterion 17 and `corpus/SOURCES.md` already
carries S040–S046, including S042 (`supersedes S006`) and S045 (`supersedes S030 — REJECTED: …`).
This seat did **not** edit either file. The independent criterion draft below is retained for
comparison; it is **not** a second numbered criterion to append.

## 1. Axes and what this seat contributes

| Axis | Contribution | Evidence | Verdict |
|---|---|---|---|
| coverage | Mines the round-12 outside disagreement over S030; compares the owner's already-present criterion 17 with an independent formulation; names the exact red/green revisions and the current S045 correction. | `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:114-124`; `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12-verifier-spotcheck.md:13`; `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:32-39`; `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-13.md:10` | **contributes; no axis verdict** — L1 owns the round verdict |
| operability | Isolated, read-only merge check: normalized-URL collision among **active** rows, opening `supersedes S<id> —` exemption, rejected history ignored, `--selftest` with in-memory fixtures, exit map. Real-data compatibility with S042→S006 and S045→S030. | `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/MistakeFix.py` | **contributes; not run** — L1 runs red-before/green-after |

The check is deliberately a **merge gate**, not scope-semantic automation: two active rows on one
canonical URL stop for human review unless the later row's `teaches` opens with a valid
`supersedes S<id> —` naming the earlier row. A differing scope string is not an exemption.

## 2. The outside disagreement, reconstructed

`[OBS-record]` Timeline, with the status of each anchor:

| Revision / artifact | S017 | S030 | Observation |
|---|---|---|---|
| `5174e15` | `mined` | `mined` | S030 admitted on the same URL as S017 with a different scope string and no supersedes link. `[OBS]` `git show 5174e15:corpus/SOURCES.md`; `[OBS-record]` `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/AttackMistake.md:16` |
| Orchestrator spot-check | — | admitted `mined`, disagreed | `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:114-117` |
| Round-12 landed `8dbfc93` | `mined` | `rejected` | Status flipped in place; S030 `used-by` is `—`; S017 takes the U2 citation; old→new logged. `[OBS]` `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:28,41 @ 8dbfc93`; `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:118-124` |
| Committed HEAD `7dcb785` | `mined` | `rejected` | Same round-12 state; no S045 yet. `[OBS]` `git rev-parse --short HEAD`; `git show HEAD:corpus/SOURCES.md` |
| Current working tree (uncommitted at observation) | `mined` | `rejected`; S045 `rejected` opens `supersedes S030 — REJECTED: …` | L1 integration added criterion 17 and S040–S046; S045 is the append-only rejection correction. `[OBS]` `git diff -- corpus/QUALITY.md corpus/SOURCES.md`; `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:29,42,54,57 @ worktree` |

Exact anchors and quotes:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:116` — “admitted as `mined` while it re-registered S017's URL for the same scope with no supersedes link” (20 words). `[OBS]`, read 2026-10-20.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12-verifier-spotcheck.md:13` — “S030 (same URL as S017) — disagree with its admission” (10 words). `[OBS]`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:106 @ worktree` — “S030 duplicated S017's URL (`wiki.hypr.land/Configuring/Basics/Window-Rules/`) for an overlapping current-wiki syntax scope with no `supersedes` link.” (19 words; same text at `:91 @ 8dbfc93`). `[OBS]`.
- `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:49-51` — “A correction is a new row whose `teaches` opens `supersedes S0NN —`.” (12 words). `[OBS]`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:29 @ worktree` S017 scope: “Current latest-git Lua-era syntax and documented effect semantics, scoped to that wiki era” (14 words), status `mined` (`:28 @ 8dbfc93`). `[OBS]`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:42 @ worktree` S030 scope: “Current Lua window-rule syntax” (5 words), status `rejected` (`:41 @ 8dbfc93`). `[OBS]`.

### 2.1 Why the fleet census did not prevent it

`[OBS-record]` ReviewSources and AttackMistake re-derived the fleet validator behavior:

- W04 keys on `scope_key = url SUBSEP scope` (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:643-645`); a
  differing scope string therefore produces only a **non-failing** W04. E04 fires only when the
  URL **and** the exact scope string match (`:647-649`). Neither computes overlapping scope.
- At `5174e15` AttackMistake's replica returned only `W04 S030 ...`, exit 0; the retained
  real-census result at HEAD is the same (`W04 S030`, exit 0). An exact-scope key cannot
  discriminate the incident. `[OBS-record]` `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/AttackMistake.md:16-19`; `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/EvidenceLedger.md:40,44`.
- The E04 exemption matches `supersedes S[0-9]{3}` **anywhere** in `teaches` (`:648`), so an
  unrelated or non-opening mention silences E04. ReviewSources F2 and AttackMistake CE1/CE2.
- The fleet census also counts a rejected row as retained history; W04 ignores status, so it stays
  visible on the current tree even though the lane corrected S030 and added S045.

Anchors: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/ReviewSources.md:13-20,38`;
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/AttackMistake.md:16-19,48-50,126,150`.

### 2.2 Why the admission bar needed a criterion

`[OBS]` The round-12 bar at `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:3-27` had
16 criteria: 1-5 are general claim admission, 6-16 are claim-level lessons. None governed
**registry-row identity**: a row could be opened on an existing row's URL as long as it was
individually grounded, and the only append-only correction route was contract rule 2's supersedes
row.

`[INF]` The missing rule was criterion-level, not a data repair. S030's in-place status flip is
contract-valid (status is mutable under rule 2), but it left the bar unable to distinguish a
correction from a new admission and left the census's non-failing W04 warning as the only trace.

## 3. Criterion: owner text already present; independent comparison

### 3.1 Owner criterion 17 (integrated working tree; uncommitted at observation)

Location: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:32-39`
(`## Criterion from the outside S030 disagreement (round 13)`). `[OBS]` `git diff` shows it is a
working-tree addition by the L1 integration; this seat did not edit it. Exact text:

> 17. Before source-fragment renumbering/merge, screen repeated canonical URLs across active rows even when scope wording differs. Review overlapping scope explicitly; reject/merge duplicates or append a genuine superseding row with a resolvable prior id. Preserve rejected history, and send distinct-scope reuse to human review rather than claiming URL equality proves semantic duplication. A warning-only shared census is not this review. (lesson: lessons/round-13.md#mistakes M1; outside finding: lessons/round-12-verifier-spotcheck.md)

Its lesson grounding exists: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-13.md:10`
(M1) records the outside disagreement, the W04-only census behavior, and the S045 correction. The
paragraph at `QUALITY.md:36-39` already states that the lane-local screen is a conservative
merge-review trigger, uses the actual S017/S030 pair as its red-before case, and preserves rejected
S030 in its green state.

**Do not append a second `17.`** — the slot is occupied and the owner text already covers the
required behavior. This is the append-only discipline applied to the criterion itself.

### 3.2 Independent draft (retained for comparison; not appended)

The text this seat would have proposed if the slot were open:

> 17. A new active (`queued`/`mined`) source row that shares a canonical URL (scheme/host case-folded; fragment, default port and one trailing path slash removed; path/query otherwise preserved) with an active row is not admitted on a differing scope string: it needs an opening `supersedes S<id> —` link naming the earlier row or a human adjudication recorded in the round lesson; a `rejected` row is retained history and is ignored by the merge check. (lesson: `lessons/round-12.md` § Outside spot-check; `lessons/round-12-verifier-spotcheck.md:13`; contract rule 2)

Comparison:

| Clause | Owner criterion 17 | Independent draft | Script |
|---|---|---|---|
| Trigger | repeated canonical URLs across active rows | new active row shares canonical URL with an active row | active-active canonical-URL pairs |
| Differing scope | “even when scope wording differs”; no URL-equality proof of semantic duplication | “not admitted on a differing scope string” | no scope comparison; collision is a review stop |
| Resolution | reject/merge duplicate or append genuine superseding row with a resolvable prior id; distinct-scope reuse to human review | opening `supersedes S<id> —` naming the earlier row or human adjudication in the round lesson | opening link must name the exact earlier row; otherwise `COLLISION`, exit 1 |
| Rejected history | “Preserve rejected history” | rejected row retained history, ignored by the check | rejected rows ignored for collisions; reported as `REJECTED_HISTORY` |
| Census boundary | “A warning-only shared census is not this review” | fleet W04/E04 boundary named | lane-local script, not a census replacement |
| Mechanics | not specified beyond “resolvable prior id” | canonicalization + opening + pairwise defined | canonicalization, opening, exists/earlier, pairwise/non-transitive |

The owner text and the independent draft agree on the behavior. The owner text is the adopted
criterion; the independent draft adds mechanical detail the owner text leaves to the witness.

### 3.3 Proposed append-only clarification (optional; not a numbered criterion)

If the owner wants the script's mechanics in `QUALITY.md`, append this paragraph **after**
`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:39` under the existing round-13
section (do not renumber or rewrite criterion 17):

```text
Mechanical witness (round 13, append-only clarification): the lane-local collision screen
normalizes URL scheme/host case, default port, fragment and one trailing path slash; it requires the
later active row's `teaches` to OPEN with `supersedes S<id> —` naming that exact earlier row
(pairwise, non-transitive). It does not score scope semantics; a same-URL active pair without that
link stops for human review. Rejected rows are retained history and are ignored by the collision
check. The red-before case is the admitted S017/S030 pair at `5174e15`; the green fixture is the
corrected registry shape with rejected S030/S045 and the S042->S006 and S045->S030 links.
```

No append is required for the script to be useful; without it, the script remains the witness named
in this report/draft, and the owner criterion 17 remains the bar.

### 3.4 Worked adjudications

| State | Active rows on URL | Expected by criterion 17 / check |
|---|---|---|
| `5174e15` S017 + S030 | S017 `mined`, S030 `mined` | **FAIL / collision S017 → S030**; differing scope is not an exemption |
| Round-12 landed / HEAD `7dcb785` | S017 `mined`, S030 `rejected` | **PASS**; one `REJECTED_HISTORY S030`; no live duplicate |
| Current working tree | S017 `mined`; S030/S045 rejected; S006 `queued` + S042 `mined` | **PASS**; `REJECTED_HISTORY S030` and `S045`; valid links S042→S006, S045→S030 |
| New active row opens `supersedes S017 — …` | S017 + new | **PASS** for that pair; link is valid and pairwise |
| New active row supersedes only rejected S030 | S017 + new active | **FAIL** against S017; rejected history does not excuse an active pair |
| New active row on a distinct canonical URL | S017 + new | **PASS**; the S030 flip's distinct-anchor route remains reachable via e.g. the 0.56.0 archive |

`[OBS-record]` The 0.56.0 archive is a distinct URL candidate for the S030 flip:
`https://wiki.hypr.land/0.56.0/Configuring/Basics/Window-Rules/` (HTTP 200, accessed 2026-10-20;
ReviewSources F6). No row is admitted by this draft.

## 4. Merge check contract

Path: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/MistakeFix.py`
(sibling of the report). Read-only; standard library only; no network, no writes.

Usage:

```sh
python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --selftest
python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry corpus/SOURCES.md
```

Exit map: `0` no live collision; `1` active-row collision(s); `2` usage/read/parse/policy error.
Output rows: `COLLISION`, `REJECTED_HISTORY`, `ERROR`, one `PASS|FAIL|ERROR` summary. The summary
prints `rows`, unique `urls`, `no_url`, `collisions`, `rejected_history`, `supersedes`, `errors`.
`rejected_history` counts rejected rows (not pairs); `supersedes` counts valid opening links (not
collisions forgiven).

### 4.1 Narrow validation boundary

Implemented:

- registry row shape (11 cells / 13 split fields), unique ids, status enum, and a no-rows guard
  (empty or misshaped table → `NO_ROWS`, exit 2);
- first bare `http(s)://` URL in `source`; canonicalization per the module docstring (scheme/host
  case-fold; default port, fragment and one trailing path slash removed; path/query otherwise
  preserved; trailing `.,;` stripped); credential material is a policy error;
- opening `supersedes S<id> —` parse; target exists and is earlier; self/unknown/forward are
  errors; link is pairwise and non-transitive;
- active-active URL collision; rejected rows ignored for collision; rejected rows sharing a URL
  with active rows are informational notes;
- `--selftest` in-memory fixtures; no file read.

Not implemented (stated limits, not pass claims):

- scope text, scope overlap, semantic similarity or “distinct anchor” judgment;
- tier, kind, anchor revision, dates, recheck cadence, used-by path existence;
- append-only history or the round-lesson old→new log;
- `REJECTED:` / `flip:` shape for rejected rows;
- URL aliases beyond the listed normalization (`www.`, http vs https, query order, percent
  encoding, redirects, `<link rel=canonical>` resolution, Markdown link wrappers);
- rows with no URL in `source` (current tree; summary prints `no_url=N`);
- supersedes truthfulness (the link is a mechanical claim; the round lesson records the reason).

### 4.2 Selftest fixtures (25, in-memory)

Required by the L1 directive:

| Fixture | Shape | Expected |
|---|---|---|
| `same-url-different-scope-still-collision` | S017/S030 both `mined`, differing scopes | 1 collision, exit 1 |
| `rejected-history-tolerated` | S017 `mined`, S030 `rejected` | 0 collisions, 1 rejected note, exit 0 |
| `valid-supersedes-permitted` | later active row opens `supersedes S001 — …` | 0 collisions, 1 valid link, exit 0 |
| `unknown-supersedes-rejected` | `supersedes S099 — …` | 1 `SUPERSEDES_UNKNOWN`, exit 2 |
| `new-rejected-row-supersedes-rejected-s030` | S045 `rejected`, opens `supersedes S030 — REJECTED: …` | 0 collisions, 1 valid link, exit 0 |

Additional fixtures: same URL/same scope collision; not-opening supersedes; supersedes a different
id; forward supersedes; non-transitive chain; active row superseding rejected S030 still collides
with active S017; mined supersedes queued; URL normalization (case/port/trailing slash/fragment);
query-distinct; scheme-distinct; own-work no-URL rows; mined-over-rejected tolerated;
rejected-later-with-used-by tolerated; three-row chain; empty registry (`NO_ROWS`); duplicate id;
malformed row; bad status; credential URL.

### 4.3 Current-tree compatibility (by inspection, not run)

- S042's `teaches` opens `supersedes S006 — …`; S006 is `queued` and earlier, so the S006/S042 pair
  is a valid exemption, not a collision.
- S045's `teaches` opens `supersedes S030 — REJECTED: …`; S030 is `rejected` and earlier, so the
  link is valid and both rows are `REJECTED_HISTORY` notes.
- S046 adds a unique URL
  (`https://gitlab.freedesktop.org/wayland/wayland-utils/-/raw/1.3.0/wayland-info/wayland-info.c`);
  it has no same-URL peer and does not collide. S040 and S043 are similarly unique.
- At the observation, the current registry is 46 rows; the script should print `PASS`,
  `collisions=0`, `rejected_history=2`, `supersedes=2`, `errors=0`, exit 0. Counts may move if
  other seats append rows.
- At `5174e15` (39 rows, no S042/S045), the script should print `COLLISION S017 -> S030`, `FAIL`,
  exit 1.

## 5. L1 runbook (not run by this seat)

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --selftest
# expect: MISTAKE_FIX_SELFTEST: PASS 25/25, exit 0

git show 5174e15:corpus/SOURCES.md > /tmp/mado-sources-5174e15.md
python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry /tmp/mado-sources-5174e15.md
# expect: COLLISION S017 -> S030, FAIL, exit 1

python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry corpus/SOURCES.md
# expect: PASS, collisions=0, exit 0; at the observed tree also
# REJECTED_HISTORY S030 and S045, supersedes=2
```

`/tmp` is a transient run input, not durable evidence (QUALITY criterion 13). The durable record is
the committed script plus the L1 receipt's quoted output and revision.

## 6. Findings and routing

1. **Criterion already present** — `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:32-39`
   carries criterion 17 (integrated; uncommitted at observation). This seat's independent draft
   converges; **do not append a duplicate 17**. If the owner wants the script mechanics in QUALITY,
   append the §3.3 clarification paragraph only.
2. **Fleet census boundary** — W04/E04 exact-scope keying cannot discriminate this class. The lane
   check is URL-only among active rows; the fleet-level normalized-URL fix remains with the fleet
   owner.
3. **S030 shape debt is being repaired append-only** — S045 (current working tree) opens
   `supersedes S030 — REJECTED: …` and leaves S030's immutable `teaches` untouched. This is the
   ReviewSources F3 option (b). Do not edit S030 in place.
4. **Supersedes tightening** — opening form + resolvable earlier id + exact pair + non-transitive.
   The current tree provides two real cases: S042→S006 (queued predecessor, valid) and S045→S030
   (rejected predecessor, valid). The fleet census's anywhere-match remains too permissive.
5. **Rejected history** — S030/S045 are retained rejection records; the check ignores them for
   collisions and reports them informationally. A rejected row with a non-empty `used-by` is still
   ignored here; registry hygiene is a separate concern.
6. **False-positive posture** — any same-URL active pair is a review stop. A genuinely distinct
   scope is not auto-exempt; human adjudication or a distinct canonical URL is the route. This is
   intentional, not scope automation.
7. **Prevention, not row quantity** — the S030 flip raised the rejected tally 2→3 between `5174e15`
   and HEAD; that is a correction, not new taste evidence
   (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/AttackMistake.md:108`).
8. **Script is wave-local** — promote to `tools/` before citing it as a standing gate; it is not a
   replacement for `mado-verify.sh` or the fleet census.

## 7. Source records (internal reads, 2026-10-20)

| Path | Line | Quote (≤25 words) | Use |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md` | 116 | “admitted as `mined` while it re-registered S017's URL for the same scope with no supersedes link” | outside disagreement |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12-verifier-spotcheck.md` | 13 | “S030 (same URL as S017) — disagree with its admission” | non-author corroboration |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` | 106 @ worktree (91 @ 8dbfc93) | “for an overlapping current-wiki syntax scope with no `supersedes` link.” | search-log errata |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` | 29, 42 @ worktree (28, 41 @ 8dbfc93) | S017 scope “Current latest-git Lua-era syntax and documented effect semantics, scoped to that wiki era”; S030 scope “Current Lua window-rule syntax” | row states |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` | 54, 57 @ worktree | S042 `supersedes S006`; S045 `supersedes S030 — REJECTED: …` | current supersedes rows |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md` | 32-39 | owner criterion 17 and the lane-local screen paragraph | adopted bar (uncommitted) |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-13.md` | 10, 35, 38 | M1; S042 supersedes S006; S045 supersedes S030 | round-13 grounding |
| `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` | 49-51 | “A correction is a new row whose `teaches` opens `supersedes S0NN —`.” | rule 2 |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/hyprland-config-era-r12.md` | 127 | “S030 was rejected in the same round as a duplicate of S017” | citation erratum |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/ReviewSources.md` | 13-20, 38 | W04/E04 exact URL+scope; F3 option (b) | census boundary |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/AttackMistake.md` | 16-19, 48-50, 126, 150 | `5174e15` S030 mined/W04 only; anywhere-supersedes gap; T1 red/green | discrimination |

No external URL was opened by this seat. The 0.56.0 archive line is `[OBS-record]` from
ReviewSources F6, not a new open by this seat.

## 8. Tooling record

Installs or upgrades: **none.** Used only the existing shell, `git`, `grep`, `sed`, and file reads.
No build, lint, formatter, test, selftest, regression, or live probe was run (wave rule; L1 runs).

## 9. What this seat did not do

- No edit to `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md`,
  `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`,
  `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md`, the gate, or any other
  shared file. The uncommitted criterion 17 and S040–S046 are other seats' work; this seat only
  observed them.
- No run of `MistakeFix.py` (including `--selftest`) and no run of the fleet census or lane gate.
- No commit, push, or worktree change.
- No host `~/.config` / `~/.local` reads, no compositor probe, no sibling or fleet-repo writes.
- No judgment on C1/C2; the script is a proposal for L1 to accept, run, and route.
