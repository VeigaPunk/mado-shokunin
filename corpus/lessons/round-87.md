# mado round 87 — lessons

Round 87, hyaku run 15, attempt 1, after the operator's "Authorize all" lift (Amendment 27). Two frozen claims
from `.ufo/waves/round-87/claims-declaration-r87.md`: C1 capability (mako effective-settings resolution, coverage) and
C2 calibration (control-figure fidelity). The stagnation nudge applies (every axis at 10; no capability row since r82).
The frozen declaration was amended before any formal scoring; the errata are in its appended section.

## Mistakes

**M87-1 — a held-control figure came from the lane's own model, not the held counter.** Class: number-drift.
Evidence: `corpus/lessons/round-86-verifier-spotcheck.md` §2 (R1); `corpus/knowledge/refusal-records-clause-observations-r86.md`
line 112 (`held_rule_new_case=0/1`); `SCORECARD.md` round-86 C2 row. The held round-85 counter's own `case_correct` scores the
witness 1/1; the `0/1` came from `quality/counters/c2-r86-clause-observations.py:574` (`held_case_correct`), which does not
pass `anchor`. Captured-by: **none** — the r86 selftest asserted the model against itself (`:736-737`). Fix: the round-87
fidelity counter `quality/counters/c2-r87-control-fidelity.py` re-derives the figure from the held counter, and an append-only
correction block reconciles it (see the Correction blocks in the r86 entry and SCORECARD). The selftest-pinning gap is not in
the frozen predicate and stays a routed limit (see the declaration errata).

**M87-2 — a manual pin named the decompressed digest as the file's digest.** Class: reference-drift.
Evidence: the declaration's frontier pin `f717848f…` labelled `mako.5.gz`; the scout's pin table
(`.ufo/waves/round-87/w1/R87Scout.md` §1): the container hashes to `17ffc88c…`, and `f717848f…` is `zcat | sha256sum`.
Captured-by: **none** — the L1 computed `zcat | sha256sum` and wrote its result under the file path. Fix: both digests are now
pinned, with the container identity demonstrated (`gzip -9 -n` reproduces the installed bytes, per the scout); the errata
record the change.

**M87-3 — a stated text assumed to sit on one line.** Class: reference-drift.
Evidence: `.ufo/waves/round-87/w1/R87ReviewFidelity.md` R87RF-D1 (HIGH): the F2 `stated_at` text `flooding 48/75 vs held 75/75`
is line-wrapped in `SCORECARD.md` (line 5062 ends at `flooding`, line 5063 carries the numbers), so the counter exited 2 at the
base revision on every run. Captured-by: **none** — the figure file was written from the prose, not from a grep of the file it
names. Fix: `stated_at` is re-pointed to `48/75 vs held 75/75` (SCORECARD.md:5063) and the counter's presence check now fails
closed on an absent text.

