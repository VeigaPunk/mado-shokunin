# Scout — C1 new-ground check: what the lane already claims about rules / getprop / attribution

Status: scoped reconnaissance only. No lane file edited except this report. No upstream URL opened, so no
`fetch/w1` receipt belongs to this seat. No installs or updates. Read-only git verb (`rev-parse`) only.
Lane tip at read time: `464a024`.

Question answered: what does the lane already claim about Hyprland rules, `getprop` and rule *attribution*
(path:line), and which questions does the frontier still name — so that a new
`corpus/knowledge/rule-attribution-r24.md` adds ground instead of restating it.

## Files read

| Path | Range read |
|---|---|
| `corpus/knowledge/window-rule-effects-getprop.md` | whole (154 L) |
| `corpus/knowledge/keybind-rule-semantics.md` | `:1-38`, `:160-315` (window-rule sections, recipes, unknowns) |
| `corpus/knowledge/hyprland-config-era-r12.md` | `:1-78`, `:90-140` |
| `corpus/README.md` | whole (195 L) |
| `corpus/knowledge/hyprland-config-plane.md` | `:97-110` (rule inventory) |
| `corpus/knowledge/arc-synthesis.md` | `:290-307` (§6 gap ledger) |
| `corpus/knowledge/config-health-report-r3.md` | `:444-455` (carried unknowns) |
| `corpus/knowledge/hyprctl-verification-layer.md` | `:245-258` (declarer-attribution unknown) |
| `corpus/SOURCES.md` | header `:9-12`; rows S016–S020 `:28-32`; S045 row `:57`; paths `:166-170`; search log `:212-244`; leads `:366-380` (grep windows) |
| `SKILL.md` | `:368-377` ("Did my window rule apply?" row) |
| `LOG.md` | `:710-718` (round-12 gate note) |
| `SCORECARD.md` | `:1540-1550` (round-24 planned line) |
| `.ufo/waves/round-13/w1/HistoricalRecon.md` | `:148-156` (rule-attribution section) |

Sweeps and their output are in §5. `[OBS]` = read directly from these bytes; `[INF]` = composite inference
from the read parts; `[UNK]` = not established by anything read here.

---

## §1 Restatement ledger — every rule/getprop/attribution claim the lane already makes

### 1.1 `corpus/knowledge/window-rule-effects-getprop.md` (MADO-R12-1, round 12)

