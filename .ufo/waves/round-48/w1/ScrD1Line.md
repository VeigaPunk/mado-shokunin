# ScrD1Line — routed D1/D3 (round 48, w1, BUILD, policy v1)

Seat: leaf scribe, no subagent dispatch. Lane `mado-shokunin`, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`.
Claim context: w1 build wave; **no counter scored, no predicate frozen by this seat** — this feeds the L1's freeze.

`Report: .ufo/waves/round-48/w1/ScrD1Line.md`

## Behaviour

Diffed the module docstring of the frozen C1 reference against the landed tool, and drafted the appended lesson lines.

| side | path | revision | blob sha256 |
|---|---|---|---|
| frozen | `.ufo/waves/round-47/l1-draft/mado-terminal.py` | `d7527d60` = base `579f694b` | `762d042c96e7e5f2c3187133b0ffe670c1d076b698b958199602cfa019aa6c08` |
| landed | `tools/mado-terminal.py` | base `579f694b` (and the working tree) | `b84d5c4f723049c0fd14189ffc7b6db1f71eb70fb97e0c476d20ddeca6de2222` |

`git cat-file -t` confirms both revisions; `git show <rev>:<path> | sha256sum` equals the working-tree bytes for both
sides, and `d7527d60:tools/mado-terminal.py` is the empty blob (`e3b0c442…`) — the frozen reference is the `l1-draft` file,
as the seat spec says.

The docstring delta is **exactly two hunks** (86 → 87 lines, `difflib` opcodes): the step-5 `command -v` sentence and the
out-of-contract list. The first is already recorded as M47-10 (`corpus/lessons/round-47.md:205`) → no new line. The second
adds three out-of-contract items. A fourth post-freeze delta left no docstring hunk (code fixed, contract text not).

Deliverable: `.ufo/waves/round-48/w1/ScrD1Line/lines.md` — five drafted lines, `**M47-11**` .. `**M47-15**`, in the
round-47 lesson's own `## Mistakes` style, each naming the frozen **and** the landed locator:

- **M47-11** `HOME unset` — docstring `tools/mado-terminal.py:85` vs frozen `:84`; the raise predates the freeze
  (frozen `:407` = landed `:410`), so the delta is contract text, and the pin's failure is conditional (`x:148/:166/:172`).
- **M47-12** `a FIFO named like a desktop file in a later application dir` — `:85-86` vs frozen `:84-85`; the raise is new
  (`:526-529`) where the frozen walk skipped (`frozen:519`).
- **M47-13** `symlink loops` — `:86` plus the blanket exit-2 sentence `:88`; no code path raises (guard `:512-514`, unchanged
  from `frozen:503`).
- **M47-14** the "anything else": step 4 of the docstring still describes the pre-H1 model (`:49-52`, byte-identical to
  `frozen:49-52`) while the walk registers any path type in later dirs (`:494-495`, `:535`).
- **M47-15** the D3 routing line, anchored at `.ufo/waves/round-47/w2/ExecC1Determinism.md:10`.

## Gates

- No counter run, no axis score, no fixture scored — none is this seat's.
- Locator/quote gate: `.ufo/waves/round-48/w1/ScrD1Line/verify-lines.py` → `receipts/verify-lines.txt`,
  **`VERIFY: 113 checks, ALL PASS`**, exit 0 (the last 9 checks are cross-seat: the peer report
  `w1/ExecHomeUnset.md` is present and carries the tokens I cite from it, and `lines.md` names the numbering collision). It asserts: both blob identities at both revisions; the docstring delta is
  exactly 2 hunks and hunk 1 is the `command -v` sentence; the frozen docstring lacks and the landed docstring has all
  three added items; 23 (file, line-range, quote) triples, each quote present in the bytes it names and reproduced in
  `lines.md`; `x:148/:166/:172` expand `${HOME}` and `:23` is `set -euf`; `case_env:222` injects HOME; 190 fixtures, none
  with HOME in `env`, none with a symlink; every receipt present with the exact bytes cited; and the write-scope invariant.
