# SentTool — round 45 w1, safety review of the C1 tool, both counters and the round's host reads

**Verdict: no HIGH finding; one MEDIUM that touches the claim's own guard (clause `r`), one MEDIUM-LOW
(tool contract), three LOW, three INFO. The reference tool itself is clean on every hostile-input axis I could
reach: no process, no socket, no output injection, regular-file-only reads, caps enforced. Detail, line-exact
evidence and remediation: `.ufo/waves/round-45/w1/SentTool/findings.md`; probe transcripts in
`.ufo/waves/round-45/w1/SentTool/raw/` (`r1`–`r12`).**

## Ranked

| # | Severity | Attacks | Repro | Remediation |
|---|---|---|---|---|
| F1 | MEDIUM | C1 clause `r` (read-only) | two evasions, both score `TARGET_MET` for a tool that spawns `hyprctl`: (a) a spawn guarded by `argv == ["--selftest"]` — the marker window opens *after* clause `s` (`c1-r45-monitors.py:342-343` vs `:354-362`); (b) a `--work` path containing one apostrophe breaks the fake binary (unquoted `: > '%s'` at `:277`) so no marker is written | marker+fakebin before clause `s` and on the selftest PATH; `shlex.quote` the marker or keep it inside the fakebin dir |
| F2 | MEDIUM-LOW | tool SETUP contract (`:25-29`, `:81`, `:85-88`) | a 900 kB nested-`[` dump is an uncaught `RecursionError` (`:305-308`): 1 423 B traceback, **exit 1 = DIFFER**, no summary line | add `RecursionError` to the `except` at `:308` + one fixture; fixable pre-install, no re-freeze |
| F3 | LOW-MEDIUM | tool cost model (`:180-182`, `:345-357`) | 290 kB config + 300 kB dump = **95.7 s** wall; quadratic in each dimension; cap-scale ≈ 19 min `[INFERENCE]` | dict-keyed `add()`, indexed `effective()` (tool fix) |
| F4 | LOW | caller files under `--work` | `ctl/run-c2-controls.py:41-44` `rmtree`s fixed child names under a caller-chosen `--work` (`:84` even creates it) | `mkdtemp(dir=work, …)`; wrap `main` in `try/finally` |
| F5 | LOW | tool stderr/exit contract | reader closes early → `BrokenPipeError` traceback at `:527`, exit 1 = DIFFER | catch `BrokenPipeError` around the write |
| F6 | INFO | counters' process model | clause `s`/`f` run an arbitrary committed blob unsandboxed with the caller's rights; not in the declared residuals | one residual line |
| F7 | INFO | freeze integrity | `ctl/run-c1-controls.py:95` reads the REF text from the working tree, not a revision | read it via `git show <freeze>:…`, or print its sha256 |
| F8 | INFO | §7 items 1/4 | neither counter refuses a `--work` outside the scratch root (both *do* honour `--work`, no `/tmp`, no `TMPDIR` → item 4 is met) | a `$HYAKU_SCRATCH` guard would also defuse F4 |

## Supports (checked and clean)

- **No process, no socket** — imports are `json math os re stat struct sys` (`mado-monitors.py:90-96`);
  `strace -f -e execve,socket,connect,openat`: one `execve` (the interpreter), zero socket/connect, only the two
  named inputs opened (`r8`). This is the promise at `:22`, now observed rather than asserted.
- **No output injection** — newline, ESC/DEL, lone surrogate and a forged `MADO_MONITORS: verdict=OK` inside a
  dump `name` are all escaped by `json.dumps(ensure_ascii)` (`:407-408`, `:430`); one record per line, summary
  last and once, ASCII-only so an ASCII stdout cannot re-open the hole (`r7`).
