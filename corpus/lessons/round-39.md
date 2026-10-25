# Lessons — mado, round 39

Round intent: registration `.ufo/waves/round-39/registration.md` (attempt-1 freeze `457d1b1`)
and its attempt-2 addendum `.ufo/waves/round-39/registration-a2.md` (freeze `d9b4e4a`, before
any C2/C3 data). C1 re-registers the repaired round-38 discrimination pair (calibration); C2
lands `tools/mado-options.py`, the config-option ownership table (operability, capability);
C3 admits `corpus/knowledge/config-option-table-r39.md` (coverage, sourced). One v2 wave
`w1` of 64 seats ran under attempt 1; attempt 2 (L1 `MadoR39a2`) integrated it.

## Gate

GATE S218 receipt=.ufo/waves/round-39/fetch/S218.bin sha256=218da390ac96bc9452090eaf74f36f7e5f61897502b22c201fc875ea82c2a0f8 quote="Options can be specified only once (if you do it more times, the previous one will be overwritten)"
GATE S219 receipt=.ufo/waves/round-39/fetch/S219.receipt.txt sha256=c15e4034200badeb275c10fd70645b1d00761f65d9477ae82e49655d7be9fe04 quote="rows=70 owner files=6 layers defaults=57 user=7 toggles=4 theme=2"
GATE S220 receipt=.ufo/waves/round-39/fetch/S220.bin sha256=0740a0c47416623ff822c69033a25db5314ee2a0eb8fc2a41fc70af77b2a603d quote="Meaning lines above the source = will be parsed first, then lines inside ~/.config/hypr/myColors.conf, then lines below."
GATE S196 receipt=.ufo/waves/round-39/fetch/S196-r39.bin sha256=f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2 quote="Their purpose is to be fed into hl.bind() or hl.dispatch()."
GATE S018 receipt=.ufo/waves/round-39/fetch/S018-r39.bin sha256=798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa quote="const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);"
GATE S162 receipt=.ufo/waves/round-39/fetch/S162-r39.bin sha256=9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b quote="m_config->registerHandler(&::handleBind, "bind", {true});"
GATE S173 receipt=.ufo/waves/round-39/fetch/S173-r39.bin sha256=fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e quote="avoid cases where a category is called the same as a handler"

