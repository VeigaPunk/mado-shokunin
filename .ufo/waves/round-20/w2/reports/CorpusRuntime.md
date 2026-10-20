# CorpusRuntime — partly falsified: the 200-largest set is crash-free and ~1.14× slower, but the new tool hangs where the old one takes 0.06 s

Scope: runtime and failure modes of `tools/mado-tripwire.py` at 28c6837
(sha256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`, byte-identical at tip
a4046a8: `diff <(git show 28c6837:...) tools/...` empty) against 1f7f995
(sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`), plus the L1
`UnboundLocalError` question.

| Question asked | Answer |
|---|---|
| 200 largest stable files: wall time each | measured; new 13.165 s vs old 11.584 s serial (1.14×); median 1.08×, max 1.82×; **new faster on 2, slower on 149** of 200 |
| any exit 2 / traceback | **none** — 400/400 runs on the sample, 11,756/11,756 over the whole stable corpus |
| any file where the new tool times out (>60 s) | **yes, one**: `KaidokuR19/KaidokuR19.EvidenceSecurity-3.jsonl` — timed out at 60.061 s under load; 30.1–33.0 s serial vs **0.06–0.07 s old** (430–550×). Not among the 200 largest |
| JS-cell `UnboundLocalError` — are there others? | **no others anywhere**: the landed tool initializes `env = bindings = None` before the language test (`tools/mado-tripwire.py:2046`); zero exit-2 over 5,878 corpus files; 9/9 synthetic JS shapes clean. The defect is only in the unlanded draft patches |

The one falsified statement is the implicit "corpus-scale cost is unchanged / no ordering regression":
the same repair that made helper resolution work makes one 736 KB transcript cost 30 s instead of
0.07 s, and a 2,080-byte synthetic cell reproduces it. The 200-largest sample the ticket names does
**not** contain that file, so a check limited to the named sample would have reported "holds".

## Axes

1. Correctness/failure surface: exit code, verdict line, JSON parse, traceback, empty stdout.
2. Cost: per-file wall time (serial, and 8–12-way concurrent), tails.
3. Trigger population: how many corpus files have the shape that causes the outlier.

## Method

- Sample: all `*.jsonl` under `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`, filtered to
  mtime ≤ start−3600 s (stable), sorted by size, top 200. 200 files, 594,558,504 bytes, largest
  13,645,711 B, 200th 2,296,844 B (`/tmp/r20w2_stable200.tsv`). Re-stat after the run: 0 files
  changed during it.
- Each invocation is `python3 -I <tool> --scan <file>` — one file per process, so any
  `could_not_evaluate` is attributable (the tool's top-level handler converts an internal exception
  into exit 2 with `"error": "internal <Type>"`, and `scan()` aborts the whole invocation on one bad
  file, so per-file runs are mandatory for attribution).
- Both tools were materialized in /tmp from lane bytes (`git show 1f7f995:...`, tip copy) and never
  run from the lane worktree. Python 3.14.8. Host shared with the other wave-2 seats, so absolute
  wall times include foreign load; the two tools ran back-to-back per file inside one worker.
- Extra sweep beyond the named sample: 5,878 stable files × 2 tools (the other 100 files were
  younger than 30 s at sweep start and were excluded as live).

## A. The 200 largest stable files

Serial pass (`CorpusRuntime/serial-runs.jsonl`, one tool at a time, 400 runs):

```
old total 11.584 mean 0.0579 median 0.0490 p95 0.1114 max 0.2600
new total 13.165 mean 0.0658 median 0.0530 p95 0.1255 max 0.3731
ratio min 0.93 p50 1.08 p95 1.39 max 1.82
new slower >2ms 149 | new faster >2ms 2
```

Concurrent pass, 8 workers (`CorpusRuntime/runs.jsonl`, 400 runs):

```
old total 27.28 mean 0.136 median 0.116 max 0.495  exit2 0  traceback 0
new total 30.24 mean 0.151 median 0.126 max 0.727  exit2 0  traceback 0
```

- Exits are only {0,1}; no `could_not_evaluate`, no traceback, no empty or unparseable verdict
  (0/400), stderr empty except 8 `SyntaxWarning` emissions from `compile()` (see B).
