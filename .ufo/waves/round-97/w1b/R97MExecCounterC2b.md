# R97MExecCounterC2b — C2 counter finalised to PRED-C2-r97-v1 (v2)

Seat: `R97MExecCounterC2b` (leaf; no subagent dispatch; no tools installed — no pacman /
uv / npx / binary install, nothing to record per the tooling directive). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base `e6152b589c2c6a28426c28263c4bcc3c46398be4`.
All probes read-only except the scratch fixture repo (own `git init` under `$S`, hygiene
assert `git rev-parse --show-toplevel` == fixture dir before every mutating call; no
commit anywhere in the lane or fleet repos). Scratch deleted before yield.

## Files changed

- `.ufo/waves/round-97/build/c2-r97-counter-selftest.v2.py` (new; 663 lines) — sha256
  `abb17a019141c57635f1c9771ad449a4348dfdc75a0bb57af3776075fe06b879`, ASCII-only,
  `python3 -m py_compile` clean, stdlib only (`argparse hashlib io json os re shutil
  subprocess sys tarfile tempfile`; subprocess is the counters' sanctioned git
  transport, as in the r96 counters).
- `.ufo/waves/round-97/w1b/R97MExecCounterC2b.md` (this report; trailer below).

The w1 draft `build/c2-r97-counter-selftest.py` (sha `5bb9a8b6…`) was read, never edited.

## CLI (every argument named; the published counting command uses exactly these 11)

```
python3 -I quality/counters/c2-r97-counter-selftest.v2.py --repo . --rev <rev> \
  --base-rev e6152b589c2c6a28426c28263c4bcc3c46398be4 \
  --expect-base-registry-sha256 <BASESKILL> \
  --panel .ufo/waves/round-97/controls/counter-selftest-panel-v2.json \
  --expect-panel-sha256 <PANEL> --expect-c1-sha256 <C1COUNTER> --expect-c2-sha256 <C2COUNTER> \
  --expect-registry-sha256 <SKILL> --expect-ledger-sha256 <LEDGER> --scratch-root <SCRATCH>
```

Optional: `--timeout SEC` (default 600, per child invocation) and `--min-checks N`
(default 6 — the frozen predicate floor; exists only so a scratch dry run can score a
two-check panel; the published command omits it, so `checks >= 6` applies at measurement).

## Behavior (contract 4 + the revised predicate, R97MReviewC2 findings 3.1-3.4)

- SETUP_ERROR (rc 2, exactly one `MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR …` line) on:
  repo/rev/base-rev unusable, panel missing/unparsable/sha-mismatch/malformed (per-counter
  `checks >= min-checks`, both declared counters present, `broken` rows >= 3 per counter,
  modes `missing-input|wrong-rev|mutated-tool`, `expect_exit` in {1,2}, mutated-tool rows
  carry a relative fixture `path` that exists under a materialised fixture root), any
  `--expect-*` sha mismatch (panel, c1, c2, SKILL@rev, SKILL@base, ledger@rev), absent
  SKILL.md / ledger / check-tool-ledger.py / counters at the pinned revision, or no
  `.ufo/waves/round-97/selftest-fixtures*` tree at `--rev`.
- Counter pin: both counters materialised with `git show <rev>:<path>` at
  `<root>/quality/counters/<name>.py` (repo-shaped layout; agreed with R97MExecC2b so
  their `__file__` walk resolves the materialised fixtures); sha pinned →
  `counter_pin=ok,ok`.
- Fixture tree: every `.ufo/waves/round-97/selftest-fixtures*` tree at `--rev`
  materialised at the same relative path; the invoked fixture root is
  `selftest-fixtures-v2` when present, else `selftest-fixtures` (printed as
  `fixtures root=…`), matching R97MExecC2b's resolution preference.
