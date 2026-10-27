# R54W2Seat09 — C1 swapped-pin control (item 9, wave 2)

- Seat: `R54W2Seat09` · role `reviewer` · wave `w2` · round 54 · 2026-10-27
- Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin` · base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa` · scored/freeze rev `350d30e4ec5531f65ce99a57efeb8216f38e678a` (lane HEAD at attack time; the freeze commit itself, per `git log e25149fe..350d30e4` → one commit "round-54: freeze claims, registration, source pins and wave one dispatch")
- Assignment (item 9, `w2-spec.json`): *Attack item 9: C1 swapped pin control. Apply C1-CTL-6; ensure implementation reads entry-declared pin. Cite frozen contract lines, exact pin spans and relevant w1 report.*
- **Pinned command status: ABSENT — NOT RUN.** `ls quality/counters | grep -c r54` → `0`; `git ls-files | grep -c r54` → `0`. `quality/counters/c1-r54-errata-truth.py` does not exist in the lane working tree or at any reachable revision, so `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>` was not executed against a landed counter; `C1-CTL-6` vs the *landed* implementation is **NOT RUN**. All runs below exercise the w1 reference draft (provenance-bound, §3), clearly labeled as such. No results are invented.

## 1. Frozen contract cited

| what | where |
|---|---|
| CTL-6 row: `C1-CTL-6 swapped-pin \| entry's P19 pin cell → Hyprland-KeybindManager.cpp \| quote absent from that pin → MISSED` | `registration.md:47` |
| Control protocol: "run against mutated trees — the counter reads all inputs from `--repo`/`--rev` git objects, so a control = a mutated copy of the scored tree" | `registration.md:40-42` (C1 control table preamble) |
| Predicate clause (d): "each of the six frozen C1 controls of `registration.md` is rejected by the counter" | `claims-frozen.md:29-30` |
| Kill rule: "if any frozen C1 control is admitted by the counter … the counter prints `verdict=TARGET_MISSED` and a non-zero exit — the claim is dead for the round" | `claims-frozen.md:37-39` |
| P19 frozen row (pin cell `Hyprland-ConfigActions.cpp:1554-1558`) | entry `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md:17` at rev `350d30e4` |

## 2. Ground truth — exact pin spans (required verdict reachability)

Pins at `.ufo/waves/round-52/fetch/` (committed, 6 tracked files):

```
$ sha256sum Hyprland-ConfigActions.cpp Hyprland-KeybindManager.cpp
a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  Hyprland-ConfigActions.cpp   (= registration.md recorded sha256)
8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40  Hyprland-KeybindManager.cpp  (= registration.md recorded sha256)
```

P19 span, `Hyprland-ConfigActions.cpp:1554-1558` (raw bytes):

```
1554     g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);
1555 (blank)
1556     if (S.m_passPressed == 1) {
1557         if (!isMouse)
1558             g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);
```

Absence of the quote from the swapped pin (required-verdict reachability):

```
$ grep -c 'sendKeyboardMods(modMask, 0, 0, 0)' Hyprland-KeybindManager.cpp → 0
$ grep -c 'm_passPressed == 1'                 Hyprland-KeybindManager.cpp → 0
$ grep -c 'sendKeyboardMods(modMask, 0, 0, 0)' Hyprland-legacy-DispatcherTranslator.cpp → 0
```

The P19 quote genuinely occurs **only** in the entry-declared pin → a counter that reads the entry cell must reject CTL-6; corroborates `w1/R54Seat34.md:98` ("`C1-CTL-6`'s required verdict is reachable: the P19 quote is absent (`raw=0`) from `.hpp`, `KeybindManager.cpp` and `DispatcherTranslator.cpp`").

## 3. Implementation under test — w1 reference draft, provenance-bound

No landed counter exists (§0), so the attack target is the w1 reference implementation: `R54Seat04` Appendix A draft, extracted from `w1/R54Seat04.md:352-1194` (843 lines):

```
sha256  085738f5742be7b4ba5c999f641cb84901c997800f741605af89978e799dd982
```

— **byte-identical** to the sha256 R54Seat04 recorded for its scratch draft (`w1/R54Seat04.md:346`). Load-bearing lines (draft-relative):

