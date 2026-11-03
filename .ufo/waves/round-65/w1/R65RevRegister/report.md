# R65RevRegister — C1 freshness-register attack report (round 65, wave w1)

Seat: R65RevRegister · Lane: mado-shokunin · Lane HEAD at attack time: `cb63ab13ccaf85191318701d5db5ace050bd5bd4` · Base: `524fa1f90b1f2de44b3019bacf833d54e0af13a0` · Date: 2026-11-03 (all times UTC in receipts).

Contract read first: `.ufo/waves/round-65/claims-declaration-r65.md` (frozen at cb63ab13). Counter draft under attack: `.ufo/waves/round-65/w1/R65ExecC1Counter/c1-r65-register.py` (sha256 prefix `6d28e6ca7c2e7a69`, `sha256sum | cut -c1-16`, rc=0). Tool installs: **none**.

## Verdicts

| Attack | Verdict |
| --- | --- |
| A1 register re-derivation (8 groups + extras) | **REPRODUCES** — zero disagreements |
| A2 file-plane gate re-run | **REPRODUCES** — CLEAN, pass=29 fail=0 unknown=0, rc=0 |
| A3 counter forgery | **DESIGN-FLAW-named**: frozen design accepts forged state cells — **recommendation: ACCEPT-WITH-REVIEWER-CROSSCHECK** (+ optional within-letter hardening, clause text below) |
| A4 header uniqueness at base | **SAFE** — 0× dated header at base/HEAD/worktree; family exactly 1× |
| A5 kill-rule honest-absent case | **INSIDE the predicate's letter** — rows count, presence does not |

## A1 — independent register re-derivation: REPRODUCES

My own probes (`a1-register-probes.sh` → `a1-register-probes-r65.txt`, wrapper rc=0, run 2026-11-03T22:35:15Z), compared line-for-line against the claimed states in `.ufo/waves/round-65/receipts/before-register-probes-r65.txt`:

- G1 hypr plane: `command -v hyprctl` rc=0 → `/usr/bin/hyprctl`; `~/.config/hypr` present; `hyprctl version` rc=0 → **Hyprland 0.56.2**, commit `efb50993780079460b0cbed1363e2166a2de1d9f` — identical to receipt.
- G2 waybar: rc=0 → `/usr/bin/waybar`, config present, process running (`pgrep -x waybar` rc=0); pacman `waybar 0.15.0-3` — matches receipt `Waybar v0.15.0`.
- G3 walker: rc=0 → `/usr/bin/walker`, config present; `walker 2.17.2-1` — matches receipt `2.17.2`.
- G4 terminals: `~/.config/{alacritty,foot,kitty,ghostty}` all present — matches receipt (4/4).
- G5 omarchy plane: `~/.config/omarchy` present, `~/.local/share/omarchy` present, `omarchy` at `~/.local/share/omarchy/bin/omarchy` rc=0 — matches receipt exactly; version file `3.8.3` (A2 gate `omarchy.version.file PASS HELD '3.8.3'`).
- G6 idle/lock: hypridle/hyprlock/hyprsunset all rc=0 → `/usr/bin/…` (3/3) — matches receipt.
- G7 omarchy skill docs: `test -d ~/.agents/skills/omarchy` present; it is a symlink → `~/.local/share/omarchy/default/omarchy-skill` (`readlink` rc=0), `SKILL.md` `test -e` rc=0 — matches receipt `present`. (My first `find -maxdepth 1 -name '*.md'` returned 0 — find-on-start-symlink artifact, not a state disagreement; resolved as above.)
- G8 windows desktop plane: `command -v powershell|pwsh|powershell.exe` rc=1 ×3 (none); `python3 tools/mado-win-desk.py` rc=2 → `MADO_WINDESK: ERROR (stage=spawn detail=interpreter not found: powershell.exe)` — genuinely unobservable on this host, exactly the contract's named example.
- Extras (receipt lines beyond the 8 groups): mako PRESENT, swayosd ABSENT, grim/slurp PRESENT — identical to receipt.
- Package cross-check `pacman -Q` rc=0: hyprland 0.56.2-4, hypridle 0.1.8-2, hyprlock 0.9.6-3, hyprsunset 0.4.0-3.

**Disagreements: none.** The receipts' claimed states reproduce on this host by my own commands, not the receipts'.

## A2 — file-plane gate re-run: REPRODUCES

`bash tools/mado-verify.sh --no-live` from the lane worktree (`a2-gate-fileplane-rerun-r65.txt`, wall 2.70 s):

- Gate bytes sha16 `050efc720599345a` (`sha256sum | cut -c1-16`, rc=0) — matches the harm-watch anchor.
- `counts: pass=29 fail=0 unknown=0 skip=8 note=4`; `MADO_VERIFY: CLEAN (29 pass, 4 notes…)`. **GATE_RC=0.** Byte-level identical summary to `receipts/gate-fileplane-r65.txt`.
- TMPDIR pointed at my scratch; the gate's own `boundary.readonly PASS` confirms config plane byte-identical before/after.

## A3 — forged input vs the counter: DESIGN-FLAW-named → ACCEPT-WITH-REVIEWER-CROSSCHECK

Counter legs (from the draft): `rows >= 8` AND `groups == 8/8` (first cells equal the 8 frozen names) AND every block-named receipt path resolves in the rev tree AND some resolved receipt contains `MADO_VERIFY: CLEAN`. **State-cell content is not a leg, and cannot be: the counter reads git objects at `--rev` only, and host truth is not in git objects.**