- Support tree (R97MMutC2b's measured blocker): the landed counters' REPO-dependent
  selftest checks open `quality/check-selftest-strength.py` and
  `quality/check-receipt-presence.py` under REPO = the layout root, so the runner
  extracts `quality/`, `tools/` and `SKILL.md` byte-exact from `--rev` with
  `git archive` (pathspecs existence-checked; the 500MB+ `.ufo` history is deliberately
  not extracted) and SETUP_ERRORs if the two quality sentinels are absent at `--rev`.
  `MADO_SELFTEST_REPO=<layout root>` is set in every child env (R97MExecC2 reads it
  first for REPO).
- Invocation shape (settled with R97MExecC2b and R97MMutC2b): the fixture TREE ROOT is
  passed EXPLICITLY as `--fixture-dir <abs>` on every selftest-form run —
  green/neutralise: `<root>/<fixture-root>`; missing-input: `<scene>/absent-fixtures`
  (nonexistent); wrong-rev: `<scene>/<fixture-root>` (truncated tree); mutated-tool:
  `<scene>/<fixture-root>` (tampered tree). The counters must treat a given
  `--fixture-dir` that is absent/unparseable as terminal SETUP_ERROR (their seat asked
  for exactly this; their chain is `--fixture-dir > --repo > __file__ walk`, never cwd,
  never a lane constant). If a counter does NOT declare the flag (argparse rc 2 with
  "unrecognized arguments"), the invocation is retried ONCE with the bare contract-4
  spelling and its own resolution governs (printed as an `invocation` detail line); a
  counter-side SETUP_ERROR is never retried (unit-verified both branches). The always-OK
  stub and the base-revision control take no `--fixture-dir` (the stub is this runner's
  own file; the base bytes refuse `--selftest` at argparse before any fixture access).
- Leg (i): each counter run as `python3 -I <layout>/quality/counters/<name>.py --selftest …`
  with cwd = layout root, env `PATH=/usr/bin:/bin`, HOME/TMPDIR inside the run dir;
  green = rc 0 + `MADO_COUNTER_SELFTEST: checks=N failed=0` with `N >= min-checks` and no
  `MADO_COUNTER_SELFTEST_FAIL:` lines → `selftest_green=x/2`, `checks=<c1>,<c2>`.
- Leg (ii): every panel neutralisation applied to the counter's own bytes (`find` must
  occur exactly once), rerun `--selftest` at the counter's real layout path (originals
  restored) so `__file__`-relative resolution sees the same layout as the green run;
  credited = rc 1 AND the declared FAIL id AND the id absent from the counter's green-leg
  baseline (see the always-OK bullet below for the full credit rule);
  `negative_ids == panel`, survivors printed as `SURVIVED`.
- always-OK control (R97MCritic2 C2-5, L1-strengthened): the ECHO stub prints the result
  line AND every panel id as `MADO_COUNTER_SELFTEST_FAIL:` lines at exit 1 while doing no
  work (ids passed as argv after `--selftest`); a stub baseline run (no ids) is taken
  once. The credit rule requires the judged instrument's OWN bytes to carry the row's
  `find` anchor exactly once, the run to exit 1 with the declared FAIL id, AND the
  unneutralised baseline of the same instrument (the green-leg output for the counter,
  the stub baseline for the stub) not to print that id already. The stub's bytes carry no
  anchor, so it is credited with none; the clause is "the counter rejects the stub on
  every neutralisation" (R97MCritic C2-3): the result line prints
  `always_ok_flagged=0 stub_uncredited=<panel>/<panel>` and both are required. Under the
  earlier "rc 1 + id in output" rule this stub would have been credited panel_total
  times (TARGET_MISSED) — the strengthened rule is what makes the control bite.
- Leg (iii): every `broken` row runs its OWN counter's `--selftest` (never this runner's
  bytes). Every invocation runs the counter from the layout root (cwd = layout root,
  `MADO_SELFTEST_REPO` set), so REPO always sees the same quality/ support tree and the
  mode isolates fixture state only, via `--fixture-dir`: missing-input hands a fixture
  dir that does not exist; wrong-rev hands a `selftest-fixtures-wrongrev-<i>` sibling
  inside the layout root whose files are truncated to 0 bytes (the `--base-rev` fixture
  state); mutated-tool hands a `selftest-fixtures-mutated-<i>` sibling whose fixture
  file named by the row's `path` carries a trailing tamper line. Required = rc
  `expect_exit` AND `expect_line` substring; `broken_modes=x/y broken_c1=a/na
  broken_c2=b/nb` printed. R97MExecC2b's landed behavior per their note — missing-input:
  FAIL ids at rc 1 (never green); wrong-rev: each fixture-reading check fails with its
  own id; mutated-tool (marker appended to the panel-named `c1/dummy-mimetext.py` /
  `c2/dummy-tool.py`): the pin check id `st-tool-pin` — is whatever R97MMutC2b freezes
  into `expect_exit` / `expect_line`; enforcement is mechanical.
