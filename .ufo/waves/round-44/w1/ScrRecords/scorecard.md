# Draft — SCORECARD.md Round 44 section (append after the Round 43 section; `<<L1>>` = value only the L1 can fill)

## Round 44 - state verdicts in the rule-size join, and the gkeep size-request entry (2026-10-26, attempt 1)

Registration `.ufo/waves/round-44/registration.md` (freeze `e2289516a9a857f55cda7be635933e89b931c3da`, base
`6a1a90528fe533cadee506a9fa3e9d13d15cc41f`): C1 extends the round-43 join (`tools/mado-geometry.py`) with window-state
verdicts; C2 is a new sourced entry for what the compositor sends the client after it has replaced the rule's box. C1's
ground is a false report in the round-43 tool: Hyprland 0.56.2 sets a maximized window's box to the work area and a
fullscreen window's box to the monitor box (`fetch-c1/Hyprland-FullscreenHandler.cpp` `setTargetSizeAndPosition`,
`Hyprland-FullscreenController.hpp` `eFullscreenMode`, `Hyprland-HyprCtl.cpp` `fullscreen` = `.internal`), so the
round-43 tool reports a fullscreen gkeep window DIFFER. Shape: **two v1 waves** - `w1` (build + first falsifiers, 38
seats) and `w2` (falsify, after the data commit, `<<L1>>` seats). Lowest-axis rule: every published axis ties at its
maximum at base (`receipts/axis-base.txt`: navigation 60/60, calibration 68/68, operability 12/12, `MADO_AXIS:
checked=3 mismatched=0`), so operability (C1) and coverage (C2) are the lowest axes. Data commit `<<L1>>`.

| Claim / axis | Before -> after | Counting command | Self-verdict |
|---|---|---|---|
| C1 **operability** (capability extension) - `tools/mado-geometry.py` gains state verdicts | `fixtures=12/26 tool=present verdict=TARGET_MISSED` exit 1 at base, clauses `a:1 b:0 b4:0 g:1 r:1` (`receipts/c1-before-base.txt`; the lattice count varies with the nonce - 13/26 in `receipts/ctl-c1.txt` - the verdict does not) -> `fixtures=26/26 tool=present verdict=TARGET_MET` exit 0 at the data commit `<<L1>>` (`receipts/<<L1>>`) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev <rev> --tool <file> --work <scratch>` (`PRED-C1-r44`) | **`<<L1>>`**; kill rule: anything but `26/26 TARGET_MET` at the data tip is an honest stop. Frozen falsifiers: `receipts/ctl-c1.txt` - 15 controls, 0 of 15 non-reference runs reach TARGET_MET (REF 26/26; do-nothing 13/26; ABSENT; 13 single-defect variants of the reference), and K13 (selftest cases removed) scores `26/26` on fixtures yet misses only clause b, so the selftest clause is load-bearing |
| C2 **coverage** (sourced; assimilation) - `corpus/knowledge/hyprland-gkeep-size-request-r44.md` | `admitted=0/1 verdict=TARGET_MISSED` exit 1 at base, clauses `a:0 b:0 c:0 d:0 e:0 f:0 g:0 h:0 i:0` (`receipts/c2-before-base.txt`; the base holds none of the chain - `git grep -ciE 'sendWindowSize\|pendingSizeAcks\|xdg_toplevel.configure\|set_size_request' 6a1a905 -- corpus/knowledge PROVINCE.md SKILL.md tools` exit 1, `receipts/c2-ground-base.txt`) -> `admitted=1/1 verdict=TARGET_MET` exit 0 at the data commit `<<L1>>` (`receipts/<<L1>>`) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo <repo> --rev <rev> --base 6a1a90528fe533cadee506a9fa3e9d13d15cc41f` (`PRED-C2-r44`) | **`<<L1>>`**; kill rule as C1. Frozen falsifiers: `receipts/ctl-c2.txt` - 3 controls (base, the staged r12 file copied verbatim to the entry path, a header-plus-census shell), 0 of 3 admitted; **no positive control existed at the freeze** - w1 builds one, its receipt and verdict are `<<L1>>` |

Separable: C1 reads the tool plus the round-42 counter (clause r, the no-harm clause); C2 reads the entry, the registry,
the lesson, the README index and the pinned receipts, and no tool. Either lands without the other (`<<L1>>` re-check).