- Write-scope gate: `git status --porcelain` shows **no modified file under `tools/`, `quality/` or `corpus/`**. The one
  modified tracked path is `.ufo/waves/round-47/w1/ExecCounterC1.md` mtime `2026-10-26 20:54:05` (+29 lines) — a third-party
  edit (my seat started 20:45 and every write of mine is enumerated below), reported verbatim, not touched.

## Touched surfaces

Written (all inside the seat dir, plus this report):
`.ufo/waves/round-48/w1/ScrD1Line.md`, `.ufo/waves/round-48/w1/ScrD1Line/lines.md`,
`.ufo/waves/round-48/w1/ScrD1Line/verify-lines.py`, `.ufo/waves/round-48/w1/ScrD1Line/receipts/` (18 files: probe
drivers `probe.sh`, `probe2-7`, `home2.sh`, `probe4.py`, `probe5.py`; their outputs `probe-out.txt`, `probe2-out.txt` …
`probe7-out.txt`, `home2-out.txt`; `receipt-home-unset-host.txt`; `verify-lines.txt`).
Read-only: the pin `/usr/bin/xdg-terminal-exec` (sha256 `89f2be9a…3127ac`), `tools/mado-terminal.py`, the frozen draft,
the counters, the fixtures, the round-47/48 lesson and wave docs, `quality/`, `corpus/`.

Not written: any tracked lane file, the lane's git/jj index, the host cache, `~/.config`, `~/.local`, PATH dirs.

## Findings

1. **D1 is three out-of-contract items, and one of them is not an exclusion at all.** `symlink loops` has no raise: the
   ancestor guard (`tools/mado-terminal.py:512-514`) prunes repeats exactly where `find -L` prunes, and pin and tool agreed
   on rc and stdout in all three shapes built (`receipts/probe2-out.txt` C, C3). The peer seat adds a fourth shape and the
  only trace-level residual: `find -L` drops a loop path from registration while the tool registers it and refuses to
  recurse — but a find-refused loop path is a directory and both sides skip a directory read as an entry
  (`tools/mado-terminal.py:551-552`), so no printed id/stdout/status can differ. The docstring's closing sentence (`:88`)
   promises exit 2 for every listed item, which is false for this one — freezing it would create a `TARGET_MISSED` the tool
   cannot fix honestly.
2. **The round-47 sentence "HOME unset → pin exit 1, empty stdout" is a sub-case.** Measured in the counter's own bwrap
   sandbox (`Box.run`, `--clearenv`): HOME absent + all `XDG_*` set → pin `rc 0` + `term.desktop`, tool `rc 2`
   (`receipts/probe4-out.txt`, `probe5-out.txt` row 1); HOME absent + `XDG_CACHE_HOME` absent, or no `XDG_*` → pin `rc 1`,
   empty stdout, tool `rc 2` (`probe5-out.txt` rows 2-3); host `env -i` → `line 148: HOME: unbound variable`, `rc 1`
   (`receipts/receipt-home-unset-host.txt` R1). So in the all-set regime the tool refuses a selection the resolver makes,
   and in the fatal regime the two refusals differ only in status — the C1 contract must pick and state which regime the
   freeze covers. This contradicts `claims.md:20` ("HOME unset modelled as the pin (… pin exit 1, empty stdout)") as a
   blanket statement and matches `corpus/lessons/round-47-verifier-spotcheck.md:46` only in the fatal regime.
   **Method trap, recorded so no other seat repeats it:** this session exports `XDG_CONFIG_HOME`, `XDG_DATA_HOME` and
   `XDG_CACHE_HOME`, so a host probe with `env -u HOME` alone leaves exactly the defaults the pin needs set and the pin
   answers from the host tree. My first host probe fell into it; `receipts/probe3-out.txt` is kept solely as that example
   and is cited as non-evidence in `lines.md`.