Every source above was opened by the L1 on 2026-10-25 (17:01 -03, `curl -sSL`, HTTP 200
each). URLs: S218 `https://wiki.hypr.land/0.56.0/Hypr-Ecosystem/hyprlang/` (`### Line Style`);
S220 `https://wiki.hypr.land/0.54.0/Configuring/Keywords/` (`## Sourcing (multi-file)`); S196
`https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/` (`#dispatchers`); S018, S162 at
Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` (`src/debug/HyprCtl.cpp:1149`,
`src/config/legacy/ConfigManager.cpp:607`); S173 hyprlang `v0.6.8` `src/config.cpp:869`. S219 is
own-work: its receipt names the tool's sha256 at `4ec582e`. S218 and S220 quotes are located
in tag-stripped, entity-decoded text (S220's page writes "it’s" with a curly apostrophe; the
quote starts after it). S196, S018, S162 and S173 re-opened byte-identical to their held
receipts (same sha256), so their held anchors stand.

Row changes (old → new):
- S218, S219, S220: new, `mined`, opened 2026-10-25, recheck on-release / on-change /
  on-release, used-by `corpus/knowledge/config-option-table-r39.md`.
- S018 used-by: `corpus/knowledge/window-rule-effects-getprop.md` → `…getprop.md,
  corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` (the amendment cites it).
- S162 used-by: `rule-attribution-r24.md, bind-table-r25.md, animation-table-r26.md,
  workspace-rules-r27.md` → the same + `config-option-table-r39.md`.
- S173 used-by: `tools/mado-binds.py` → `tools/mado-binds.py,
  corpus/knowledge/config-option-table-r39.md`.
- S196: re-opened, no cell changed.

Refused candidate rows this round:
- **0.56.0 Variables page as S218** (`https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/`,
  sha256 `400d1819…2801`, seats ExecAssimFetches/ScrLesson): its quote ("You are allowed
  multiple hl.config() invocations …") documents the Lua `hl.config()` surface; the host
  parses a hyprlang `.conf` tree, and the page itself points hyprlang readers to the 0.54
  pages. Era fence (QUALITY 15/16). Flip: the host moves to a Lua config.
- **0.56.0 Dispatchers page as a new S220** (registration.md's assignment): the URL is held
  as S196 with byte-identical bytes; a second row is a within-scope duplicate URL. Cited
  as S196 instead. Flip: none — the held row serves.

### Assimilation ledger — shokuknow `merge/mado/` (read-only)

Theme: dispatcher surface and request-socket resolution. **Admitted (re-grounded):** the
package's amendment to `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`,
appended as a dated section citing S018 and S196 re-opened this round; the package's text,
dates and quotes are not cited. **Refused:** the package's other amendments
(`dispatcher-semantics-r25.md`, `ipc-contract-r25.md`, `waybar-module-text-route-r25.md`)
— not this round's theme, stay unassimilated (flip: a later round takes that theme); and
the four package entries refused in round 38 stay refused with their round-38 reasons
(`corpus/lessons/round-38.md` assimilation ledger; seat RevAssim re-checked them).
No staged `SOURCES.append.md` row was appended: the amendment cites held rows only.

Id collision check (`.ufo/waves/round-39/assimilation/`, the §10 0–3-space pattern, run
after this round's rows): reg-ids 214, staged-ids 147, collisions 22 —
S203–S221, S253, S258, S277 (held ids the package also stages; no append, so no renumber
map). Guard proof: a scratch registry row `  | S002 |` against a staged `S002` gives
`collisions` = S002 (`assimilation/guard/`).

Quarantine slice (register under shokuknow, mado data rows: 13; `assimilation/quarantine-slice`),
hand-checked by seat ExecQuarantineSlice and spot-checked by the L1 (S189, S199/S200, S224):
present — S189 (`EventManager.cpp:128` `eventString = std::format`, re-fetched by the L1),
S195, S201, S205, S228; absent, refused (fabrication class) — S224 (the cited timestamp is
not in `~/.cache/ai-usage/status.json`, L1 grep count 0; the telemetry file rotated);
unreachable, unverifiable — S199, S200 (CSDN answers HTTP 521, L1 re-check 521); no locator,
unverifiable — S209, S222, S223, S225, S235. Adoption from the register stays closed.

### considerthese

`considerthese/2026-10-24.md` proposal 4 (the config-option table — who owns each key,
checked against `getoption`) is mined: C2 and C3. `considerthese/2026-10-25.md` proposal 3
(watch M37-5 by name) is served by C1's re-registration.

### Spot-check of the round-38 non-author closure (`round-38-verifier-spotcheck.md`)

Routed items: C1 re-registration (this round's C1); the refuted addendum-5 sentence of the
fleet round-38 report (erratum in the round-39 report, text from seat ScrErratum); the
eventq receipt regenerated census-only (`.ufo/waves/round-39/w1/ExecEventqSnapshot/`,
socket2 rows and subscriber peers only); the inherited round-38 seat reports (committed in
`457d1b1`); SCORECARD "2 refused" → 3 (corrected in the round-39 SCORECARD section).

## Mistakes

**M39-1 — a registration named counters as predicates that its freeze commit did not hold.**
Class: unfrozen predicate. Evidence: `.ufo/waves/round-39/c3/freeze-counter-check.txt`
(freeze `457d1b1`: `MISSING quality/counters/c3-r39-options.py`,
`MISSING quality/counters/c4-r39-options-entry.py`, missing=2); the C2 draft a seat wrote
after dispatch could not reach TARGET_MET for any tool (`w1/CritC2Control.md`,
`w1/RevC2Counter.md`; clause f is `not tool_present` inside `all()`); the C3 counter never
existed (`w1/CritC3Control.md`). Captured-by: QUALITY criteria 49 and 61 (smoke-run every
named command at the freeze) — present, not applied. Fix: criterion 64 (a pre-dispatch
command over the registration's counter paths, receipt committed with the freeze); shown
able to fail — missing=2 at `457d1b1`, missing=0 at `d9b4e4a`.

**M39-2 — exact-keyword exclusion let handler calls into the option table.** Class:
parser boundary. Evidence: `.ufo/waves/round-39/c2/real-tree-diff.txt` — on the host tree
the wave-built tool (`cee78d99…`, selftest 69/69) listed `binddr`, `bindeld`, `bindld`,
`bindmd` and five `windowrule:*` fields as options (79 rows; 70 are options). Found
independently by seat SctHeldEntries (§3.1) and the L1. Captured-by: none — the selftest
had no flag-variant or keyed-block case, though `knowledge/bind-table-r25.md` already held
that `bind` takes flags. Fix: exclusion grounded in S162/S173 (allow-flags handlers, keyed
special categories) with two selftest assertions; each one-line mutant fails 69/71
(`c2/selftest-mutA.txt`, `c2/selftest-mutB.txt`), and the counter's generated trees carry
the distractors (the wave-built tool scores `fixtures=1/11`, `c2/ctl-wave-v1.txt`).

Misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`, 2026-10-25): one
untracked path, `.ufo/waves/round-30/wave1/ScribeLesson.md`, written by another lane's
round-30 seat (no mado mention) — not this round's; nothing moved.
