# CritC1Capability — w2 report (C1 capability row, SKILL.md § "Rule size versus reported size", PROVINCE.md tool row)

STATUS: **complete**. Findings at `.ufo/waves/round-43/w2/CritC1Capability/findings.md`; receipts beside it.
Data commit `1959770657f1f8665097c1aed4be6c1cbb07139f`; host read-only (only `hyprctl clients -j`). No repository file edited,
no host mutation, no counter/build/gate run, no subagent, no tool installed.

## Answer to the assigned question

The installed tool (`e3c2e471…`, byte-identical to the round-42 reference) **delivers the capability its docstring defines**:
37 adversarial cases over inputs, grammar, clients, exit map and the process/socket/file discipline all match the landed text,
`--selftest` is `73/73`, and a real run opens exactly the two caller-supplied files with zero socket/clone/fork. The failures are
all in the landed prose.

**Host rule set** (40-file transitive `source` closure of `~/.config/hypr/hyprland.conf`, 77 `windowrule` lines): **7 `size`
rules — the tool supports 3**, and 4 are dropped into `unsupported=`, which merges them with 3 dropped `float` rules
(`unsupported=7` total; `rules=3 float_rules=6 other=61`). The limit is **not** stated honestly in SKILL.md: the file contains
zero occurrences of `match:tag`, `match:title`, `windowrulev2` or `source` in this context, the section never defines
`unsupported`, and `--rules ~/.config/hypr/hyprland.conf` itself returns `rules=0`, `NO_SIZE_RULES`, exit 4.

## Findings (severity, axis, smallest safe correction)

| id | what | sev | correction |
|---|---|---|---|
| F1 | `PROVINCE.md:32` "`--selftest` opens no file" — **false**: strace shows `openat("/", O_RDONLY)` and `openat("/dev/null", O_RDONLY)` from selftest's unreadable-path cases; "writes nothing" holds (only `write(1)`, zero `O_WRONLY\|O_CREAT`) | S3 | say it reads `/`, `/dev/null` and one nonexistent path; drop the `mkfifo\|O_WRONLY\|O_CREAT` parenthetical (it cannot prove an `O_RDONLY` non-open) |
| F2 | `PROVINCE.md:32` "`--clients` … at most 1048577 B" — **false for the file form**: 1048577 B → `SETUP too_large`; accepted max is 1048576 (the docstring already says so) | S3 | "at most 1048576 B (the stdin form consumes one more byte to detect oversize)" |
| F3 | SKILL § "Rule size versus reported size" never states the support ceiling (single `match:class` only; `unsupported` merges size+float; `source` not followed); 4 of 7 host size rules invisible, and the entry file reads as an empty verdict | S2 | one sentence naming the ceiling and the 3-of-7 host figure, or name it beside `<file>` in the decision row |
| F4 | `SKILL.md:270` TILED licence asserts a past event ("never ran for it") from two current values; the branch is `m_firstMap`-guarded | S3 | "the matched client reports `floating=false`, so its reported goal is not the floating path's" |

F3's counts are a re-measurement of w1 `ExecLiveHost` F4/F5 (still true at the data commit); the new material is the text-honesty
question and the entry-file `rc 4` measurement. F1/F2/F4 are new.

## Evidence

- `receipts/battery.txt` (37 cases, every claim sentence run; stderr 0 B on all exits) · `receipts/strace.txt` (selftest + real run)
- `receipts/coverage.txt` (40 files, 77 rule lines, 7 size / 3 supported, entry-file rc 4) · `receipts/honesty-grep.txt`
  (SKILL/PROVINCE text at the data commit) · `receipts/pins.txt` (tool/reference/gkeep/SKILL/PROVINCE shas)
- `receipts/verify-quotes.txt` — `QUOTES: 15/15 found`; `receipts/shas.txt`; replay scripts in `receipts/repro/`
  (replayed 37/37 identical from the seat copies alone).

Tooling: none installed (`strace` present on the host; no `pacman`). Scratch `/fast/scratch/hyaku/mado-r43/CritC1Capability`
removed before yield; nothing citable lived there.
