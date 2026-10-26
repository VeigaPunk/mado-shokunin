# ConnCrossClaim — round-43 w1: C1 × C2 cross-claim / cross-source matrix

Seat: ConnCrossClaim. Lane: mado-shokunin. Wave: round-43 w1. Date: 2026-10-26.
Scope: frozen registration (b2e2efd), counters PRED-C1-r42 / PRED-C2-r43, reference
`.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`, control runners, receipts, pinned receipts
S290-S299, host files. All quotes below verified by `verify-quotes.py` (seat receipt
`quotes-verified.txt`); every locator is on the **raw** pinned bytes.

## 1. Evidence base (verified)

| pin | file | verified locator | claim support |
|---|---|---|---|
| S290 | Hyprland-RegexMatchEngine.cpp | 16 `re2::RE2::FullMatch(other, *m_regex) != m_negative;`; 7-12 `negative:` prefix | anchored FullMatch |
| S291 | Hyprland-WindowRuleApplicator.cpp | 421-428 `WINDOW_RULE_EFFECT_SIZE` stores expression `static_.size`; 389-396 FLOAT/TILE set `static_.floating` | size/float effects |
| S292 | Hyprland-DefaultFloatingAlgorithm.cpp | 55-66 `if (WINDOW->m_ruleApplicator->static_.size) { ... windowGeometry.w = COMPUTED->x; ... }` (in `newTarget`); 96/102 `target->setPositionGlobal(windowGeometry)`; 116 X11-OR branch sets `m_pendingReportedSize = ...size(...GEOMETRIC_GOAL)` | floating-algorithm consumption |
| S293 | Hyprland-Target.cpp | 10-14 `ITarget::setPositionGlobal` stores `m_box`; 68-70 `rememberFloatingSize` | target storage |
| S294 | Hyprland-WindowTarget.cpp | 36-39 `CWindowTarget::setPositionGlobal` → `updatePos`; 70-74 `if (floating() && m_window && ...) m_window->setBox(m_box.logicalBox); if (CONFIGURECLIENT) m_window->sendWindowSize();` | window storage |
| S295 | Hyprland-GeometricMovableAnimated.cpp | 17-24 `size(eGeometricValueType)` → `GEOMETRIC_GOAL: m_realSize->goal()` / CURRENT: value(); 43-46 `setBox` → `*m_realSize = x.size()` | animated var goal/value |
| S296 | Hyprland-HyprCtl.cpp | 394-395 JSON template `"at": [{}, {}], "size": [{}, {}],`; **426-428 JSON args `w->position/size(...GEOMETRIC_GOAL)`**; 447-448 text format same | `hyprctl clients -j` size = goal |
| S297 | host-gkeep.conf | 2 float on, 3 center on, 4 `windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$`; byte-identical to live `~/.config/hypr/gkeep.conf` (verified `cmp`) | host rule text |
| S298 | host-clients-r43.json | 4 clients, all `mapped: true`, `floating: false`, size 1720×1414, classes Alacritty/zcode/grok-bot/chromium (raw locator: chromium record at 47-61) | host census |
| S299 | gkeep-ui-excerpt.py | 33 `window.set_default_size(420, 500)`; 6 `application_id="org.omarchy.gkeep"`; header claims ui.py lines 446-488 (end, 488 lines), full-file sha256 07a3c4a5… — all verified on disk (excerpt ≡ `sed -n '446,$p'` modulo 2-line synthetic header) | client own request |

Host-file checks (read-only): `cmp` pinned S297 ≡ live `~/.config/hypr/gkeep.conf`; ui.py sha256 matches S299 header; live C1 run receipt `live-geometry-host.txt` (L1, 2026-10-26T04:17): Hyprland 0.56.2 @ efb5099; host run `exit=3` `verdict=NO_MATCHING_CLIENT` (rules=1 float_rules=1 other=1 unsupported=0 clients=4 matched=0).

Registry: `corpus/SOURCES.md` at HEAD tops at S289 (226 rows); **S290-S299 do not exist yet** anywhere (freeze added only fetch pins; rows are added by the entry); S300+ free. So all ten receipts are NEW ids for C2 (clause c: opened 2026-10-26, etc.).

## 2. Matrix: C1 contract sentences × C2 claim areas × sources

C1 sentences (frozen counter docstring + reference docstring, `ctl-ref-tool.py.txt`); C2 areas from registration's "end to end" list.

