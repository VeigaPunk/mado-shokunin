# CritFsPremise — C1 premise falsification (round 44, w1)

**Result: premise's factual core holds; its "false report" claim is wrong; the report word is right but the top
verdict over-claims.** Findings: `.ufo/waves/round-44/w1/CritFsPremise/findings.md`.

## What I attacked, and what survived

1. *"Hyprland replaces the box, so DIFFER was false."* The box replacement is real and keyed on the **internal**
   mode only (`pins/Hypr-FullscreenHandler.cpp:191-198`; `size` in the dump is the goal, `pins/HyprCtl.cpp:427`,
   so there is no pending window to catch). The "false" label does not survive: the round-43 tool documented
   DIFFER as "a report, not a fault" (`tools/mado-geometry.py:57`), and SKILL.md's DIFFER/TILED rows already
   licence a compositor-set box. DIFFER was **true about the box, silent about the cause** — a diagnosis gap.
   `registration.md:13` ("a false report") should be withdrawn; it is the same class as closure D2.
2. *"Maybe `fullscreen` 1/2 can be set while the box is the rule's."* Refuted on this commit: the mode and the box
   are set in one main-thread call, and the guard is internal-mode driven, so `fullscreenstate 0 2` (client-only)
   leaves the box untouched while internal 2 always replaces it (`pins/Hypr-DispatcherTranslator.cpp:188-206`).
   Coincidence cases exist (rule size == monitor box / work area) and are correctly refused by the contract
   (`c1-r44-geometry-states.py:238`, fixture `fsagree0`) — this is C1's strongest support, not a hole.
3. *"Maybe the rule's size is still meaningful while maximized."* Partly right, and it matters: the `size` rule is
   read only on the first map (`pins/Hypr-DefaultFloatingAlgorithm.cpp:49,55`); afterwards the floating algorithm
   restores the **remembered** box (`:85-87`), stored on FS entry (`pins/Hypr-FullscreenHandler.cpp:131`). So a
   window that was 420x500 and then went fullscreen returns to 420x500 on exit — the rule is suspended, not dead;
   the dump just cannot see the stored box. That supports "not comparable" over "OK".
4. *"Is FULLSCREEN/MAXIMIZED the right report?"* Right as a **state label**, wrong as a **replacement for the
   comparison**: with the state verdicts in place, a dump whose every matched client is fullscreen/maximized
   prints `differ=0` and `verdict=OK` with exit 0. Measured on frozen dumps (`scenarios/`, `receipt-runs.txt`):
   S1 `DIFFER rc1 → OK rc0`, S2 same, S7 `differ 2 → 0 rc1 → rc0`; S8 keeps DIFFER only because an independent
   window really differs. The hole is not new (TILED already gave `OK` with nothing compared, S3 r43), which is
   why the correction belongs to both words at once.

## Counterexample (the strongest one available locally)

`scenarios/S1-float-fullscreen-rule420.json` — floating gkeep, internal 2, box 3440x1440 (DP-1 monitor box;
host geometry in `receipt-host.txt`), rule `size 420 500`:

```
r44 MADO_GEOMETRY: … matched=1 … agree=0 differ=0 tiled=0 badsize=0 maximized=0 fullscreen=1 verdict=OK   rc=0
```

Five words above contradict "OK": the rule is not in effect, and no client was compared. Exit 0 is the
machine-facing surface (`SKILL.md:281` still says "1 DIFFER (at least one matched client differs)").

## Impacted axes

- **operability (C1)**: the frozen model (`c1-r44-geometry-states.py`) *requires* the `verdict=OK` of S1, so no
  control in `receipts/ctl-c1.txt` can catch this; controls test conformance to the model, not the model.
- **no-harm clause `r` is vacuous**: `grep -c fullscreen quality/counters/c1-r42-geometry.py` = 0, so no r42
  fixture carries the field and the old contract cannot observe the change.
- **documentation**: `SKILL.md:281` exit map + the verdict table need FULLSCREEN/MAXIMIZED rows with a "not
  compared" licence; PROVINCE.md row; the claim text in `registration.md`.
- **coverage (C2)**: the round-44 entry must distinguish internal from client FS and say which box is sent, or it
  inherits the same conflation the state verdict now relies on.

## Smallest safe correction

Make exit 0 mean "compared and agreed": when `matched > 0`, `agree == 0`, `differ == 0`, print a distinct word
(e.g. `NOT_COMPARED`) with a non-zero exit instead of `OK`, for TILED-only and state-only dumps alike. One branch,
one exit code, no new tally; then withdraw the registration's "exit codes are unchanged" sentence and update
`SKILL.md:281`. Alternative (more information, 26 fixtures to re-derive): keep the geometry counts for state
clients and add `state=` to the client line.

## Evidence (seat dir `.ufo/waves/round-44/w1/CritFsPremise/`)

- `findings.md` — full argument, scenario table with tool output / true state / right-wrong.
- `pins/` + `pins/SHA256SUMS` — 15 files at Hyprland `efb50993…` (handler twin sha `5bfed3aa…`) + ref-tool copy.
- `scenarios/` — 8 dumps + `rules.conf`; `receipt-runs.txt` — both tools' byte output per dump + identity checks.
- `receipt-host.txt` — read-only `hyprctl version|getoption|monitors|clients` (dwindle, DP-1 3440x1440, reserve 26).
- `quotes.json` + `verify-quotes.py` + `receipt-quotes.txt` — 40/40 quotes verified at the cited line.

Not verified (declared): a live fullscreen/maximized window (needs a compositor mutation — forbidden); a
fullscreen group member's dump; the map-order of `size` vs `maximize`/`fullscreen` rules for rule-born maximized
windows. Tool installs: none (nothing installed, no package transaction).