- `:404` `pin_name, anchor_text = parse_pin_cell(cells[pin_idx])` — pin resolved from the **entry row's own cell**;
- `:420` `pin_bytes = blob(repo, rev, FETCH_REL + "/" + pin_name)` — quote occurrence searched in the **entry-declared** pin;
- `:432` `if quote_frozen: counts["quotes"] += 1` (only after hits in that pin);
- `:488` `if quote_frozen and pin_frozen and anchor_frozen: counts["anchors"] += 1` — the entry-vs-frozen pin equality as a second, independent rejection leg;
- `:615-622` `ctl_swapped_pin` — internal control mutates `cells[4]` to `Hyprland-KeybindManager.cpp:<anchor>`, exercising the same path.

This is the design R54Seat02 measured as the non-gameable branch: "range-only with the pin resolved from the frozen table instead of the entry cell: admits `C1-CTL-2`, `C1-CTL-4` and `C1-CTL-6` outright" (`w1/R54Seat02.md:173-182`) — i.e. the entry-cell read at `:404`/`:420` is exactly what my item must ensure.

## 4. Runs — fixture protocol and exact outputs

Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat09`; fixture `D=mktemp -d` inside it; `git clone --no-local --no-hardlinks` of the lane → `D/ctl6.9XHMOL`; clone HEAD verified `350d30e4…`; `git -C D rev-parse --show-toplevel` printed `D` and was asserted equal before the commit (toplevel check quoted in the transcript below). Fixture-only throwaway identity via `git -c user.name=… -c user.email=…`; the lane was never mutated.

**R1 — draft at the scored rev, pristine fixture** (sanity; matches `w1/R54Seat04.md:113-121`):

```
$ python3 -I c1-r54-errata-truth.py --repo $D --rev 350d30e4ec5531f65ce99a57efeb8216f38e678a --work $S/work1
detail: control C1-CTL-1 spliced-quote rejected (quotes=3/4)
detail: control C1-CTL-2 shifted-anchor rejected (anchors=3/4)
detail: control C1-CTL-3 hash-tamper rejected (pins=3/4)
detail: control C1-CTL-4 wrong-range rejected (anchors=3/4)
detail: control C1-CTL-5 dropped-proposition rejected (propositions=3/4)
detail: control C1-CTL-6 swapped-pin rejected (quotes=3/4)
MADO_ERRATA_TRUTH: rev=350d30e4… propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
exit=0
```

**R2 — C1-CTL-6 applied externally.** Mutation: entry P19 pin cell `Hyprland-ConfigActions.cpp:1554-1558` → `Hyprland-KeybindManager.cpp:1554-1558` (unique string; P20's `:1576` cell untouched); committed in the fixture only:

```
toplevel=/fast/scratch/hyaku/mado-r54/R54W2Seat09/ctl6.9XHMOL   (asserted == D)
CTL6REV=ac4443fd394bdec1becfaee76120621d34d012d8
git -C $D diff 350d30e4… HEAD -- <entry>  → 1 file changed, 1 insertion(+), 1 deletion(-)
  -| P19 | … | Hyprland-ConfigActions.cpp:1554-1558 | …
  +| P19 | … | Hyprland-KeybindManager.cpp:1554-1558 | …