- **Path handling** — `open(O_RDONLY|O_NONBLOCK)` + `fstat`/`S_ISREG` on the fd (`:120-138`): FIFO 0.01 s (no
  hang), directory, `/dev/zero`, symlink loop, `/proc/self/mem` → `SETUP unreadable`; symlink→regular read;
  check is post-open, so no TOCTOU redirect. `/proc` files are admitted by the contract and inert — the tool
  prints selectors and names only (`r6`).
- **Caps** — stdin 1 048 577 B → `too_large`, exactly-at-cap file parsed, over-cap config → `too_large` (`r12`);
  the only over-cap-scale risk is F3's CPU cost.
- **Regex** — every pattern `fullmatch`, bounded quantifiers, all five use sites `fullmatch`; no catastrophic
  backtracking path found (`:99-104`, `:197`, `:208`, `:217`, `:259`, `:298`).
- **Live receipt is honest and replayable** — `receipts/live-monitors-host-l1.txt` names
  `tool sha256 c6ac5fc2…`, which is the reference's bytes, and `config sha256 69c9d899…`, which is the host
  file's; replaying its own projected dump against the host config reproduces its three lines byte for byte
  (`r9`).
- **Live receipt is shape-only** — no serial, description, make/model, window title, process table or home
  listing; only the output name, numeric geometry and two content hashes. Meets considerthese `2026-10-26.md`
  proposal 1 for this file; the replay caveat is that a projection without `id`/`description` cannot agree on a
  `mirror` or long-`desc:` rule, so the replay claim is scoped to this case.
- **Pins** — all nine `fetch/` files verify against `receipts/fetch-sha256.txt` (`r9`).
- **c2 counter writes nothing** — no `tempfile`/`rmtree`/`makedirs`/write-mode `open`; git objects via
  `git -C repo show|ls-tree` only (`c2-r45-monitor-entry.py:125-141`).
- **c1 scratch** — existing `--work` (`:379`) → `mkdtemp(dir=a.work)` (`:381`) → `rmtree` of that child only, in
  `finally` (`:385`); `--work` is explicit everywhere, no `TMPDIR` reliance (`r10`).

## Routing for the L1

- **F2 and F5 are tool-side and the tool is still a draft** (`tools/mado-monitors.py` is not installed; the C1
  before-state is `tool=absent`): both can be fixed before integration without touching the frozen predicate or
  re-freezing. F2 then wants one extra fixture; no existing fixture changes.
- **F1, F4, F7 are in frozen bytes** (`quality/counters/c1-r45-monitors.py`, `.ufo/waves/round-45/ctl/run-c2-controls.py`)
  → routed as counter/driver amendments next round, with a re-freeze. F1 does not change any number already
  published in `receipts/ctl-c1.txt` (that run used a plain scratch path and a tool that spawns only in
  fixtures), but it does mean "0 of 16 controls MET" is weaker evidence than it reads: the anti-cheat clause is
  evadable in two ways.
- **F8/F4 together**: the cheapest single hardening is a `--work` locality guard plus `mkdtemp` in ctl-c2.

## Scope and hygiene

Read `registration.md` first (freeze `22a8dedd`, base `0c89478a`); lane HEAD during review `ebdba13f`. Every
probe ran under `/fast/scratch/hyaku/mado-r45/SentTool/` with `mkdtemp(dir=…)`, receipts copied into this seat
dir and the scratch tree deleted. Fixture clones were `git clone --shared --no-checkout` into scratch with
`git -C <clone> rev-parse --show-toplevel` asserted before the first commit, and a scratch identity
(`seat@scratch.invalid`) used only there. No lane/fleet/template/script/index write, no `pacman`, no service or
compositor mutation; the only compositor-adjacent command was one `hyprctl version` under `env -i`, which
refused (no instance signature). No tool was installed, so there is no version/channel line to record.
Residuals: the compositor semantics are untouched by this review (that is the non-author reading), F3's
cap-scale figure is extrapolated, and socket-level evasion of clause `r` was not attempted (already a declared
residual in the registration).
