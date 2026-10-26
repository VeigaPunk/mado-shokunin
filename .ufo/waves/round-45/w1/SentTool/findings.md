# SentTool — safety review, round 45 w1 (mado round 45, hyaku run 9)

Seat: `SentTool`. Surfaces assigned: `.ufo/waves/round-45/l1-draft/mado-monitors.py` (the C1 reference),
`quality/counters/c1-r45-monitors.py`, `quality/counters/c2-r45-monitor-entry.py`, both control drivers
(`.ufo/waves/round-45/ctl/run-c{1,2}-controls.py`), the fake PATH binaries clause `r` builds, and
`receipts/live-monitors-host-l1.txt`. `registration.md` (freeze `22a8dedd`, base `0c89478a`) was read first.

Lane HEAD while reviewing: `ebdba13f`. Reference bytes throughout: `l1-draft/mado-monitors.py` sha256
`c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be` — the same value the live receipt names
(`raw/r9-provenance-replay.txt`). Nothing in the lane, the host config tree or the compositor was written or
mutated; the only compositor commands I ran are outside the allowed list (`hyprctl version` was invoked by me
exactly once, from an empty environment, and refused: `raw/r11-selftest-window.txt`). Every probe ran under
`/fast/scratch/hyaku/mado-r45/SentTool/`, copied out to `raw/`, and the scratch tree is deleted.

## Ranked findings

| # | Severity | Attacks | One line | Receipt |
|---|---|---|---|---|
| F1 | MEDIUM | C1's read-only clause `r` | clause `r` is evadable two ways; both let a tool that spawns `hyprctl` score `TARGET_MET` | `raw/r11-selftest-window.txt`, `raw/r1-clause-r-failopen.txt` |
| F2 | MEDIUM-LOW | the tool's own SETUP contract | a 900 kB JSON dump is an uncaught `RecursionError`: traceback, **exit 1 = the DIFFER code** | `raw/r2-nested-json-recursion.txt` |
| F3 | LOW-MEDIUM | the tool's cost model | two inputs each under the 1 MiB cap cost 95.7 s; superlinear in both dimensions | `raw/r3-cost-amplification.txt` |
| F4 | LOW | caller files under `--work` | `ctl/run-c2-controls.py` `rmtree`s fixed child names under a caller-chosen `--work` | `raw/r4-ctl-c2-rmtree.txt` |
| F5 | LOW | the tool's stderr/exit contract | a reader that closes early yields a `BrokenPipeError` traceback and exit 1 | `raw/r5-broken-pipe.txt` |
| F6 | INFO | counters' process model | clause `s`/`f` execute an arbitrary committed blob unsandboxed with the caller's rights | `raw/r10-scratch-discipline.txt` |
| F7 | INFO | freeze integrity | the positive control's REF text is read from the lane working tree, not a revision | `raw/r10-scratch-discipline.txt` |
| F8 | INFO | §7 items 1/4 | neither counter checks that `--work` is under the scratch root (both do honour it) | `raw/r10-scratch-discipline.txt` |

Verified clean (they support the claims) is in the next section: no process, no socket, no output injection,
regular-file-only reads, caps enforced, receipt honest and replayable, pins verified.

---

## F1 — MEDIUM — the read-only clause `r` is evadable; a spawning tool scores `TARGET_MET`

