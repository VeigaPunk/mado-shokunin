# R54Seat14 — cross-claim causal separability review (connector, item 14)

Base: `e25149fec8152a3aabd2b18a0ee8663b23cf65aa` (verified `git rev-parse HEAD`; `--show-toplevel` = lane root).
Scope: C1 (errata source-truth counter) vs C2 (uwsm-app entry/counter). Read-only. No host reads, no producer runs,
no lane tracked edits, no installs (tool updates: none; used `python3` 3.14.8, `sha256sum`, `grep`, `sed`, read-only `git`).

Axes named for this review: (A) causal separability of the two read-sets; (B) judge satisfiability of each frozen
quote rule against committed pins; (C) shared-surface contamination. Attacked predicates: PRED-C1-r54 clause (a)
quotes/anchors and (d) controls; PRED-C2-r54 clause (b) quotes/pin-commit and (c) host joins; the frozen
"Causal separability" read-sets in `claims-frozen.md`.

Distinct input from other seats: I did not re-run the per-claim counters (none exist at base). I tested the
*judge itself* across both claims at once, plus cross-claim occurrence and the shared-surface diff.

## 1. Probe (judge sensitivity, all frozen quotes, real pins)

Script: `/fast/scratch/hyaku/mado-r54/R54Seat14/judge_probe.py` (python3 -I, stdlib only; removed at yield). Judges:
J0 = exact byte substring; J1 = whitespace runs collapsed on both sides; J2 = J1 + `*`/backtick stripped from the pin.

```
== frozen quotes: judge J0 exact | J1 ws-collapse | J2 ws+markdown-strip ==
P19   J0=False J1=True  J2=True  file=Hyprland-ConfigActions.cpp
P20   J0=True  J1=True  J2=True  file=Hyprland-ConfigActions.cpp
P21   J0=False J1=True  J2=True  file=Hyprland-legacy-DispatcherTranslator.cpp
P22   J0=False J1=True  J2=True  file=Hyprland-legacy-DispatcherTranslator.cpp
S375  J0=False J1=True  J2=True  file=uwsm-0.27.1-README.md
S376  J0=False J1=False J2=True  file=uwsm-0.27.1-uwsm-app.1.scd
S377  J0=True  J1=True  J2=True  file=uwsm-0.27.1-main.py
== controls under J2 (shared normalizer) ==
C1-CTL-1 spliced     J0=False J1=False J2=False
C2-CTL-1 forged      J0=False J1=False J2=False
== cross-claim occurrence: C1 quotes in C2 pins, C2 quotes in C1 pins (J2) ==
done   (no HIT lines)
```

Supporting byte evidence (`sed -n`, `grep -nF`):
- `round-52/fetch/Hyprland-ConfigActions.cpp:1553-1559` = blank / `sendKeyboardMods(modMask,0,0,0);` (1554) / blank /
  `if (S.m_passPressed == 1) {` (1556) / `if (!isMouse)` (1557) / `sendKeyboardKey(...)` (1558). P19 is a five-line span, so the
  registration's anchor "exactly 1554–1558" is correct only under whitespace collapse.
- P21 spans 619 (`auto result = sendshortcut(modifiedArgs);`) / 620 blank / 621 (`if (keyState == 2 && result.success)`) / 622 (`result = ...`).
- P22 spans 573 (`if (!keycode)`) / 574 (`return {...}`). P20 at 1576 is verbatim (J0).
- `round-54/fetch/uwsm-0.27.1-README.md:117-118` = `- Difference between environment state before and after preparation is exported` / `  into systemd user manager (...)`. The S375 quote is wrapped across a markdown bullet and a newline.
- `uwsm-0.27.1-uwsm-app.1.scd:60` = `*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon`. The frozen S376 text has no `*`, so `grep -c "uwsm-app client sends arguments"` = 0. The apostrophe is ASCII (`od -c` confirmed).
- `uwsm-0.27.1-main.py:3714` verbatim (J0).

## 2. Findings

### F1 — BLOCKING judge gap, shared by both claims (axis B)
The frozen rules do not let a faithful counter admit the real pins.
- C1 registration allows interior-newline normalization "ONLY where the frozen quote itself carries a newline (P19/P21/P22 are single logical lines)". None of P19/P21/P22 carries a newline, yet their own anchors span 2–5 physical lines. Under the literal rule (J0), `quotes` = 1/4 (P20 only), so `verdict=TARGET_MISSED` on honest sources.
- C2 registration states no judge at all for S375–S377. Under J0, quotes = 1/3 (S377 only).
- Any counter that admits the real quotes must use J1 (P19, P21, P22, S375) and, for S376, J2 (markdown strip). The C1 rule does not authorize J1 or J2 for C1 and C2 has no rule. Adding normalization therefore changes a frozen judge, which the honesty rules forbid without `claims-frozen-v2.md`.
- Consequence for separability: the quote judge is the single shared dependency between the two claims. Whichever judge is chosen must be declared once and applied identically to both, or each claim gets its own declared judge. I have not chosen one; this is a freeze-completeness decision for L1.

