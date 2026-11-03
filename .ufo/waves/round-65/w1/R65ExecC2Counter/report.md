# R65ExecC2Counter — `quality/counters/c2-r65-landing-instrument.py` (claim C2)

Draft for L1 integration (nothing written into `quality/`):

| file | sha256 | size |
|---|---|---|
| `.ufo/waves/round-65/w1/R65ExecC2Counter/c2-r65-landing-instrument.py` | `b8658db640142a011a5b8d421b8f037bfb74a63fabd5bd12b4e04116b00e18b7` | 253 lines |
| `selftest.log` (real-instrument selftest leg, retained) | `4eeec7ee31cda1d1966878f21a57c5c2433f70e59a92cdb34e713a428ace6c44` | 1484 B |
| `landing.log` (real-instrument landing leg, retained) | `2b2ff887698b52ab473c9c26770b8f0e81c77012d8834224bc294ddae155e4e6` | 1572 B |
| `proofs.out` (full battery transcript) | `8b2327abc8e8b0627db7bc55cfef78cc72a0fec4680e1621bf49f8d9490e070d` | 8143 B |

Python 3.14.8, stdlib only (`argparse os shutil subprocess sys`). Frozen contract:
`.ufo/waves/round-65/claims-declaration-r65.md` §C2 + the seat prompt.

Report-path note: the trailer names `.ufo/waves/round-65/w1/R65ExecC2Counter.md`; the wave
write bound restricts every seat write to its own seat dir, so this report is filed at
`.ufo/waves/round-65/w1/R65ExecC2Counter/report.md` with an identical copy at
`.ufo/waves/round-65/w1/R65ExecC2Counter/R65ExecC2Counter.md`.

## What the counter implements (frozen steps, verbatim)

1. `git ls-tree --name-only <rev> -- quality/landing-counters.sh` must name exactly one path;
   otherwise `MADO_R65_INSTRUMENT: instrument=absent verdict=TARGET_MISSED rev=<rev> rc=1`, exit 1.
2. `git archive <rev> -- <4 paths> | tar -x -C <work>/wt`, preserving repo-relative paths;
   any missing extraction target fails closed:
   `MADO_R65_INSTRUMENT: reason=extraction-incomplete missing=<paths> verdict=TARGET_MISSED rev=<rev>`, exit 1.
3. `bash <work>/wt/quality/landing-counters.sh --selftest --scratch-root <work>/st` → own rc.
4. `bash <work>/wt/quality/landing-counters.sh --repo <abs> --rev <rev> --scratch-root <work>/run`
   → own rc + full stdout to `<work>/landing.log`.
5. `MADO_R65_INSTRUMENT: selftest=<rc> landing=<rc> green=<yes|no> verdict=TARGET_MET|TARGET_MISSED rev=<rev>`;
   exit 0 iff `selftest rc=0 AND landing rc=0 AND 'MADO_LANDING_COUNTERS: GREEN' in landing stdout`.

Scratch: `--scratch-root` required, `realpath`-resolved; refused (exit 2, one stderr line, no
verdict) when it is itself a symlink or resolves under `/tmp`/`/var/tmp`. Work dir
`<scratch>/c2r65-<pid>/` (with `wt/ st/ run/`) is removed in a `finally` block.

## Proofs (command → stdout, exit code)

Battery driver: `bash /fast/scratch/hyaku/mado-r65/w1/R65ExecC2Counter/proofs.sh` → `rc=0`
(transcript `proofs.out`). Draft identity: `sha256sum`/`wc -l`/`ast.parse` → AST_OK, 253 lines.

### P1 — MISS leg at base (required)

```
$ python3 <draft> --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --rev 524fa1f90b1f2de44b3019bacf833d54e0af13a0 \
    --scratch-root /fast/scratch/hyaku/mado-r65/w1/R65ExecC2Counter/st
MADO_R65_INSTRUMENT: instrument=absent verdict=TARGET_MISSED rev=524fa1f90b1f2de44b3019bacf833d54e0af13a0 rc=1
EXIT=1
```

### P2 — MISS at the contract rev (sanity: instrument still absent)

```
$ python3 <draft> --repo …/mado-shokunin --rev cb63ab13ccaf85191318701d5db5ace050bd5bd4 \
    --scratch-root …/st2
MADO_R65_INSTRUMENT: instrument=absent verdict=TARGET_MISSED rev=cb63ab13ccaf85191318701d5db5ace050bd5bd4 rc=1
EXIT=1
```