- Both tools hashed the same bytes: `sha` in the verdict equal old vs new for 200/200 files.
- No file in this sample times out; slowest new 0.373 s serial, 0.727 s under 8-way load.
- Behaviour delta in the sample: raw finding rows 928 → 955 (+27). 85 files differ by the new
  `"evidence"` marker (old rows have no such field); 82 of those differ *only* by it. Row changes,
  all four explained:
  - `TabiR17.C2Counter-2.jsonl` 0 → 17 rows, label `clean` → `findings` (helper-carried
    `git add/commit` the old tool never reached; all `observed`).
  - `JjLaneHelperV2-2.jsonl` +10 rows (same class: `git add/commit`, `jj file`).
  - the 13.6 MB session loses exactly one row: `('vcs_write','jj:git',1713)` — the command is
    `jj git init --help`, so the removal is the intended help-form repair.
  - `MadoR13.jsonl` +1 row is a duplicate: one tool call (`call_60b`, line 470) emits the same
    `pacman -Q wayland-utils wayland wayland-protocols hyprland` row twice, once
    `"evidence":"observed"` and once `"lead"`. Old emitted one row. Flagged for the precision/no-harm
    owners, not judged here.

## B. Failure modes, both tools, whole corpus

`CorpusRuntime/full-sweep.jsonl` — 5,878 stable files × 2 tools = 11,756 runs, 12 workers:

```
new n 5878 exit2 0 tb 0 timeouts 1 stderr 49
old n 5878 exit2 0 tb 0 timeouts 0 stderr 49
```

- **Zero** exit 2, `internal …`, traceback, empty verdict or unparseable verdict for either tool.
- The 49 stderr lines are the same files for both tools: `<eval>:N: SyntaxWarning: "\x" is an
  invalid escape sequence` emitted by `compile()` on transcript cells. Harmless here; it would only
  matter if a caller ran the tool under `-W error` or asserted an empty stderr.
- old worst case over the corpus: 0.617 s (13.6 MB file). new worst case excluding the timeout:
  14.138 s (`MadoR17/MadoR17.RevengeUnparsed.jsonl`, old 0.24 s). Files >0.5 s: old 6, new 18.
