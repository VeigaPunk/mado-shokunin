# w2/SentLiveRun — live host run reproduction + injection/ReDoS review of the landed tool (round 44)

Status: **complete**. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, head `290cddea` (data commit
`e4678921`, base `6a1a9052`), freeze `03fa5c618b089064a657b3d79d3d4272ae4b6894`.
Landed tool reviewed: `tools/mado-geometry.py`, sha256 `1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4`
— byte-identical to the freeze's reference `.ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt` (`cmp` → `REF_IDENTICAL`)
and to the receipt's own header hash. Round-43 baseline: `git show 6a1a9052…:tools/mado-geometry.py`, sha256
`e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`.
Host Hyprland 0.56.2 at `efb50993780079460b0cbed1363e2166a2de1d9f`; python3 3.14.8; nothing installed; no package
transaction; no compositor mutation (reads only: `version`, `clients -j`); no subagent; scratch
`/fast/scratch/hyaku/mado-r44/SentLiveRun` used for raw dumps and the round-43 copy and removed at the end.

## What was run

| # | command | result |
|---|---|---|
| A | `python3 -I .ufo/waves/round-44/w2/SentLiveRun/make-live-receipt.py --tool tools/mado-geometry.py --rules ~/.config/hypr/gkeep.conf` (issues `hyprctl version`, then `hyprctl clients -j` twice: once for the pipe, once for the state columns) | re-run 2026-10-26T14:44:47-03:00; stdout 3 lines **equal to receipt lines 3-5**, `exit=3`, stderr 0 bytes; state block equal to receipt lines 8-10 → `live-run.txt` |
| B | `project.py` on a 14:38 capture (`hyprctl clients -j`) | 10-key projection `live-clients-projected.json` sha256 `1600c170…`; raw 2619 B sha256 `9a3192a3…` not retained; tool on raw and on projection → same stdout sha `634af233…` → `projection-invariance.txt`, `raw-dumps.sha256` |
| C | `capture-twice.py` (two fresh captures, compared in memory) | both raw sha `1d4fbc8a…` (2619 B), both projections sha `3e9c88d5…`, `projections identical: YES`; r43 and landed both rc 3, stdout sha `634af233…` → `capture-twice.txt` |
| D | `make-state-dumps.py` + `state-matrix.py` (14 state dumps built from the projected live record) | `state-matrix.txt` |
| E | `fuzz-differential.py --r43 R43.py --tool tools/mado-geometry.py --cases 400` | 400 cases, **0 mismatches**; `differential.txt` |
| F | `probe-security.py --r43 R43.py --tool tools/mado-geometry.py` | `injection-probe.txt`, `args-probe.txt`, `redos-probe.txt` |
| G | `strace -f -e trace=execve,execveat,socket,connect,bind,openat,open,unlink,rename,write python3 -I tools/mado-geometry.py --clients <dump> --rules ~/.config/hypr/gkeep.conf` | `trace-summary.txt` |
| H | `python3 -I .ufo/waves/round-44/w2/SentLiveRun/verify-quotes.py` | `VERIFY_QUOTES: PASS (15 of 15 verified)` |

## Findings

### F1 — the live receipt reproduces exactly (supports the target; no defect)

What it attacks: `.ufo/waves/round-44/receipts/live-geometry-host-r44.txt:1-10` as a claim about this host at this
commit. Re-run with the two allowed read verbs only, the tool on stdin exactly as the documented pipe:

```
MADO_GEOM_RULE: n=1 file=1 effect=float arg=on class=^(org.omarchy.gkeep)$
MADO_GEOM_RULE: n=2 file=1 effect=size arg=420x500 class=^(org.omarchy.gkeep)$
MADO_GEOMETRY: rules=1 float_rules=1 other=1 unsupported=0 clients=3 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT
exit=3
```

