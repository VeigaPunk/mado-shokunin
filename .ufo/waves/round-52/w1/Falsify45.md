# Falsify45 — C2 source proposition entailment

## Deliverables
- `Falsify45.md` — scoped falsification report (this file).

## Findings
- **Attacked item/predicate:** C2 proposition-to-source entailment: each material factual proposition must be mapped to a pinned exact quote with explicit support rationale (claims-frozen.md §C2; registration.md §Frozen predicates).
- **Hypothesized bypass:** a correctly pinned, short quote on a source row is accepted even if the associated factual proposition says something unrelated or contradicted. This targets entailment, not path/quote binding.
## Probe

- **Detector under test:** existing C2-r51 `bind_row` acceptance function, which checks row/pin/line/quote binding, not proposition entailment. It is a bounded proxy for the exact gap being attacked, not the new round-52 counter or a full claim-level detector.
- **Fixture/source candidate:** preserved receipt `Falsify45/proposition-pristine.txt`; the synthetic pin text mirrors the actual pinned `Hyprland-KeybindManager.cpp:113` from `.ufo/waves/round-51/fetch/Hyprland-KeybindManager.cpp`. Source URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp`; locally accessed from the prior-round fetch on 2026-10-27, not fetched upstream this round. Located quote: `m_dispatchers[name] = [n = std::string(name)](std::string args)` (under 25 words); the entry describes closure registration.
- **Reproducible command:** run from any directory; this repeats the pristine case using the preserved receipt. The same `bind_row` call was used for pristine, mutated, and restored bytes.
  `PYTHONDONTWRITEBYTECODE=1 python3 -c 'import importlib.util,pathlib; p="/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r51-dispatch-entry.py"; s=importlib.util.spec_from_file_location("c",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); line=pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/Falsify45/proposition-pristine.txt").read_text().strip(); man={"Hyprland-KeybindManager.cpp":{"row":"S364","file":"src/managers/KeybindManager.cpp"}}; pin=("x\\n"*112+"m_dispatchers[name] = [n = std::string(name)](std::string args)").encode(); print(m.bind_row("S364",[line],man,{"Hyprland-KeybindManager.cpp"},lambda _:pin))'`
- **Actual outputs:** pristine: `(('Hyprland-KeybindManager.cpp', 113, 113, 'm_dispatchers[name] = [n = std::string(name)](std::string args)', 'The table maps each name to its own distinct dispatcher implementation. `m_dispatchers[name] = [n = std::string(name)](std::string args)` (Hyprland-KeybindManager.cpp:113)'), '')`; mutated: same success tuple with proposition `The table deletes every dispatcher entry before a key press.`; restored: same output as pristine. The initial one-line synthetic pin returned `(None, 'pin_line_out_of_range:Hyprland-KeybindManager.cpp:113')`; after expanding to 113 lines, pristine/mutated/restored all returned success.
- **Mutation and verdict:** changed only the proposition sentence, preserving row, exact quote, locator, and pin. The detector **survived** this false proposition (coverage finding; proposition-level entailment not detected). Pristine/restored fixture SHA-256: `92decb66ee54a19f140432abde7e54a9142c46ef4582abb94d766563b2fee2b0`; mutated fixture SHA-256: `87478dc8ec15af58fb8766d5e18696e5b13c9dcba1cc16e938f8a6ef0b335c5a`. Pristine and scratch copy of the checker both had SHA-256 `ebe39e1183375e0fb102124057eafecc9a21bdfc330c04ceb03759093d10e6dd`; no checker bytes were mutated. Restored fixture bytes match pristine hash.
- **Limitations:** the probe directly exercises the existing row-binding helper with a synthetic manifest/pin loader; it does not execute the legacy counter end-to-end, does not test a round-52 draft counter, and does not establish upstream semantic truth. The older checker is a diagnostic baseline only. No source URL was fetched in this source-only pass.

## Report

Report: `.ufo/waves/round-52/w1/Falsify45.md`