| Line(s) | Already-claimed content | Class |
|---|---|---|
| `:3-6` | Source list: S016 hyprctl wiki, S017 Window Rules wiki, S018 `src/debug/HyprCtl.cpp` lines 1463-1645 at `efb5099…`, S019 host captures, S020 host rule files; `verified-at: 2026-10-19`, `covers: U1` | `[OBS]` |
| `:10` | Host Hyprland 0.56.2 / tag `v0.56.2` / commit `efb5099…` | `[OBS]` |
| `:12` | `hyprctl --help` lists `getprop … → Gets a window property` and `workspacerules → Lists all workspace rules`; `getprop <regex> <property>` form | `[OBS]` |
| `:14` | Measured Alacritty `opacity 0.97`, `opacity_inactive 0.9`, `opacity_fullscreen 1`, `opacity_override false` | `[OBS]` |
| `:16` | Global `decoration:active_opacity` / `inactive_opacity` = `1.000000`, `set: false` | `[OBS]` |
| `:18` | **"effect-read, not match-read"**: the value agrees with declared effects, but the command does not report which rule supplied it; matching-rule identity `[UNK]` | `[INF]` |
| `:24-25` | `getprop` is a window-property read; `workspacerules` is separate; missing selector/property → `not enough args` | `[OBS]` |
| `:26` | Bare `Alacritty` selector → `window not found`; `class:Alacritty` and address → `0.97` | `[OBS]` |
| `:27-28` | Per-window opacity field values as above; global options `1.000000`/`set:false` | `[OBS]` |
| `:29` | Host declares `opacity 0.97 0.9` for `match:tag terminal`, tag assigned to `(Alacritty|kitty|com.mitchellh.ghostty|foot)` | `[OBS]` |
| `:30` | Host also declares `opacity 0.97 0.9` for `match:tag default-opacity` after sourcing app rules | `[OBS]` |
| `:31` | `workspacerules -j` returned `[]` at capture | `[OBS]` |
| `:32` | Unknown property → `prop not found`; nonexistent class → `window not found` | `[OBS]` |
| `:33` | Handler resolves with `query().selector(WINREGEX).runWindow()`; opacity read through `m_ruleApplicator` alpha getters (`HyprCtl.cpp#L1463-L1475`, `#L1492-L1504`, `#L1565-L1575`) | `[OBS]` |
| `:34` | `getprop` reads an effect value; repeated `0.97 0.9` declaration prevents unique attribution | `[INF]` |
| `:35` | Wiki documents `match` fields vs effects, all-props-match, top-to-bottom effects, opacity multiplication | `[INF-docs]` |
| `:36` | Current wiki is Latest git, modified 2026-08-26; says hyprlang deprecated since 0.55 | `[INF-docs]` |
| `:37` | Which rule matched, whether another rule supplied the same opacity, and final rendered opacity are **not** established | `[UNK]` |
| `:66-76` | Table comparing declared terminal effect, declared generic effect, per-window getter, global options, fullscreen/override — with "can be compared without claiming match attribution" | `[OBS]`/`[INF]` |
| `:121-127` | Handler read path returns a selected property value or an error string; **"It does not include a rule name, matched condition, ordered match list, or rule-source attribution"** | `[OBS]` |
| `:129-132` | Corrects `arc-synthesis.md:300` ("no rule-read verb") and `config-health-report-r3.md:449`; old notes left unchanged; exec-once untouched | `[OBS]` |
| `:134-143` | Limits: one window/address/property set; clients projection omitted tags/titles; equal `0.97`/`0.9` ambiguous; no pixel alpha; current wiki is Lua-era | `[OBS]` |
| `:144-148` | **Rejected:** "`getprop` proves which window rule matched" (flip: version-pinned surface returning rule name/matched-condition record); **Rejected:** "`0.97` proves the terminal-specific rule" (flip: attribution interface or controlled isolated rule state) | `[INF]` |

### 1.2 `corpus/knowledge/keybind-rule-semantics.md` (MADO-4 / MADO-R2-2, round 2), window-rule parts

| Line(s) | Already-claimed content | Class |
|---|---|---|
| `:8` | Version pin 0.56.2, commit `efb5099…` | `[OBS]` |
| `:15-19` | Claim boundary: no keystroke injection, no dispatch, no mutation; read-only `binds`/`clients`/`getoption` | `[OBS]` |
| `:173-178` | Anonymous `windowrule = [effects…, props…]` and named-block forms; named blocks exist 3× in plane; props/effects any order; **all props must match**; one of each `match:` type; at least one prop | `[INF-docs]`+`[OBS]` |
| `:179-180` | Era pin: `default/hypr/windows.conf:2` labels stock rules "Hyprland 0.53+ syntax" | `[OBS]` |
| `:181` | Regex is Google RE2; `negative:` negates | `[INF-docs]` |
| `:183-201` | Effective written order 1–7 through the include graph; 79 sourced rule statements = 4+69+2+4; 3 named; file sha256 prefixes | `[OBS]` order + `[INF-docs]` semantics |
| `:203-213` | Matching-order decision table: top-to-bottom order matters; **named rules first**; last match wins for effects; static vs dynamic effects; opacity is a product unless `override`; tag dynamics with `*`; only named rules live-toggleable via `hyprctl keyword 'windowrule[name]:enable false'` | `[INF-docs]` |
| `:215-221` | Props used in plane: `match:class`, `match:title`, `match:tag`, booleans; layerrules use `match:namespace` | `[OBS]`+`[INF-docs]` |
| `:222-236` | Static/dynamic effect inventory actually declared in the plane | `[OBS]` |
| `:238-250` | Worked chains (Alacritty default-opacity chain; ai-usage float chain) | `[INF]` |
| `:252-270` | **Live tag state** via `hyprctl clients -j`: 3 Alacritty windows, tags `default-opacity*` / `terminal*`; only 1 matches declared intent; `*` suffix confirmed; cause of divergence `[UNK]` | `[OBS]`/`[INF-docs]`/`[UNK]` |
| `:271-286` | Recipes: `binds -j`, reconciliation, `clients -j` tags, `getoption` values, named-rule toggle recipe marked mutating/operator-only/not run | `[OBS]` |
| `:288-302` | Unknowns: no dispatcher fired; docs drift + untested current-only props (`scrolling_width`, `allows_input`, `match:xdg_tag`); `default-opacity*` divergence cause; togglesplit behavior; **"Per-window effective values (applied opacity product, scroll factor) are not directly readable via hyprctl"** (`:299-300`); `match:tag` subtleties untested | `[UNK]` |

