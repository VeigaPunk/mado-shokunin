# ExecC2Stability — C2 flake probe (two sequential re-demonstrations at base `8e5d9369`)

Leaf executor, mado round 24 wave 1. Assignment: run the frozen C2 counter twice in sequence at
`8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` (timeout 900 each), compare per-row observed/exit, record the
sha256 of the sibling harness `tameshi-shokunin/tools/mutate-and-run.sh` before and after, save both JSONs,
and name every row whose observed status differs or depends on mutable sibling or network state.

**Verdict: STABLE across the two runs — 12/12 rows have identical `observed`, `exit`, `ok`, `reason` and
`in_population`; both runs report `mismatches=1/12` (the base value). The single mismatch (`tripwire evidence
marker`, observed `fails`, exit 0) is a deterministic output-rule mismatch at this revision, not flake: a
one-shot diagnostic of the same argv reports `L` 15/18 where the frozen rule requires 17/18. Six rows read
mutable state outside the REV tree (two fleet scripts, three live-lane scripts, one network call, plus the
foreign git object stores the regression legs replay); none changed during the probe. Harness sha256 is
identical before, between and after both runs.**

## What I ran

CWD for both runs: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24`.

```
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh   # before
timeout 900 python3 -I c2/count.py 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122 --json > evidence/c2-stability-1.json
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh   # between
timeout 900 python3 -I c2/count.py 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122 --json > evidence/c2-stability-2.json
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh   # after
```

- Run 1: exit 1, wall 251 s, JSON written 2026-10-23 00:58:56 -03 (start derived from mtime minus wall,
  about 00:54:45). stderr empty.
- Run 2: exit 1, wall 255 s, JSON written 01:03:11 -03 (start about 00:58:56). stderr empty.
- Exit 1 is the counter's frozen "at least one mismatch" code (docstring exit map); it is the expected base
  value, not a flake signal.
- Both JSONs: `mado-r24-c2-count-v1`, `revision=8e5d9369…`, `population=12`, `mismatches=1`,
  `manifest_sha256=sha256:e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02`,
  `counter_sha256=sha256:a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8`,
  `status_table_present=false`.
- Receipts: `evidence/c2-stability-1.json` (6264 bytes,
  `sha256:2ccd1d5f4edb6d4f84b9552e5db4fdf6ea3066fea21b5e00431f06c568258094`) and
  `evidence/c2-stability-2.json` (6264 bytes,
  `sha256:fbaacadc940f484cb883f10f6196a3be08061c8b144d2648cc29fa78ab83f6cd`).
- The two files are not byte-identical because the counter substitutes its random scratch mkdtemp path into
  `argv`/`cwd` (`count.py:264-265`, `{TREE}`/`{CENSUS_ROOT}`). A full structural walk of both JSON trees shows
  17 differing scalar paths, all inside `argv`/`cwd`, differing only by the `run-<rev8>-<suffix>` directory
  name. Every semantic field (`name`, `stated`, `observed`, `ok`, `exit`, `reason`, `in_population`) is equal.

## Per-row result (both runs)

Stated is `works` for all 12 rows because the REV tree predates the round-24 status table
(`status_table_present=false` in both JSONs).

| # | capability | run 1 observed / exit | run 2 observed / exit | differs | external input |
|---|---|---|---|---|---|
| 1 | sources registry | works / 0 | works / 0 | no | fleet script (live working tree) |
| 2 | verdict gate (live + file plane) | works / 0 | works / 0 | no | archived REV tree only (`--no-live`) |
| 3 | hermetic self-test | works / 0 | works / 0 | no | archived REV tree only |
| 4 | mutation regression with re-cut | works / 0 | works / 0 | no | sibling harness + fleet git object stores + `/tmp` |
| 5 | post-hoc transcript tripwire | works / 0 | works / 0 | no | archived REV tree only |
| 6 | tripwire frozen replay (gate entry) | works / 1 | works / 1 | no | archived REV tree only (exit 1 is an allowed code) |
| 7 | landedness check | works / 0 | works / 0 | no | network (`git ls-remote origin`) |
| 8 | tripwire evidence marker | fails / 0 | fails / 0 | no | live lane working-tree script + LANE git objects |
| 9 | harness fail-closed check | works / 0 | works / 0 | no | archived REV tree only |
| 10 | tripwire reached-body sweep | works / 0 | works / 0 | no | live lane working-tree script + LANE git objects |
| 11 | detector removal-side guard | works / 0 | works / 0 | no | live lane working-tree script + LANE git objects |
| 12 | artifact-only assessment integrity | works / 0 | works / 0 | no | archived REV tree only |

No row's `observed` status, `exit` code, `ok` flag or `reason` string differs between the runs.

## The one mismatch is deterministic, not a flake

Row 8 (`tripwire evidence marker`, `manifest.json:93-103`) runs
`python3 {LANE}/.ufo/waves/round-20/tw-precision.py {REV}` with cwd `{LANE}` and a rule requiring
`"L": {"passed": 17, "total": 18}` and `"P": {"passed": 66, "total": 66}`. Observed in both runs: exit 0,
`reason="output did not match the frozen rule"`.

Diagnostic one-shot of exactly that argv (same REV, cwd the lane), not part of the timed pair:

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
timeout 600 python3 .ufo/waves/round-20/tw-precision.py 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122
```

