# R80ExecC2Run — C2 rerun and the two new rows against the real replies

Seat: R80ExecC2Run (executor, leaf). Lane: mado-shokunin, round 80, wave 1.
Frozen measured rev: `6c302a53eb8f577e83fbcadc01e05a286778df8e`; base: `e10f7e9f528b13195a1cdde28a68a702af3045c4`. Date: 2026-11-04.
Axes: (1) reproduction of the frozen C2 measurement, (2) fidelity of the two new rows against live replies, (3) evidence integrity while the shared worktree moves.

Writes stayed inside `.ufo/waves/round-80/w1/R80ExecC2Run/` plus the seat's report path. No commit, no push, no mutating git/jj, no frozen-instrument edit; the frozen counter blob was extracted read-only into the seat dir for evaluation. Scratch `/fast/scratch/hyaku/mado-r80/R80ExecC2Run` removed at exit (`scratch-removed`).

## 1. Frozen counting command — rerun at the measured rev

Executed verbatim from the lane root:

```
python3 -I quality/counters/c2-r80-runbook.py --repo . --rev 6c302a53eb8f577e83fbcadc01e05a286778df8e --controls .ufo/waves/round-80/controls/c2-runbook-cases-r80.json --carried .ufo/waves/round-79/controls/c2-runbook-cases-r79.json --scratch-root /fast/scratch/hyaku/mado-r80/R80ExecC2Run
```

Saved: `c2-after.txt` (1 line), `c2-after.rc` = **2**.

```
MADO_R80_RUNBOOK: ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)
```

This is the instrument's designed tree-binding refusal; the declaration maps rc 2 to "setup error (never a verdict)". Cause, verified read-only:

- HEAD advanced 11 commits past the freeze and the shared worktree moved while this seat ran: `HEAD=ff314eb0…` observed early, `HEAD=681be825…` at the final snapshot (repairs R1/R2/R3 and receipts).
- SKILL.md bytes: frozen rev `0702f8d0ea92…` vs tree/HEAD `e7412d8cc397…` — one line: the `mado-r80-barfoot-composition-counter` selftest cell `48/48 → 60/60` (commit `5788d3e4`).
- Frozen pins vs tree at the final snapshot (blobs at `6c302a53` re-hashed and compared):

| instrument | frozen rev blob (pinned) | tree at 681be825 |
|---|---|---|
| `quality/counters/c2-r80-runbook.py` | `462287fb…` (pin) | `d422892b…` (R2+R3 repairs) |
| `quality/counters/c1-r80-multisurface.py` | `6268667c…` (pin) | `f0ffeb20…` |
| `tools/mado-barfoot.py` | `c3eb5fbe…` (pin) | `5b9e2930…` (R1) |
| c2 control set | `f1dfb5f4…` | `f1dfb5f4…` (equal) |
| c1 control set | `17c27157…` | `17c27157…` (equal) |
| declaration | `9398d53f…` | `66d62358…` (append-only R1–R3 addenda) |
| `SKILL.md` | `0702f8d0…` | `e7412d8c…` (one cell) |

The declaration's R1–R3 addenda are append-only and match the instrument repairs; no frozen control set moved.

Recorded measurements on disk (read-only): `receipts/measurement-c2-r80.txt` — `TARGET_MET` at `6c302a53…` (`cases=24 executed=24 matched=24 shapes=19/19 anchors=24/24 rows=24/24 control_new=0/2 mutants=16 killed=16 … tree=bound`); `receipts/measurement-c2-r80-at-tip.txt` — the same green contract at `231f92bc…` (`tree=bound`). My rerun at the frozen rev against today's post-freeze tree cannot yield a verdict by design; a verdict-bearing rerun must run at a rev whose bytes are checked out — the parent's post-integration gate.

## 2. The two new rows' real replies

- `chords.txt`: `omarchy menu keybindings --print | cut -c1-35` → rc 0 (pipe status), **193 lines**.
- `state.txt` / `state.rc`: `systemctl --user is-active hypridle` → word **`inactive`**, rc **3**.

## 3. Independent checker (`check_chords.py` → `chords-check.json`)

Parsed with the declaration grammar: chord = 1–4 distinct words from SUPER/SHIFT/CTRL/ALT joined by ` + `, then one key; or a bare key (strict reading: key is one whitespace-free token).

Counts:

- total lines **193**
- chord lines **169** (167 with single-token keys + 2 with multi-word keys)
- bare lines **24** (21 single-token + 3 multi-word)
- structural failures: **0** — no foreign modifier word, no numeric mask, no repeated modifier, no `→` in any line, no empty line, no padded/doubled key, no stray `+` outside ` + `
- longest line: **35 chars** — `cut -c1-35` never clipped visible content and never exposed the arrow column (longest chord text: 29 chars, matching `receipts/chord-grammar-live-r80.txt`)

Modifier tuples — 12 distinct sets, all words from the allowed four, max 3 modifiers used (grammar allows 4):