### 1.3 `corpus/knowledge/hyprland-config-era-r12.md` (MADO-R12-2), rule parts

| Line(s) | Already-claimed content | Class |
|---|---|---|
| `:15` | Window-rule syntax had a documented breaking rewrite at 0.53; later releases document additive fields/fixes, not a second blanket rewrite | `[INF-docs]` |
| `:21-31` | Lua is the forward surface from 0.55; hyprlang kept "1 - 2 releases"; not a calendar deadline | `[INF-docs]` |
| `:33-43` | Default file selection `.lua` over `.conf`; no merge; not a host loaded-path observation | `[INF-docs]`/`[UNK]` |
| `:51-57` | Era table: 0.53 "completely overhauled" syntax; 0.54 archive `windowrule = match:class …` + named form; 0.55 `confine_pointer`; 0.56 `stableid:`, `no_auto_hdr`, `suppress_event`; 0.56.2 `gaps_out`/`float_gaps` fix | `[INF-docs]` |
| `:59-71` | v0.54 `match:*` form vs current Lua `hl.window_rule({…})`; named rule-surface additions; no complete parser-change log | `[INF-docs]`/`[UNK]` |
| `:79-86` | Host 0.56.2, no `~/.config/hypr/*.lua`, `configProvider: hyprlang`, empty `configerrors`; loaded path `[UNK]`; empty configerrors is not a rule-effect test | `[OBS]`/`[UNK]` |
| `:99-107` | Limits: documentation-era map; one-release uncertainty; moving pages; no rule fired | `[OBS]` |
| `:109-116` | Rejected: "0.55 immediately rejects hyprlang"; "host definitely loaded hyprland.conf"; "0.56 no-breaking-changes is a behavior freeze"; "wiki Lua examples prove host supports every property" | `[INF]` |
| `:120-122` | Recheck: reopen migration notice, 0.55/0.56 notes, v0.56.2 tag, current and 0.54 pages on release/migration | — |
| `:125-140` | S030 → S017 citation mapping erratum (every historical S030 occurrence resolves to S017) | `[OBS]` |

### 1.4 `corpus/README.md` — index and frontier statements about rules

| Line(s) | Content |
|---|---|
| `:16` | Coverage-map row for `keybind-rule-semantics.md`: 192 binds; declared rule semantics; "window rules: syntax era pinned (§4.1), evaluation order …" |
| `:34` | Coverage-map row: "`hyprctl getprop` is a read-only per-window *effect* read (applied value, **no rule attribution**)" |
| `:35` | Coverage-map row: config era, 0.53 rule-syntax break, host `configProvider: hyprlang` |
| `:62` | Route row "Hyprland config, binds, rules and display"; limit cell: "Parsed declarations do not prove dispatcher behavior, rule effects or exec-once results." |
| `:83-85` | Frontier bullet: "Rendered UI, Waybar module text, Walker socket protocol, dispatcher behavior **and per-window rule effects**: [arc gap ledger] §6." |
| `:98-100` | Frontier bullet: round 12 moved per-window rule *effects*, config era, portals onto sourced ground (links to the three notes) |
| `:101-102` | Frontier bullet: "**Still open: rule *attribution***, output-management behavior, the input debugging ladder and Waybar module text — study paths and queued sources in [SOURCES]" |
| `:103-121` | Later bullets close the other three items of that sentence only to bounded documentary routes (round 14 output `:106-109`; round 15 input `:110-115`; round 16 Waybar `:116-121`), each still naming runtime behavior unmeasured |

### 1.5 Supplemental lane positions (outside the four named files)

