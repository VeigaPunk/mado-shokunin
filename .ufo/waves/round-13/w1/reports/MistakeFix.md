# MistakeFix — round 13 / w1 — report

Seat: `MadoR13.MistakeFix` (executor, leaf; no delegation, no background jobs).
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Axes: **coverage** (sourced incident → criterion comparison and grounding) and **operability**
(isolated normalized-URL merge check with hermetic `--selftest`). No axis verdict is issued.

## Outcome

- Mined the round-12 outside disagreement over S030: an **active-row URL duplicate** admitted as
  `mined` despite a differing scope string and no supersedes link.
- Observed that the current working tree **already carries criterion 17**
  (`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:32-39`; integrated by the L1,
  uncommitted at the 2026-10-20 observation), grounded in `corpus/lessons/round-13.md:10` M1.
  This seat's independent draft converges with it; **no second `17.` is proposed**. An optional
  append-only mechanical clarification is in §2.
- Wrote the isolated check at
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/MistakeFix.py`
  (sibling of this report). It is read-only, standard-library only, and was **not run** by this
  seat. L1 runs red-before/green-after.
- No shared file was edited; no test/build/lint/formatter was run; no commit or push.
- Working-tree note: `corpus/QUALITY.md` and `corpus/SOURCES.md` are modified by other seats;
  S040–S046 are present, including S042 (`supersedes S006`) and S045
  (`supersedes S030 — REJECTED: …`). This seat only observed them.

## 1. Incident reconstruction

| Revision | S017 | S030 | Fact |
|---|---|---|---|
| `5174e15` | `mined` | `mined` | S030 admitted on S017's URL with scope “Current Lua window-rule syntax” vs S017's “Current latest-git Lua-era syntax and documented effect semantics, scoped to that wiki era”; S030's `teaches` has no supersedes link. `[OBS]` `git show 5174e15:corpus/SOURCES.md`; `[OBS-record]` `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/AttackMistake.md:16` |
| spot-check | — | admitted, disagreed | “admitted as `mined` while it re-registered S017's URL for the same scope with no supersedes link” — `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:116` |
| round-12 `8dbfc93` | `mined` | `rejected` | In-place status flip; `used-by` moved to S017; old→new logged. `[OBS]` `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:28,41,91 @ 8dbfc93`; `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:118-124` |
| HEAD `7dcb785` | `mined` | `rejected` | Same round-12 state; no S045 yet. `[OBS]` `git rev-parse --short HEAD` |
| current tree | `mined` | `rejected`; S045 `rejected` opens `supersedes S030 — REJECTED: …` | Other seats added criterion 17 and S040–S046; S045 is the append-only correction. `[OBS]` `git diff -- corpus/QUALITY.md corpus/SOURCES.md`; `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:29,42,54,57 @ worktree` |

Corroboration: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12-verifier-spotcheck.md:13`
(“S030 (same URL as S017) — disagree with its admission”); citation erratum at
`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/hyprland-config-era-r12.md:127`.

Why the existing machinery missed it:

- The fleet validator's W04/E04 key on the exact `(URL, scope-string)` pair
  (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:643-649`, `[OBS-record]`
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/ReviewSources.md:13-20` and
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/AttackMistake.md:16-19,48-50`).
  W04 is non-failing; E04 needs the same scope string. AttackMistake's replica at `5174e15`
  returned only `W04 S030`, exit 0; the retained real-census result at HEAD is the same. It cannot
  discriminate the incident.
- The round-12 admission bar (`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:3-27`)
  had 16 criteria but none for registry-row identity/duplication. Contract rule 2 supplied
  append-only and the supersedes form, not a collision gate
  (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:49-51`).
- Consequence: the correction was data-complete but criterion-incomplete. S030's in-place status
  flip is contract-valid, yet the bar could not distinguish a correction from a new admission, and
  the immutable `teaches` cell could not carry a `REJECTED:` reason (ReviewSources F3).

## 2. Criterion: owner text already present; independent comparison

### 2.1 Owner criterion 17 (integrated working tree; uncommitted at observation)

Location: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:32-39`
(`## Criterion from the outside S030 disagreement (round 13)`). Exact text:

