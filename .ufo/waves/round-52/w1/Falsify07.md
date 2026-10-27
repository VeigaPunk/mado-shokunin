# Falsify07 — C2 held-ground novelty

## Attack

Attacked predicate: C2's requirement for a “distinct Hyprland dispatcher-execution mechanism” and registration's no-work check that the separate target slug is absent at base. The concrete failure mode is slug-only novelty: a new slug can wrap a paraphrase of an existing mechanism and still be absent at base. That absence establishes a new identifier, not a distinct mechanism.

The base entry already directly covers dispatcher lookup/call from the keypress path and explicitly says the socket request enters “the same table” (round-51 corpus entry, sections 1, 3, 8). In particular its S364/S366 source coverage includes `m_dispatchers.find(...)` for both paths. A candidate reusing that mechanism under a new slug would not be novel merely because the slug is new. See the seat-local adversarial fixture.

## Reproduction and result

Read-only setup/commands:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
git rev-parse HEAD
git status --porcelain
cat .ufo/waves/round-52/receipts/c2-base.txt
```

Observed: HEAD was `85d57a818c3707397e21c840b6498b105ba798aa`; checkout had only untracked `.ufo/waves/round-52/` campaign data. The receipt reports the old target slug `knowledge/hyprland-dispatcher-dispatch-r51.md` present and its old checker admits it; registration explicitly says that receipt is not trusted for the new C2 target and calls for a separate slug absent at base. No round-52 candidate or new counter was present in this checkout, so no actual checker pass/fail was reproduced. **Reproduced: predicate-level bypass, yes; actual new-counter bypass, no (counter/candidate unavailable).** Fixture: `Falsify07/novelty-fixture.md`.

The cited base entry itself records this source URL and exact located quote (checked locally; source URL was not fetched in this source-only assignment): Hyprland `KeybindManager.cpp`, `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp`, quote `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);` (entry cites line 785). Its HyprCtl source URL is `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp`; quote `m_dispatchers.find(DISPATCHSTR)` (entry cites line 1149). Base entry's `verified-at` date: 2026-10-27. No external source candidate was opened/fetched by this seat.

## Limitations / residual risk

This demonstrates the insufficiency of slug absence as a novelty measure, not that the future C2 deliverable actually uses this bypass. Whether an independently judged, properly bounded entry distinguishes a genuinely different dispatcher-execution mechanism remains untested. Semantic novelty cannot be established from slug/pin binding alone; the frozen claim's outside source-truth review is relevant. No repo files outside the permitted report and seat directory were changed; no scratch artifacts were created.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify07/novelty-fixture.md`
- `.ufo/waves/round-52/w1/Falsify07.md`

Report: `.ufo/waves/round-52/w1/Falsify07.md`