3. **The FIFO exclusion is conditional, and the tool is broader than the script.** The pin *registers* a FIFO in a later
   dir and blocks only when it reads it: with no list file the FIFO is the first fallback candidate → blocked, `rc 124` under
   `timeout 5` (`probe2-out.txt` B); with a list file naming the valid entry the pin answers `rc 0` + `term.desktop` while the
   tool still exits 2 at walk time (`probe7-out.txt`). Peer corroboration: `w1/ExecHomeUnset.md` (same round) reports the pin
   registering the FIFO ("registered … as entry") and answering `rc 0` when it is not the candidate read.
4. **The landed docstring's step 4 is stale against the landed code (not only against the pin).** It still says
   `` `find -L <dir>/. -type f` over the application dirs `` and "a path counts when its part after `<dir>/./`…"
   (`:49-52`), while the walk applies `-type f` to the first dir only and registers any path type later (`:494-495`, `:535`).
   Proof: a directory named `x.desktop` in the later dir shadows the valid file in the earlier one — tool prints nothing,
   `rc 1`, explain "is shadowed by … (the later application dir wins)"; pin prints nothing, `rc 1`
   (`probe6-out.txt` tree A). This is M47-10's class one layer down: the reference drift was fixed in the code and left in
   the contract text, which is what the freeze reads. The peer seat drafted the same finding independently as its own
   `**M47-12**` (its section 5); it has since relabelled that line "placeholder label only — `ScrD1Line` numbers the step-4
   item M47-14 and the FIFO item M47-12" and asks for one step-4 line. `lines.md` records both sides, so the labels to land
   are M47-11 delta / M47-12 FIFO / M47-13 loops / M47-14 step 4 / M47-15 readdir routing.
5. **D3 routed, not claimed.** `M47-15` directs the readdir-order blind spot (`w2/ExecC1Determinism.md:10`) into the
   round-48 fixture work with M47-10: a two-valid-candidates case whose winner depends on readdir order, recorded with its
   order or a set-valued `expect`, so a `sorted()` mutant fails a fixture rather than a nonce lottery. No fixture in the
   frozen 190 can see it (builder varies path depth only, `.ufo/waves/round-47/ctl/build-fixtures.py:70`, stability test
   `:76`).

## Out of scope (not done, not claimed)

C1's warm-cache implementation and its counter/fixtures (schema v2, `prime`/`after`/`cache`), D2 (session-material number
with a receipt), D4 (the round-47 entry's off-by-one erratum), R3 (session-material synthetic marker), R4b (round-45 errata
under the frozen round-45 verdict), M47-10's fixture work, `w2/CritC1Explain.md` (explain `cmd=` compared),
`w2/SentC1Sandbox.md` F1-F4. No lesson or corpus file was edited: the lines are drafted for the L1 to append.

## Limits

- The pin's HOME/failure matrix was measured in the r47 counter's `bwrap` sandbox and with `env -i` on the host; other
  sandboxes (e.g. one that binds `/etc`) could add a third regime and were not built.
- Loop coverage is three shapes (self-loop, ancestor loop, entry reachable only through a looped subdir) in the
  first-walked dir; a loop in a later dir was reasoned about but not run.
- The FIFO cases use one FIFO per tree; multiple FIFOs, or a FIFO that is reachable only through a symlinked subtree, were
  not probed.
- The three loop shapes and the FIFO registration are also reported by peer seat `w1/ExecHomeUnset.md`; I did not re-run
  their drivers, only my own.
- No tool was installed or upgraded; no package manager, no compositor call, no GUI, no terminal launch. The pin ran only
  with `--print-id`, always with `XDG_CACHE_HOME` inside the scratch root; the host cache `~/.cache/xdg-terminal-exec`
  mtime is `2026-10-26 17:42:25.200770484 -0300` before and after. Scratch `/fast/scratch/hyaku/mado-r48/ScrD1Line`
  (4.1 MB) was removed; every receipt was copied into the seat dir first.
