# ExecAxisBase — round 48 w1: base receipts of the published axis table + round-47 counter harm-watch

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. REV under test: `579f694b45c797a9c39761fdb4f9e0a1b71b3585`
(round-47 closure commit = round-48 base). Lane HEAD while measuring: `5ff167423ee410251da0ef0c82f8e6fa25875665`
("round-48: claims, w1 spec + dispatch, census before"); the only tracked delta base..HEAD is `.ufo/waves/round-48/*`
(claims, spec, dispatch, census) — no instrument, counter, fixture, record or corpus file moved, so a worktree run of a
counter is byte-identical to the blob at base (verified per file in `receipts/counters-base.txt`).

Receipts (all written by this seat, transcripts unedited):
- `receipts/axis-base.txt` — the calibration gate and each of the three instruments it names, at REV, with exit codes.
- `receipts/c1-r47-base.txt` — full `PRED-C1-r47` transcript at REV: 195 `clause=` lines, final `PRED-C1-r47:` line at
  `:196`, `RC=0` at `:197`.
- `receipts/c2-r47-base.txt` — full `PRED-C2-r47` transcript at REV.
- `receipts/counters-base.txt` — counter/pin digests at REV vs worktree, invocations, final lines, exit codes.

## 1. Axis table: gate at base → `checked=3 mismatched=0`, rc 0

Command: `cd mado-shokunin && python3 -I quality/check-axis-scores.py --rev 579f694b45c797a9c39761fdb4f9e0a1b71b3585 --repo .`

```
MADO_AXIS_ROW: axis=navigation published=64/64 derived=64/64 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=82/82 derived=82/82 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=579f694b45c797a9c39761fdb4f9e0a1b71b3585
```
rc 0 (`receipts/axis-base.txt:26-29`).

The publication the gate parses at REV is the last unquoted marker, `SCORECARD.md` line 2675 (computed:
`git show REV:SCORECARD.md | grep -n "Axis table re-derived"`), which publishes `navigation 64/64; calibration
resolved-active 82/82; operability selftest 12/12` — the gate's `published=` cells are that line's, so the pass is not a
parse of some earlier publication.

The gate re-derives from the *committed bytes at REV*, not from the worktree (`quality/check-axis-scores.py:121-141`
`show()`/`run_script()`), so this is a measurement at base, not at HEAD.

Consistency with the round-47 closure receipt: `.ufo/waves/round-47/receipts/axis-tip.txt:4` reads
`MADO_AXIS: checked=3 mismatched=0 rev=f2b8568b9f605902e374a0274914a32def66aa0b`, and `f2b8568` is an ancestor of
`579f694` (2 commits: `d40189c9`, `579f694b`). Both revisions derive and publish the same three cells (64/64, 82/82,
12/12), i.e. the two commits between the tip receipt and base left the axis table neither stale nor changed.

## 2. Each instrument the gate names, run directly at REV

