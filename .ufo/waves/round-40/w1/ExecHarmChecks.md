# ExecHarmChecks — round-40 w1: round-start harm baselines beyond the committed receipts

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
Base measured: `9fc511ddce708327377161202f358ce37dc266ba` (round-39 verifier spot-check)
HEAD during runs: `e2b51d3b3f79768282914d57c1fa32cc85dcb06a` (wave spec/dispatch; base is an ancestor —
`git merge-base --is-ancestor` → yes)
Evidence dir: `.ufo/waves/round-40/w1/ExecHarmChecks/` (36 files; `results.tsv`, `commands.txt`)
Tracked files touched: **none** (`git status --porcelain -- corpus tools quality scripts MANIFEST.json
.ufo/state .ufo/watchdog.log` → empty). Writes confined to the seat dir and this report.
Tool installs: none needed (no package/tool transaction was run).

## 0. Inputs are the base bytes

`script-hashes.txt` — sha256 of every gate script at `9fc511d` vs the worktree, all `SAME`:
`tools/mado-options.py 461f8c3c…`, `tools/mado-verify.sh 050efc72…`,
`quality/check-index.py 2c8798ce…`, `quality/check-index-rows.py 2fd1c003…`,
`quality/check-evidence-pointers.py 3b6907cc…`, `quality/check-axis-scores.py 461f913a…`.
The freeze commit adds only `quality/counters/c1-r40-live.py` and `c2-r40-forms-entry.py`
(`git diff --stat 9fc511d..HEAD -- corpus/ tools/ quality/`), so every number below is base behavior.

## 1. The five named baselines (each with its exit code)

| # | command (as run, absolute paths) | exit | key line | evidence |
|---|---|---|---|---|
| 1 | `python3 -I $L/quality/check-index.py --repo $L --rev 9fc511d…` | **0** | `MADO_INDEX: rev=9fc511dd… indexed=56/56 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | `01-check-index.out` |
| 2a | `python3 -I $L/quality/check-index-rows.py --help` | **0** | usage: `[--rev REV] [--repo REPO] [--root ROOT] [--selftest]` | `02a-check-index-rows.help` |
| 2b | `python3 -I $L/quality/check-index-rows.py --repo $L --rev 9fc511d…` (documented invocation: reads `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*.md` at a git revision via `--rev` under `--repo`) | **0** | `MADO_INDEX_ROWS: rev=9fc511dd… rows=56 errors=0 warns=3` | `02b-check-index-rows.out` |
| 3a | `python3 -I $L/quality/check-evidence-pointers.py --help` | **0** | usage: `[--repo .] [--rev master] [--branch master]` | `03a-check-evidence-pointers.help` |
| 3b | `python3 -I $L/quality/check-evidence-pointers.py --repo $L --rev 9fc511d… --branch master` | **0** | `PRED-PTR-r36-v1 … pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=35 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET` | `03b-check-evidence-pointers.out` |
| 4 | `bash $L/tools/mado-verify.sh --no-live` (run with cwd `$L`) | **0** | `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only — live layer skipped: --no-live)`; `counts: pass=29 fail=0 unknown=0 skip=8 note=4` | `04-mado-verify-no-live.out` |
| 5 | `python3 -I $L/tools/mado-options.py --selftest` | **0** | `MADO_OPTIONS_SELFTEST: 71/71 passed` | `05-mado-options-selftest.out` |

The three pre-existing `WARN cited-glob-nomatch` lines in 2b are baseline noise, not new harm:
`.ufo/evidence/round-12/getprop-*.txt` (`knowledge/window-rule-effects-getprop.md`),
`.ufo/evidence/round-12/drift-*.txt` (`knowledge/config-drift-r12.md`),
`.ufo/waves/round-24/fetch/S###.bin` (`knowledge/rule-attribution-r24.md`).

The two `dangling_r35` lines in 3b (`…/scratch/SimplifyCounter/`, `…/scratch/MutC1Drop/mutants/`) are the
declared superseded pointers; they are *closed* (`dangling_r35_closed=1`), not harm.

## 2. Baselines beyond the committed receipts (X-series, all read-only)

| # | check | exit | base observation | evidence |
|---|---|---|---|---|
| X1 | `check-axis-scores.py --repo $L --rev 9fc511d…` | 0 | `MADO_AXIS: checked=3 mismatched=0 rev=9fc511dd…` (nav 56/56, cal 51/51, op 12/12) — reproduces `receipts/axis-base.txt` | `check-axis-scores.base.out` |
| X2 | `bash tools/mado-verify.sh --selftest` | 0 | `MADO_SELFTEST: 460/460 assertions passed` — reproduces `receipts/selftest-base.txt` | `mado-verify.selftest.out` |
| X3 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | 0 | 7×`W04` + 1×`W01 S277` + `mado ok …/corpus/SOURCES.md` — byte-equal to `receipts/census-before.txt` | `sources-census-validate.out` |
| X4 | `mado-options.py --home $HOME` (non-live static table) | 0 | 70 rows, all `set=true`, layers `defaults 57 / user 7 / toggles 4 / theme 2`; **sha256 `65f18828145111832477669164a93f56e6725616f5bcc9ede43ee3e8fbd730cd`** | `mado-options.static-home.out` |
| X5 | `mado-options.py --home <round-39 host-tree copy> --getoption <round-39 synthetic dump>` | 0 | 74 rows; `agreement 41 / config-only 18 / agreement* 6 / mismatch 5 / live-default 4`; **sha256 `6af65e6a8dad3883b2b1e7e62272ba3f3d850f4980012ddd0f8301d447a82bea`** | `mado-options.getoption-copy.out` |
| X6 | exit map of the existing paths (`exitmap.txt`) | 3 / 4 / 4 / 2 | no-home → **3**, missing `--getoption` → **4**, malformed `--getoption` → **4**, `--bogus` → **2** | `exitmap-*.out` |
| X7 | hermetic gate selftests | 0 | `MADO_INDEX_SELFTEST: 12/12`, `MADO_INDEX_ROWS_SELFTEST: 10/10`, `MADO_AXIS_SELFTEST: 18/18` | `*.selftest` |
| X8 | `check-evidence-pointers.py --repo $L --rev master --branch master` (literal usage defaults) | 0 | `verdict=TARGET_MET`, identical counters to 3b | `check-evidence-pointers.tipmaster.out` |