exit 0 after 6.4 s, `schema=mado-tw-precision-r20-v1`, `rev=8e5d9369…`,
`tool_sha256=sha256:cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`,
`score=9.4857`, families `P 66/66`, `S 17/17`, `W 21/22`, `H 47/52`, `L 15/18`. The rule asks for L 17/18,
the bytes at this revision say L 15/18, so `fails` is stable and correct. Output retained in
`/tmp/tw-precision-r24.json` (scratch; the numbers are quoted here because the item names only the two
count JSONs as lane evidence). This is measurement, not adoption of the sibling SCORECARD status table; the
numbers happen to agree with its row for this capability.

## Rows that depend on mutable sibling or network state

None of these flipped during the probe, but each can change without any change to the REV tree. This is the
asked-for list (reason included):

1. **sources registry (row 1)** — executes the live fleet script
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (`manifest.json:9`), which is outside the REV
   tree and outside the archived census root. `sha256:3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`
   before and after both runs (35466 bytes, mtime 2026-10-19 21:22:45 -03). A sweep for `curl`, `wget`,
   `ls-remote`, `git fetch`, `git clone` and live URLs found no network verb or non-fixture URL in the script
   (the only `https://` strings are test-fixture rows), so it is sibling-mutable but not network-dependent.
   It flips only if an edit changes census check behaviour or the `mado<TAB>ok` line.
2. **mutation regression with re-cut (row 4)** — `MADO_VERIFY_HARNESS` points at the live sibling
   `tameshi-shokunin/tools/mutate-and-run.sh` (`manifest.json:47`). Its sha256 is identical before, between
   and after the runs: `sha256:fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de`
   (102681 bytes, mtime 2026-10-22 07:04:10 -03, unchanged). The gate prints the harness sha as *provenance,
   not gated* (`tools/mado-verify.sh:2257-2258`); the recorded revision
   `sha256:b56c6e57…` already differs from the current harness and PASS still holds, so a sibling edit is
   consumed silently and the row flips only if the edit changes sweep behaviour (the 10-defect kill table or
   SETUP arms, `tools/mado-verify.sh:2245,2292`). The row also replays pinned revisions out of other fleet
   repositories' git object stores and needs writable `/tmp` and 600 s of CPU; heavy concurrent load or a
   damaged foreign repo could turn it into SETUP/FAIL or a timeout (124).
3. **landedness check (row 7)** — network by contract:
   `git -C "$LANE" ls-remote origin refs/heads/master` under `timeout 60`
   (`.ufo/waves/round-19/landed-check.sh:78,87-88`). A network or remote-configuration failure exits 2, which
   is not in the row's `exit_ok` and would flip observed to `fails`. Forward movement of the remote master
   would *not* flip the observed status, because `LANDED`, `LOCAL_ONLY` and `MISSING` all satisfy the frozen
   rule (`manifest.json:81-91`); only the setup-failure arm changes the counter's answer.