| # | C1 contract sentence | C2 claim area | pins | consistency |
|---|---|---|---|---|
| M1 | "Hyprland 0.56.2 consumes a window rule `size W H` when a floating window opens (the floating algorithm reads the rule's size and stores it as the window's box); a tiled window never reads it" (ref 4-6) | floating algorithm; target/window storage; size effect | S292:55-66; S291:421-428; S293:10-14; S294:70-74; version: live receipt | CONS — `static_.size` has **exactly one consumer across all seven pins** (grep `static_.size` → only DefaultFloatingAlgorithm.cpp:55,58), in `CDefaultFloatingAlgorithm::newTarget` (floating algorithm). "TILED" verdict semantics = this fact |
| M2 | "A client MATCHES a rule … `re.fullmatch(REGEX, class)` succeeds (Hyprland: `RE2::FullMatch`)" (counter 38-39; ref 40) | RE2 FullMatch | S290:16 | CONS — both anchored; C1 restricts the regex alphabet (counter residual: Python `re` ≠ RE2; alphabet restricted to where they agree). Same RX `^(org.omarchy.gkeep)$` used by C1 selftest and by C2 clause h parser |
| M3 | rule-line grammar: `windowrule[ \t]*=(.*)`; effect = first token of field 0; `size`/`float` supported; every other line incl. `windowrulev2` counts nowhere (counter 26-37) | host rule text (S297) | S297:2-4; (no Hyprland source pinned) | CONS for the host's rules — **grammar itself is unpinned** (see §4): C1 asserts it without a Hyprland primary source; C2 only needs the host's own text |
| M4 | clients: skip `mapped` false; `floating` true only JSON true; `size` = list of exactly two ints ≥ 0 else none (counter 41-48) | host census; animated var | S296:426-428 (int args); S298:49 (mapped true) | CONS — HyprCtl emits `sc<int>(...)` (always ints); host clients all mapped |
| M5 | last matching size rule ⇒ want; last float ⇒ float_rule; verdicts BADSIZE/TILED/AGREE/DIFFER (counter 45-48) | size/float effects | S291:389-396,421-428; S292:55-66 | CONS — last-wins matches applicator overwrite semantics (`static_.size = expr`), FLOAT sets `static_.floating`, TILE inverts |
| M6 | output: per-rule/per-client lines; V order NO_SIZE_RULES/DIFFER/NO_MATCHING_CLIENT/OK; DIFFER is a report, not a fault (user resize/compositor clamp) (counter 50-56, ref 57-58) | — | S296 (JSON keys) | CONS — DIFFER's meaning is the C1-side interpretation of M1/M8 |
| M7 | example: `hyprctl clients -j \| mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf` | host census | S297; S298; live receipt | **CROSS-CORROBORATION** — the live host run of the exact example yields `clients=4 matched=0 verdict=NO_MATCHING_CLIENT exit=3`, which is exactly C2 clause h's recomputed census (total=4 floating=0 gkeep=0). C1's live run and C2's census line agree by independent routes |
| M8 | (implicit data meaning) the `size` field compared is what HyprCtl emits | animated variable behind `hyprctl clients -j` size = GEOMETRIC_GOAL (not current value) | S296:427-428; S295:17-24 | CONS — C1 consumes exactly what C2 explains. Subtlety: since the reported size is the **goal**, a mid-animation differ is expected; C1's DIFFER/residual "user may have resized" absorbs this. No contradiction |
| M9 | C2: client's own request `set_default_size(420, 500)`, `application_id="org.omarchy.gkeep"`; rule size == request size, ID fully matches RX (clause h(3)) | S299:33,6; S297:4; S290:16 | CONS — 420×500 = 420×500; `org.omarchy.gkeep` matches `^(org.omarchy.gkeep)$` |

C1's own `--selftest` mirrors the host rule exactly: ref 267 `gk = "windowrule = float on, match:class ^(org.omarchy.gkeep)$\nwindowrule = size 420 500, match:class ^(org.omarchy.gkeep)$\n"` — same digits 420/500, same RX (host adds `center on`; C1 counts center as `other`, and the live run shows `other=1` — consistent with host-gkeep.conf line 3).

## 3. Findings