| Line(s) | Content |
|---|---|
| `corpus/knowledge/hyprland-config-plane.md:97-110` | Declared rule inventory: local `input.conf:45-46`, `ai-usage.conf:2-5`; stock `windows.conf` L3 `suppress_event maximize, match:class .*`, L6 `tag +default-opacity`, L15 `opacity 0.97 0.9, match:tag default-opacity` |
| `corpus/knowledge/arc-synthesis.md:300` | Superseded negative: "window-rule effects / exec-once results \| no rule-read verb in Hyprland 0.56 (r2/R3-2)" (left in place; corrected by r12 note `:129-132`) |
| `corpus/knowledge/config-health-report-r3.md:449` | Superseded negative: "Whether any window rule currently matches an open window (no rule-read verb; U4, carried)." |
| `corpus/knowledge/hyprctl-verification-layer.md:251-253` | Different sense of attribution: `getoption` *declarer* attribution ("last declarer wins") with a precision caveat; 56 claim→live pairs; not rule attribution |
| `corpus/SOURCES.md:28-32` | Mined rule rows S016 (hyprctl wiki), S017 (Window Rules wiki), S018 (`HyprCtl.cpp` 1463-1645), S019 (own-work host capture), S020 (own-work host rule files); all `opened 2026-10-19`, `used-by` the getprop note |
| `corpus/SOURCES.md:168` | U1 study path: S002 → S018 → S019 → S020 → S016 → S017 (handler before docs) |
| `corpus/SOURCES.md:229` | Search-log question: "does pinned Hyprland 0.56.2 have a read-only per-window rule-effect query, and can it attribute a returned value to a rule?" |
| `corpus/SOURCES.md:57` | S045: window-rules duplicate-admission correction (S030 rejected, not a new fact) |
| `SKILL.md:372` | Answer row: "Did my window rule apply?" → "0.56.2 has an *effect* read, not a *match* read: `getprop` returns the applied value with no rule attribution"; several rules can yield the same value |
| `LOG.md:714-715` | Round-12 landing note: getprop is "an effect read without rule attribution — corrects `arc-synthesis.md:300` / `config-health-report-r3.md` … without editing them" |
| `SCORECARD.md:1546` | Planned round-24 line names "province frontier work (Walker provider behaviour or rule attribution)" |
| `.ufo/waves/round-13/w1/HistoricalRecon.md:151-156` | Wave report (not corpus): calls rule attribution "an upstream architectural limitation … No lane tool can fabricate rule attribution without upstream Hyprland modifications" — stronger than any corpus claim |

---

## §2 Open questions the frontier names