## 3. Findings that change how the L1 must read the harm watch

**F1 — the round-39 tool receipt is NOT a regression oracle (attacks `.ufo/waves/round-39/w1/ExecOptionsRealTree/run-static.stdout`, `run-getoption.stdout`).**
At base the tool emits **70** rows for that host-tree copy; `run-static.stdout` carries **79** and
`run-getoption.stdout` **83**. Diffing field-by-field, the *only* divergence is 9 extra keys in the
round-39 files — `binddr`, `bindeld`, `bindld`, `bindmd` and `windowrule:{fullscreen, id_inhibit,
match:class, name, no_follow_mouse}` — with every shared row's `value/owner/layer/line/set` identical.
This is the pre-fix parser described at `corpus/lessons/round-39.md:107-108` ("listed `binddr`,
`bindeld`, `bindld`, `bindmd` and five `windowrule:*` fields as options (79 rows; 70 are options)").
So: do not diff C1's output against the round-39 stdout files and call the 9-row gap a regression; the
correct oracles are X4 and X5, captured here.

**F2 — C1 can be regression-checked without touching `$HOME` (supports X4).**
`mado-options.py --home $HOME` and `--home .ufo/waves/round-39/w1/ExecOptionsRealTree/host-tree` produce
**byte-identical** output (`cmp` → identical, sha `65f1882…`). The committed host-tree copy is therefore a
faithful stand-in for the live host config bytes as far as the option table is concerned.

**F3 — verify's two `hypr` NOTEs are baseline, not new harm (attacks a plausible misreading of check 4).**
`hypr.file.sha_pin NOTE hyprland.conf sha256 ce7483f35ab5… drifted from round-1 pin 4f52854a3c14…` and
`hypr.backups NOTE 2 backup file(s) under ~/.config/hypr` are present at base. The config-plane pin for
round-40 is `gate boundary.readonly PASS … combined sha 3826214e5114…` — compare *that* line at the end.

**F4 — check 3b measures the working tree, not the revision (constrains when the L1 re-runs it).**
`inherited_dirty` comes from `git status --porcelain` over 13 fixed round-35 `INHERITED_PATHS`; it was 0 at
base. Unrelated untracked wave output does not affect it, but a re-run during an uncommitted edit of one of
those 13 paths would report dirty.

**F5 — 3b has a coverage limit for round 40 (attacks "the pointer gate will catch round-40 pointers").**
`check-evidence-pointers.py` parses only `## Round 35` / `## Round 36` sections of `LOG.md`/`SCORECARD.md`
(`pointers_r36=35` at base). A dangling round-40 pointer — e.g. the C2 own-work receipt path — is **not**
measured by it; `check-index-rows.py` (2b) is the gate that resolves row-cited paths at the revision.

**F6 — 71/71 is the *before*, not the target (constrains check 5).**
`receipts/c1-before-base.txt` records `clause=b rc=0 selftest=71/71`; C1 clause b requires `k == n >= 79`.
A tip run that still reads `71/71` means C1 did not land, and a tip run reading `71/71` must not be
recorded as "unchanged/safe".

## 4. Exact re-run lines for the L1 at round end

Full list with expectations: `.ufo/waves/round-40/w1/ExecHarmChecks/commands.txt`. The five mandatory ones,
with `<REV>` = data commit (then the tip):

```
L=/home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I $L/quality/check-index.py --repo $L --rev <REV>
python3 -I $L/quality/check-index-rows.py --repo $L --rev <REV>
python3 -I $L/quality/check-evidence-pointers.py --repo $L --rev <REV> --branch master
bash $L/tools/mado-verify.sh --no-live                       # cwd $L; compare full 46-line output
python3 -I $L/tools/mado-options.py --selftest               # MUST read k/n >= 79/79, not 71/71
```

Expected at tip: 1 → `indexed=57/57` (`[INFERENCE]` 56 + the one new C2 note); 2 → `rows=57 errors=0`;
3 → `verdict=TARGET_MET`; 4 → same `CLEAN (29 pass, 4 notes)` and same `combined sha 3826214e5114…`;
5 → all-pass with `n >= 79`.
Recommended tripwires (cheap, catch C1 changing existing behavior): X4 sha `65f1882…` unchanged,
X5 sha `6af65e6…` unchanged, X6 codes `3/4/2` unchanged, X3 still exit 0 (an `E03` duplicate id or `E11`
used-by-missing from the two new C2 rows is the realistic way it flips to exit 1).

## 5. Risks and blockers

- **Blockers: none.** Every named check was run to completion; no command needed a live compositor.
- I ran **no** `hyprctl` verb at all (not even the allowed read-only `getoption`): nothing in this seat's
  scope required it, and the live census is another seat's claim. No host config tree, service, sibling lane
  or fleet path was written.
- Residual risk this seat cannot remove: check 4's file plane is host-config-dependent, so its 29-pass line
  set is only comparable on the same host; and 3b's `tip_axis_transcript` depends on a committed
  `quality/receipts/axis-<40hex>.txt` (base satisfies it via `axis-520c631d…`), so the L1 must keep the axis
  transcript committed at the data tip.