$ python3 -I c1-r54-errata-truth.py --repo $D --rev ac4443f… --work $S/work2
detail: P19 pin Hyprland-KeybindManager.cpp differs from the frozen table Hyprland-ConfigActions.cpp
detail: P19 quote not contiguous in Hyprland-KeybindManager.cpp
…
MADO_ERRATA_TRUTH: rev=ac4443f… propositions=4/4 quotes=3/4 anchors=3/4 pins=4/4 controls=6/6 verdict=TARGET_MISSED
exit=1
```

**→ REJECTED with the registration-required verdict** (`registration.md:47`: "quote absent from that pin → MISSED"), and the two detail lines are direct proof the implementation reads the **entry-declared** pin (`KeybindManager.cpp`) and fails the quote leg there. Both independent legs bite: quotes 3/4 (`:420` search) and anchors 3/4 (`:488` equality). Consistent with `w1/R54Seat04.md:120`, `w1/R54Seat33.md:116`, `w1/R54Seat01.md:323`.

**R3 — one-line gameable variant (pin from the frozen table, entry cell unread).** Patch after draft `:404`: `pin_name = FROZEN[pid][0]`. On the **same CTL-6-mutated tree**:

```
MADO_ERRATA_TRUTH: rev=ac4443f… propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=5/6 verdict=TARGET_MISSED
detail: control C1-CTL-6 swapped-pin ADMITTED (quotes=4/4)
exit=1
```

The clause measurement passes **4/4 across the board on a control-mutated tree** — the swap is invisible to every measurement leg; the verdict is held at MISSED **only** by the counter's own internal control leg (`controls=5/6`). On the pristine base the same variant is indistinguishable from the honest draft (identical counts) — the gameability is invisible on honest trees.

**R5 — blind shape (same patch + control leg faked to `return 6`).** On the CTL-6-mutated tree:

```
MADO_ERRATA_TRUTH: rev=ac4443f… propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
exit=0
```

A counter that never reads the entry-declared pin and self-reports its control leg prints the full frozen `TARGET_MET` line, exit 0, on a C1-CTL-6-mutated tree. Only an externally built and externally run CTL-6 mutant (exactly R2) distinguishes it. This re-confirms mechanically what `w1/R54Seat02.md:173-182` and `w1/R54Seat30.md:163-165` argued from design.

## 5. Findings

| id | severity | finding | evidence |
|---|---|---|---|
| F1 | verified-positive | The w1 reference implementation **reads the entry-declared pin**: external CTL-6 rejected with the exact frozen required verdict (quotes=3/4, exit 1), and the internal `ctl_swapped_pin` control degrades the quotes leg. | §3 code lines `:404/:420/:432/:488/:615-622`; R1, R2 |
| F2 | HIGH — process gap | **No landed C1 counter exists at w2 start** (`ls quality/counters \| grep -c r54` → 0; `git ls-files \| grep -c r54` → 0). C1-CTL-6 against the *landed* implementation: **NOT RUN / absent**. Every R-run above is against the byte-identical w1 draft, not the canonical pinned command. | §0 |
| F3 | MEDIUM — contract reliance | With the entry-cell read removed, all four clause counts still measure 4/4 on a CTL-6-mutated tree (R3); rejection then hangs solely on the counter's self-reported control leg, and faking that leg yields full TARGET_MET on the mutated tree (R5). The frozen receipt rule ("the counter's own control run is committed per control", `claims-frozen.md:45`) plus external per-control runs are both load-bearing; the L1 integration should run each control against a mutated copy of the scored tree, not trust `controls=6/6`. | R3, R5; `w1/R54Seat30.md` |
| F4 | INFO | CTL-6 mutation shape: I kept the anchor inside the swapped cell (`Hyprland-KeybindManager.cpp:1554-1558`), per the entry's `Pin:anchor` cell format; the quote is absent from that pin at any anchor reading, so the required verdict is reachable either way. | §2, R2 |
| F5 | INFO | R2's rejection fires on two legs (quotes via the entry-declared search, anchors via the frozen-table equality). A counter rejecting CTL-6 through the equality leg alone while searching the frozen pin (R3 shape) would still be verdict-correct today — the internal control is what keeps it honest; see F3. | R2 vs R3 |

## 6. Residual risk and verification gaps

- The canonical pinned command could not be exercised — there is no landed `quality/counters/c1-r54-errata-truth.py`; C1-CTL-6 (and the other five controls) against the landed counter remain unverified until the L1 lands it and re-runs the receipt suite.
- Draft-provenance caveat: my R-runs certify the R54Seat04 draft's behavior. If integration lands a different implementation, F1 must be re-established there; F3/F5 define the acceptance bar (external mutant run must flip any entry-cell-blind shape to MISSED).
- Upstream identity of the round-52 pins (beyond committed sha256 agreement) was not re-verified — offline seat, out of scope for this item.

## 7. Compliance

- Lane/fleet/sibling/source files: untouched (only this report written, at the assigned path). No git/jj mutation outside the scratch fixture; fixture commits made only after `git -C D rev-parse --show-toplevel` equaled `D`. No delegation, no background jobs, no host reads, no network, no tool installs. No ENOSPC observed (`/fast` had 580G free).
- Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat09` (draft copies, fixture clone `ctl6.9XHMOL`, work dirs `work1…work5`) **removed before yield**.

Report trailer: `.ufo/waves/round-54/w2/R54W2Seat09.md`
