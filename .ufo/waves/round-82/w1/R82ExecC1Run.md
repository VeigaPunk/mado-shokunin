# R82ExecC1Run — independent replay of the C1 counting command

Seat: leaf executor. Task: replay the frozen C1 counter verbatim over the lane (read-only),
diff against both pinned receipts, re-run the base-only control, report the contract numbers
and exit statuses. Nothing in the lane was edited.

Frozen instruments observed (sha256 prefixes and full hashes agree with the wave card):

| instrument | sha256 |
|---|---|
| `quality/counters/c1-r82-allocation-band.py` | `1e9f394df80284e78f1fdf3f24cb5e14d1e4091f4880ccc60a2a45060b54612d` |
| `.ufo/waves/round-82/controls/c1-cases-r82.json` | `e404bb3fa93d5f12338129adc8733574084e6fab2ee12fbb471dd45df94a315f` |
| `.ufo/waves/round-81/controls/c1-cases-r81.json` | `ab8154a1d4bc5d2a0f58bef8aeb675605e50ecfe932406b39b0a0c2df0533d52` |
| `tools/mado-barfoot.py` @ `780c30fc…` (frozen) | `380075284d7d5c6f56a82600935d512def617223be27f33241ff5dbcb0bcab59` |
| `tools/mado-barfoot.py` @ `6ea2386d…` (base) | `a129a435572805c3ae7730714f0dafdea2b9a7e420f53f0d109dc2d5f57d1230` |
| pinned `measurement-c1-r82.txt` | `b840376a5eb74d5b4d5c0fc08b4a082b16048b192aaf6b5e9bdf06300e7fc5d0` |
| pinned `control-c1-r82-at-base.txt` | `418af3c1d7188505edacf4ae6ddb41955309ed96dc5ffb572f7903db412c46c0` |

Revisions resolve to themselves (`git rev-parse` of both the freeze and the base print the
full 40-char hashes unchanged), and the two tool hashes above are recomputed from the
committed bytes with `git show <rev>:tools/mado-barfoot.py | sha256sum`, independently of the
counter.

## 1. Frozen command, verbatim

cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`, scratch root
`/fast/scratch/hyaku/mado-r82/R82ExecC1Run`:

```
python3 -I quality/counters/c1-r82-allocation-band.py --repo . \
  --rev 780c30fcae12d74ce8ab3b871a0888696c2415d9 \
  --base-rev 6ea2386d49318a5f223097c78b5fe79c31b064f8 \
  --controls .ufo/waves/round-82/controls/c1-cases-r82.json \
  --carried .ufo/waves/round-81/controls/c1-cases-r81.json \
  --scratch-root /fast/scratch/hyaku/mado-r82/R82ExecC1Run
```

- stdout saved to `replay-freeze-at-base.out` (8150 bytes, 84 lines), stderr to
  `replay-freeze-at-base.err` (only the `time(1)` line: `WALL=56.52s MAXRSS=22620KB`).
- **exit status 0** (target met, per the counter's documented exit map `0` met / `1` missed /
  `2` setup error).
- The counter wrote only under the given scratch root and removed its own `c1-r82-*`
  generation directory in its `finally` block: `find <scratch> -maxdepth 1 -name 'c1-r82-*'`
  now yields 0 entries. Nothing was written to `/tmp`.

## 2. Diff against the pinned measurement receipt

```
diff -u .ufo/waves/round-82/receipts/measurement-c1-r82.txt replay-freeze-at-base.out
```

- `diff` exit 0, **zero diff lines**; both files 84 lines.
- `cmp -s` reports identical; `sha256sum` of the replay output is
  `b840376a5eb74d5b4d5c0fc08b4a082b16048b192aaf6b5e9bdf06300e7fc5d0`, equal to the pinned
  receipt's.
- Scratch-dependence: **there are no scratch-dependent lines at all** — the counter prints no
  filesystem paths on stdout (only `MADO_R82_CASE` / `MUTANT` / `BASE` / `CONTROL` /
  `BARFOOT` lines). The comparison is therefore whole-file byte identity, stricter than the
  ticket's "every line except the scratch-dependent none".
- Difference report: none. (No line pair to show.)

Independent aggregation of the replay output with `grep -c` (not trusting the terminal line):

```
cases=47  case_correct=47  mutants=34  killed=34
distinct_case_names=47  distinct_mut_names=34  unkilled=0
```

No case name or mutant name occurs twice, so `correct=47`/`killed=34` are counts of distinct
frozen cases and distinct named mutations, not repeated rows.

## 3. Base-only control re-run

```
python3 -I quality/counters/c1-r82-allocation-band.py --repo . \
  --rev 6ea2386d49318a5f223097c78b5fe79c31b064f8 \
  --base-rev 6ea2386d49318a5f223097c78b5fe79c31b064f8 \
  --controls .ufo/waves/round-82/controls/c1-cases-r82.json \
  --carried .ufo/waves/round-81/controls/c1-cases-r81.json \
  --scratch-root /fast/scratch/hyaku/mado-r82/R82ExecC1Run