4. **tripwire evidence marker (row 8), tripwire reached-body sweep (row 10), detector removal-side guard
   (row 11)** — the argv executes `{LANE}/.ufo/waves/round-20/...` scripts from the **live lane working
   tree**, not from the archived REV tree (`manifest.json:94,119,132`; `{LANE}` substitution at
   `count.py:239,264-265`). They read committed bytes through the lane repo (`tw-precision.py:18,31`,
   `a2-guards.py:53`; fixture pin `6a7d9ca0…` for rows 10-11). During the probe window the lane advanced
   (see below), but
   `git diff --name-only 8e5d9369 HEAD -- .ufo/waves/round-20 tools/ SCORECARD.md` returns only
   `SCORECARD.md`, so the executed scripts were byte-identical to the REV copies. An uncommitted or later
   committed edit to `.ufo/waves/round-20/` (or a checkout in progress at the moment a row starts) silently
   changes what a base-REV count measures.

Rows 2, 3, 5, 6, 9 and 12 execute only files extracted from REV (`git archive`, `count.py:124`) and have no
sibling or network input. They still share the host toolchain (`bash`, `python3`, `git`, `tar`, `timeout`)
and `/fast/scratch` space, which the probe held constant.

## State captured around the probe

- Sibling harness `mutate-and-run.sh`: `sha256:fb91ef76…` before, between and after; content, size and mtime
  unchanged.
- Fleet census script: `sha256:3fb72615…` before and after.
- Lane HEAD moved twice around the probe: `464a024` committed 2026-10-23 00:53:36 -03 (control receipts),
  `81955bd` 00:55:57 -03 (round-24 status table appended to SCORECARD), `cf86f9e` 01:03:16 -03 (C1 note,
  5 s after run 2 wrote its JSON). Neither commit entered the counted tree because the counter archives REV
  by object id; `status_table_present=false` in both JSONs confirms no status-table row names any of the
  twelve capabilities at REV (that table landed in `81955bd`, after the base commit).
- Working tree at the end of the probe window: only untracked round-24 files (`git status --porcelain`), no
  tracked modification.
- Concurrent seats were running the same counter: scratch has foreign `run-6239f342-…` (01:00) and
  `run-8e5d9369-…` (01:03) directories; my two run directories were removed by the counter's own cleanup.
  Wall time did not drift from the base smoke (251 s / 255 s versus 248.18 s).
- Read-only posture: `tools/` untouched, no write verb against the lane or fleet repo, no package or service
  change, no `hyprctl` call, no installs or tool updates.

## Files changed

| Path | State | sha256 / size |
|---|---|---|
| `.ufo/waves/round-24/evidence/c2-stability-1.json` | new evidence | `sha256:2ccd1d5f4edb6d4f84b9552e5db4fdf6ea3066fea21b5e00431f06c568258094`, 6264 B |
| `.ufo/waves/round-24/evidence/c2-stability-2.json` | new evidence | `sha256:fbaacadc940f484cb883f10f6196a3be08061c8b144d2648cc29fa78ab83f6cd`, 6264 B |
| `.ufo/waves/round-24/w1/reports/ExecC2Stability.md` | this report | — |

Nothing else was written in the lane. No lane source file, counter, manifest or SCORECARD byte was edited.

## What this probe does not establish, risk and blockers

- The probe did not inject a network failure, a harness edit or a working-tree swap; the dependency claims
  above are read from the frozen command paths and the tools' own contracts, not from a negative experiment.
  Under injection, rows 1, 4, 7, 8, 10 and 11 are the ones expected to move; [INFERENCE] for how each would
  land.
- The counter does not report per-row durations, so the 600 s regression timeout margin is unknown; only the
  whole-run walls (251 s / 255 s) are measured. Under much heavier sibling load, row 4 could time out and
  flip to `fails`/124.
- The probe was run at base `8e5d9369` as assigned. It says nothing about the landed tip; the current HEAD
  SCORECARD now carries the round-24 status table, so a tip count would be a different measurement and was
  not run here (`evidence/c2-after-81955bd5.txt` exists in the lane but was not opened or judged).
- Host behaviour remains [UNK]: no compositor or session read was needed or performed.
- Risk carried by the design, not this run: three rows measure live-lane scripts against a pinned REV, and one
  row measures a sibling harness whose digest is provenance-only. A stable pair of runs today does not freeze
  those inputs.
- Blockers: none.

Report: .ufo/waves/round-24/w1/reports/ExecC2Stability.md