**Attacks:** the C1 predicate's clause `r` (`quality/counters/c1-r45-monitors.py:19-20` in its docstring,
implementation `:272-279`, `:354-362`), i.e. the round's only guard on the reference's promise at
`l1-draft/mado-monitors.py:22` ("It reads files and standard input only; it starts no process and opens no
socket"). It also defeats control `K08-LIVE-HYPRCTL`, which is the registered anti-cheat for exactly this.

**Exploit path (a) — the `--selftest` window is outside the marker.** Clause `s` runs the tool with `--selftest`
at `:342-343` (env `{"PATH": "/usr/bin:/bin", ...}` at `:343`); the marker and its fake binaries are created
afterwards at `:354-355` and checked once at `:362`. A tool that spawns `hyprctl` **only** when
`argv == ["--selftest"]` is therefore invisible to the marker. Demonstrated: the reference plus three lines
guarded on that argv, committed in a scratch clone, scores
`fixtures=49/49 selftest=ok readonly=ok ... verdict=TARGET_MET` (rc 0). With the real PATH,
`/usr/bin/hyprctl` is reachable, so the spawn happens; it fails to connect (no `HYPRLAND_INSTANCE_SIGNATURE`,
no `XDG_RUNTIME_DIR`), so **no live state is read** — the defect is that the clause does not see the process,
not that host state leaked.

**Exploit path (b) — the fake binary is written with an unquoted shell interpolation.** `:277` writes
`: > '<marker>'` into a `#!/bin/sh` script. The marker is `os.path.join(work, "marker-%d" % seed)` (`:354`)
and `work` is a `mkdtemp` under the caller's `--work` (`:381`). One apostrophe in that path makes `/bin/sh`
fail (`unexpected EOF while looking for matching '`), so **no marker is ever created** and `:362` reports
`readonly=ok`. Demonstrated end-to-end: the reference plus a single discarded `hyprctl version` call in
`run()` scores `readonly=fail/TARGET_MISSED` with a plain `--work` and `readonly=ok/TARGET_MET` with
`--work` under `.../q'w` — same committed bytes.

**Impact:** a candidate tool in w1/w2 can satisfy the round's read-only claim while starting processes, and the
registered control suite reports it clean (path (a) needs no unusual environment at all). It does not move any
number in `ctl-c1.txt`, which was produced with a plain scratch path.

**Smallest remediation:** (1) move marker + fake-bin construction **above** the clause-`s` subprocess and put
`fakebin` on the selftest `PATH` too, so both invocations write the marker; (2) write the marker path through
`shlex.quote`, or keep the marker inside the fake-bin directory and refer to it as `"$(dirname -- "$0")/marker"`
so no caller-controlled string is interpolated. Both are counter amendments (frozen for this round → next
round, with a re-freeze).

## F2 — MEDIUM-LOW — deeply nested JSON escapes `bad_json` and exits 1

**Attacks:** the tool's documented setup contract at `l1-draft/mado-monitors.py:25-29` ("Setup failure" … "is bad_json") and `:81`
("stderr empty on exit 0/1/3/4/5"), and the `DIFFER = exit 1` convention at `:85-88`.

**Exploit path:** `parse_monitors` catches only `(UnicodeDecodeError, ValueError)` at `:307-308`. A 900 000-byte
file of `[` (under the 1 048 576 cap at `:98`) makes `json.loads` raise `RecursionError`, which is neither: the
process prints a 1 423-byte traceback to stderr and exits **1**, with no `MADO_MONITORS:` summary line. Exit 1
is the DIFFER verdict code, so a caller — and the C1 counter's own fixture logic, which requires stderr empty
and an exact stdout — cannot distinguish "the outputs disagree" from "the dump was garbage". Stack high-water
was 8 140 kB (bounded, but 8× the input).

**Smallest remediation:** add `RecursionError` to the `except` at `:308` and one fixture in the counter's
`FIXTURES` with a nested-`[` dump. The tool is a draft, not yet installed, so this can be fixed **before**
integration with no re-registration: no existing fixture changes.

## F3 — LOW-MEDIUM — superlinear cost inside the caps

**Attacks:** the tool's own resource bound. `add()` at `:180-182` rebuilds the whole rule list per parsed line
(O(n) per line ⇒ O(n²) per file); `effective()` at `:345-357` scans every rule per output (O(rules × outputs)).

**Exploit path:** both inputs are capped at 1 MiB, which bounds *bytes* but not the product. Measured in this
seat: 10 000 rules (290 000 B config) × 100 000 outputs (300 001 B dump) = **95.7 s** wall, exit 3. Growth is
clean quadratic in each dimension (config only: 0.06 / 0.20 / 0.75 / 3.14 s at 2/4/8/16 k lines; rule×output
product only: 0.09 / 0.33 / 1.29 s at 1/2/4 k×k). Cap-scale worst case ≈ 33 825 rules × 349 525 outputs
≈ 19 min single-core **[INFERENCE — extrapolated from the measured 1e9 pairings → 95.7 s; not run]**.

**Impact:** a wrong or hostile 300 kB dump stalls a seat's 10 s fixture budget (the counter kills each fixture
at `:315`, so it degrades to `FAIL timeout`, not a hang), and an operator piping a large dump waits minutes for
a verdict. No crash, no memory growth beyond the inputs.