### P3–P6 — scratch-root refusals (required)

```
$ … --scratch-root /tmp/c2r65-probe
MADO_R65_INSTRUMENT: scratch-root refused: /tmp-family root: /tmp/c2r65-probe (real path /tmp/c2r65-probe)
EXIT=2
$ … --scratch-root /var/tmp/c2r65-probe
MADO_R65_INSTRUMENT: scratch-root refused: /tmp-family root: /var/tmp/c2r65-probe (real path /var/tmp/c2r65-probe)
EXIT=2
$ ln -s …/st …/link-to-st; … --scratch-root …/link-to-st
MADO_R65_INSTRUMENT: scratch-root refused: path is itself a symlink: …/link-to-st
EXIT=2
$ ln -s /tmp …/link-to-tmp; … --scratch-root …/link-to-tmp/st
MADO_R65_INSTRUMENT: scratch-root refused: /tmp-family root: …/link-to-tmp/st (real path /tmp/st)
EXIT=2
```

### P7 — fixture battery (stub instrument: orchestration/discrimination only)

Fixture repo: `git clone --shared` of the lane into scratch, toplevel asserted
(`git -C <fixture> rev-parse --show-toplevel` = fixture realpath) before every commit; commits
carry only the stub instrument / one deleted dependency. Rows are the counter's exact stdout
and exit code:

| variant (fixture commit) | counter stdout | exit |
|---|---|---|
| v1 green stub | `selftest=0 landing=0 green=yes verdict=TARGET_MET` | 0 |
| v2 landing RED / rc 1 | `selftest=0 landing=1 green=no verdict=TARGET_MISSED` | 1 |
| v3 selftest rc 3, landing GREEN | `selftest=3 landing=0 green=yes verdict=TARGET_MISSED` | 1 |
| v4 GREEN token but landing rc 1 | `selftest=0 landing=1 green=yes verdict=TARGET_MISSED` | 1 |
| v8 GREEN only on stderr, rc 0 | `selftest=0 landing=0 green=no verdict=TARGET_MISSED` | 1 |
| v5 citecheck deleted at rev | `reason=extraction-incomplete missing=tools/mado-receipt-citecheck.py verdict=TARGET_MISSED` | 1 |

Each stub also echoed its argv into the retained logs, proving the contract mapping: selftest
gets `--scratch-root <work>/st`; landing gets absolute `--repo <fixture>`,
`--rev <fixture sha>`, `--scratch-root <work>/run` (see `selftest.log`/`landing.log`).

### P8 — integration against the real sibling instrument

Sibling draft bytes pinned at `sha256 c12b72e20cfaeb92e7ff242b26f2a26eecd6184610e78287fb7b326a30fd5e9a`
(copied into the fixture at `quality/landing-counters.sh`, fixture rev `c314e284…`):

```
$ python3 <draft> --repo <fixture> --rev c314e28484e03dbc53869e6722736c5ca8e51144 \
    --scratch-root …/fx-st-real
MADO_R65_INSTRUMENT: selftest=0 landing=0 green=yes verdict=TARGET_MET rev=c314e28484e03dbc53869e6722736c5ca8e51144
EXIT=0
```

`selftest.log` ends `MADO_LANDING_COUNTERS_SELFTEST: 19/19 assertions passed`;
`landing.log` carries all four legs rc=0 (`nav indexed=78/78 … coverage=10.0000/10`;
`MADO_USED_BY … TARGET_MET`; `LEDGER … population=104 … TARGET_MET`;
`MADO_CITECHECK … missing=0 … TARGET_MET`) and the summary
`MADO_LANDING_COUNTERS: GREEN (nav=0 usedby=0 ledger=0 citecheck=0 rev=c314e284…)`.

### P9 — object-only read proof

After the fixture worktree was checked out to `cb63ab13` (`WORKTREE_HAS_INSTRUMENT=no`), the
counter scored the earlier stub rev again: `selftest=0 landing=0 green=yes verdict=TARGET_MET`,
exit 0 — the instrument bytes come from git objects at `--rev`, never the worktree.

### P10 — edge observation: nonexistent `--repo`