| axis | command | output | rc |
|---|---|---|---|
| navigation | `python3 -I quality/check-index.py --rev 579f694b… --repo .` | `MADO_INDEX: rev=579f694b… indexed=64/64 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | 0 |
| calibration | `python3 -I .ufo/waves/round-31/c2/count.py 579f694b…` | `METRIC literal lines=74/95 fraction=0.7789` / `METRIC active=82 resolved_active=82 fraction=1.0000` / `PRED-C2-r31-v2 verdict=TARGET_MET` | 0 |
| operability | `python3 -I quality/check-index.py --selftest` | `MADO_INDEX_SELFTEST: 12/12 assertions passed` | 0 |

Each instrument's `A/B` equals the cell the gate compared (`64/64`, `82/82`, `12/12`), so the MATCH rows are reproduced
by direct invocation and not only through the gate's wrapper. The calibration instrument also prints six
`WARN criterion … unverifiable (… path)` lines and 13 `LINE … superseded excluded` lines; they are its normal
record-scoping output at this REV and do not affect `active/resolved_active` (`receipts/axis-base.txt:36-60`). No scratch
clone was needed: all three instruments are revision-addressed read-only (`git show REV:path` with `GIT_*` stripped) and
were run in the lane; the only temporary files are the gate's own instrument copies under `TMPDIR`.

## 3. Round-47 C1 counter at base → `TARGET_MET`, rc 0

Command: `python3 -I quality/counters/c1-r47-terminal.py --repo . --rev 579f694b… --work /fast/scratch/hyaku/mado-r48/ExecAxisBase/c1`
(41 s wall; `TMPDIR` also under the seat scratch).

```
PRED-C1-r47 clause=a tool=present
PRED-C1-r47 clause=s rc=0 last='MADO_TERMINAL_SELFTEST: 43/43 passed'
PRED-C1-r47 clause=x explained=190/190
PRED-C1-r47 clause=g generated=150/150
PRED-C1-r47 clause=r trips=0
PRED-C1-r47: fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=579f694b45c797a9c39761fdb4f9e0a1b71b3585 nonce=3088085692
```
rc 0. 190/190 fixtures, 190/190 explanations, 150/150 generated cases, selftest 43/43, `trips=0` read-only — the
round-47 tool `tools/mado-terminal.py` still meets the frozen C1 predicate at base, and `explain`'s `cmd=` comparison
(clause x, the round-47 `CritC1Explain.md` item) holds there.

Judge integrity: the counter's pinned resolver at REV is
`.ufo/waves/round-47/fetch/xdg-terminal-exec` = `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`,
byte-equal to the host `/usr/bin/xdg-terminal-exec` digest named in the round-48 C1 claim. Counter and fixture bytes at
REV equal the worktree bytes (`quality/counters/c1-r47-terminal.py` sha256 `2b9c2d0e…abf3f8`, fixtures `4836cc1d…13dd86`),
so the scored predicate is the committed one.

## 4. Round-47 C2 counter at base → `TARGET_MET`, rc 0

Command: `python3 -I quality/counters/c2-r47-terminal-entry.py --repo . --rev 579f694b…`

```
PRED-C2-r47: admitted=1/1 verdict=TARGET_MET rev=579f694b45c797a9c39761fdb4f9e0a1b71b3585
```
rc 0, clauses a–i all `1`, `steps=7 script_cited=7 script=xdg-terminal-exec:1500`, `quotes=15`, held ids
`S056-S060` unchanged (`receipts/c2-r47-base.txt:12-18`). Counter bytes at REV = worktree (`cdd4c846…bc6e9be5`).

## 5. Axis naming (godspeed)

1. **Gate parity** — published cell equals re-derived cell, per axis at base: 3/3 MATCH (was 3/3 at the round-47 tip).
2. **Instrument reproducibility** — each named instrument invoked directly returns the same fraction the gate derived.
3. **No-harm** — the two round-47 counters that the round is about to extend/replace still print `TARGET_MET` with the
   frozen tool and entry at base, i.e. w1's C1/C2 work starts from a green, recorded baseline.
4. **Evidence exactness** — every number above is a line in a seat transcript; counter/pin digests are computed, not typed.

## 6. Risks / limits of this baseline

- The C1 counter's `generated` clause draws 150 cases from `--nonce` (here `3088085692`, printed in the receipt), so a
  second run at the same REV is a different sample; `TARGET_MET` at base is one recorded sample, not a corpus-wide proof.
- The C1 judge is this host's `bash/find/awk/tr/ls/md5sum` at count time inside its bwrap sandbox (`bubblewrap 0.13.1`,
  `strace 7.2`); a host tool change would move the judge, and the counter's own drift check (oracle vs recorded
  `expect`) is the only detector.
- Both counters were run at REV from their worktree files; that equals the REV blobs only because of the verified
  byte-identity in `receipts/counters-base.txt` — re-run after any counter edit must not reuse this receipt.
- No tool was installed or upgraded for this seat; no process launch outside the counters' own sandbox, no host cache
  read or write, `/fast/scratch/hyaku/mado-r48/ExecAxisBase` removed after the receipts were copied.