### F2 — cross-claim occurrence is zero; normalizer is the only coupling vector (axis A)
- No C1 quote occurs (J2) in the uwsm pins, and no C2 quote occurs (J2) in the round-52 pins: zero HIT lines.
- The two controls that matter for admission (C1-CTL-1 spliced P19, C2-CTL-1 forged S376) are still rejected under J2, so a shared normaliser does not by itself admit a control.
- Coupling risk remains structural: `quality/counters/` has only self-contained stdlib `c*-*.py` scripts (`ls quality/counters | grep -v '^c[0-9]-'` → only `__pycache__`). A shared helper module (e.g. `_common.py` for quote normalization) would be a third input that neither frozen read-set lists, breaking "C1 reads only …" / "C2 reads only …". Keep each counter self-contained.

### F3 — round-52 hash file name mismatch (axis A/B)
- Registration cites "hashes from its committed `SHA256SUMS.txt`" for `round-52/fetch/`. The committed file is `.ufo/waves/round-52/fetch/SHA256SUMS` (no `.txt`); `ls` shows no `.txt`.
- The hash values agree with the frozen table: `sha256sum` on the four round-52 pins gives a83abeb5…, 746c6f51…, 8d8f35fc…, 7248cbb8…, which match the frozen table and the file contents.
- Separability risk: a counter hard-coded to `SHA256SUMS.txt` returns pins 0/4 (false MISSED). A glob fallback (`**/SHA256SUMS*`) from C1 would pick up `round-54/fetch/SHA256SUMS.txt`, a C2 input. That file contains only the three uwsm hashes, so the result is 0/4 and the failure is in the safe direction, but C1 would then read a C2 input. Fix: C1 reads exactly `.ufo/waves/round-52/fetch/SHA256SUMS` (fixed path, no glob).

### F4 — C2 registry-leg format coupling (axis B, minor)
The live draft entry's provenance line reads `source: S375–S377` with an en dash. Frozen clause (a) requires the entry "citing rows S375, S376 and S377". A parser that accepts only a comma list or ASCII hyphen rejects a valid entry (false MISSED). The counter should parse `S\d+` tokens, or the range, and the test should include the en-dash form.

### F5 — C2 clause (c) is copy-gameable text presence (axis A/B)
The frozen host set already appears in existing corpus notes, so clause (c) is text presence and cannot tell a copied join from a new one (counts from `grep -rl -F` over `corpus/knowledge`):
- `bindings.conf:2`: 5 files (e.g. `terminals-and-omarchy.md:95`, `xdg-terminal-selection-r47.md:74`).
- `autostart.conf:1`: 6 files; `omarchy-toggle-idle:9`: 1 file.
- `xdg-terminal-selection-r47.md` carries exactly one frozen host string (`bindings.conf:2`), so the frozen do-nothing control (recycled r47 entry) fails clause (c) by count, but a recycled entry with two copied joins would pass (c). Clause (b) is the only real backstop; (c) must not be read as evidence of a new join.
- The counter must not open the host paths (lane rule); it can only check the entry text.

### F6 — live C2 writes present in the lane tree during this review (axis C)
While reading, uncommitted C2 writes were present: `git diff --stat` = `corpus/README.md` +2, `corpus/SOURCES.md` +3 (S375–S377), and untracked `corpus/knowledge/uwsm-app-environment-r54.md` (21 lines). I did not touch them. Separability check on the diff:
- The README diff touches only the index table (new `uwsm-app-environment-r54.md` row) and a round-54 bullet. It does not touch the C1 row (`hyprland-synthetic-dispatch-r52-errata-r53.md`, line 81) or any C1 file.
- The SOURCES diff adds only S375–S377. No prior uwsm URL exists (`grep -n uwsm corpus/SOURCES.md` → only line 523 prose), so the census W04 duplicate-URL list cannot grow from these rows.
- C1's frozen inputs (errata entry, round-52 fetch, C1 counter) are not touched by the C2 diff. Causally separate as frozen.
- Contamination vector to watch: C2 controls C2-CTL-1 (S376 row) and C2-CTL-5 (URL commit) mutate `SOURCES.md`/README. If run in place in the lane tree, they race with C1 and the nav counter. They must run on mutated copies in scratch, each from git objects.

## 3. Separability verdict (my scope)
- C1 and C2 read-sets are disjoint as frozen; no quote, pin or row is shared; the only shared surfaces are `corpus/README.md`, `corpus/SOURCES.md` and the navigation/census counters, which C1 does not read.
- Contamination is not present in the live tree at this moment. Two frozen-text defects can cause false verdicts in either direction and should be fixed before scoring: F1 (judge, blocking for both) and F3 (path).
- Recommended for L1 (not decided by me): declare one judge for both claims in a v2 freeze, or honest-stop on quotes; fix the round-52 hash file name; keep counters self-contained; run C2 controls on scratch copies.

## 4. Verification commands (exact)
- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse --show-toplevel` → lane root; `rev-parse HEAD` → `e25149fe…`.
- `sha256sum` over `round-52/fetch/Hyprland-*` → four frozen hashes, match.
- `sha256sum -c round-54/fetch/SHA256SUMS.txt` → three `OK`.
- `python3 -I judge_probe.py` → table above.
- `grep -rl -F <host string> corpus/knowledge` counts (F5).
- `git diff --stat`, `git diff -- corpus/README.md corpus/SOURCES.md` (read-only; F6).

## 5. Not done (scope)
No counter run (none at base; C1/C2 counters are other seats' scope). No host file reads. No `tools/mado-verify.sh` run (baseline is sonic/sentinel scope). Scratch file removed at yield.
