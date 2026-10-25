# ExecHarmChecks — harm baselines at the round-41 freeze commit

Round 41 (hyaku run 7, 2026-10-25), inline v1 wave w1, seat `ExecHarmChecks`.
Everything below was **run**, not inferred: each block is the verbatim stdout+stderr of the command
named above it, captured to `out-*.txt` in this directory (sha256 manifest at the end).

## Environment (what the numbers are measured in)

| item | value |
|---|---|
| clone | `D=$(mktemp -d)` → `$D/lane` = `/tmp/tmp.Npi7p9BBiM/lane`, `git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin "$D/lane"` |
| toplevel check | `git -C "$D/lane" rev-parse --show-toplevel` → `/tmp/tmp.Npi7p9BBiM/lane` (equals the clone root; no throwaway identity, no commit made) |
| checkout | `git -C "$D/lane" checkout -q 60c3914154333180450d5da27ba222d5763cc56a`; `rev-parse HEAD` → `60c3914154333180450d5da27ba222d5763cc56a` |
| freeze commit | `60c3914 round-41: v1 freeze (registration, C1/C2 counters, controls, base receipts, source receipts)`; `git diff --stat ab2bfaa..60c3914` → 24 files, +4796. `git diff --name-only ab2bfaa..60c3914` lists only `.ufo/waves/round-40/w1.ready.dispatched`, `.ufo/waves/round-41/**` (23 files) and `quality/counters/c1-r41-globals.py`, `quality/counters/c2-r41-focus-entry.py` — **none of the seven instruments measured below, and no corpus/README/SOURCES file, changed in it**, so these are the base numbers re-measured at the freeze |
| python | `Python 3.14.8` (all `python3` calls used `-I`, isolated mode) |
| bash | `GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)` |
| working dir | `cd "$D/lane"` for commands 1–6; command 7 ran from `/home/vgpnk/Projects/shokunin` (see its note) |
| residue | `git -C "$D/lane" status --porcelain` after all runs → **empty** (no instrument wrote into the tree) |

## The seven commands

| # | command (cwd = clone root at freeze) | exit | counted line |
|---|---|---|---|
| 1 | `bash tools/mado-verify.sh --selftest` | **0** | `MADO_SELFTEST: 460/460 assertions passed` |
| 2 | `python3 -I tools/mado-options.py --selftest` | **0** | `MADO_OPTIONS_SELFTEST: 211/211 passed` |
| 3 | `python3 -I quality/check-index.py --rev 60c3914… --repo .` | **0** | `MADO_INDEX: … indexed=58/58 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` |
| 4 | `python3 -I quality/check-index-rows.py` (bare) | **2** | `SETUP_ERROR: --rev or --root is required` |
| 4b | `python3 -I quality/check-index-rows.py --rev 60c3914… --repo .` (supplementary, see note) | **0** | `MADO_INDEX_ROWS: … rows=58 errors=0 warns=3` |
| 5 | `python3 -I quality/check-axis-scores.py --repo . --rev 60c3914…` | **0** | `MADO_AXIS: checked=3 mismatched=0 rev=60c3914…` |
| 6 | `python3 -I tools/mado-eventq.py --selftest` | **2** | `mado-eventq.py: error: unrecognized arguments: --selftest` |
| 7 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | **0** | `mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` |

### 1. `bash tools/mado-verify.sh --selftest` — exit 0

```
MADO_SELFTEST: 460/460 assertions passed
```

1 line. Usage read first (`tools/mado-verify.sh:18-21`: "`--selftest` hermetic fixture tests, no
substrate reads"; exit map `0 = CLEAN`-equivalent / `2 = tool error incl. a failing --selftest`).

### 2. `python3 -I tools/mado-options.py --selftest` — exit 0

```
MADO_OPTIONS_SELFTEST: 211/211 passed
```

1 line.

### 3. `python3 -I quality/check-index.py --rev 60c3914154333180450d5da27ba222d5763cc56a --repo .` — exit 0

```
MADO_INDEX: rev=60c3914154333180450d5da27ba222d5763cc56a indexed=58/58 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
```

1 line. This is the navigation axis instrument (`quality/check-axis-scores.py:11-13`).

### 4. `python3 -I quality/check-index-rows.py` (bare, as assigned) — exit 2

```
SETUP_ERROR: --rev or --root is required
```

1 line. The tool's own usage (`quality/check-index-rows.py:462-471`) requires `--rev` (with
`--repo`) or `--root`; a bare invocation is a **usage error, not a fidelity failure** (its exit map:
"2 setup error"). The bare run therefore carries no row-fidelity signal.