1. **`corpus/README.md:101-102`** — "Still open: rule *attribution*, output-management behavior, the input
   debugging ladder and Waybar module text — study paths and queued sources in [SOURCES]." After the
   round-14/15/16 bullets (`:103-121`), rule attribution is the only item of that sentence with **no** round
   moving it to any sourced ground. `[OBS]` (wording) / `[INF]` (the "only item" reading follows from the
   later bullets' own scope sentences).
2. **`corpus/README.md:83-85`** — the older frontier bullet still lists "per-window rule effects" among
   unresolved arc-gap-ledger surfaces. This overlaps, and is in tension with, `:98-100`, which says effects
   moved to sourced ground. `[OBS]`
3. **`corpus/README.md:62`** — route limit: "Parsed declarations do not prove dispatcher behavior, rule
   effects or exec-once results." `[OBS]`
4. **`corpus/knowledge/window-rule-effects-getprop.md`** names the question in-note: effect-vs-match
   distinction `:18`; `[UNK]` row `:37`; response-path gap `:127`; two rejected attribution claims with
   explicit flip conditions `:146-147`.
5. **`corpus/knowledge/keybind-rule-semantics.md:288-302`** — unknowns 3 (tag-divergence cause), 5
   (per-window effective values "not directly readable via hyprctl"), 6 (`match:tag` subtleties untested).
6. **`corpus/knowledge/hyprland-config-era-r12.md`** — `[UNK]` whether any unlisted parser behavior changed
   `:62`; no field-by-field 0.53–0.56 compatibility matrix `:72`; recheck triggers `:120-122`.
7. Registration `C1` (`registration.md:31-49`) restates the target: which rule produced an applied effect,
   and what upstream offers to tell.

---

## §3 Claim families already occupied — restatement traps for the new entry

Anything below is already on corpus record; a new note that repeats it adds no ground.

1. "`getprop` is an effect read, not a match read" — getprop `:18`, `:37`; SKILL `:372`; README `:34`;
   LOG `:714`.
2. "The handler response carries no rule name, matched condition, ordered match list or rule-source
   attribution" — getprop `:127`, `:146`.
3. The measured opacity example and its ambiguity (terminal tag vs default-opacity tag) — getprop `:14`,
   `:27-30`, `:34`, `:66-76`; keybind `:238-250`, `:252-270`; config-plane `:97-110`.
4. `getprop` CLI shape, selector behavior and error strings — getprop `:12`, `:24-26`, `:32`.
5. Documented rule evaluation semantics (props vs effects, all-props-match, top-to-bottom, named-first,
   last-match, static/dynamic, opacity product, tag dynamics, named-rule toggle) — getprop `:35`; keybind
   `:173-181`, `:203-213`.
6. Host rule inventory, tags and the observed `default-opacity*` divergence — keybind `:183-201`,
   `:215-236`, `:252-270`; config-plane `:97-110`.
7. Rule-syntax era history 0.53→0.56.2 and the hyprlang support window — config-era `:15`, `:21-43`,
   `:51-71`; README `:35`.
8. `getoption` *declarer* attribution (a different meaning of "attribution") — hyprctl-verification
   `:251-253`.
9. The named-rule toggle recipe as mutating/operator-only/not run — keybind `:213`, `:286`.
10. The two superseded negative claims and the fact that old notes were left unedited — getprop `:129-132`;
    arc-synthesis `:300`; R3 `:449`.

---

## §4 What the four files do **not** claim (delta orientation, observed absences)

These are absences in the read bytes, each backed by the read ranges above; they are orientation, not a
research plan, and concurrent wave-1 seats are already fetching parts of this area (see §6).

- **Rule identity structures upstream:** no corpus claim about rule names/IDs, `RuleEngine` match records,
  `WindowRule` properties, or the rule applicator's typed storage. The only pinned code span on record is
  `HyprCtl.cpp` 1463-1645 (S018). getprop `:33`, `:127` stop at the response path.
- **Layer-rule behavior/attribution:** only declared layerrule syntax (`match:namespace`, keybind `:221`) and
  the `no_anim` effect (`:235-236`) are claimed; no layer-rule effect read or attribution statement exists.
- **Tag field as an upstream-documented read:** `clients -j` tags are a host observation (keybind
  `:252-270`, S019 own-work capture); no note claims an upstream byte documents that field as
  attribution evidence.
- **The getprop property list:** the "See the wiki for a list of properties" text is quoted as host help
  output (getprop `:93`); no note pins a wiki/source list of readable properties.
- **sha256 on rule sources:** no rule-source row records a sha256 (§5). C1 v2 also demands `opened
  2026-10-23`, so S016–S020 cannot be reused as C1 rows regardless of URL form.
- **Correction coverage:** keybind `:299-300` still says per-window effective values are not directly
  readable via hyprctl; the r12 note's `Corrects` section names only arc-synthesis `:300` and R3 `:449`
  (getprop `:129-132`). The keybind sentence is thus uncorrected in corpus — a new entry should not imply
  the lane already reconciled it.
- **Wording tension:** README `:83-85` vs `:98-100` (see §2 item 2) is unresolved in the bytes.
- **Round-13 report overreach:** `.ufo/waves/round-13/w1/HistoricalRecon.md:156` claims attribution is an
  "upstream architectural limitation" and that no tool could fabricate it. The corpus only establishes that
  the inspected response path lacks attribution. A new note must not inherit the stronger claim unless its
  own bytes support it.

Map of the new-ground area already opened by concurrent wave-1 seats (receipt names under
`.ufo/waves/round-24/fetch/w1/`, not read by this seat): `SrcHyprCtl-1`, `SrcWindowRule-1..2`,
`SrcWindowRuleApplicator-1..2`, `SrcRuleEngine-1..2`, `SrcRuleBase-1..3`, `SrcMatchEngine-1..12`,
`SrcLayerRule-1..6`, `SrcEffectContainer-1..3`, `SrcWindowView-1..2`, `SrcLuaRules-1..3`,
`SrcLuaQuery-1`, `SrcLegacyConfig-1`, `WikiWindowRules-1`, `WikiHyprctl-1`, `WikiLayerRules-1..2`,
`WikiTags-1..2`, `WikiDebugging-1..3`. `[OBS]` listing only; contents not inspected here.

---

## §5 Sweeps (commands and output)

Run from `/home/vgpnk/Projects/shokunin/mado-shokunin`, all read-only.

```text
$ test -e corpus/knowledge/rule-attribution-r24.md; echo "test -e rc=$?"
test -e rc=1

$ grep -c 'rule-attribution' corpus/README.md
0

$ grep -rn -i "attribution" corpus --include='*.md' | wc -l
20

$ grep -rli -i "attribution" corpus --include='*.md' | sort
corpus/knowledge/executor-test-sufficiency.md
corpus/knowledge/gate-mutation-proof.md
corpus/knowledge/hyprctl-verification-layer.md
corpus/knowledge/province-accuracy-selfaudit.md
corpus/knowledge/window-rule-effects-getprop.md
corpus/lessons/round-12.md
corpus/lessons/round-14.md
corpus/lessons/round-18.md
corpus/lessons/round-19.md
corpus/lessons/round-19-verifier-spotcheck.md
corpus/lessons/round-22.md
corpus/README.md
corpus/SOURCES.md

$ grep -rn -i "getprop" corpus --include='*.md' | awk -F: '{print $1}' | sort | uniq -c
      1 corpus/knowledge/config-drift-r12.md
     40 corpus/knowledge/window-rule-effects-getprop.md
      5 corpus/lessons/round-12.md
      1 corpus/lessons/round-12-verifier-spotcheck.md
      1 corpus/lessons/round-13.md
      1 corpus/lessons/round-15-verifier-spotcheck.md
      2 corpus/README.md
      8 corpus/SOURCES.md

$ for id in S016 S017 S018 S019 S020; do printf '%s: ' "$id"; grep -E "^\| $id " corpus/SOURCES.md | grep -c 'sha256'; done
S016: 0
S017: 0
S018: 0
S019: 0
S020: 0
```

Reading of the last sweep `[OBS]`: none of the five mined rule rows carries a `sha256:` value for its source,
so none meets C1 v2's sha256 equality clause; they also carry `opened 2026-10-19`, not `2026-10-23`.

Lane state used: `git rev-parse --short HEAD` → `464a024`. No branch, index or worktree mutation performed.

---

## §6 Confidence and remaining unknowns

- High confidence (direct reads) on §1 ledger entries and §5 outputs; the line anchors are from the current
  lane bytes at `464a024`.
- High confidence that the four named files contain no claim of *positive* rule attribution and no claim that
  upstream exposes a per-rule record; the strongest statement on record is the response-path absence at
  getprop `:127`.
- `[UNK]` whether any Hyprland 0.56.2 source path outside `HyprCtl.cpp` 1463-1645 (e.g. event payloads, IPC
  events, debug overlay) exposes rule identity: I opened no upstream bytes (none of my reads fetched a URL),
  so this stays unestablished by me and is exactly what wave-1 source seats are opening.
- `[UNK]` whether the wave-1 fetch receipts above were fetched from the pinned commits and with what
  sha256 — not inspected by this seat.
- `[INF]` Overlap risk: §4's absences match the fetch-receipt names already in `fetch/w1`; the new note's
  claim rows should cite freshly pinned raw URLs opened 2026-10-23 and must not lean on S016–S020.

## Verdict

The lane's existing rule ground is a bounded effect-read plus declared-syntax/evaluation semantics; the
single open item the frontier names is **rule attribution** (`corpus/README.md:101-102`), with two wording
tensions flagged (`README.md:83-85` vs `:98-100`; `keybind-rule-semantics.md:299-300` vs the r12 getprop
correction scope). A new `rule-attribution-r24.md` adds ground only if its rows go beyond the ten occupied
families in §3 and beyond the five already-mined rows' non-reusable anchors.

Report: .ufo/waves/round-24/w1/reports/ScoutPriorNotes.md
