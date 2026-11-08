# R100MLabratUnset — falsification labrat (H1: PATH-unset default search path)

Seat: R100MLabratUnset. Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin.
Role: falsifier. One hypothesis, one bounded probe. Scratch-only fixtures;
no lane edits, no host writes. Instruments (spawn gio; label nothing):
hand-built probe `labrat_hand.py` and oracle-comparison driver
`labrat_oracle.py` in scratch. No candidate code written.

## Hypothesis H1

"With PATH absent from the environment, `gio launch` resolves a bare `Exec`
program through `/bin:/usr/bin:.` and the load gate refuses when the program
is reachable only through a case-private directory."

Verdict: NOT FALSIFIED. Every measurement is consistent with H1, including
the TryExec cases (4)(5) as specified, plus a discriminating argv detail
below that cuts for the contract, not against it.

## Ground (re-measured, not trusted)

- /usr/bin/gio sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462 — matches L1 ground.
- glib2 2.90.1-1 (pacman -Q).
- /bin/sh and /usr/bin/sh -> bash; /bin/true and /usr/bin/true present.
- Round-99 oracle sha256 cbfff7a4b64e63f3e6861d29d1c5639de2c25abe2f6875088918abb45d129199 used as the agreement instrument (imported as a module, `runs=2`, `agreed` read from its return).

## Fixture shape (all in scratch; cwd = case root)

Desktop file `case.desktop`, probe script (`#!/bin/sh`, one `printf` line
append to `$PROBE_OUT`, copied shape from the r99 oracle PROBE_SH).
Every launch ran with `env -i`: LC_ALL=C, HOME=<root>/h, PROBE_OUT=<root>/out,
plus PATH only where the case sets it. Desktop path passed to gio as an
absolute path. `Terminal` never set.

## Task 1 — hand-built measurement (`labrat_hand.py`, total wall 10.9 s)

| case | fixture | PATH | rc | stderr first line | probe record |
|---|---|---|---|---|---|
| 01-root-unset | `probe` at root, `Exec=probe` | absent | 0 | (none) | 1 rec: `ARGV0={root}/./probe ARGC=0 CWD={root}` |
| 02-bin-unset | `probe` only at `<root>/bin`, `Exec=probe` | absent | 1 | `gio: Unable to load application information for '<root>/case.desktop'` | 0 |
| 03-bin-pathset | same as 02 | `<root>/bin` | 0 | (none) | 1 rec: `ARGV0={root}/bin/probe` |
| 04-tryexec-root-unset | root probe; `Exec=probe`, `TryExec=probe` | absent | 0 | (none) | 1 rec: `ARGV0={root}/./probe` |
| 05-tryexec-root-empty | same as 04 | `""` (set-but-empty) | 0 | (none) | 1 rec: `ARGV0={root}/probe` |
| 06-tryexec-helper-bin-unset | root probe; `Exec=probe`, `TryExec=helper`, helper only in `<root>/bin` | absent | 1 | `gio: Unable to load application information for '<root>/case.desktop'` | 0 |
| 07-tryexec-helper-bin-empty | same as 06 | `""` | 1 | `gio: Unable to load application information for '<root>/case.desktop'` | 0 |

Each ran once (hand probe); per-case wall ~1.5 s (the 1.5 s quiet wait).

Reading:

1. (1) CONFIRMS the trailing `.`: bare `probe` at the case root is found
   with PATH absent. The launch cwd is the case root, so `.` = root.
2. (2) CONFIRMS H1's refusal half: a program reachable only via a
   case-private bin is NOT found with PATH absent. The default
   `/bin:/usr/bin:.` does not know that directory.
3. (3) Controls (2): the same fixture with PATH set to the private bin
   launches (`ARGV0={root}/bin/probe`). The refusal in (2) is a PATH
   effect, not a fixture defect.
4. (4) `TryExec=probe` with PATH absent also resolves through the default
   (launches). H1's first half holds for TryExec too.