**Smallest remediation:** key rules by selector (`dict`) in `add()`, and index the last rule per name / the
first empty-selector rule / `desc:` prefixes in `effective()`. This is a **tool** fix, not a counter change: the
reference is still a draft, and the counter's 10 s per-fixture timeout (`:315`) already bounds a hostile fixture.

## F4 — LOW — `ctl/run-c2-controls.py` deletes fixed names under the caller's `--work`

**Attacks:** caller data, not the claim. `clone()` at `:41-44` builds `os.path.join(work, name)` from the fixed
names in `runs` (`P`, `R14-COPY`, `SHELL`, `WIDE-RANGE`, `HIDDEN-LINE`, `FORGED-PIN`, `FALSE-URL`,
`PROSE-CENSUS`, `ANCHOR-PAST-EOF`) and `rmtree`s it before cloning; `:84` `os.makedirs(a.work, exist_ok=True)`
means `--work` need not even exist. So `--work /home/someone` deletes `/home/someone/P` if present (reproduced
on a decoy directory). `run-c1-controls.py:66` and the c1 counter `:381` both use `mkdtemp(dir=…)` and are not
exposed. Secondary: ctl-c2 has no `try/finally`, so a clone built before an exception leaks (the c1 driver has
one at `:124`).

**Smallest remediation:** `tempfile.mkdtemp(dir=work, prefix=name + "-")` in `clone()`, and wrap `main` in
`try/finally`.

## F5 — LOW — `BrokenPipeError` traceback and exit 1 when the reader closes early

**Attacks:** the same contract line as F2 (`:81`: stderr empty on exit 1). All output is one
`sys.stdout.write` at `:527`; `| head -1` on a 16 000-rule config produces a 382-byte traceback and exit 1,
which collides with DIFFER. Smallest remediation: catch `BrokenPipeError` around the write (and `os._exit` /
close cleanly). Tool fix (draft, not yet installed); low impact, but piping into `head` is a normal
operator gesture.

## F6 — INFO — the counters execute an arbitrary committed blob, unsandboxed

Clause `s` (`:341-343`) and clause `f` (`:314-316`) run the tool bytes from the revision with
`subprocess.run`, `cwd` set to a fixture dir and a three-variable env, but no namespace/seccomp/rlimit: the blob
runs with the invoking user's full rights. This is inherent to scoring a tool, and the round's threat model
treats the tool as the claim, but it is not in either counter's declared residuals — worth one line there.

## F7 — INFO — the positive control's REF is read from the working tree

`ctl/run-c1-controls.py:95` does `open(os.path.join(lane, REF)).read()`: the REF control is whatever
`l1-draft/mado-monitors.py` holds at run time, not a blob at a revision. Every other input in the driver is
revision-addressed (`git -C d show BASE:tools/mado-geometry.py`). Freeze integrity is then carried by the
receipt's sha256 only; `raw/r9-provenance-replay.txt` shows the current value agrees with the live receipt.
Smallest remediation: read REF through `git show <freeze>:…` once the draft is committed, or record its sha256
in the ctl output line (the counter already prints `rev=`).

## F8 — INFO — `--work` locality is caller-enforced