> 17. Before source-fragment renumbering/merge, screen repeated canonical URLs across active rows even when scope wording differs. Review overlapping scope explicitly; reject/merge duplicates or append a genuine superseding row with a resolvable prior id. Preserve rejected history, and send distinct-scope reuse to human review rather than claiming URL equality proves semantic duplication. A warning-only shared census is not this review. (lesson: lessons/round-13.md#mistakes M1; outside finding: lessons/round-12-verifier-spotcheck.md)

Its grounding exists: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-13.md:10`
(M1) records the outside disagreement, the W04-only census behavior, and the S045 correction. The
paragraph at `QUALITY.md:36-39` states the lane-local screen is a conservative merge-review trigger,
uses the actual S017/S030 pair as its red-before case, and preserves rejected S030 in its green
state.

**Do not append a second `17.`** — the slot is occupied and the owner text covers the required
behavior. This is append-only discipline applied to the criterion itself.

### 2.2 Independent draft (retained for comparison; not appended)

> 17. A new active (`queued`/`mined`) source row that shares a canonical URL (scheme/host case-folded; fragment, default port and one trailing path slash removed; path/query otherwise preserved) with an active row is not admitted on a differing scope string: it needs an opening `supersedes S<id> —` link naming the earlier row or a human adjudication recorded in the round lesson; a `rejected` row is retained history and is ignored by the merge check. (lesson: `lessons/round-12.md` § Outside spot-check; `lessons/round-12-verifier-spotcheck.md:13`; contract rule 2)

The owner text and the independent draft agree on active-row URL screening, differing-scope
non-exemption, rejected-history preservation, and human review. The owner text leaves the mechanics
at “resolvable prior id”; the script supplies canonicalization, opening-position, pairwise and
non-transitive checks.

### 2.3 Optional append-only clarification (not a numbered criterion)

If the owner wants the script mechanics in `QUALITY.md`, append this paragraph **after**
`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:39` under the existing round-13
section:

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
in this report and the owner criterion 17 remains the bar.

### 2.4 Worked states

| State | Active rows on URL | Check result |
|---|---|---|
| `5174e15` | S017 `mined`, S030 `mined` | **FAIL**, `COLLISION S017 -> S030` |
| HEAD `7dcb785` | S017 `mined`, S030 `rejected` | **PASS**, `REJECTED_HISTORY S030`, exit 0 |
| current tree | S017 `mined`; S030/S045 rejected; S006 `queued` + S042 `mined` | **PASS**, `REJECTED_HISTORY S030` and `S045`, valid links S042→S006 and S045→S030 |
| New active row opens `supersedes S017 — …` | S017 + new | **PASS** for that pair |
| New active row supersedes only rejected S030 | S017 + new active | **FAIL** against S017; rejected history does not excuse an active pair |
| New active row on a distinct canonical URL | S017 + new | **PASS**; the S030 “distinct anchor” flip remains reachable via e.g. the 0.56.0 archive (ReviewSources F6) |

## 3. Merge check

Path: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/MistakeFix.py`.
Read-only; standard library only; `--selftest` reads nothing.

```sh
python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --selftest
python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry corpus/SOURCES.md
```

Exit map: `0` no live collision (rejected history allowed); `1` active-row collision requiring
review or a supersedes link; `2` usage/read/parse/policy error. Output: `COLLISION`,
`REJECTED_HISTORY`, `ERROR`, and a `PASS|FAIL|ERROR` summary with `rows`, `urls`, `no_url`,
`collisions`, `rejected_history`, `supersedes`, `errors`. `rejected_history` counts rejected rows
(not pairs); `supersedes` counts valid opening links (not collisions forgiven).

Deliberately narrow: row shape/id/status, a no-rows guard (empty or misshaped table → exit 2),
first URL in `source`, canonicalization (scheme/host case-fold; default port, fragment and one
trailing path slash removed; path/query otherwise preserved; trailing `.,;` stripped), credential
rejection, opening supersedes resolution (exists/earlier/self/forward), active-active URL collision,
rejected-history notes, and no-URL accounting. **Not** checked: scope semantics, tier/kind/anchor/
dates/used-by existence, append-only history, `REJECTED:`/`flip:` shape, URL aliases beyond the
listed normalization, Markdown link wrappers, redirects/canonical links, or rows whose URL is only
in `anchor` (the summary prints `no_url=N`).

Selftest: 25 in-memory fixtures. The four required L1 cases are present and named
`same-url-different-scope-still-collision`, `rejected-history-tolerated`,
`valid-supersedes-permitted`, `unknown-supersedes-rejected`; the S045-rejected-supersedes-S030 case
is `new-rejected-row-supersedes-rejected-s030`. Extras cover same-scope collision, not-opening,
other-id, forward, non-transitive chain, active-over-rejected, mined-supersedes-queued, URL
normalization, query/scheme distinctness, no-URL rows, mined-over-rejected, rejected-with-used-by,
three-row chain, duplicate id, malformed row, bad status, credential URL, and an empty registry
(`NO_ROWS`). Expected output: `MISTAKE_FIX_SELFTEST: PASS 25/25`
(`[INF]` from code review; L1 runs it).

Current-tree compatibility (by inspection, not run): S042's `teaches` opens `supersedes S006 — …`
(S006 is `queued`, earlier) and S045's opens `supersedes S030 — REJECTED: …` (S030 is `rejected`,
earlier). Both are valid pairwise exemptions. S045 is rejected and appears as a `REJECTED_HISTORY`
peer of active S017; S042 is active and is not a history note. S046 adds a unique URL
(`https://gitlab.freedesktop.org/wayland/wayland-utils/-/raw/1.3.0/wayland-info/wayland-info.c`);
it has no same-URL peer and does not collide. S040 and S043 are similarly unique. At the observation
the current registry is 46 rows; expect `PASS`, `collisions=0`, `rejected_history=2`,
`supersedes=2`, `errors=0`, exit 0. Counts may move if other seats append rows. At `5174e15` (39
rows, no S042/S045/S046), expect `COLLISION S017 -> S030`, `FAIL`, exit 1.