**M87-4 — a surface was called "not held" without reading the lane's own notes.** Class: scope.
Evidence: the declaration's C1 surface sentence; `corpus/knowledge/waybar-walker-plane.md` §4 records the mako chain by hand
(OBS, core.ini lines and click actions) and `.ufo/waves/round-87/w1/R87Critic.md` (C1 WEAKENED). Captured-by: **none**
(the declaration was written without a grep of the lane's knowledge for `mako`). Fix: the basis is restated in the errata: the
held notes observe the chain, and no note resolves effective values. C1 claims only the resolver.

**M87-5 — a pin-free fixture set was attacked after it changed.** Class: landing.
Evidence: `R87Sentinel.md` F1/F2 and `R87MutTester.md` D1/D2 record a case file with `app_name`/`modes` keys, lowercase-invalid ids
and a `.config_mako/config` typo; the file on disk at the wave's close (22 cases, sha256 `0a955874…`) has the counter's keys and
the corrected path. Captured-by: the wave's own attack seats (after their reads), not the lane. Fix: the attacks were re-run
against the final bytes in this round's measurement; the earlier findings are recorded as void for the final file.

## Wave findings routed (instruments frozen or named as limits)

| finding | seat | severity | disposition |
|---|---|---|---|
| tool falls back to `$HOME` for `~/` includes when `--home` is absent | ReviewMako D1, Sentinel F3 | medium | **fixed**: refused with "needs --home" |
| bare `none` / `invoke-default-action` accept trailing words | ReviewMako D2 | medium | **fixed**: refused |
| refusal wording blames valid boolean syntax | ReviewMako D3 | low | **fixed** (wording) |
| symlinked include escaping HOME is read | Sentinel F4 | medium | named limit: the manual allows absolute include paths, so containment is a policy the manual does not state |
| 14 of 19 added mutants survive the frozen cases | MutTester D4/D5/D6 | medium | named limit: the frozen case set lacks casefold, prefix, include-cycle and symlinked-config cases; routed to round 88 as a superseding set |
| correction disjunct accepts a correction block whose value text is merely present | Critic C2-after, ReviewFidelity | medium | named limit: the block is human-authored; the counter checks the id and the literal value, not the reasoning |
| selftest pins the r86 model (`c2-r86-clause-observations.py:736-737`) | Critic C2-root | medium | named limit: not in the predicate; routed (the fix changes the r86 counter, which is frozen) |
| the F2 selftest stub is not a derivation | MutTester D10 | low | named limit: the real counter runs the r86 counter; only the selftest stubs it |
| `--expect-figures-sha256` absent from the declared command | MutTester D8 | medium | fixed in the measured command (the declaration errata record it) |
| `mako.5.gz` path is the only mako man page on the host | Scout §1 | info | noted |

## Gate

### Registry row (S493) — opened 2026-11-05

- Source: mako(5) manual text of the installed mako 1.11.0-1, locator `/usr/share/man/man5/mako.5.gz`.
- Container sha256 `17ffc88c9950ba83a60a8d5bdf4cb528ca994adc6ba58e9386a81617b9db1670`; decompressed text sha256
  `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba` (both by the scout seat, 2026-11-05).
- Located quote (≤25 words, line 47): "Includes a config at the specified path. The path must be absolute" (grammar digest, R87Scout §2.2).
- Tier A (installed documentation of the version the host runs); scope: mako config grammar, mako 1.11.0-1.

### Candidates considered (round 87)

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/mako-criteria-resolution-r87.md` (grammar, refusals, controls) | **admit** | each rule cites a manual line that the scout and the reviewer re-read; refusals name what the manual leaves unstated | a manual line that contradicts a rule |
| `#` mid-line as a comment | **reject** | manual line 24 states only whole-line `#`; the entry lists it as UNSTATED | a manual line stating mid-line comments |
| relative `include=` resolved from the including file | **reject** (not modelled) | manual line 48 states absolute or `~/` only; the resolver refuses | a manual line stating relative resolution |
| waybar-walker-plane §4 mako observations (reused) | **admit as held** | held note, re-read for the host anchors | host bytes that changed |
| "tool carries no defects" | **reject** | the wave found D1–D3 | a clean attack set across rounds |

### Spot-check

Pending: the non-author closure is the operator-dispatched verifier (LEARNING.md). This lesson records no spot-check result.

### Census

- Round start: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` exit 0, 427 rows
  (`receipts/census-start-r87.txt`).
- Round end: [[CENSUS]].

## Considerthese

`considerthese/2026-11-04.md` proposal 7 ("mark each figure as relayed or re-measured") is already held by QUALITY criterion 76,
which requires a `relayed:` label for every number a mining note repeats from `considerthese/`. No new criterion is added;
the figures in this round's entries carry their commands. Proposal 7's wording is not a second rule.

## Domain share

New artifacts this round: one knowledge entry (`mako-criteria-resolution-r87.md`, desktop-facing), one tool
(`tools/mado-mako.py`, desktop-facing: reads the mako config), two record counters (lane-internal). Desktop-facing: 2 of 4.
Command: `ls corpus/knowledge/mako-criteria-resolution-r87.md tools/mado-mako.py quality/counters/c1-r87-mako-criteria.py quality/counters/c2-r87-control-fidelity.py | wc -l` → 4.
