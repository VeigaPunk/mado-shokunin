# Falsify38 — C2 proposition-map completeness

## Deliverables

- This report: `.ufo/waves/round-52/w1/Falsify38.md`
- Seat directory `.ufo/waves/round-52/w1/Falsify38/`:
  - `build_fixture.py` — seat-local fixture builder (rebuilds the two-commit fixture repo)
  - `check.py` — structural checker implementing the counter-side checks of the frozen C2 predicate
  - `receipt-base.txt` — no-work control run (entry absent → `TARGET_MISSED`)
  - `receipt-bypass.txt` — bypass run (4/4 declared propositions bound + smuggled unmapped false claim → `TARGET_MET`)
  - `receipt-mutant.txt` — negative-control run (broken P2 binding → `TARGET_MISSED`)

## Finding

- **Attacked item/predicate:** C2 frozen predicate, completeness direction — "every material factual proposition is mapped" (`.ufo/waves/round-52/claims-frozen.md` §C2; `.ufo/waves/round-52/registration.md` §Frozen predicates: "at least four substantive propositions; each maps to an opened-this-round `S###` row, a pin path/revision and exact located quote <=25 words, with a written support rationale; every material factual proposition is mapped. A counter checks proposition count, row/pin/quote bindings and index").
- **Concrete failure mode:** the counter-side checks are satisfiable over an *author-declared* proposition set while the entry body carries additional material factual claims that are mapped nowhere. The structural counter can verify bindings only for propositions the entry itself declares (count ≥4, row/pin/quote ≤25 words/rationale per declaration, index presence); it has no mechanical way to enumerate "material factual propositions" out of free prose, so any mechanistic claim stated outside the declared map is invisible. An entry can therefore pass every counter-side check while asserting a false, unmapped fact in body prose.
- **Reproducible setup/command** (all work under the seat scratch root, cleaned after receipt capture; rebuild anywhere):
  1. `python3 .ufo/waves/round-52/w1/Falsify38/build_fixture.py` — creates a two-commit fixture repo (`base` = registry + README + round-52 fetch pins, entry absent; `data` = adds `corpus/knowledge/hyprland-dispatcher-execution-r52.md` with 4 fully bound propositions P1–P4 plus a fabricated unmapped claim at entry lines 32–34: "the dispatcher table is rehashed every sixty seconds to keep the press path latency flat"). Registry rows S370–S373 are `status=mined`, `opened=2026-10-27`; pin bytes are copied read-only from the lane's round-51 pins (Hyprland @ `efb50993`).
  2. `python3 .ufo/waves/round-52/w1/Falsify38/check.py --repo <fixture> --rev <base> --base <base>` → `verdict=TARGET_MISSED` exit 1 (no-work control behaves).
  3. `python3 .ufo/waves/round-52/w1/Falsify38/check.py --repo <fixture> --rev <data> --base <base>` → `a ok=1`, `b ok=1 propositions=4 bound=P1,P2,P3,P4`, `verdict=TARGET_MET` exit 0 — with the smuggled false claim still in the body. The real pin contains no rehash logic (`grep -ciE 'rehash' .ufo/waves/round-51/fetch/Hyprland-KeybindManager.cpp` → `0`), so the unmapped claim is not merely unmapped but false.
  4. Negative control: break P2's quote (`m_dispatchers.find(DISPATCHSTR)` → `...NONEXISTENT...`) and re-run → `b ok=0 ... notes=P2=quote_not_at_pin`, `verdict=TARGET_MISSED` exit 1, confirming the checker discriminates declared bindings and the bypass is specific to the completeness direction, not a vacuous checker.