Receipt line 5 (`clients=3 matched=0 … verdict=NO_MATCHING_CLIENT`) and `exit=3` are reproduced line for line;
stderr is 0 bytes (`live-run.txt`). The receipt's header claims also hold: tool sha256 `1da3dda…`
(receipt:1) = the file on disk, and `Hyprland 0.56.2 … efb5099…` = `hyprctl version` today. The receipt's state
block is reproduced too (`Alacritty False 0 0`, `zcode False 0 0`, `grok-bot False 0 0`; two captures taken
seconds apart are byte-identical, and the client set is the same three classes as the w1 reads
`w1/ExecLiveHost.md` F1/F2). `clients=3`, `unmapped=0` and `matched=0` are the only counts the receipt prints and
all three are reproduced; the raw dump's session material (titles, focus history) is not retained and never printed
(`raw-dumps.sha256` records the hash only).

Severity: none (positive). Repro: `make-live-receipt.py` row A above.

### F2 — the non-state path is byte-identical to round 43 (supports registration clause r; no regression)

What it attacks: the landed docstring's "a dump with no maximized or fullscreen matched client prints the round-43
line unchanged" and the C1 contract's r clause. Two independent checks:

- 400 randomized dumps whose `fullscreen` is never a JSON integer 1 or 2 (absent, `0`, `true`, `2.0`, `"2"`, `3`,
  `-1`) crossed with 8 `size` shapes, 4 classes, mapped/unmapped: **stdout, stderr and exit code identical** to the
  round-43 tool in all 400 (`differential.txt`).
- On the live dump, both tools emit stdout sha `634af233…`, rc 3 (`capture-twice.txt`).

Severity: none (positive). Repro: row E; row C for the live bytes.

### F3 — the state dimension behaves as the docstring says (supports C1's operability surface)

What it attacks: the landed docstring's verdict order and exit map. `state-matrix.txt`, fixtures built from the
projected live record:

| fixture | rc | verdict | state tokens |
|---|---|---|---|
| `fullscreen` (size = monitor box, `fullscreen: 2`) | 5 | NOT_COMPARED | `maximized=0 fullscreen=1` |
| `maximized` (`fullscreen: 1`) | 5 | NOT_COMPARED | `maximized=1 fullscreen=0` |
| `maximized-nonfloating` (would have been TILED in r43) | 5 | NOT_COMPARED | `maximized=1 fullscreen=0` |
| `fullscreen-and-tiled` | 5 | NOT_COMPARED | `tiled=1 … fullscreen=1` |
| `fullscreen-and-agree` | 0 | OK | `agree=1 … fullscreen=1` |
| `fullscreen-and-differ` | 1 | DIFFER | `differ=1 … fullscreen=1` |
| `fs-bool-true` / `fs-string-2` / `fs-float-2.0` / `fs-mode-3` / `fs-mode-negative` / `fs-mode-0` / `fs-mode-null` | 0 | OK | no state tokens — each non-integer-1-or-2 value ignored |
| `fs-unmatched-class` (`fullscreen: 2`, class not matched) | 3 | NO_MATCHING_CLIENT | no state tokens — unmatched state not counted |
| live projection | 3 | NO_MATCHING_CLIENT | no state tokens |

Exit codes are the child's own, not a shell tail. `DIFFER` still outranks `NOT_COMPARED`, `OK` is not printed when
`agree=0` and a state client matched, and a TILED-only dump stays `OK` (docstring lines 69-77; `tools/mado-geometry.py:200`,
`:277`). The state words appear only when `maximized + fullscreen > 0`, which is why the live summary is the r43 line.

Severity: none (positive). Repro: row D.

### F4 — the field the tool reads is the compositor's internal mode (supports the state premise)