```
$ … --repo …/no-such-repo --rev HEAD …
MADO_R65_INSTRUMENT: ls-tree rc=128: fatal: cannot change to '…/no-such-repo': No such file or directory   (stderr)
MADO_R65_INSTRUMENT: instrument=absent verdict=TARGET_MISSED rev=HEAD rc=1
EXIT=1
```

Fail-closed, one stdout verdict line; the git diagnostic stays on stderr.

### P11 — relative `--repo` is resolved before use

```
$ cd …/R65ExecC2Counter && python3 <draft> --repo fixture --rev becc9e36ca28… --scratch-root …/st-rel
MADO_R65_INSTRUMENT: selftest=0 landing=0 green=yes verdict=TARGET_MET rev=becc9e36ca28a728bf87a3ab82570e52564d7a7d
EXIT=0
child landing argv (retained log): repo=/fast/scratch/hyaku/mado-r65/w1/R65ExecC2Counter/fixture
```

The child instrument always receives an absolute `--repo`, as the sibling contract requires.

## Design decisions / additions beyond the frozen steps (flagged for L1 + critic)

1. **Evidence sidecars (addition, in-scratch only).** The seat prompt requires copies of both
   legs' outputs in the seat dir, but the frozen contract removes `<work>` in `finally`. The
   counter therefore retains `<scratch>/c2r65-<pid>.selftest.log`, `…landing.log`, and
   `…landing.err.log` (only when non-empty) before cleanup. They stay under the caller's own
   scratch root, so the instrument policy "writes only under its scratch root" holds; the
   frozen `<work>/landing.log` is still written first. `selftest.log`/`landing.log` in this
   seat dir are those sidecars from P8.
2. **`--scratch-root` is created when missing** (`os.makedirs(..., exist_ok=True)`; failure →
   exit 2). Needed because the work dir lives under it; an unusable root never produces a
   verdict.
3. **Hardening, fail-closed only:** 1800 s per-leg timeout → rc 124; unexecutable `bash`/`tar`
   → rc 127; the counter's own git calls run with `GIT_*` stripped so ambient `GIT_DIR` cannot
   redirect the object read; children inherit the caller's full environment (the instrument
   contract requires that).
4. **Absent line carries the literal `rc=1` token** exactly as the seat prompt's print spec
   writes it; the process also exits 1.

## Findings / defects seen (outside my write scope)

- **Sibling draft cannot be run in place.** `bash .ufo/waves/round-65/w1/R65ExecLandingCounters/landing-counters.sh
  --repo <lane> --rev cb63ab13…` prints `nav rc=0`, then `usedby/ledger/citecheck rc=2` with
  `python3: can't open file '…/R65ExecLandingCounters/../quality/…'` and
  `MADO_LANDING_COUNTERS: RED`, exit 1 — expected, because the frozen sibling resolution is
  script-relative (`../quality/...`) and only resolves at the integrated location
  `quality/landing-counters.sh`. Its own `--selftest` was green in place (19/19, exit 0). L1:
  only the integrated path is meaningful; P8 proves the green path there.
- **Sibling bytes moved during the wave:** `42f620f1…` at first read (19:39) → `c12b72e2…` at
  battery time (19:41, stable through 19:42). My integration pins `c12b72e2…`; the counter
  reads instrument bytes at the scored rev, so later sibling edits cannot change a verdict
  already measured at a fixed rev.
- `git ls-tree` exits 0 with **0 lines** for a non-matching pathspec — the line count, not the
  rc, is the presence discriminator (P1/P2 re-derive this).

## Bounds / compliance

- Writes: seat dir + `/fast/scratch/hyaku/mado-r65/w1/R65ExecC2Counter` only. Fixture commits
  live only in the scratch clone; `git rev-parse --show-toplevel` asserted before each commit;
  the lane's tracked tree is clean (`git status --porcelain | grep -v '^??'` → TRACKED_CLEAN).
- Read-only elsewhere: lane git objects, sibling draft bytes, host tools. No network, no
  pacman, no service/session mutation, no `agent://all`, no spawns. No credential-shaped data
  captured.
- Scratch removed before yield (`rm -rf /fast/scratch/hyaku/mado-r65/w1/R65ExecC2Counter`), after
  copying `selftest.log`, `landing.log`, `proofs.out` here.