- Leg (iv) controls: base-revision counters refuse `--selftest` (argparse rc 2, 0/2
  green) → `base_refuse=ok`.
- Registry (3.1, R97MCritic C2-2): counts re-derived from `SKILL.md` at BOTH `--base-rev`
  and `--rev` for the three named INSTRUMENTS (`tools/mado-mimetext.py` and the two
  counters), counted as per-artifact COVERAGE (an instrument counts once when >= 1 table
  row names it). The receipt-presence kill-set is a pinned input named inside the
  existing `mado-selftest-strength` row's population, not a registry row, so it is not
  counted. Printed `registry=<b>-><r>` (declared 1->3) plus per-artifact pair counts for
  diagnosis.
- Ledger (3.2/3.4): membership read from `quality/tool-ledger.md` at `--rev` (table rows
  naming each counter path) → `ledger_members=x/2` (invariant, required 2/2), then
  `quality/check-tool-ledger.py` materialised from `--rev` and run as
  `--repo <repo> --rev <rev>` requiring `uncovered=0` (the checker's LEDGER summary line
  is echoed).
- Result: exactly one `MADO_COUNTER_SELFTEST_COUNT:` line; rc 0 TARGET_MET / 1
  TARGET_MISSED / 2 SETUP_ERROR. MET requires: pin ok, 2/2 green with checks >= floor,
  `negative_ids == panel_total (>= 2*min-checks)`, `broken_modes == broken` with >= 3 ok
  per counter, `base_refuse=ok`, `always_ok_flagged=0`,
  `stub_uncredited=panel/panel`, registry `1->3`,
  `ledger_members=2/2`, ledger `uncovered=0`.

## Exact retained evidence (scratch `/fast/scratch/hyaku/mado-r97/R97MExecCounterC2b`, deleted)

Fixture: a two-commit git repo (`base` = no-`--selftest` synthetic counters, 1-row
SKILL.md; `rev` = selftest-enabled synthetic counters resolving their KEY subtree under
the committed `.ufo/waves/round-97/selftest-fixtures/` tree via `--fixture-dir` (or the
`__file__` walk), 4-row SKILL.md plus the amended strength row naming the kill-set a
second time, ledger with 5 rows (the two quality support stand-ins included so the
runner's sentinel gate and the ledger checker's population rule both hold), the real
`quality/check-tool-ledger.py` copied in, and `quality/check-selftest-strength.py` /
`quality/check-receipt-presence.py` stand-ins committed for the support-tree sentinels).
Panel: two checks per counter (ids `src-marker`, `src-pin-check`; each `find` verified to
occur exactly once) + 3 broken rows per counter (missing-input → 2/"SETUP_ERROR",
wrong-rev → 2/"SETUP_ERROR", mutated-tool path `c{1,2}-r96/dummy_tool.py` →
1/"MADO_COUNTER_SELFTEST_FAIL: pins-match").

- Green dry run (`--min-checks 2`, two-check panel), rc 0 — the echo stub ran at rc 1
  printing every panel id (`stub <path> <id> rc=1 flagged=False` on all four rows) and
  was credited with none:

```
MADO_COUNTER_SELFTEST_COUNT: TARGET_MET pred=PRED-C2-r97-v1 rev=d1428a50… base=a03c69f9…
counter_pin=ok,ok selftest_green=2/2 checks=3,3 negative_ids=4/4 broken_modes=6/6
broken_c1=3/3 broken_c2=3/3 base_refuse=ok always_ok_flagged=0 stub_uncredited=4/4
registry=1->3 ledger_members=2/2 ledger_uncovered_ok=True
```