5. (5) `TryExec=probe` with `PATH=""` also launches, but — discriminating
   detail — `ARGV0` differs: `{root}/probe` (empty entry) vs `{root}/./probe`
   (unset default, `.` entry). Both succeed; the argv0 strings differ.
   This is the measurable form of "unset != empty" even in the success
   region. A frozen case that only checked status would call 04/05
   identical; the argv vectors separate them.
6. (6) A `TryExec` naming a program that exists only in the private bin
   kills the load (rc=1, load refusal) even though `Exec=probe` is
   resolvable. TryExec is gated through the same PATH source.
7. (7) Same with `PATH=""`: refusal. Set-but-empty has no private-bin
   knowledge either.

No measurement contradicts H1. The two success-region neighbours the
contract must separate (claims-declaration-r100.md C1, point 1: a program
that exists only in `/usr/bin` reachable under unset, unreachable under
`PATH=""`) were not directly fixture-d here because planting into the host
`/usr/bin` is a host write; the separation is instead established by
(4) vs (5) argv and by (6)/(7) refusing under both. The `/usr/bin`-only
arm of C1 point 1 remains for the executor seats to freeze with a host
binary name, not a planted one.

## Task 2 — oracle agreement (`labrat_oracle.py`, total wall 21.5 s)

Same cases through the round-99 oracle module (imported, `runs=2`):

| case | oracle expect | rc | agreed |
|---|---|---|---|
| o01-root-unset | launches=1, argv=[{root}/./probe] | 0 | True |
| o02-bin-unset | error=load | 1 | True |
| o03-bin-pathset | launches=1, argv=[{root}/bin/probe] | 0 | True |
| o04-tryexec-root-unset | launches=1, argv=[{root}/./probe] | 0 | True |
| o05-tryexec-root-empty | launches=1, argv=[{root}/probe] | 0 | True |
| o06-tryexec-helper-bin-unset | error=load | 1 | True |
| o07-tryexec-helper-bin-empty | error=load | 1 | True |

Hand-built fixtures and the oracle agree on all 7 (verdict AND argv0).
The oracle's `path: null` arm runs with PATH absent from the child
environment (verified: its own `path_string` returns None and `measure_once`
only sets `env["PATH"]` when the string is not None; smoke-tested indirectly
by the `{root}/./probe` argv, which cannot occur if a host PATH leaked in).

One oracle usage note for the build seats: the r99 oracle writes its own
`probe.sh` into every case root, but a bare `Exec=probe` needs a file named
`probe`. The oracle case `files` map supplies it (base64 of the probe body);
a hand-built fixture needs the same filename care. An oracle case whose
`files` omits the bare program will measure error=load regardless of PATH —
a fixture bug, not a PATH result.

## Falsification summary

- H1 stands. No contradiction in 7 hand cases + 7 oracle repeats.
- Most valuable by-products for the C1 executor seats:
  (a) unset vs empty success-region separation via argv0 (`./probe` vs
  `probe`) — freeze a case pair whose expect contains the argv vector, not
  just launches;
  (b) TryExec reads the same PATH source — a `TryExec` arm in the
  `path-default` class tests the gate, not the launch;
  (c) load refusals print one generic line, so frozen labels must come
  from the argv/out record, not stderr partitioning.

## Hygiene

- Scratch: /fast/scratch/hyaku/mado-r100/R100MLabratUnset (instruments
  `labrat_hand.py`, `labrat_oracle.py`, fixture roots under `hand/roots`,
  `oracle/roots`) — deleted before yield.
- No install performed (nothing needed). No lane edit. No host write beyond
  scratch. No terminal launch (every env had no host PATH).

## Anchors

- Witnessed runs: hand probe total 10.9 s, oracle comparison total 21.5 s
  (ran serially on the loaded host).
- Receipt: .ufo/waves/round-100/receipts/labrat-unset-r100.txt

Report: .ufo/waves/round-100/w1/R100MLabratUnset.md