### Capabilities (round 44)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| rule size versus reported size join | read one or more Hyprland config files and one `hyprctl clients -j` dump (file or stdin) and report, per client matched by a `windowrule = size W H, match:class RX` line (RE2-compatible regex subset, `re.fullmatch`), AGREE / DIFFER / TILED / BADSIZE **plus the window state the client reports** - FULLSCREEN (fsmode 2) and MAXIMIZED (fsmode 1), ranked BADSIZE -> FULLSCREEN -> MAXIMIZED -> TILED -> AGREE -> DIFFER, with ` maximized=<n> fullscreen=<n>` in the summary exactly when their sum is > 0 and the round-43 line byte-identical otherwise - and NO_MATCHING_CLIENT / NO_SIZE_RULES / SETUP verdicts with exit codes; starts no process, opens no socket | `tools/mado-geometry.py` (selftest `<<L1>>`/`<<L1>>`); `quality/counters/c1-r44-geometry-states.py` 26/26 at `<<L1>>`; clause r re-runs the round-43 counter at `37/37` on the same bytes (`receipts/<<L1>>`); live host run `receipts/<<L1>>` | 43 (state verdicts 44) |

Row form (argument): the round-43 row is **extended in place**. `AXES.md` §Capabilities admits a row through a round
that demonstrates the capability running: the capability named here (the join) first ran in round 43, so a second row
would give one tool two overlapping descriptions that diverge as the tool changes, and leaving the round-43 text as
written would describe a verdict set the tool no longer ends at (a fullscreen gkeep window reads `FULLSCREEN`, never
`DIFFER` - the very false report C1 exists to remove; at base the installed tool's own docstring lists only
`BADSIZE (size none) | TILED (not floating) | AGREE (size == want) | DIFFER`, `tools/mado-geometry.py:49`, and
`grep -c 'FULLSCREEN\|MAXIMIZED\|maximized=' tools/mado-geometry.py` is 0). Round 30's "corrected scope" row is precedent for a *correction*
of a row's scope; this is an extension of the same verb, and the cell `43 (state verdicts 44)` records both rounds in
the form the table already uses (`5 (re-demonstrated 12)`).

### Sources, saturation, planned

Sources 234 -> 238 rows (S298-S301, tier `<<L1>>`, `mined`, opened 2026-10-26 - the four non-held pins of `fetch/`, by
document); held S164 (Window.cpp) is pinned by `receipts/fetch-sha256.txt` and its `used-by` `<<L1>>` (old->new in
`corpus/lessons/round-44.md`); knowledge entries 60 -> 61. Assimilation: `gkeep-client-size-request-r12.md` is the predecessor
candidate (`<<L1>>` admitted as such); `<<L1>>` of r9/r13/r14/r15 refused with reason and flip. considerthese `2026-10-25.md`
proposal 1 ("track the domain-versus-meta ratio as a running number") `<<L1>>`. Mistakes `<<L1>>` mined; QUALITY
`<<L1>>`; `<<L1>>` from the round-43 closure's routed defects D1-D4, D6, D7. Saturation 9.0 / N=3 unchanged; retired:
none.

Axis table re-derived at `<<L1>>` plus the round-44 records commit (one new indexed entry, criteria `<<L1>>`):
navigation `<<L1>>`; calibration `<<L1>>`; operability selftest `<<L1>>`.

### Planned (round 45; intent only)

1. A live gkeep window on the host session, read with the extended `tools/mado-geometry.py` (operator opens gkeep; mado
   reads only) - turns the FULLSCREEN/MAXIMIZED path from a fixture fact into a host observation.
2. Close the round-44 open predicate defects under a new registration: C2's missing positive-control family and its
   do-nothing admission, C1's sandbox detection and b4 site counting.
3. The remaining gkeep-theme residue (the map-time journal route; `fetchClass`) as a third entry.

### Wave w2 outcome (round 44)

Wave `w2` (`<<L1>>` seats, `<<L1>>` dead) re-ran both counting commands `<<L1>>`, re-ran the frozen controls `<<L1>>`,
confirmed separability in both directions `<<L1>>`, and reported `<<L1>>` self-assessment mismatches `<<L1>>`. Tip receipts
at `<<L1>>`: C1 `fixtures=26/26 tool=present verdict=TARGET_MET` exit 0 (`receipts/<<L1>>`), C2 `admitted=1/1
verdict=TARGET_MET` exit 0 (`receipts/<<L1>>`), census `<<L1>>` (`receipts/<<L1>>`), `MADO_AXIS checked=3 mismatched=0`
(`receipts/<<L1>>`).

Open predicate defects reported by w2 (no re-registration after data): `<<L1>>`.

**Erratum (round 44, closure D5; Round 43 left as written).** Round 43's `### Sources, saturation, planned` reads "Mistakes
M43-1..8 mined", but `corpus/lessons/round-43.md:191` carries **M43-9**, so the lesson covers M43-1..9; round-43
`registration.md:5` says 37 `w1` seats, and 38 ran (`LOG.md:2489`).