**(1) A C1 contract sentence resting on a source fact C2 will state — dependence consistent in both directions.**
`M2/M8` are the pair. C1's match model (M2) rests on "Hyprland matches rules with `RE2::FullMatch`" — C2 states exactly that from S290:16. C1's input data (M8) is "the size `hyprctl clients -j` reports", which C2 explains as the animation GOAL from S296:427-428. Both directions consistent: C2's pinned facts do not contradict anything C1 asserts; C1's model does not require anything C2 would deny. Dependence is **one-way** (C1 inherits compositor facts; C2 produces their pins) — no circularity, no shared scoring surface (C1 never reads C2 files; C2 never runs C1's tool; §5).

**(2) Facts one claim needs that the other contradicts — none found.** Checked candidates and why not:
- "size rule applies to every window" vs TILED/float-only: the only `static_.size` consumer in all pins is the floating algorithm (S292:55) → no contradiction.
- "size is two ints" vs HyprCtl `sc<int>`: always ints → consistent.
- `negative:` prefix (S290:7-12): C1's alphabet rejects `:` so such rules are `unsupported`, never evaluated; C2 documents the prefix. No overlap → no contradiction.
- `windowrulev2`: C1 deliberately ignores; C2's scope is the host's `windowrule` lines → no contradiction.
- "no gkeep window open": C2 census gkeep=0 ⇔ C1 live run `matched=0` → agreed.
- C1 `other` counts `center`; C2 includes `center=on` in the census line → agreed.

**(3) A source that would strengthen both and is not yet pinned.**
1. **Hyprland `src/config/ConfigManager.cpp`** (windowrule parsing: line grammar, effect tokens, `match:class` field, `windowrulev2` existence). This is the primary source for C1's M3 grammar (currently an unpinned assumption — the only C1 contract claim with no pinned Hyprland source) and it anchors C2's "host rule text → effects" chain beyond own-work S297. Would strengthen both; needs a new id S300+ and an L1 fetch (out of seat reach; a recommendation, not actionable here).
2. **Oracle observation**: a `hyprctl clients -j` dump taken while the host's gkeep window is actually open (floating, 420×500). It would give C1 a live AGREE case (today the host run is `NO_MATCHING_CLIENT`) and verify C2's whole chain end-to-end (rule → floating → box → goal → census). Registration's C1 residual explicitly reserves it ("an oracle observation, if the wave obtains one, is reported, not scored"). Seats cannot produce it (no host mutation/spawn/input injection); it remains the cheapest *shared* falsification probe for w2.
3. Optional: full `ui.py` pin (vs excerpt S299) and the RE2 wrapper (`src/misc/Regex.cpp`?) if it exists — marginal, grows trust root; not recommended.

**(4) Separability — delete the tool ⇒ C2 still 1/1; delete the entry ⇒ C1 still 37/37.**
Static (counters read): `c1-r42-geometry.py` contains zero references to `corpus/`, `knowledge`, `SOURCES`, registry, lesson or the entry (grep empty); its only inputs are `git show <rev|base>:tools/mado-geometry.py` (or `--tool` bytes), the sandbox and generated fixtures. `c2-r43-gkeep-entry.py` contains exactly one C1 token — the residual sentence line 86 "C2 does not depend on C1's tool"; its inputs are entry, README index, lesson, `corpus/SOURCES.md` registry, fetch pins. ⇒ neither scoring path touches the other side's artifact.
Empirical (run in scratch):
- C1 with the reference via `--tool`, `--rev a35cfdf…`, nonce 42aa42aa…: **`fixtures=37/37 tool=present verdict=TARGET_MET`** (seat receipt `c1-ref-run.txt`) — C1's target is reached with the entry absent (it does not exist anywhere yet) and with no C2 artifact present.
- C2 control P, real scorer (frozen counter): **`admitted=1/1 verdict=TARGET_MET`** (seat receipt `c2-control-p-real.txt`) — C2's target is reached while `tools/mado-geometry.py` is absent (untracked; not in any rev).
⇒ deleting either artifact leaves the other scoring at target; the kill rules are unaffected. Note: C1's *real* score still awaits the tool being committed at the data commit (a C1-side dependency, not separability).

## 4. Risks / recommendations

- **Quote-binding gap for the GOAL claim.** Control P's pinned quote for S296 is `"size": [{}, {}],` (line 395, the JSON template) and for S295 is `*m_realSize = x.size();` (line 45, setBox). Neither quote alone supports "reported size = GEOMETRIC_GOAL". If the entry asserts that claim it should quote S296 content that contains the actual call — a viable word-bounded ≥3-word quote is `sc<int>(w->position(Desktop::View::IGeometric::GEOMETRIC_GOAL).x), sc<int>(w->position(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x),` (3 words, starts at raw line 426; verified), or S295 lines 17-24 (`case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();`). Clause g binds the sentence to the quote; pick the quote that actually says the thing.
- **"Only floating" exclusivity is not quoteable from S292 alone.** `windowGeometry.w = COMPUTED->x;` proves consumption, not exclusivity; exclusivity is established by the grep over all pins (one consumer). The entry should word it as "in the default floating algorithm (`newTarget`)" rather than an absolute, or keep M1's wording.
- **C1's grammar (M3) is the least-sourced contract claim.** If w2 wants a hole, ConfigManager is the target; likewise it is the top shared strengthening pin (§3.1).
- **Live host run is a shared observable.** `live-geometry-host.txt` is both C1's example output and an independent confirmation of C2's census; w2 falsifiers can reuse it as a cross-check baseline.

## 5. Tooling / method notes
- No tools installed (existing python3/git/bwrap used; no pacman, no -Sy/-Syu, no host mutation, no compositor writes; `hyprctl` not invoked by this seat — host facts taken from the L1 receipts).
- Empirical runs: `python3 -I quality/counters/c1-r42-geometry.py --repo . --rev a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f --tool .ufo/waves/round-42/c1/ctl-ref-tool.py.txt --nonce 42aa42aa42aa42aa` (C1R42_TMP=scratch); C2 control P real via `run-c2-control-p.py` (imports `run-c2-controls.py`, `score(base, admitted(), "real")`), TMPDIR=scratch.
- Scratch `/fast/scratch/hyaku/mado-r43/ConnCrossClaim` removed after completion; all cited receipts copied into this seat dir.
