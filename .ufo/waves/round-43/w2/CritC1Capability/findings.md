# CritC1Capability — does the installed tool deliver what SKILL/PROVINCE claim?

Round 43 (hyaku run 8), inline v1 wave **w2** — falsify the landed data. Seat `CritC1Capability`, leaf.
Target: the C1 operability claim (`tools/mado-geometry.py`) as the landed data commit describes it — `SKILL.md`'s new decision row /
probe row / § "Rule size versus reported size", and `PROVINCE.md`'s new tool row.

- Data commit `1959770657f1f8665097c1aed4be6c1cbb07139f` (base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`); host 2026-10-26,
  Hyprland 0.56.2 `efb50993780079460b0cbed1363e2166a2de1d9f`.
- Tool at the data commit: sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`, `cmp`-identical to
  `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (`receipts/pins.txt`). `SKILL.md` blob at that commit: `1753e844…`;
  `PROVINCE.md` blob: `28ff57dd…` (copies kept as `receipts/SKILL-data.md`, `receipts/PROVINCE-data.md`).
- Method: every sentence about the tool turned into an input and run (37 cases, `receipts/battery.txt`), the host's whole
  sourced rule set loaded read-only (`receipts/coverage.txt`), process/socket/file discipline traced (`receipts/strace.txt`),
  and the landed prose grepped for the support limit it states (`receipts/honesty-grep.txt`). Quotes: `verify-quotes.py`
  → `receipts/verify-quotes.txt` (`QUOTES: 15/15 found`). Replay from this seat alone: `receipts/repro/` (37/37 cases identical).

## Verdict

**The tool delivers the capability its docstring defines, and every input/output/exit claim I could turn into an input held.**
All four of the failures are in the landed prose, not the program: two false cells in `PROVINCE.md:32`, one support limit the
new SKILL section never states (and the host's own entry file trips on), and one verdict licence that claims a past event from
two current values. No axis is harmed by the tool itself; the operability row's *evidence* is narrower than its text reads.

## The host's real rule set (the question this seat was pointed at)

Read-only, `~/.config/hypr/hyprland.conf` and its transitive `source` closure (18 `source` statements, one toggle glob, one
nested `apps.conf`): **40 files, 77 `windowrule` lines, 16 with effect `size`/`float`** (`receipts/coverage.txt` §1-§2, §5).

| effect | lines | tool supports | tool counts `unsupported` |
|---|---|---|---|
| `size` | **7** | **3** (gkeep 420×500, ai-usage 875×600, localsend 1100×700) | **4** (pip 600×338 `match:tag`, system 875×600 `match:tag`, steam 1100×700 and 460×800 `match:class` + `match:title`) |
| `float` | 9 | 6 | 3 (pip `match:tag`, system `match:tag`, webcam-overlay `match:title`) |

The summary line merges both effects: `rules=3 float_rules=6 other=61 unsupported=7`. So **3 of the host's 7 size rules are
reachable**; the count of size rules the tool dropped cannot be read off `unsupported=7` at all. Reproduced at the data commit;
same counts as w1 `ExecLiveHost` F4/F5 (`w1/ExecLiveHost.md`), which is why the numbers here are a re-measurement, not a
re-finding — the new part is what the landed SKILL text says about them (F3).

And the trap the decision row does not name: `--rules ~/.config/hypr/hyprland.conf` — the file its own `<file>` placeholder most
naturally denotes — returns `rules=0 … verdict=NO_SIZE_RULES`, exit 4, because the tool does not follow `source`. All 7 size
rules are behind that file and the tool reports none of them, with no warning (`receipts/coverage.txt` §3).

## Findings

### F1 — `PROVINCE.md:32`: "`--selftest` opens no file" is false (S3, falsified)

Counterexample: `strace -f -e trace=openat … python3 -I mado-geometry.py --selftest` records three fixture opens —
`openat(AT_FDCWD, "/nonexistent/none", O_RDONLY|O_NONBLOCK)` → `ENOENT`, `openat(AT_FDCWD, "/", …) = 3`,
`openat(AT_FDCWD, "/dev/null", …) = 3` — from `selftest`'s own unreadable-path cases (`read_regular("/nonexistent/none")`,
`("/")`, `("/dev/null")`, tool copy line 388, `receipts/strace.txt`). The other half holds: the only `write()` is to fd 1, and
`grep -c 'O_WRONLY|O_CREAT'` over the whole trace is 0, so **no file is written**. The cited proof cannot reach the claim it is
attached to: `grep -n 'mkfifo\|O_WRONLY\|O_CREAT'` says nothing about `os.open(..., O_RDONLY)`.

- Impacted axis: operability (C1) — the safe-probe fence rationale ("touches nothing") rests on this cell.
- Smallest safe correction: "…; `--selftest` reads only `/`, `/dev/null` and one nonexistent path for its unreadable-path cases,
  and writes nothing (stdout only)." Drop the grep parenthetical, or re-point it at `open(`.

### F2 — `PROVINCE.md:32`: "at most 1048577 B" for `--clients` is one byte wrong (S3, falsified)

Counterexample: a regular `--clients` file of exactly 1048577 B → `MADO_GEOMETRY: SETUP too_large`, exit 2; 1048576 B is
accepted (`receipts/battery.txt`, cases `clients-too_large(1048577B-file)` and `clients-exact-1048576B`). 1048577 B on stdin is
also `too_large` — the reader *consumes* up to 1048577 bytes to detect the overflow, it does not accept that size. The tool's own
docstring states the threshold correctly ("an input larger than 1048576 bytes is too_large"); only the PROVINCE cell drifts.

- Impacted axis: operability (C1), record accuracy.
- Smallest safe correction: "at most 1048576 B (the stdin form consumes one byte more to detect oversize)".

### F3 — SKILL.md never states the support ceiling, and the entry file reads as an empty verdict (S2, capability gap)

The landed § "Rule size versus reported size" (`SKILL.md:246-290`) says what is read ("`windowrule = size W H, match:class RX`
and `windowrule = float on|off, match:class RX` lines", `:249-250`) and how lines are numbered (`:252`), but it never says:

1. that the tool counts only **one** criterion and only `match:class` — `grep -c 'match:tag'`, `'match:title'`, `'windowrulev2'`
   over the whole `SKILL.md` are **0, 0, 0** (`receipts/honesty-grep.txt`);
2. that `unsupported=` **merges size and float** — `unsupported` occurs only as a raw output field (`:225`, `:284`) and inside one
   licence phrase ("unsupported-grammar file", `:273`), never defined;
3. that `source` statements are **not followed**, so passing the orchestrator is not passing the rule set.

Measured consequence: 4 of the host's 7 size rules are invisible (`size` × 4 in the table above), and the natural invocation
`--rules ~/.config/hypr/hyprland.conf` yields `rules=0`, `verdict=NO_SIZE_RULES`, exit 4. The per-verdict licences are
defensible in isolation (`:273` does say "no supported `size` line"), but the row's own question — "Does the size a window rule
asks for match the size the compositor reports?" — therefore reads as answered when it is not, and `rules=3` invites the reading
"the host has three size rules". The probe row's host evidence (`:225`) is a single leaf file (`unsupported=0`), which cannot show
the ceiling either.

- Impacted axes: operability (C1) and coverage — the config-plane answer SKILL routes to this tool is 3/7 of the host's size rules.
- Smallest safe correction: one sentence in the section (e.g. after `:252`): "Only a `windowrule` line with a single
  `match:class` criterion is counted; `match:tag`, `match:title`, any extra `match:` field, `windowrulev2` and the block form are
  dropped (size and float merged into `unsupported=`), and `source` statements are not followed — pass every file. On 2026-10-26
  that is `rules=3` of 7 size rules across the 40-file closure, and `--rules hyprland.conf` alone returns `rules=0`, rc 4."
  Cheap alternative if the sentence is unwanted: name the ceiling in the decision row next to `<file>`.

### F4 — `SKILL.md:270` TILED licence asserts a past event the dump cannot carry (S3, licence overreach)

The cell reads "the matched client is not floating, so the first-map floating branch that reads `static_.size` never ran for it".
Upstream that branch is guarded by `m_firstMap` (`Hyprland-DefaultFloatingAlgorithm.cpp:49`, fetch receipt), i.e. whether it ran
is *history*; the tool reads only the current `floating` flag and `size`. A window that opened floating (branch ran) and was later
tiled reports `floating=false` and lands in TILED. `[INFERENCE]` — not demonstrable without mutating the session, which is barred.

- Impacted axis: operability (C1) licence precision; the verdict output itself is unaffected (a tiled window's reported goal is
  the layout's, so the box would not equal `want` anyway).
- Smallest safe correction: "the matched client reports `floating=false`, so its reported goal is not the floating path's; the
  rule's size is inert for this client" — keep the existing class-level caveat in the "does not license" cell.

## What held (the tool needs no change)

| Claim (locator) | Attack | Result |
|---|---|---|
| inputs: `--rules` each read whole, 1048576 B cap (`PROVINCE.md:32`) | 1048576 B / 1048577 B rules file | accepted / `SETUP too_large` |
| missing, unreadable, directory, FIFO or non-regular path is a setup error | missing path, directory, FIFO, `/dev/null`, `/dev/zero`, mode-000 file | `SETUP unreadable`, exit 2 each; symlink→regular accepted |
| clients input regular file or `-`, UTF-8 JSON list of objects | object JSON, 1048577 B file, FIFO, 1048576 B padded | `bad_json` / `too_large` / `unreadable` / accepted |
| setup failure = one stdout line, exit 2 (`docstring`) | 16 setup cases | one line, exit 2, stderr 0 B in every case |
| exit map 0/1/3/4 and its order | agreement, differ, no-match, no-size dumps | `OK`/`DIFFER`/`NO_MATCHING_CLIENT`/`NO_SIZE_RULES`, rc 0/1/3/4 |
| `windowrulev2` ignored, counted nowhere | v2-only file | `other=0 unsupported=0 rules=0` |
| unsupported grammar (`match:tag`, extra field, `[..]`, 201-char regex) | one fixture each | `unsupported=1`; 200-char accepted |
| rules numbered across files, last matching `size` wins | two files, both orders, `--rules` order | n=1.. across files; last file's rule is `want` (matches `applyStaticRule` in rule order, `Hyprland-WindowRuleApplicator.cpp:492,506`) |
| `mapped:false` skipped; size must be two JSON ints (no bool/float/negative) | `--selftest` 73 cases + host dump | `MADO_GEOMETRY_SELFTEST: 73/73 passed` |
| "starts no process, opens no socket and reads no config tree of its own" (`SKILL.md:250`) | strace of a real run | 0 socket/connect/clone/fork; opens exactly the two caller files; 1 write, to fd 1 |
| tool is the round-42 reference; host receipt reproducible | sha/cmp; gkeep.conf vs fetch pin | identical `e3c2e471…`; `3726e488…` both sides; L1's `rules=1 … rc 3` line reproduced |
| upstream citations in the section | `HyprCtl.cpp:395,427-428`; `GeometricMovableAnimated.cpp:19-20`; `DefaultFloatingAlgorithm.cpp:49,55-56`; `WindowRuleApplicator.cpp:422,426`; `RegexMatchEngine.cpp:16,7-8` | all read and correct at `efb5099…` |

## Reproduce

`receipts/repro/gen-fixtures.sh` → `receipts/repro/battery.sh` (point `G=` at `receipts/mado-geometry-copy.py`);
`repro/gen-coverage.sh` + `repro/srcwalk.py` + `repro/classify.py` (host read-only); `repro/gen-strace.sh`;
`repro/gen-honesty.sh`; then `python3 verify-quotes.py`. Hashes: `receipts/shas.txt`.

## What this seat did not do

No repository or host write; no `pacman`/install; no counter run; no build/lint/test gate; no subagent; no `hyprctl` verb beyond
`clients -j`; no compositor oracle. Scratch `/fast/scratch/hyaku/mado-r43/CritC1Capability` was used for fixtures only and is
deleted before this seat yields — nothing citable lives there.
