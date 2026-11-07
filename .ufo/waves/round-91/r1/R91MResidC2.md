# R91MResidC2 — residual attack on C2 (seat-report retention gate)

Seat: critic, residual call r1, round 91. Target: the FROZEN bytes of C2 — `quality/check-seat-reports.py`
at `0e09349e2c735c9fe1d4ba8d5c4ef79506f2d0bc` (sha256 `13c4b0a7dc4bbc39c70731dd35ec1f312c09f1a48f3b620e02945184d9cce39a`,
confirmed from `git show`, equal to the declaration's candidate digest). Read-only git in the lane; all fixtures under
`S=/fast/scratch/hyaku/mado-r91/R91MResidC2` (deleted on exit). No lane file other than this report was written.

Axes named: **C2 operability** (wave evidence retention) and **C1 coverage** (default-application plane). Everything
below touches C2 only; I read no C1 tool.

---

## 1. Re-run of the measurement argv — reproduced, rc 0

Copies taken from the frozen commits (sha256 checked before use):

```
$ git show 0e09349e:quality/check-seat-reports.py  -> sha256 13c4b0a7…39a   (309 lines)
$ git show 0e09349e:quality/counters/c2-r91-seat-reports.py -> sha256 c74f5baa…486 (341 lines)
```

Run from the lane root, verbatim argv from the declaration with `--scratch-root` under `$S`:

```
$ python3 -I quality/counters/c2-r91-seat-reports.py --repo . --rev 0e09349e2c735c9fe1d4ba8d5c4ef79506f2d0bc \
  --base-rev cc0381db585cc44c3dfc13ced807409c32c45bb0 \
  --set .ufo/waves/round-91/controls/seat-reports-set-r91.json \
  --mutants .ufo/waves/round-91/controls/seat-reports-mutants-r91.json \
  --expect-set-sha256 9a05fa8ad4ef771eab9a6e9f4e8f22bfd01155483d92da2134274c705d5cb7dc \
  --expect-mutants-sha256 7cf06df7dc0903e1291d00df4473d23b695f563bc9b24a2663d8c18348ebfcdd \
  --fresh 60 --scratch-root /fast/scratch/hyaku/mado-r91/R91MResidC2
MADO_SEAT_REPORTS: TARGET_MET pred=PRED-C2-r91-v1 rev=0e09349e… base_rev=cc0381db… expectations=59 met=59
  fresh=60/60 fresh_seed=331657383 selftest=ok:SEAT_REPORTS_SELFTEST: checks=16 failed=0 mutants=55 killed=55
  base_met=0 always_ok_met=5 always_missing_met=0 receipt_presence_met=11 check_sha256=13c4b0a7…39a
rc=0    (48.9 s wall)
```

`diff` of every `mutant …` line and the `MADO_SEAT_REPORTS:` line against
`.ufo/waves/round-91/receipts/c2-measured-r91.txt` → **empty** (identical, zero `FAILED` lines). `fresh_seed=331657383`
= `0x13c4b0a7`, the first 8 hex of the check's sha256 — the seed rule holds. `--selftest` run directly:
`SEAT_REPORTS_SELFTEST: checks=16 failed=0`, rc 0.

## 2. The two gate runs, and whether each finding is true

### 2a. `--worktree --round 91` on the lane (r1 reports not yet written; `r1/` was empty)

```
$ python3 -I $S/check-seat-reports.py --repo <lane> --worktree --round 91
SR01 missing round-91/r1 R91MResidC1 .ufo/waves/round-91/r1/R91MResidC1.md
SR01 missing round-91/r1 R91MResidC2 .ufo/waves/round-91/r1/R91MResidC2.md
SR01 missing round-91/w1 R91MScoutSources .ufo/waves/round-91/w1/R91MScoutSources.md
SEAT_REPORTS: mode=worktree rev=worktree rounds=1 waves=2 seats=16 trailered=16 present=13 missing=3
  empty=0 unsafe=0 untrailed=0 verdict=MISSING
rc=1
```

All three are true by hand at run time: `ls .ufo/waves/round-91/r1/` was empty and
`ls .ufo/waves/round-91/w1/R91MScoutSources.md` → rc 2 (ENOENT); `git cat-file -e master:<p>` → rc 128 for all
three. The r1 dispatch names both r1 reports as rendered trailers (`R91MResidC1.md`, `R91MResidC2.md`) and both are
in flight — that is the gate doing its job, not a false positive. In `--rev 0e09349e --round 91` (the r1 dispatch is not
committed) the same gate reports `seats=14 … present=13 missing=1` (R91MScoutSources), rc 1.

### 2b. `--rev master --all` (`master` = `cbbeb862`, one commit past the C2 rev)

```
$ python3 -I $S/check-seat-reports.py --repo <lane> --rev master --all
… 134 × "SR01 missing round-N/<wave> <seat> <path>" (135 stdout lines incl. summary)
SEAT_REPORTS: mode=rev rev=cbbeb862… rounds=47 waves=62 seats=1746 trailered=1746 present=1612 missing=134
  empty=0 unsafe=0 untrailed=0 verdict=MISSING
rc=1
```

Hand truth, independent of the gate (a second extractor: `git ls-tree -r --name-only master .ufo/waves`, per-dispatch
`git show master:<p>`, its own line scan, then `git cat-file -e/-s master:<path>`):

* seats = 1746, findings = 134, and the tuple set **(SR id, round, wave, seat, path) is set-equal to the gate's 134
  lines** (`equal True`; no finding only in one side). No false positive, no missed finding.
* 1746/134 ≠ the set's 1732/133 only because `master` is one commit past `0e09349e`: round-91's committed dispatch (14
  seats, 1 missing = R91MScoutSources) is now in the tree. At the frozen base `cc0381db` the gate reproduces the set
  exactly: `--all` → `rounds=46 waves=61 seats=1732 present=1599 missing=133`, rc 1, and the eight round rows →
  36/36, 11/13, 3/10, 0/14, 0/12, 0/16, 0/16, 2/13 (rc 1,1,1,0,0,0,0,1). All nine were re-derived by the independent
  extractor and are **set-equal** to the gate's lines.
* One `*-dispatch.json` in the tree is outside the gate's layout:
  `.ufo/waves/round-50/w1/ScrQualityR50/fixtures/w1-dispatch.json` — a wave-fixture payload nested inside a round-50
  report directory. It is correctly out of scope (documented: only `round-<N>/<wave>-dispatch.json`). No lane dispatch
  has a dotted/uppercase wave name that the `DISPATCH` regex would skip.
* Separability spot check: the C2 counter at the C1 rev → `SETUP_ERROR quality/check-seat-reports.py absent at
  54a0683c…`, rc 2 (as the claim states).

## 3. Break attempts — gate output, correctness, and what the frozen predicate can see

Each probe is a fresh tree under `$S/probe/<id>`; command is
`python3 -I $S/check-seat-reports.py --repo <tree> --worktree --round 7` unless stated. `$S/probe.py`,
`$S/probe3.py`, `$S/probe4.py` build them; the essential files are inlined below so each is reproducible.

| # | input | gate output | right? | predicate blind? |
|---|---|---|---|---|
| P1 | dispatch = valid JSON, 32 MiB `task` + real trailer | rc 0, `seats=1 present=1 verdict=OK`; 8 MiB 0.12 s/33.9 MB RSS, 32 MiB 0.33 s/83.0 MB RSS | yes (linear, no cap, no wrong answer) | yes — no fixture has a large dispatch; a gate that *dropped* large dispatches would pass unnoticed |
| P2 | `task` is an object / a number | `SR04 untrailed round-7/w1 A`, rc 1 | yes (cannot be checked) | yes — set/`fresh` never make `task` non-string; a gate that mislabelled it SR01 is not caught |
| P3 | `name` = `"Seat A"`, report missing | `SR01 missing round-7/w1 Seat A .ufo/waves/round-7/w1/A.md` (rc 1) | **line is ambiguous**: the documented finding is `<…> <seat> <path>` with no quoting, so seat/path cannot be split | yes — fresh names are `S[a-h]{5}<digit>`; set has no spaced name |
| P3c | `name` contains `\n` | finding line splits into two lines (`… w1 Seat` / `B .ufo/…`) | **no** — machine-unparseable output | yes |
| P4 | trailer path ends with `/`, the file exists | `SR01 missing … A.md/`, rc 1 | yes (a trailing-slash path is not a file); P4b: the same on a symlink reports SR01, not SR03 — same verdict | yes |
| P5 | report is a FIFO | `SR01 missing`, rc 1 | acceptable (not a regular file; cf. F17 directory → SR01) | yes |
| P5b | **dispatch** is a FIFO | **hangs with no output** (killed at 6 s); no timeout anywhere in the gate | **no** — a gate on a commit path that never returns (finding F4) | yes — no fixture; the counter's 600 s timeout would only surface it as a failure |
| P6 | UTF-8 unicode name present + missing (`Séat-ü.md`, `存在しない.md`) | present=1, `SR01 … 存在しない.md`, rc 1 | yes | yes |
| P7 | CRLF in the task text (rendered and plain) | both trailers recognised (present 1 / `SR01` for B), rc 1; lone-`\r` without newline also fine | yes (`\s*$` eats the `\r`) | yes — no CRLF fixture anywhere |
| P8 | same wave name `w1` in rounds 7 and 8 | `--all`: rounds=2 waves=2 seats=2, `SR01 … round-8/w1 B …`, rc 1; `--round 7`: rc 0 | yes | yes |
| P9 | trailer names `PROVINCE.md` (existing, unrelated file) | `present=1 verdict=OK`, rc 0 | intended: set fixture `H03-rev-present-outside-waves` asserts exactly this rc 0 | — (covered) |
| P10 | prose line `Report: n/a` | `SR01 missing … n/a`, rc 1 | per the documented grammar (`^Report: (\S+)$` is a residual trailer) yes; a false positive for a prose line that happens to be one token | yes — fresh "prose" is multi-token only |
| P11 | NUL inside the trailer path | `SR01 missing … A.md` (NUL passed through), rc 1 | yes (`os.path.*` reject NUL) | yes |
| P12 | report reached through a **symlinked parent dir** that leaves the repo | `present=1 verdict=OK`, rc 0 | **no** — the "report" is not in the repo (finding F5); `--rev` on the same layout would say SR01 | yes — only *leaf* symlinks are generated |
| P13 | `--round 7 --round 7` | `rounds=2 waves=2 seats=2 missing=2`, the same finding twice, rc 1 | **no** — the same wave counted twice (finding F3) | yes — no fixture repeats a round |
| P14 | trailer path with a lone surrogate (JSON `\udcff`), report missing | `SR01 … .ufo/waves/round-7/w1/\xff.md` — **raw 0xff byte in stdout**, rc 1 | output is not UTF-8; the canonical judge's `text=True` decode raises `UnicodeDecodeError` and the whole counter dies (finding F2) | yes — no such fixture |
| P14b | same, report present with a non-UTF-8 filename | `present=1 verdict=OK`, rc 0 | yes | yes |
| P15 | a **dispatch stored as a symlink** in a git tree (`w1` real, `w2` symlink; B's report missing) | worktree: `waves=2 seats=2 missing=1 verdict=MISSING` rc 1; **`--rev HEAD`: `waves=1 seats=1 present=1 verdict=OK` rc 0** | **no** — the whole w2 wave is dropped silently in rev mode (finding F1) | yes — no fixture stores a dispatch as a symlink |
| P16 | `tasks` contains strings/numbers | `SR04`×2 with seat `?` + the real `SR01`, rc 1 | yes | yes |
| P17 | rendered trailer to `old.md` (missing) then plain line to `new.md` (present) | `SR01 … old.md`, rc 1 | intended: set `F09-rendered-beats-plain` labels exactly this | — (covered) |
| P19 | `counts.total=14` but one task | `seats=1 … verdict=OK`, rc 0 | not covered by the SR rules; a truncated `tasks` array is invisible in the verdict (finding F6, coverage note) | yes |

Reproducer shape for the two verdict-changing probes:

```python
# P15 (rev mode drops a symlinked dispatch)
d = mk(); write(f"{W}/w1-dispatch.json", disp(A -> {W}/w1/A.md)); write(f"{W}/w1/A.md","x")
write(f"{W}/w2-dispatch.json.real", disp(B -> {W}/w2/B.md"))          # B's report is never written
os.symlink("w2-dispatch.json.real", f"{d}/{W}/w2-dispatch.json")
git -C d init -q; assert toplevel == d; git -C d add -A; commit as fixture
# git ls-tree -r HEAD: 100644 w1-dispatch.json, 120000 w2-dispatch.json
# worktree -> rc 1, waves=2, SR01 w2/B ;  --rev HEAD -> rc 0, waves=1, verdict=OK
```

## 4. Is the fresh leg's truth independent of the check?

Yes, but it adds no new edge class.

* **Independence holds.** `fresh_fixtures` (`quality/counters/c2-r91-seat-reports.py:169-238`) builds each tree from
  `random.Random(seed)` and derives the expected rc/ids/summary from *its own* writes; it never runs a check. I traced
  all 15 states (`:173`) against the check's documented grammar and found **no mislabel**: `dotname` (`name..md`)
  → present (component is not `..`); `dotdot` → SR03 (a `..` component, even though the normalised file exists);
  `dir` → SR01; `symlink` → SR03; `abs` → SR03; `empty` → SR02; `plain-*` → the plain grammar; `prose`/`inline`/
  `trailing` → SR04 (single-token grammar / prose after a path); `present`/`plain-present` write non-empty files.
  Summary fields (`seats/trailered/present/missing/empty/unsafe/untrailed/rounds/waves`) match the check's counters
  for every state; `chosen` is `rounds` (never a subset), so `rounds`/`waves` agree with `--all`.
* **What it cannot see.** The vocabulary is the *set's* vocabulary plus random composition. Reconstructed from the
  seed it emits 60 fixtures (32 `--all`, 15 git, 1 clean/rc 0; ids SR03 97 / SR01 92 / SR02 23 / SR04 125; 1–3 rounds;
  ≤ 20 seats) and **contains none of**: a spaced/newline/non-UTF-8 seat name, CRLF text, a trailing-slash path, a FIFO,
  a non-UTF-8 path byte, a symlinked *dispatch*, an oversized dispatch, a duplicate `--round`, a `counts` mismatch.
  So the fresh leg tests the gate's *verdict on well-formed dispatches*, not its **dispatch enumeration** (F1) or its
  **output encoding** (F2) — exactly the two live defects. With 59/60 fresh fixtures at rc 1, false-positive pressure
  comes from the set's clean rows (86–89, F01/F08/F15/F21/F28, H03), not from fresh.

## 5. Findings (ranked), with the smallest safe correction

**F1 — `--rev` mode silently skips a dispatch stored as a symlink; the gate returns `verdict=OK` with a whole wave
unchecked.** `quality/check-seat-reports.py:74-77` records `120000` entries only in `self.links`, and `paths()`
(`:79-80`) enumerates `self.sizes` (blobs) alone; `--worktree` enumerates the same file (`:102-108`) and follows it on
read (`:119-124`). Reproducer P15: same tree → worktree rc 1 `waves=2 … missing=1`, `--rev HEAD` rc 0 `waves=1 …
verdict=OK`. This is the M90-4 failure class the gate exists to prevent (a lost seat report that no check names), and
it is the only probe that changes a verdict direction. Not visible to the frozen predicate (§4).
*Axis:* C2 operability. *Correction:* enumerate every `*-dispatch.json` entry in the tree
(`self.sizes` ∪ `self.links`) and raise `SetupError("dispatch is a symlink: <path>")` for a non-blob dispatch (fail
closed, rc 2) — or, if following is wanted, resolve the link target inside the tree once; either way the two readers
must not disagree. Costs one line plus one branch; no other expectation moves.

**F2 — finding lines are not guaranteed parseable/UTF-8.** (a) `name` is printed raw (`:159`): a space makes the
`<seat> <path>` split ambiguous (P3) and a newline splits the record (P3c). (b) A path with a lone surrogate is printed
with `surrogateescape`, i.e. a raw `0xff` byte (P14); `quality/counters/c2-r91-seat-reports.py:67` runs the check with
`text=True`, so this raises `UnicodeDecodeError` inside `run_check` and **kills the counter process** (verified by
calling `run_check` on the P14 tree: `COUNTER CRASH UnicodeDecodeError … 0xff`). The lane has no such input today, so
neither the measurement nor any mutant is affected.
*Axis:* C2 operability (diagnosability). *Correction:* render seat and path with `json.dumps(..., ensure_ascii=True)`
(single token, round-trips), and make the counter's `run_check` decode with
`bytes` + `errors="surrogateescape"` rather than `text=True`.

**F3 — duplicate `--round N` double-counts.** `:293` appends to a list and `:147` iterates it unchanged:
`--round 7 --round 7` → `rounds=2 waves=2 seats=2` and the same finding twice (P13).
*Correction:* `rounds = sorted(set(rounds))` before the loop. No fixture has duplicates.

**F4 — a FIFO at a dispatch path blocks `--worktree` forever** (P5b: no output in 6 s; the gate has no timeout;
`open()` at `:119-124` blocks). `--rev` cannot hit it (git stores blobs/symlinks only), so this is another
mode asymmetry. *Correction:* `if not stat.S_ISREG(os.stat(p).st_mode): raise SetupError(...)` before reading, or
`os.O_NONBLOCK`. A hung gate on the records-commit path is a worse outcome than a setup error.

**F5 — worktree mode accepts a report reached through a symlinked parent directory that escapes the repo** (P12:
`present=1 verdict=OK`; `/etc`-style trees are readable). `unsafe()` and `size()` test only the leaf (`:110-114`,
`:127-128`). `--rev` reports SR01 for the same layout, so the two readers disagree again. *Correction:* in worktree
mode reject a path whose `os.path.realpath` is not inside `os.path.realpath(self.repo)` (`SR03 unsafe`), which also
subsumes the leaf-symlink case.

**F6 — coverage note, not a rule violation:** a dispatch whose `counts.total` disagrees with `len(taskCall.tasks)` is
reported `verdict=OK` (P19). The `seats` field in the summary is the only signal. If the L1 wants a truncated dispatch
to fail closed, that is a new rule (and a new predicate), not a fix to these bytes.

**Checked and correct (no finding):** huge dispatch (linear, no cap), non-string `task` → SR04, trailing slash → SR01
(SR03 vs SR01 on a symlink-with-slash is a label difference with the same verdict), FIFO *report* → SR01, UTF-8 unicode
paths in both directions, CRLF in rendered and plain trailers, the same wave name in two rounds, NUL in a path,
`H03`-style outside-waves present, `F09`-style rendered-over-plain precedence, non-object `tasks`, absolute existing
paths → SR03, and base-rev `--all`/per-round reproduction (set-equal).

## 6. Axes and duplicate authority

* **C2 (operability):** F1 is a fixable defect in a claimed behaviour (detect a lost seat report) that the frozen
  predicate cannot falsify; F2–F5 are robustness/output/coverage defects that do not move a measured expectation.
  None of them makes TARGET_MET false: the measurement is reproduced exactly, and all 59 set expectations plus 55
  kills plus 60 fresh are true on the frozen bytes. The tradeoff the canonical judge would have to accept is
  "a symlinked dispatch is not a dispatch", which contradicts the gate's own purpose — I would reject that tradeoff
  and fix F1 rather than declare it out of scope.
* **C1 (coverage):** untouched.
* **Duplicate authority:** none over dispatches at `cc0381db` (`git grep 'Report:' cc0381db -- quality tools scripts`
  → only `quality/check-deliverables.py`, whose `TRAILER` reads `Report:` lines *inside seat reports*, a different
  object and a different grammar: `^Report:\s*`?([A-Za-z0-9_.][A-Za-z0-9_./+-]*\.md)`?\s*$`). The two grammars now
  coexist (rendered vs plain vs backticked declaration); that is a documentation risk, not a second authority.

## 7. Dead steps / installs / scratch

No dead steps; no tool installed (nothing needed; pacman untouched). Every command above ran read-only except git
`init/add/commit` inside `$S/probe/p15-symlink-dispatch`, which asserted `git -C $D rev-parse --show-toplevel` = `$D`
before the first commit. Scratch `S=/fast/scratch/hyaku/mado-r91/R91MResidC2` was removed on exit (report is the only
artifact kept, inside this file).
