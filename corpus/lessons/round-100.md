# mado round 100 — lesson

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, round 100 (hyaku run 15, attempt 1), base
`43309e6af9a3b57f1bc839a826bef1f8eb7495e4`. Claims: C1 coverage — the unset-PATH default branch of
the launch load gate becomes a measured case class; C2 operability — the harm watch's per-leg cap
becomes measured and its panel runs green. Pre-file amendments A1-A5 / B1-B5 in `plans/round-100.md`.

## Gate

Every row below was opened by this lane this round; the quote is located in the bytes the row names
and is at most 25 words.

### Admit

| id | source | opened | located quote | why it is this round's ground |
|---|---|---|---|---|
| S533 | GLib 2.90.1 `gutils.c` — https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c | 2026-11-08, HTTP 200, sha256 `65086c29…3771` (identical to the row's pin) | `path = "/bin:/usr/bin:.";` — `gutils.c:388`, in the UNIX unset block `:376-389` | C1's sourced claim: this literal is what the round turns from a modelled constant into a measured case class; the entry `corpus/knowledge/gio-launch-path-default-r100.md` cites it and its `used-by` cell now names that entry |

### Reject

| item | source | opened | located quote | reason and flip condition |
|---|---|---|---|---|
| staged `S205` (shokuknow `merge/mado/SOURCES.append.md`) | Hyprland wiki — Dispatchers (Lua config API), `content/configuring/core/dispatchers.md` | 2026-11-08, read-only inside `/home/vgpnk/Projects/shokuknow/merge/mado/` | `force_idle` sets elapsed time for all idle timers ignoring idle inhibitors (staged row's own `teaches` cell) | refused for this round's theme: the only `elapsed` hit in the package is a Hyprland idle-timer dispatcher (round-6 material), not a per-leg wall-clock measurement and not GLib's launch environment. Flips if a future round takes the idle-timer plane, where this row is already inside the lane's own Hyprland surface and should then be registered under its own scope |

`Assimilation: none` for this round, with the sweep that establishes it:
`.ufo/waves/round-100/assimilation/connector-sweep-r100.txt` (`grep -niE 'launch|/bin:/usr/bin|PATH
default|elapsed|per-leg|spawn'` over `MERGE-REPORT.md` and `SOURCES.append.md`: 9 hits, all
historical round-6/7 Hyprland material; zero on `PATH default` or `per-leg`).

## Mistakes

**M100-1 — a receipt assembled after the fact lost the run's terminal marker, and the counter
refused the whole measurement.**

Class: a receipt built by copying an intermediate file instead of the run's own output (the same
family as round 99's M95-2 "the digest is not the page": an artifact that looks like the run but is
not).
Evidence: the per-leg timing pass (`/fast/scratch/hyaku/mado-r100/harm-timing/run.sh`) tee'd its 28
rows into `timing.txt` but printed `TIMING-DONE` only to stdout; the receipt was then assembled from
`timing.txt`, so it carried 28 rows and no terminal marker. The first C2 measurement exited 2 after
~1 minute: `SETUP_ERROR timing receipt has no TIMING-DONE line`
(`.ufo/waves/round-100/receipts/c2-control-no-done-r100.txt` reproduces it against the same receipt
with that line removed).
Captured-by: the counter's own `timing-done-required` selftest check (it exists for exactly this
shape) and the receipt's fail-closed parse — no lane gate caught it, and none could have: the receipt
is written by hand at the boundary.
Fix: the runner writes every line of the receipt it will be judged on (rows *and* the terminal
marker) with one `tee`, and the counter refuses a receipt without the marker. Shown able to fail:
the control above exits 2 with the exact message, and the frozen receipt passes all nine conjuncts'
inputs (`.ufo/waves/round-100/receipts/c2-measured-r100.txt`).
Second-order fix carried into C1: the same class would have bitten the case file, so every label
there was measured twice by the oracle and the two runs must agree (`agreed: true` per case,
`receipts/c1-cases-r100.txt`), and the counter's `--selftest` pins the pin-mismatch refusal.

**M100-2 — an instrument's environment modelled the neighbour of the case it scored.**

Class: a harness that constructs the subject's environment from its own convention instead of from
the case's declared semantics (round 99's counter scored a `path: null` case with `PATH=""` in the
tool's environment — set-but-empty — while the case means *absent*).
Evidence: `.ufo/waves/round-100/w1/R100MMutPath.md` finding 1 and
`controls/launchenv-mutants-r100-probe.txt` ("the round-99 counter's env (PATH:"", --path omitted)
does NOT model unset: measured on a built root, PATH absent answers {root}/./probe while PATH=""
answers {root}/probe").
Captured-by: the mutation seat, before the counter existed; a counter that had reused the round-99
`run_tool` verbatim would have scored the new class wrong and turned C1 into an honest stop for a
reason that was not the model's.
Fix: `quality/counters/c1-r100-launchenv-path.py` puts `PATH` in the tool's environment only when
the case declares one, its selftest asserts both directions (`unset-means-absent`,
`declared-means-empty-string`), and the mutant `m2` (unset read as empty) is killed by two cases.

## Considerthese

`considerthese/2026-11-07.md` proposal 3 (one of the file's still-unimplemented suggestions) is
mined into `corpus/QUALITY.md` criterion 173: a library-semantics re-implementation carries an
exhaustive small-domain sweep against the shipped library, independent of author-written selftests.
Grounding opened this round: `corpus/lessons/round-95.md` M95-1 (the VT/`isspace` miss whose own
selftest certified it) and its five named wave seats — the pointer resolves to committed bytes
(`w1/R100MConnector.md` §3.2). The round's own C1 class is a small-domain sweep of the PATH shapes
(absent / empty / `.` / private / working-dir) and carries the same rule at the branch level.

## Domain share

Desktop-facing share of this round's artifacts: 4 of 9 (the tool, its case class, the knowledge
entry, the harm watch) — the other five are instrument and record work (counters, receipts, plan,
ledger, lesson). The desktop-facing finding a reader can act on: with no `PATH` in the launcher's
environment, a desktop file whose `Exec` names a program that exists only in `~/.local/bin` (or any
directory not on `/bin:/usr/bin:.`) **will not launch at all** — `gio launch` refuses at load time
with `Unable to load application information`, and the same file launches when `PATH` is set. That
is the round-99/100 boundary in one sentence, measured (`pd-private-unset` against
`pd-private-onpath`).