with `registry artifacts covered base=1 rev=3` — the kill-set row still present in the
fixture SKILL.md is not counted (instruments only, R97MCritic C2-2). Ledger leg printed
the real checker's `LEDGER: population=5 ledger_rows=5 uncovered=0 dangling=0
bad_pointer=0 empty_desc=0 verdict=TARGET_MET`.
- Red dry run (missing panel), rc 2:
  `MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR pred=PRED-C2-r97-v1 panel …/no-such.json missing`.
- Landed-bytes layout verification (scratch, deleted): reproducing the runner's exact
  layout shape by hand (landed counter bytes at `quality/counters/<name>.py`, the two
  quality support files, the counters seat's committed-fixture tree at
  `.ufo/waves/round-97/selftest-fixtures/`, cwd = layout root, `MADO_SELFTEST_REPO` set,
  explicit `--fixture-dir`), BOTH landed counters' `--selftest` printed
  `MADO_COUNTER_SELFTEST: checks=7 failed=0` and exited 0 — R97MMutC2b's measured
  blocker (`checks=7 failed=4`: C2-green-target-met / C2-missing-panel /
  C2-wrong-rev-pin / C2-mutant-mismatch, all REPO-dependent reads) is fixed at the
  runner level.
- Retry branch unit-verified against the final bytes: a `--selftest`-only counter run
  with `--fixture-dir` prints `invocation …: --fixture-dir refused (unrecognized
  arguments); retried bare` and returns the bare run's green result; a counter printing
  `SETUP_ERROR` at rc 2 is not retried.
- Four defect fixes found by these dry runs, all in the RUNNER (fixture-side bugs exposed
  real runner hazards): (1) neutralised bytes must land at the counter's real layout path
  (a sibling `neutralised.py` breaks `__file__`-relative fixture derivation and every
  neutralisation SETUP_ERRORs); (2) broken scenes under the layout root leak the layout's
  fixtures to upward walks (missing-input scored rc 0 green) — scenes now live in a
  sibling of the root; (3) a `NameError` on early SETUP_ERROR (`scenes_dir` referenced in
  `finally` before assignment); (4) the fixture root handed to a counter is the TREE ROOT
  (`selftest-fixtures[-v2]`), whose per-counter subtree the counter resolves itself — the
  first cut passed the tree root to synthetic counters that expected their subtree,
  SETUP_ERRORing the whole green leg until the resolution contract matched
  R97MExecC2b's.

## Coordination

- `R97MMutC2b` (panel owner): received the full broken-row contract — per-row `counter`,
  the three constructions with the exact invocation per mode, `always_ok_flagged`
  semantics, `--min-checks`; their blocker (counters falling through to lane fixtures)
  is answered by the explicit `--fixture-dir` plus the sibling-scene isolation; with
  R97MExecC2b's landed ids the panel declares `mutated-tool` rows against
  `c1/dummy-mimetext.py` / `c2/dummy-tool.py` expecting `st-tool-pin`.
- `R97MReviewC2b`: their registry pairs-vs-coverage finding and their
  flag-less-counter finding are both folded (coverage counting; discriminating bare
  retry), progress note with the final sha sent.
- `R97MExecC2b`: their (a)/(b) requests already hold — the runner materialises the
  counters at `quality/counters/<name>.py` inside the layout root and the fixture tree at
  the exact relative path, and additionally passes the tree root explicitly as
  `--fixture-dir` (their preferred resolution arm), so no `--repo` addition is needed.

## Risks / blockers for the L1

- The invocation contract assumes the landed counters declare `--fixture-dir` (they do,
  per R97MExecC2b's resolution note); flag-less counters fall back to the bare spelling
  via the retried invocation, where their own resolution governs.
- Explicit-dir-terminal (a given `--fixture-dir` that is absent ⇒ SETUP_ERROR, no
  fallback) is assumed per the counters' seat; if a landed counter falls through
  instead, the missing-input row's declared expectation simply changes (the panel is
  frozen against the landed bytes by R97MMutC2b).
- The fixtures are materialised from every `.ufo/waves/round-97/selftest-fixtures*` tree
  at `--rev`; the invoked root prefers `-v2`, else the contract-4 name.
- Runtime: serial child invocations (~40 with a 14-row panel); the r96 counters' selftests
  run mini production runs, so the measurement may take tens of minutes — `--timeout` is
  per invocation, there is no global deadline.

## Checks for the main agent

- `python3 -m py_compile` + `sha256sum` of `build/c2-r97-counter-selftest.v2.py` ==
  `abb17a01…6b879` (663 lines).
- After the L1 lands the counters, panel and SKILL/ledger: replay the counting command
  (with the freeze's sha pins) from the lane root and expect rc 0 with
  `counter_pin=ok,ok selftest_green=2/2 negative_ids==panel broken_modes==broken
  base_refuse=ok always_ok_flagged=0 stub_uncredited=panel/panel registry=1->3
  ledger_members=2/2 ledger_uncovered_ok=True`.

Report: .ufo/waves/round-97/w1b/R97MExecCounterC2b.md