```

- stdout `replay-base-only.out` (8279 bytes, 84 lines), stderr empty.
- **exit status 1** — the documented "target missed" code, which is the *expected* outcome
  for the held round-81 tool on a set containing the eight allocation cases; a `0` here would
  have been the defect.
- `diff -u .ufo/waves/round-82/receipts/control-c1-r82-at-base.txt replay-base-only.out`:
  exit 0, zero diff lines, `cmp` identical, sha256
  `418af3c1d7188505edacf4ae6ddb41955309ed96dc5ffb572f7903db412c46c0` equal to the pinned
  receipt's.
- Terminal line: `cases=47 correct=39 mutants=34 killed=28 base_correct=39/47 carried=39/39
  tool_selftest=121/121 verdict=TARGET_MISSED rev=6ea2386d… tool_sha256=a129a435…`.
- The six unkilled mutants are exactly the allocation-class mutations whose anchors do not
  exist in the base tool, reported by the counter as `reason=anchor-absent` (not as silent
  passes): `alloc-explicit-overridden`, `alloc-zero-accepted`, `alloc-axis-lost`,
  `alloc-negative-accepted`, `alloc-unknown-kept`, `alloc-composition-ignored`. This matches
  the base tool having no `--allocation` input, and it confirms the 8-case delta
  (`47 − 39 = 8`) is the client-allocation band C1 claims to add.

## 4. Contract numbers and exit statuses

Contract line reproduced verbatim by the freeze replay:

```
MADO_R82_BARFOOT: cases=47 correct=47 mutants=34 killed=34 base_correct=39/47 carried=39/39 tool_selftest=133/133 verdict=TARGET_MET rev=780c30fcae12d74ce8ab3b871a0888696c2415d9 tool_sha256=380075284d7d5c6f56a82600935d512def617223be27f33241ff5dbcb0bcab59
```

| field | value |
|---|---|
| `cases` | 47 |
| `correct` | 47 |
| `mutants` | 34 |
| `killed` | 34 |
| `base_correct` | 39/47 |
| `carried` | 39/39 |
| `tool_selftest` | 133/133 |
| `verdict` | `TARGET_MET` |

Supporting `BASE`/`CONTROL` lines from the same run agree: `base_correct=39/47
base_sha256=a129a435…` and `control sha256=e404bb3f… carried=39/39`.

Exit statuses observed:

| run | exit | meaning |
|---|---|---|
| frozen C1 command (freeze rev + base rev) | 0 | target met |
| base-only control (`rev=base`, `base_rev=base`) | 1 | target missed — expected at base |
| counter's own `--selftest` | 0 | `MADO_R82_BARFOOT_SELFTEST: 84/84` |
| extracted frozen tool `--selftest` | 0 | `MADO_BARFOOT_SELFTEST: 133/133` |

The last two are extra probes: the `133/133` in the contract line is the *measured tool's*
selftest, which the counter only parses from the tool's output. I re-ran it directly from the
committed bytes (`git show 780c30fc…:tools/mado-barfoot.py`, sha256 `38007528…`) and got
`133/133` with rc 0, and separately ran the counter's own checker self-test (`--selftest`,
distinct from the tool's) at `84/84` with rc 0. So both the inner 133 checks and the outer
checker are green independently of the regex that copies the number into the contract line.

## Lane cleanliness

`git status --porcelain` in the lane lists only other seats' artifacts (`corpus/README.md`,
`corpus/SOURCES.md`, `.ufo/waves/round-82/fetch/`, `w1.ready.dispatched`, `w1/`,
`corpus/knowledge/bar-footprint-allocation-r82.md`); none is attributable to this seat. All
git use here was read-only (`rev-parse`, `show`, `status`). No mutating git/jj command, no
commit/push, no edit to a frozen instrument, the claim declaration, `.ufo/state/`,
`.ufo/watchdog.log`, `.scratch/`, the fleet root, or a sibling lane. Scratch evidence is
retained under `/fast/scratch/hyaku/mado-r82/R82ExecC1Run/` (`replay-freeze-at-base.out/.err`,
`replay-base-only.out/.err`, `diff-freeze.txt`, `diff-base.txt`, `counter-selftest.out`,
`tool-selftest.out`, `mado-barfoot-freeze.py`) and contains no monitor description/serial/
make/model, token, session id, or home path — only lane-relative instrument paths and hashes.

No tool was installed or upgraded; none was needed.

## Findings

1. The C1 receipt is reproducible: an independent verbatim replay at the freeze produced a
   byte-identical 84-line receipt with `TARGET_MET`, rc 0, and all seven contract figures
   reproduced without relying on the terminal line.
2. The base-only control is reproducible: byte-identical to its pinned receipt, rc 1, with
   `correct=39/47` and exactly six anchor-absent allocation mutants accounted for.
3. No defect found; the frozen instruments, control sets and both receipts are internally
   consistent with each other and with the committed tool bytes.

STATUS: ok