| tuple | lines |
|---|---|
| SUPER | 42 |
| SUPER + SHIFT | 36 |
| SUPER + CTRL | 26 |
| SUPER + SHIFT + ALT | 22 |
| SUPER + ALT | 19 |
| ALT | 7 |
| SUPER + CTRL + ALT | 6 |
| SHIFT + ALT | 3 |
| SUPER + SHIFT + CTRL | 3 |
| CTRL + ALT | 2 |
| SHIFT | 2 |
| SHIFT + CTRL + ALT | 1 |

Lines outside the strict single-token-key reading (5; **not** structural failures — the formatter's key names contain spaces):

- `COPILOT KEY` — bare, 2 tokens (the menu's code:201 marker per the declaration)
- `SUPER + LEFT MOUSE BUTTON`, `SUPER + RIGHT MOUSE BUTTON` — 3-token keys
- `switch:off:Lid Switch`, `switch:on:Lid Switch` — bare, 2 tokens

The frozen `chord_shape` matcher accepts all of them (tail non-empty, no `+`, no padding); the declaration's "one key" is the formatter's keysym expression, not necessarily whitespace-free.

`min_chords` comparison against the counter's frozen control value (`min_chords: 100`, `min_lines: 100`, mods `[ALT, CTRL, SHIFT, SUPER]`, `max_mods: 4`): chords **169 ≥ 100** holds; lines 193 ≥ 100 holds. Headroom 69 chords.

Corroboration: the lane's live receipt `receipts/chord-grammar-live-r80.txt` reports the identical totals (`lines=193 chords=169 bare=24`), the same 12 modifier renderings and `longest chord column: 29`; it records a strict-grammar verdict `False`, which the R2 addendum explains (the formatter intermittently renders `MODS + ` with no key — 41 such lines in one invocation, none in the next). Today's capture carries **zero** empty-key lines: all 169 chord lines have a non-empty key.

## 4. Bare-key forms and chord-confusion check

24 bare lines = 23 distinct forms: `F9` (×2), `PRINT`, `COPILOT KEY`, `switch:off:Lid Switch`, `switch:on:Lid Switch`, and 18 `XF86*` keys: AudioLowerVolume, AudioMicMute, AudioMute, AudioNext, AudioPause, AudioPlay, AudioPrev, AudioRaiseVolume, Calculator, KbdBrightnessDown, KbdBrightnessUp, KbdLightOnOff, MonBrightnessDown, MonBrightnessUp, PowerOff, TouchpadOff, TouchpadOn, TouchpadToggle.

Could any be mistaken for a chord? **No.** Chord recognition is keyed on the literal ` + ` separator; no bare form contains it, so no bare line ever counts as a chord. The multi-word bare forms (`COPILOT KEY`, `switch:*:Lid Switch`) contain no ` + ` and are simply not chords for the frozen matcher. Conversely the mouse-button chords split correctly at the last ` + `, and the description column starts beyond char 35 (longest line exactly 35), so no description text can contaminate a key tail.

## 5. State row

Pair: word **`inactive`** + rc **3** — consistent with the declared contract (`active` ⇔ rc 0, otherwise rc 3).

Frozen matcher evaluated through `special_matches` (the counter's `case_correct` path, which bypasses the rc==0 gate for `is_active`/`refusal`), on the captured pair and on the committed fixtures of both new cases (control set sha `f1dfb5f4…`, verified against the frozen rev and the tree):

| implementation | real chords reply | real state pair | keybindings negatives | keybindings samples | state negatives | state samples |
|---|---|---|---|---|---|---|
| frozen `462287fb…` | true | true | 8/8 rejected | 2/2 accepted | 4/4 rejected | 3/3 accepted |
| tree `d422892b…` (R2/R3) | true | true | 8/8 rejected | 2/2 accepted | 4/4 rejected | 3/3 accepted |

The two implementations differ only in the chord empty-key branch (tree adds the `probe = line` acceptance and drops the `not tail` guard); no divergence on the real reply or the committed fixtures.

## Evidence (all in this seat dir)

- `c2-after.txt` (1 line), `c2-after.rc` (= 2)
- `chords.txt` (193 lines), `state.txt` (`inactive`), `state.rc` (= 3)
- `check_chords.py`, `chords-check.json`
- `frozen-c2-r80-runbook-6c302a53.py` (extracted frozen blob, sha256 `462287fb…`), `frozen_matcher_eval.py`, `frozen-matcher-eval.json`

## Risks / open

- The shared worktree advanced during the seat (HEAD `ff314eb0` → `681be825`; R1/R2/R3 repairs committed). Any verdict-bearing C2 rerun must be taken at a rev whose bytes are checked out; at the frozen rev the counter must refuse until the tree is restored or the measurement is re-bound — the parent's post-integration gate.
- `min_chords=100` is a floor checked against 169 chord lines; a reply with fewer than 100 chords would fail the row (ample headroom here).
- The 5 multi-word-key lines depend on reading the declaration's "one key" as the formatter's keysym expression; a strict whitespace-free reading would flag them. The frozen matcher's tolerance and the row's committed samples are consistent with the former.

STATUS: ok — all assigned steps executed and evidenced.
Missing: nothing in this seat's scope; a verdict-bearing C2 rerun at a tree-bound revision belongs to the parent's post-integration gate.