## 4. L1 runbook (not run here)

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --selftest
# expect PASS 25/25, exit 0

git show 5174e15:corpus/SOURCES.md > /tmp/mado-sources-5174e15.md
python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry /tmp/mado-sources-5174e15.md
# expect COLLISION S017 -> S030, FAIL, exit 1

python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry corpus/SOURCES.md
# expect PASS, collisions=0, exit 0; at the observed tree also
# REJECTED_HISTORY S030 and S045, supersedes=2
```

The `/tmp` input is a transient run artifact, not durable evidence (QUALITY criterion 13); the
durable record is the committed script plus the L1 receipt's quoted output/revision.

## 5. Findings, limits, routing

1. **Criterion already present** — `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:32-39`
   carries criterion 17 (integrated; uncommitted at observation). The independent draft converges;
   do not append a duplicate 17. Optional mechanical clarification: §2.3, appended under the
   existing section only.
2. **Fleet census boundary** — W04/E04 exact-scope keying cannot discriminate this class. The lane
   check is URL-only among active rows; the fleet-level normalized-URL fix remains with the fleet
   owner.
3. **S030 shape debt repaired append-only** — S045 opens `supersedes S030 — REJECTED: …` and leaves
   S030's immutable `teaches` untouched (ReviewSources F3 option (b)). Do not edit S030 in place.
4. **Supersedes tightening** — opening form + resolvable earlier id + exact pair + non-transitive.
   The current tree supplies two real cases: S042→S006 (queued predecessor) and S045→S030 (rejected
   predecessor). The fleet census's anywhere-match remains too permissive.
5. **Rejected history** — S030/S045 are retained rejection records; the check ignores them for
   collisions and reports them informationally. A rejected row with a non-empty `used-by` is still
   ignored here; registry hygiene is separate.
6. **False-positive posture** — any same-URL active pair is a review stop. A genuinely distinct
   scope is not auto-exempt; human adjudication or a distinct canonical URL is the route. This is
   intentional, not scope automation.
7. **Prevention, not row quantity** — the S030 flip raised the rejected tally 2→3 between `5174e15`
   and HEAD; that is a correction, not new taste evidence
   (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/AttackMistake.md:108`).
8. **Script is wave-local** — promote to `tools/` before citing it as a standing gate; it is not a
   replacement for `mado-verify.sh` or the fleet census.

## 6. Evidence

- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:114-124` — outside
  spot-check and post-review old→new table.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12-verifier-spotcheck.md:13` —
  non-author corroboration.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:29,42,106 @ worktree` and
  `:28,41,91 @ 8dbfc93` — S017/S030 rows and the search-log duplicate erratum; `:54,57 @ worktree`
  — S042/S045 current-tree supersedes rows.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md:32-39` — owner criterion 17 and
  the lane-local screen paragraph (uncommitted).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-13.md:10,35,38` — M1, S042
  supersedes S006, S045 supersedes S030.
- `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:49-51` — append-only and
  supersedes rule; `:34-35` rejected-row shape; `:75-76` census duplicate-id-only baseline.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/hyprland-config-era-r12.md:127` —
  S030→S017 citation erratum.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/ReviewSources.md:13-20,38` —
  W04/E04 exact-scope boundary and S045 option.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/AttackMistake.md:16-19,48-50,126,150` —
  `5174e15` census equality, anywhere-supersedes gap, T1 red/green.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/EvidenceLedger.md:40,44` —
  retained exact-URL census result.

No external URL was opened by this seat; the 0.56.0 archive is `[OBS-record]` via ReviewSources F6.

## 7. Files written

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/MistakeFix.md` — draft,
  criterion comparison and optional clarification (working paper).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/MistakeFix.md` — this
  report.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/reports/MistakeFix.py` — the
  read-only merge check.

No other file was modified. Tooling record: no installs or upgrades; no build/lint/test/formatter/
selftest/regression/live probe was run by this seat.