- **Actual result:** reproduced by executed fixture runs, captured in `receipt-base.txt`, `receipt-bypass.txt`, `receipt-mutant.txt`. **Reproduced: yes.**
- **House-exemplar surface:** the template pattern already exhibits the asymmetry. In the round-51 exemplar entry, the r51 counter's clause (b) binds only the 6 `source:`-line rows, while the entry body carries 79 pin-locator citations and ~102 prose sentences ≥5 words outside those lines (`grep -cE '^\s*source\s*:' corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` → `6`; `grep -oE '\((Hyprland|wiki)[A-Za-z0-9._-]+:[0-9]+' corpus/knowledge/hyprland-dispatcher-dispatch-r51.md | wc -l` → `79`; sentence count via `python3` split → `102`). Row/pin/quote binding has never covered body-granular claims; an r52 counter that scores only the declared proposition map inherits the gap.
- **Distinction from Falsify30:** Falsify30 attacked *line*-granularity inside the r51 counter's existing `bind_row`/`clause_b` acceptance path (one matching quote on an S-row line marks the row verified; other propositions on that same line are unexamined) — inspection-only. This seat attacks the *declared-set* completeness direction end-to-end: an executable fixture proves `TARGET_MET` is reachable while a false material claim sits entirely outside the declared map, with both the no-work control and a binding-broken mutant correctly failing. The two failure modes compose; neither subsumes the other.

## Source evidence

- `.ufo/waves/round-52/claims-frozen.md` and `.ufo/waves/round-52/registration.md`: frozen C2 predicate and counter-check assignment (local repository evidence).
- `quality/counters/c2-r51-dispatch-entry.py:405-424` (`clause_b` scores only rows collected from `SRC_RE` lines), `:329-375` (`bind_row` verifies a quote at a locator, nothing about proposition coverage of body prose) — the structural template any r52 counter will iterate from (local repository evidence).
- `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:14-19` (6 `source:` rows) vs body steps/chain (79 located citations, ~102 sentences): measured smuggle surface (local repository evidence).
- Fixture pins: `.ufo/waves/round-51/fetch/Hyprland-KeybindManager.cpp:785`, `:42`, `:112-113`; `Hyprland-HyprCtl.cpp:1149`; `Hyprland-legacy-DispatcherTranslator.cpp:32`; `Hyprland-SharedDefs.hpp:53` — the real quoted lines used by P1–P4 (source: Hyprland @ `efb50993780079460b0cbed1363e2166a2de1d9f`, already-opened round-51 rows S364–S366/S369; accessed 2026-10-27, locally pinned bytes, no fetch).
- No external source candidate opened; no URL access beyond the already-held pinned bytes.

## Affected axes

- **Coverage: at risk.** "Proposition count, row/pin/quote bindings and index" can all hold while a material factual proposition in the entry is unmapped and false. The frozen completeness clause is therefore not enforced by the assigned counter-side checks; it rests entirely on the outside source-truth reviewer noticing the smuggled claim.
- **Operability: no demonstrated harm.** The attack is source-only and adds no runtime, producer, or package dependency.

## Limitations / dissent

- The frozen predicate explicitly assigns source truth to an outside reviewer; this attack shows the counter alone does not enforce "every material factual proposition is mapped", not that a truthful entry cannot be written nor that the outside review must fail.
- The completeness gap is a fixable defect of check design, not grounds to reject the claim: the smallest safe correction is to require the entry to confine all mechanistic claims to the declared proposition map (e.g. body-prose scan rejecting sentences that assert mechanism — verbs/identifiers from the pinned sources — outside mapped propositions, or an explicit "no unmapped mechanism claims" section verified by the counter), plus reviewer spot-check of body prose, not only of the map. Sentence→proposition assignment is semantic, so the correction bounds the surface rather than proving completeness.
- No frozen claim or predicate was edited; no tracked lane file was touched. Report dissent: none beyond the above.

## Verification and safety

- Executed: fixture build, base-control run, bypass run, mutant run — commands and outputs preserved in the seat-dir receipts.
- Safety: source-only; no package queries, live reads, process/compositor probes, input capture, screenshots, or producer execution; lane repo read-only except the seat dir and this report; scratch confined to `/fast/scratch/hyaku/mado-r52/Falsify38/` and removed after receipt capture; no installs (no tooling needed).
- Checks main agent should run: re-run the three receipt commands from the seat dir against a rebuilt fixture; confirm the smuggled sentence at fixture entry lines 32–34 has no row/pin/quote/rationale binding; decide whether the completeness clause needs the bounded correction above before scoring C2.

## Report

- `.ufo/waves/round-52/w1/Falsify38.md`