**4b (supplementary, labelled):** the same tool at the same revision with its required argument —

```
MADO_INDEX_ROWS: rev=60c3914154333180450d5da27ba222d5763cc56a rows=58 errors=0 warns=3
WARN cited-glob-nomatch: `.ufo/evidence/round-12/getprop-*.txt` in row knowledge/window-rule-effects-getprop.md
WARN cited-glob-nomatch: `.ufo/evidence/round-12/drift-*.txt` in row knowledge/config-drift-r12.md
WARN cited-glob-nomatch: `.ufo/waves/round-24/fetch/S###.bin` in row knowledge/rule-attribution-r24.md
```

exit 0, 4 lines. 58 rows, 0 ERROR, 3 WARN (glob-shaped citations that match nothing at the rev;
WARNs never affect the exit code — docstring "Exit: 0 no ERROR finding … WARN lines never affect
the exit code"). **The 3 WARNs are the pre-existing baseline, not round-41 damage**: the same three
rows exist at base (the freeze commit changed no corpus file: `git diff --name-only
ab2bfaa..60c3914` lists only `.ufo/waves/round-40/w1.ready.dispatched`, `.ufo/waves/round-41/**`
and `quality/counters/{c1-r41-globals,c2-r41-focus-entry}.py`).

### 5. `python3 -I quality/check-axis-scores.py --repo . --rev 60c3914154333180450d5da27ba222d5763cc56a` — exit 0

```
MADO_AXIS_ROW: axis=navigation published=58/58 derived=58/58 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=55/55 derived=55/55 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=60c3914154333180450d5da27ba222d5763cc56a
```

4 lines. All three axes MATCH at the freeze: this reproduces the registration's
"every published axis ties at its maximum at base" premise, and the frozen
`receipts/axis-base.txt` line-for-line except its `rev=` value (that receipt reads `rev=ab2bfaa…`,
mine reads `rev=60c3914…`; the three fractions and `checked=3 mismatched=0` are identical).

### 6. `python3 -I tools/mado-eventq.py --selftest` — exit 2

```
usage: mado-eventq.py [-h] [--ss-file SS_FILE] [--log LOG]
                      [--journal-file JOURNAL_FILE] [--disable-logs {0,1}]
                      [--expect-client EXPECT_CLIENT] [--socket2 SOCKET2]
                      [--snapshot-out SNAPSHOT_OUT]
mado-eventq.py: error: unrecognized arguments: --selftest
```

5 lines, exit 2. **The tool exists but has no `--selftest` flag** (`tools/mado-eventq.py:208-218`
defines only `--ss-file --log --journal-file --disable-logs --expect-client --socket2
--snapshot-out`; `grep -n selftest tools/mado-eventq.py` is empty). The assignment's "if it exists"
condition resolves to: the file exists, the flag does not, so there is **no eventq selftest
baseline** — its self-check is a live/substrate read (needs `ss`, the socket2 path, `hyprctl
getoption`), which the host-safety rules forbid this seat from running. Recorded as a gap, not as
a pass.

### 7. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` — exit 0

```
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W01	S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

9 lines (TSV), exit 0: 7×`W04`, 1×`W01` (S277), and the `mado ok` line. **The counted line for this
baseline is `mado<TAB>ok<TAB><registry path>` plus the W/E census: `ok` with 7 W04 + 1 W01.**

Note (scope): this is the only command of the seven that reads the **live lane tree** (its
`--root` is the fleet root, as assigned) rather than the clone; it is read-only
(`scripts/sources-census.sh:6` "Read-only: parses shokunin.conf LANES rows textually … writes only
stdout or --out"). Diffed against the frozen `receipts/census-before.txt`
(`git show 60c3914:.ufo/waves/round-41/receipts/census-before.txt`): **identical** for all 9 lines;
the frozen file carries one extra trailing line, `exit=0`.

## Cross-checks against the frozen receipts (supports, at freeze)

| frozen receipt at 60c3914 | my run | relation |
|---|---|---|
| `receipts/selftest-base.txt`: `MADO_SELFTEST: 460/460 assertions passed` | command 1 | identical line |
| `receipts/axis-base.txt`: navigation 58/58, calibration 55/55, operability 12/12, `MADO_AXIS checked=3 mismatched=0`, `rev=ab2bfaa…` | command 5 | identical except `rev=` (mine at the freeze rev) |
| `receipts/census-before.txt` (9 TSV lines + `exit=0`) | command 7 | identical on all 9 lines |
| `receipts/c1-before-base.txt`: `fixtures=0/24 tool=absent verdict=TARGET_MISSED`, `exit=1` | not re-run here | out of this seat's scope (C1 counter run belongs to the C1 seats) |
| `receipts/c2-before-base.txt`: `admitted=0/1 verdict=TARGET_MISSED`, `exit=1` | not re-run here | out of this seat's scope (C2 counter run belongs to the C2 seats) |

## What these baselines constrain for the data commit

A data commit that lands C1/C2 must **keep**: `MADO_SELFTEST: 460/460` (any drop is damage — the
verify suite is a fixed assertion count, so a new tool/entry that changes it must be reported, not
silently absorbed), `MADO_OPTIONS_SELFTEST: 211/211`, `MADO_INDEX` `missing=0 dangling=0
duplicates=0` with `indexed=A/B` where B rises by exactly the number of new `corpus/knowledge/*.md`
notes (C2 adds one → [INFERENCE] `59/59`, since `MADO_INDEX` counts notes at the rev), `MADO_INDEX_ROWS` `errors=0` (warns may stay at 3 or rise only
with an explicit glob citation in the new row), `MADO_AXIS checked=3 mismatched=0`, and the census
`mado ok` with no new E-code. A new `E`-code, a `missing=`/`dangling=`/`duplicates=` above 0, a
dropped assertion count, or a non-zero `mismatched=` at the data commit is a harm regression against
this baseline.

## Residue (measured, not assumed)

- **Clone tree:** `git -C "$D/lane" status --porcelain` after all eight runs → **empty** (no
  instrument wrote into the tree; the three `quality/` checkers document "Writes: nothing; stdout
  only", `quality/check-index.py:30`, `quality/check-index-rows.py:36`).
- **`--selftest` scratch:** `tools/mado-verify.sh:1874-1878` removes its outer scratch on success
  (`if [ "$n_fail" = 0 ]; then rm -rf "$T" …`). My verify run finished at 20:00:51 (mtime of
  `out-verify-selftest.txt`, 16.6 s wall, started ≈20:00:35) and **no
  `/tmp/w5-mado-m52-selftest.*` directory carries an mtime in that window** — the population present
  (105 dirs, minute buckets 17:59 → 20:04; the nearest later bucket is 20:04, 4 dirs) belongs to
  concurrently running sibling seats, not to this seat; I removed none of them.
- **`mado-options.py --selftest`:** `tempfile.mkdtemp(prefix="mado-options-st-")`
  (`tools/mado-options.py:1203`) with `shutil.rmtree(…, ignore_errors=True)` (`:2095`);
  `ls -d /tmp/mado-options-st-*` → **0 entries**.
- **Census:** `scripts/sources-census.sh:6` "Read-only … writes only stdout or --out"; no `--out`
  passed, so stdout only.
- **Clone cleanup:** `/tmp/tmp.Npi7p9BBiM` removed at the end of this seat
  (`rm -rf /tmp/tmp.Npi7p9BBiM`; `ls -d /tmp/tmp.Npi7p9BBiM` afterwards → no such file).

## Output manifest (verbatim captures in this directory)

```
87957cb61aeec8d591a7bc1407113ae8bba756773d838bc48080a8bb2b399695  out-check-axis-scores.txt        (4 lines)
3d2d8ba229e30d36601aac1ca563344b032255cdd193ce4323585999b1de9ba4  out-check-index-rows-bare.txt    (1 line)
eeece2b7febff5a5d7ead4020aeaebed2d24dfa1767dbce157833a25214b423e  out-check-index-rows-rev.txt     (4 lines)
81cc75aed08cb6ae61b78313003e423c97b5c932621cc99848ffe7ded85caf65  out-check-index.txt              (1 line)
a282a04aae285089e7b04a56a8d694c85543fa5fd5a0437f577629e4a758717e  out-eventq-selftest.txt          (5 lines)
647b6712816c655002f1c8b16ce98c40255b53363bee7fe9693c411cc648a007  out-options-selftest.txt         (1 line)
858315d225193675535aafa5be0bfd7ee1fad308db763d22e2065021a097bcc3  out-sources-census-validate.txt  (9 lines)
58e720ddd3eaf6aba84ad6d37efe309c3e6b5b1d3d9aede880e4230a62543d90  out-verify-selftest.txt          (1 line)
```

Clone `/tmp/tmp.Npi7p9BBiM/lane` removed after the captures (`rm -rf /tmp/tmp.Npi7p9BBiM`); no
other path was written, no git verb beyond `clone/checkout/rev-parse/status/show/diff/log/ls-tree`
(read-only) was used, no package transaction, no compositor/journal-client access.