`fetch-c1/Hyprland-HyprCtl.cpp:431` feeds `"fullscreen"` from `getFullscreenModes(w).internal` (line 432 feeds
`"fullscreenClient"` from `.client`), and the enum is `FSMODE_MAXIMIZED,` = 1, `FSMODE_FULLSCREEN,` = 2
(`fetch-c1/Hyprland-FullscreenController.hpp:13-15`); both pins re-hash to `receipts/fetch-sha256.txt`. So reading
`fullscreen` (not `fullscreenClient`) is the pin's fact, and the tool's `1 or 2, not bool, not float` input shape is
what this host emits (`fullscreenClient` is carried and never read — `SKILL.md:281`).

### F5 — ReDoS surface unchanged; a pre-existing accepted shape still hangs the tool (no round-44 regression)

What it attacks: the claim that the round-44 edit did not widen the tool's regex surface, and `SKILL.md:305-311`'s
description of it. The edit adds no regex: `SAFE`, `MATCH_FIELD`, `RULE_LINE`, `NUM` are byte-identical between
round 43 and the landed file (`CONSTANTS_IDENTICAL`, `SAFE = re.compile` at `tools/mado-geometry.py:89`), and the
16-pattern acceptance matrix is identical tool-for-tool (`redos-probe.txt`), including the six patterns both accept
that backtrack catastrophically: `(a+)+`, `(a|a)+`, `(a*)*`, `(a+)*`, `(a|aa)+`, `a(b+)+c`.

Cost, identical on both tools (`(a+)+`, class `"a"*n+"b"`):

| n | 18 | 20 | 22 | 24 | 26 |
|---|---|---|---|---|---|
| landed wall | 0.034 s | 0.061 s | 0.167 s | 0.617 s | **2.391 s** |

×4 per +2 characters, i.e. exponential. The documented guard works on the landed tool: under `timeout 5`, a 31-char
class → rc 124, **0 bytes of stdout, 0 bytes of stderr**; a 1024-byte class → rc 124, 0 bytes (`redos-probe.txt`).
Exploit path (unchanged since round 43, LOW-MEDIUM): a local Wayland client chooses its own `app_id`, so a client can
advertise `"a"*31+"b"`; if the user's rule file holds a nested-quantifier pattern, the next manual run of this
diagnostic hangs instead of printing a verdict. No privilege boundary is crossed (the tool is user-run, read-only,
socket-free), and the pattern must come from the user's own config. Impact: a DoS of the diagnostic, misread as
"still thinking". Smallest remediation is documentation plus the existing `timeout 5`; changing `regex_ok` to reject
nested quantifiers would change the contract and is **not** a w2 edit. See F9 for the text defect.

### F6 — no injection surface found in the landed tool (no regression)

What it attacks: the tool's stdout as a line protocol, given untrusted client text and attacker-shaped rule files.
All in `injection-probe.txt`:

- class `"org.omarchy.gkeep\nMADO_GEOMETRY: … verdict=OK"` → the client is dropped before any line is printed
  (`matches()` rejects characters below U+0020, `tools/mado-geometry.py:207`); `matched=0`, no forged line.
- class with ESC → same; class `a"b%sc` → `class="a\"b%sc"` (JSON quoting; `%` is data, not a format directive);
  class `hélloé` → `class="h\u00e9llo\u00e9"`.
- nine hostile rule bodies (lookaround, backref, missing separator, 9-digit argument, `\d`, control char, space,
  quote, `%`) → `unsupported=9`, no rule line, `NO_SIZE_RULES` rc 4: a rule regex cannot inject because `SAFE`
  excludes whitespace, `=` and newlines.
- malformed dumps (`{"a":1}`, `[1,2,3]`, invalid UTF-8) → one line `MADO_GEOMETRY: SETUP bad_json`, rc 2, stderr
  empty; 1048577-byte input → `SETUP too_large`; empty list → `NO_MATCHING_CLIENT` rc 3.
- argument/path matrix (10 cases: `--selftest` with extras, duplicate `--clients`, missing flag, `--rules -`,
  directory, `/dev/null`, `/dev/zero`, unknown flag) → `SETUP usage` rc 2 or `SETUP unreadable` rc 2, exactly as the
  docstring says; `--rules -` is a path named `-`, not stdin (`args-probe.txt`).