- Label counts drifted on the corpus: old 4506 clean / 1372 findings, new 4501 / 1376 — four files
  flip clean→findings (the sample's flip is one of them). Not judged here.

## C. The timeout: file, trigger, scaling

Observed record, `full-sweep.jsonl` line 6165:

```
{"key":"new","exit":null,"label":"","timed_out":true,"wall_s":60.061,
 "path":"…/2026-10-20T12-57-31-587Z…/KaidokuR19/KaidokuR19.EvidenceSecurity-3.jsonl"}
```

Serial repeats of the same file (`--scan`, no other load from my harness):

```
run0 old 0.07s rc=0 clean findings=0   run0 new 33.00s rc=0 clean findings=0
run1 old 0.06s rc=0 clean findings=0   run1 new 30.63s rc=0 clean findings=0
run2 old 0.07s rc=0 clean findings=0   run2 new 30.12s rc=0 clean findings=0
```

30 s of CPU to produce zero rows. Peak RSS of that child: 52,296 KB.

Trigger, reduced to one 2,080-byte eval cell from the file (its `def safe(n)` block plus one call):

```
v1 def+call   bytes=2080  new wall 27.97s rc=0   |  old wall 0.08s rc=0
v3 def+call   bytes=2082  new wall 28.10s rc=0
v2 same file with the final for-loop removed (no call to safe)  new wall 0.04s
```

Mechanism [INFERENCE, backed by cProfile]: `spawn_scan` expands every call to a visible helper while
depth < 4 (`tools/mado-tripwire.py:1825`), and `bind_literal` keeps a binding even for non-literal
arguments — `literal_value` returns `LITERAL_MISS` (`:1216`, `:1250-1264`) and `bind_literal` stores
it (`:1690`) — so a helper that calls itself N times is re-expanded multiplicatively at each level
(bound 4): ≈N⁴ expansions on a bare body (measured below), 14,446 real `prepare_eval_calls`
expansions on the corpus cell. Each expansion pays a full `prepare_eval_calls` walk of the body
(`:1732`). `cProfile` on the file: 873,783,236 calls, `prepare_eval_calls` 141 s of 165 s (profiled).

Scaling on a minimal self-recursive helper (`def f(n): f(n) × N; f(1)`, tiny body):

```
N=16 1.74s   N=24 7.47s   N=32 23.49s   N=40 52.68s      (old: no expansion path, 0.08s on the same shape)
```

A realistic dispatcher helper with ~45 self-calls and a non-trivial body is therefore effectively an
unbounded hang (`~N⁴ × body`); the corpus instance has 24 self-calls inside a 2 KB body and costs 30 s.

Exposure (AST census over all 6,078 `*.jsonl` present at census time, counting a `def F` whose own
body calls `F` ≥8 times and which is called at module level; `CorpusRuntime/recursive-helper-exposure.json`):

```
safe 24 …/KaidokuR19/KaidokuR19.EvidenceSecurity-3.jsonl      <- the 30 s file
resolve 9 …/MadoR17/MadoR17.RevengeUnparsed.jsonl             <- the 14 s file
files with body-fanout>=8 AND module-level call: 2
```

Exactly the two measured slow files, and no third. So within this corpus the firing population is
fully enumerated — the risk is not "unknown files will hang", it is that these two exist and any
future transcript with a recursive helper of that shape joins them. Note the depth bound caps the
work at 4; a 5th level would multiply the same file by ~N again.

## D. The JS-cell `UnboundLocalError`

- Landed tool: `scan_file` sets `env = bindings = None` at `tools/mado-tripwire.py:2046` **before**
  the language test and the unconditional `classify_eval(code, language, env, bindings)` call at
  `:2053`. `classify_eval` early-returns `([], 1, 0)` for any non-Python language (`:1767`), so a JS
  cell never enters binding analysis. There is no JS branch anywhere in the file, and none in the
  file's history between 1f7f995 and 28c6837 (single commit; `grep '"js"'` over every revision: 0).
- Synthetic cells (both tools, `/tmp/r20js/`): language `js`, `javascript`, `JS`, absent, empty code,
  non-string `code`, missing arguments, backticks containing `sudo pacman -S` — 9/9 exit 0/1,
  `eval_unparsed=1` for the JS ones, no exit 2, no traceback. Order-sensitive pair: JS-then-Python
  and Python-then-JS files both exit 1 with the single expected `package_query` row on the Python
  cell — the order dependence that produced the draft bug is absent.
- Corpus: 0 exit 2 over 5,878 files, with `eval_unparsed` identical old vs new (27 in the 200 file
  sample) — i.e. JS cells are counted as unparsed, never analyzed, never crashing.
- Independent corroboration (peer report, read-only): `w2/reports/RevengeEnvBug.md:9` locates the
  defect in `TwRuleB.patch:799-809` and `TwRuleB-v2.patch:840-850` — both drafts assign `bindings`
  unconditionally but `env` only inside the Python branch, then pass `env` on the JS path. Those
  patches were not landed. **Answer: there are no other UnboundLocalErrors, and the landed tool
  cannot produce this one; the class exists solely in the unlanded drafts.**

## Limits

- The 200-largest sample is size-ranked, not round-ranked; the timeout file (736 KB) is outside it by
  construction, which is exactly why the extra full-corpus sweep was run.
- Timeout at 60.061 s is a wall-clock observation under a 12-worker sweep with other seats active on
  the host; serial repeats took 30.1–33.0 s. The regression is real either way (old 0.06 s); whether
  a specific harness hits 60 s depends on its load and its budget.
- Runtime comparison is wall time, not `sys` CPU; no per-run RSS for the sample (only the outlier was
  measured, 52 MB).
- Exposure census counts syntactic shape, not reachability: it over-counts nothing at ≥8 in this
  corpus (2/6,078), but a helper whose call sites are unreachable in practice is still counted — the
  two counted files are both measured slow, so the census and the timing agree here.
- I did not run the precision/recall suites, the isolation check, `--frozen`, or any VCS experiment —
  out of this item.
- Behaviour deltas (evidence markers, +27 rows, one duplicate observed+lead row) are reported as
  observed, not adjudicated; the no-harm/precision owners judge them.

## Installs

none.

## Artifacts

| path (relative to lane root) | sha256 |
|---|---|
| `.ufo/waves/round-20/w2/CorpusRuntime/runs.jsonl` (400 runs, 200 files, 8-way) | `59f39b24a5eb7866c183113092bdfa875279a6acaa58da656c8de45479f51319` |
| `.ufo/waves/round-20/w2/CorpusRuntime/serial-runs.jsonl` (400 serial runs) | `2a0ac167ff147d117bf09797cfc9d969713dfd33e43a2a5a379727394b3e6ad1` |
| `.ufo/waves/round-20/w2/CorpusRuntime/full-sweep.jsonl` (11,756 runs, 5,878 files) | `c78a9de3c6d3cd392525005d19d839d84ff003c823df5899fbb56ad7618bc3d1` |
| `.ufo/waves/round-20/w2/CorpusRuntime/recursive-helper-exposure.json` | `b1ab0538c9e4b6fdf83222abc2acd1a3aa4048ed0de0f394f19f14109dd1168f` |

Reproduce (both tool copies must be built from lane bytes, never run from the lane worktree):

```sh
cd $(mktemp -d) && git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin c \
  && git -C c remote remove origin
git -C c show 1f7f995:tools/mado-tripwire.py > /tmp/tw-old.py
cp c/tools/mado-tripwire.py /tmp/tw-new.py
python3 -I /tmp/tw-new.py --scan /home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR19/KaidokuR19.EvidenceSecurity-3.jsonl
# ~30 s new vs 0.06 s old; a 2,080-byte cell of its `def safe(n)` block + `safe(1)` reproduces ~28 s
```