Cheapest forge demonstrated (`a3-forge.sh` → `a3-forge-r65.txt`): scratch fixture repo (toplevel-asserted before every git mutation, per host guard) = base PROVINCE.md + appended block headed `### Surface state register (2026-11-03, forged A3 fixture…` with **8 rows whose state cells are all FALSE** (probe cells contradict my A1 observations for 7/8 groups) + one receipt pointer to the real committed `gate-fileplane-r65.txt`:

```
MADO_R65_REGISTER: rows=8 groups=8/8 receipts=1 resolved=1 gate=ok verdict=TARGET_MET rev=42670341a54fa9791a29e4cf5b43215b66b5e9f7
FORGED_RC=0
```

Controls on the same run: base-only fixture → `TARGET_MISSED` rc=1; lane at base → rc=1; lane at HEAD → rc=1 (both reproduce `receipts/control-c1-c2-base-r65.txt` independently). So the counter discriminates exactly block-shape + receipt-resolution + gate-token, and **the frozen design accepts forged state cells — plainly stated.**

**Defensible? Yes, given the three legs of the design:** (i) the L1 integrates the block from observed receipts (the rows are derived from this round's probes, not invented); (ii) this seat independently re-derived all 8 groups (A1, zero disagreements) — the truth binding actually executed, by a non-author; (iii) non-author closure re-runs the counter, which verifies mechanism (shape/receipts/gate line) — the only thing a git-objects-only counter can honestly promise. Per-row truth is enforced by the frozen kill rule at write time, not by the counter; no counter variant honoring the frozen predicate can change that. **Recommendation: ACCEPT-WITH-REVIEWER-CROSSCHECK.** The crosscheck exists and is this report's A1.

Optional within-letter hardening (does **not** change the predicate; each enforces a letter already in the frozen sentence — "an appended … block" (singular) and "each row … plus … a committed receipt pointer" (per row); note (c) alone would have rejected my cheapest forge, since it pointed at the file-plane receipt, while the predicate names a **live** gate run):

> TIGHTEN clause text (counter-internal, non-predicate): (a) count HEADING-prefixed blocks; return TARGET_MISSED `reason=block-count=<N>` unless exactly one exists (the finder is currently first-match, so a second appended block would shadow the first); (b) every data row must contain at least one token matching the frozen RECEIPT_RE, else TARGET_MISSED `reason=row-without-receipt=<first cell>` (today receipts are mined from any token in the block, so 8 rows can share 1 pointer — my forge did); (c) the gate leg requires `MADO_VERIFY: CLEAN` in `.ufo/waves/round-65/receipts/gate-live-r65.txt` at rev (present at cb63ab13, `counts: pass=52 fail=0 unknown=0`, `mode: live`), not in any resolved receipt.

Even with (a)+(b)+(c), a forger naming the live receipt in every row still passes — forgery resistance is process-bound (kill rule + reviewer crosscheck + L1 integrating from observed receipts), and that is the honest claim to make.

## A4 — 2026-11-03 header uniqueness at base: SAFE

`git show <rev>:PROVINCE.md | grep -c`:

- `### Surface state register (2026-11-03` → **0** at base `524fa1f9…` (rc=1), **0** at HEAD `cb63ab13…` (rc=1), **0** in worktree (rc=1). No block exists to grab.
- Family `### Surface state register (` → **1** at base, **1** at HEAD, **1** in worktree (rc=0 each) — the single 2026-10-31 register at line 145 is the only same-family block, so the 8-group source register is unambiguous.
- The counter's block finder therefore cannot grab a wrong block at base (control MISSes, confirmed) — but it is first-match, so at landing it should assert exactly-one (hardening (a) above).

## A5 — kill-rule honest-absent case: INSIDE the letter

Declaration quote (claims-declaration-r65.md, C1 Kill rule): *"if a group is genuinely unobservable on this host (e.g. the Windows desktop plane — no powershell here), its row records exactly that with the probe that shows it, and that row still counts (the predicate is re-derivation with an honest state cell, not presence)."* The counter's `rows >= 8` / `groups == 8/8` legs count rows regardless of the state cell, so a windows row recording non-derivability counts — matches the letter. Evidence that the honest cell is derivable here: G8 probes above (3 shells absent rc=1; `mado-win-desk.py` rc=2 with spawn-failure verdict).

## Defects seen

- None in the lane at cb63ab13. Design observations on the draft counter (`6d28e6ca7c2e7a69`): first-match block finder; receipts mined block-wide rather than per-row; gate token satisfied by the file-plane receipt. All named in A3 with clause text; none block landing of an honest block.

## Residual risk / verification gaps

- Live gate not re-run by this seat (A2 scope was file-plane); live receipt verified at bytes level only (`mode: live`, `pass=52 fail=0 unknown=0`, CLEAN at HEAD).
- Local omarchy version file is `3.8.3` (HELD pin) while the contract's sourced leg names S097 "omarchy v3.8.4 … payload": if the S097 re-open confirms 3.8.4 upstream, the contract's own erratum path applies (row names it; never a silent pin bump) — flag for L1/ScribeLesson.
- Counter bytes may move before landing; the A3 verdict is structural (git-objects-only counters cannot verify host state) and holds for any variant honoring the frozen predicate.

## Evidence index (all in this seat dir)

- `a1-register-probes.sh`, `a1-register-probes-r65.txt` — A1 probes + output.
- `a2-gate-fileplane-rerun-r65.txt` — A2 sha + gate run + rc.
- `a3-forge.sh`, `a3-forge-r65.txt` — A3 forge + controls + rc.
- Scratch `/fast/scratch/hyaku/mado-r65/w1/R65RevRegister/` removed at exit (fixture repos included); every receipt was written directly to this seat dir. No tool installed; no config/compositor state touched; no r56-era material opened; no credential-shaped output captured (G8 verdict line carries field names only).