One residual, pre-existing and not a tool defect: `class` is client-chosen, so a matching client whose class is
`x verdict=OK` prints that token before the tool's own verdict; `grep -o 'verdict=[A-Z]*'` then yields
`['verdict=OK', 'verdict=DIFFER', 'verdict=DIFFER']`. The client line's last field and the summary line are
unambiguous, and this seat compared whole lines, not greps. (w1/ScrSkillProvince item 13 and
w1/SentLiveReads S5 raised the same reader hazard; the prose fix is not in the landed `SKILL.md`.)

### F7 — no new process, socket or write surface (PROVINCE row holds on the landed bytes)

`trace-summary.txt` from the row-G trace: 0 `socket`/`connect`/`bind`; 1 `execve` (the interpreter itself); the only
input opens are the two caller paths with `O_RDONLY|O_NONBLOCK|O_CLOEXEC`; 0 `O_WRONLY`/`O_RDWR`/`O_CREAT`/`O_TRUNC`/
`O_APPEND`; 0 `unlink`/`rename`; one `write(1, …, 306)` and zero writes to fd 2. The landed diff adds no import
(`json, os, re, stat, sys` before and after) and no new file open, so `PROVINCE.md:32`'s "no compositor socket, no
Wayland client, no network, no config tree, no process started … stdout only" is true of the landed file, not only of
the reference.

### F8 — OPEN content defect: the documented host run carries round-43 counts (LOW)

What it attacks: `SKILL.md:293-294`, the `clients=4` example at `SKILL.md:299`, and the same summary in the command
row at `SKILL.md:225`, all dated 2026-10-26. The landed receipt for the same day and commit says `clients=3`
(`receipts/live-geometry-host-r44.txt:5`), and today's host has three mapped clients (all `floating=false`, i.e.
three tiled), so the example's `clients=4` and "four tiled" cannot be the round-44 run. The four-client output is the
round-43 receipt's line (`.ufo/waves/round-43/receipts/live-geometry-host.txt:10`, whose census includes `chromium`),
i.e. a stale round-43 paste labelled as the round-44 host run. The verdict is unaffected — only the counts are.