Section 7 item 4 of the round prompt (`/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-45.md`) asks that no
committed driver write under `/tmp` regardless of `TMPDIR`/`--work`. **Both counters and both drivers pass
that**: no `/tmp` literal, no `TMPDIR` read, every temp root is `mkdtemp(dir=<explicit>)`
(`r10-scratch-discipline.txt`). What they do **not** do is refuse a `--work` outside the scratch root —
`c1-r45-monitors.py:379` requires only that it exists, `run-c2-controls.py:84` creates it. Since the mis-set
in F4 turns with that, a cheap guard (`--work` must be under `$HYAKU_SCRATCH` unless `--force`) would close
both.

---

## Verified clean — what supports the claims

| Check | Result | Receipt |
|---|---|---|
| No process, no socket in the tool | imports are `json math os re stat struct sys` only (`:90-96`); `strace -f -e execve,socket,connect,openat`: exactly **one** `execve` (the interpreter), **zero** socket/connect, and only the two named inputs are opened | `raw/r8-syscalls.txt` |
| No output injection | a `name` with `\n`, ESC/DEL, a lone surrogate, or a forged `MADO_MONITORS: verdict=OK` is escaped by `json.dumps(ensure_ascii)` (`:407-408` for the rule line, `:430` for the output line) and stays on one line; the summary appears once, last; output is pure ASCII, so an ASCII stdout cannot break it | `raw/r7-output-injection.txt` |
| Path handling | `os.open(O_RDONLY|O_NONBLOCK)` then `fstat`+`S_ISREG` (`:120-138`): FIFO returns in 0.01 s (no hang), directory / `/dev/zero` / symlink loop / `/proc/self/mem` → `SETUP unreadable`; symlink→regular is read. A TOCTOU swap cannot redirect the read, because the check is on the opened fd | `raw/r6-path-handling.txt` |
| `/proc` files as `--config` | admitted (they are `S_ISREG`), and inert: the tool prints only parsed selectors and dump names, never file content, so `/proc/self/environ` yields `NO_RULES` | `raw/r6-path-handling.txt` |
| 1 MiB caps | stdin 1 048 577 B → `too_large`; file exactly at the cap → parsed; config > cap → `too_large`. Bounded read loop, no unbounded read on a device | `raw/r12-caps.txt` |
| Regex cost | every pattern is `fullmatch` with bounded quantifiers (`:99-104`) and every use site is `fullmatch` (`:197`, `:208`, `:217`, `:259`, `:298`); no nested `*`/`+` over unbounded text, no catastrophic backtracking path found | by inspection of `:99-104` and those five sites |
| Live receipt is honest | its `tool sha256` is the reference's bytes and its `config sha256` is the host file's; replaying the receipt's own projected dump against the host config reproduces its three recorded lines byte for byte | `raw/r9-provenance-replay.txt` |
| Live receipt is shape-only | no serial, description, make/model, window title, process table or home listing; only the output name, numeric geometry and two content hashes. This meets considerthese `2026-10-26.md` proposal 1 for this file | `raw/r9-provenance-replay.txt` |
| Pins | all nine `fetch/` files verify against `receipts/fetch-sha256.txt` | `raw/r9-provenance-replay.txt` |
| c2 counter writes nothing | no `tempfile`, `rmtree`, `makedirs` or write-mode `open`; it reads git objects through `git -C repo show|ls-tree` (`:125-141`) and prints | `raw/r10-scratch-discipline.txt` |
| c1 scratch | `--work` must exist (`:379`) → `mkdtemp(dir=a.work)` (`:381`) → `rmtree` of that child only, in `finally` (`:385`); no `/tmp`, no `TMPDIR` | `raw/r10-scratch-discipline.txt` |

## Residuals of this review

- I did not test the compositor side at all: no `hyprctl` read beyond the one refused `version` call, so the
  tool's *semantic* agreement with Hyprland is untouched here (that is the C2/non-author reading).
- F3's cap-scale figure is extrapolated, not measured (marked `[INFERENCE]`).
- I did not attempt socket-level evasion of clause `r` (a tool opening Hyprland's `.socket2` directly); the
  registration already declares clause `r` as PATH-only.
- Read-only git only; no lane, fleet, template, script or index file was written. No tool was installed, so
  there is no tool/version/channel line to record.
