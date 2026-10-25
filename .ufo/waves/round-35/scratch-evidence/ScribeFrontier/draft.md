## Sources & frontier

**Registry rows before → after.** 192 → 200 (+8). Counted, not quoted:

```sh
git show 19e4ab3171c1540c40d6b12097745af98053b07d:corpus/SOURCES.md | grep -c '^| S[0-9]'   # → 192 (r35 freeze rev; same 192 at r34 tip dff394109f3c)
grep -c '^| S[0-9]' corpus/SOURCES.md                                                    # → 200 (re-run post-land)
```

The land is insertion-only — eight lines inside the registry table after the
S202 row, zero lines changed or removed (`git diff <rev> -- corpus/SOURCES.md`
adds 8, deletes 0). The frozen admission counter re-counts the same surface:
`python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json`
→ `closed_entries=3 closed_rows=8 open_cites=0 TARGET_MET`.

**Rows added by tier.** Eight rows, all `own-work`/tier **A**, all `status=mined`,
all opened 2026-10-24, continuing the id space contiguously from S202 (no gap):

| row | surface | cites |
|---|---|---|
| S203 | `omarchy-first-run` installer — the setup path that asks nothing | `idle-lock-never-asked-r12.md` |
| S204 | journal + flag sweep — zero `omarchy-toggle` invocations, zero idle flag files | `idle-lock-never-asked-r12.md` |
| S205 | idle-chain present state — hypridle pid 1667, session start lines, timeouts 150/152 | `idle-lock-chain-armed-r14.md` |
| S206 | `config.jsonc` `custom/idle-indicator` block — the click runs `omarchy-toggle-idle` | `idle-lock-offered-in-the-bar-r15.md` |
| S207 | `idle.sh` indicator — two-state vocabulary, tooltip "Idle lock disabled" | `idle-lock-offered-in-the-bar-r15.md` |
| S208 | `omarchy-menu` — Idle Lock in the Toggle submenu, `*Idle*) omarchy-toggle-idle ;;` | `idle-lock-offered-in-the-bar-r15.md` |
| S209 | four dated `config.jsonc` copies, every one carrying the handler, oldest 2026-10-03 | `idle-lock-offered-in-the-bar-r15.md` |
| S210 | `~/.local/state/omarchy/toggles/hypr` — 2 toggle files, 0 name the idle lock | `idle-lock-offered-in-the-bar-r15.md` |

Adopted from merge-package ids S315, S316, S327, S335, S336, S337, S340, S342,
re-pointed by document and re-grounded in-round (each `anchor` cell carries the
committed receipt `.ufo/waves/round-35/fetch/S###.receipt.txt` and its sha256).

**Rows touched old → new.** None. No existing row's `status`, `recheck` or
`used-by` cell changes — the three admitted entries cite only the eight new
rows, and the append is pure insertion (0 deleted lines). No row's status
flips: the eight adopted rows land already `mined`, and no queued row advances
this round.

**Frontier rows advanced.** `corpus/README.md` index rows 47 → 50 (+3), one
per admitted entry, plus one new Frontier bullet (draft, appended after the
round-25 block; not gate-checked):

> - Round 35 moves the idle-lock **control surface** onto host-measured
>   sourced ground: the first-run questionnaire that asks nothing and the
>   journal that records no toggle invocation ([never asked](knowledge/idle-lock-never-asked-r12.md)),
>   the armed chain's present state — hypridle live, timeouts 150/152
>   ([chain armed](knowledge/idle-lock-chain-armed-r14.md)) — and the two
>   surfaces that *do* offer the choice: the bar's `custom/idle-indicator`
>   click-handler and the menu's Idle Lock entry, with the indicator's own
>   two-state vocabulary ([offered in the bar](knowledge/idle-lock-offered-in-the-bar-r15.md);
>   S203–S210). This **corrects** the earlier over-read "the desktop never
>   offers the choice" — it never offers it at setup; the running interface
>   offers it continuously, and the operator never took it (zero invocations).
>   Still open: the rendered indicator text and tooltip pixels, the toggle's
>   effect when clicked, and idle/lock transitions, listener firing and lock
>   success (round-17 items, unchanged). The operator's preference stays
>   `[UNK]` — it answers to one person, not to a file.

The `README.md` frontier's "Screen / idle / lock" route line stays accurate:
no idle/lock transition was exercised this round.


**Assimilation line.** Entries admitted: **3** of 69 proposed
(`idle-lock-never-asked-r12`, `idle-lock-chain-armed-r14`,
`idle-lock-offered-in-the-bar-r15` — each rewritten for lane ids and re-grounded
in-round; the package's 2026-10-06 oldest-copy figure is superseded by this
round's measured 2026-10-03, recorded in the adopted entry's §5). Rows
refused: **139** of 147 staged — none is cited by an admitted entry and the
frozen predicate counts exactly `closed_rows=8`, `open_cites=0`, so any extra
append fails its own spec; flip: a later round that freezes a claim over those
documents and re-grounds them — the route this round (and round 34 for the
waybar pair) already exercised. Same reason and flip for the 66 refused
knowledge items: 62 new-file proposals plus the 4 entry amendments
(`ipc-contract-r25`, `dispatcher-semantics-r25`,
`waybar-module-text-route-r25`, `dispatcher-surface-and-request-grammar-r26`),
all outside the round's two frozen claims.