Exact corrections (L1's call):

- `SKILL.md:293-294`, replace the sentence
  "Host run 2026-10-26, no gkeep window open: the gkeep rule file declares `size 420 500` and the dump holds four tiled clients, so nothing matches."
  with
  "Host run 2026-10-26, no gkeep window open: the gkeep rule file declares `size 420 500` and the dump holds three tiled clients, so nothing matches."
- `SKILL.md:299` (example block) and `SKILL.md:225` (command row): `clients=4` → `clients=3`, everything else unchanged.

Evidence: row A output (`clients=3`, three tiled clients), row C (two captures, same three clients, `unmapped=0`),
`receipts/live-geometry-host-r44.txt:5`.

### F9 — OPEN content defect: the ReDoS trigger class is under-described (MEDIUM for the text, not the tool)

What it attacks: `SKILL.md:305-307`, "A rule regex inside the accepted alphabet with an alternation under a repeat,
such as `(a|aa)+$`, makes the tool hang …". The landed `regex_ok` also accepts **nested quantifiers**
(`(a+)+`, `(a*)*`, `(a+)*`, `a(b+)+c` — all `True` in `redos-probe.txt`), and that shape is the cheaper trigger:
2.39 s at 26 characters and past 5 s at 31, versus the documented `(a|aa)+$` at about 4.6 s for 38 characters. A
reader who trusts the sentence will believe a nested-quantifier rule is safe. w1 already flagged this
(`w1/ScrSkillProvince.md:113` item 12; `w1/SentLiveReads` S2) and it is unchanged in the data commit — this seat
re-measures it on the landed bytes and reports it as still open.

Exact correction (L1's call), `SKILL.md:305-307`: replace
"A rule regex inside the accepted alphabet with an alternation under a repeat, such as `(a|aa)+$`, makes the tool hang on a long class string"
with
"A rule regex inside the accepted alphabet with a repeat nested inside or around a repeat, such as `(a|aa)+$` or `(a+)+`, makes the tool hang on a long class string"

The rest of the paragraph (the `timeout 5` command at `SKILL.md:309`, "treat exit 124 as no verdict", RE2's
non-backtracking) is correct and stays: rc 124 with zero bytes of output is measured on the landed tool.

## Not established (declared)

- **No live maximized or fullscreen window.** The live dump carries `fullscreen: 0` for all three clients, so F1
  reproduces a `NO_MATCHING_CLIENT` run and nothing more; F3/F4's state paths are synthetic dumps built on the
  projected live record plus the pinned assignment. Creating a fullscreen gkeep window needs the operator's keys
  (`hyprctl dispatch` is out of bounds here).
- **Raw dumps not retained.** `raw-dumps.sha256` keeps hashes and the dropped-key list; the raw bytes lived in
  scratch and are gone, per the shape-only rule (w1/ExecLiveHost). The receipt's own raw hash is not recoverable for
  comparison — only its printed state columns are, and all four match.
- **Client order is not stable.** Two captures seconds apart were byte-identical (`1d4fbc8a…`), but the 14:38 capture
  differed from the 14:44 run in ordering/focus material, so the projection file sha (`1600c170…`) differs from the
  capture-twice projection sha (`3e9c88d5…`) although both describe the same three clients with the same ten fields.
  Nothing in F1-F3 depends on order: the live dump matches no rule, so line order never enters the stdout.
- **Not scored.** This seat does not run `c1-r44-geometry-states-v2.py` or `c2-r44-gkeep-size-request-v2.py` and makes
  no claim about their after-data lines; F5/F9 are tool and prose defects, not predicate defects, so no
  re-registration is triggered.

## Files written (all inside `w2/SentLiveRun/`, plus this report)

`live-run.txt` (row A receipt), `live-clients-projected.json` (10-key projection), `raw-dumps.sha256`,
`projection-invariance.txt`, `capture-twice.txt`, `state-dumps/*.json` (14 fixtures), `state-matrix.txt`,
`differential.txt`, `injection-probe.txt`, `args-probe.txt`, `redos-probe.txt`, `trace-summary.txt`,
`verify-quotes.out`, and the builders `make-live-receipt.py`, `project.py`, `capture-twice.py`,
`make-state-dumps.py`, `state-matrix.py`, `fuzz-differential.py`, `probe-security.py`, `verify-quotes.py`.
No tracked file was edited; `git status --porcelain` shows only `w2/` and the wave's ready markers. Nothing written
outside the seat dir; scratch removed.

Tooling: nothing installed (python3 3.14.8, `/usr/bin/strace`, `git` and `hyprctl` already present); no package
transaction, per the paused-pacman guard.

## Checks the integrator should run

- `python3 -I .ufo/waves/round-44/w2/SentLiveRun/verify-quotes.py` → `VERIFY_QUOTES: PASS (15 of 15 verified)`.
- `git show 6a1a9052…:tools/mado-geometry.py > /tmp/r43.py && R43_TOOL=/tmp/r43.py python3 -I .ufo/waves/round-44/w2/SentLiveRun/capture-twice.py --tool tools/mado-geometry.py`
  on a live host → identical rc/stdout for both tools when no client is in a state.
- `sha256sum tools/mado-geometry.py` → `1da3dda…`; `cmp tools/mado-geometry.py .ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt` → identical.
- `grep -rn 'clients=4' SKILL.md` → lines 225 and 299 (F8), and `grep -n 'alternation under a repeat' SKILL.md` → 306 (F9).
