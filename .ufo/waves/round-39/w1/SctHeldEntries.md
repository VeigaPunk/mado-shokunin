# SctHeldEntries — held-ground survey for the C3 config-option-table entry (round 39, w1)

Seat: `SctHeldEntries` (scout, leaf). Scope: survey the **already-held** knowledge about
general-option ownership so the C3 entry `corpus/knowledge/config-option-table-r39.md`
adds only what is not held, and state the non-overlap boundary. Read-only everywhere:
no lane file was edited except this report; no compositor, socket, package or host
mutation; no tool installed (none needed).

Lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`. HEAD at survey time
(`git rev-parse HEAD`) = `457d1b125932c1e0d797061a2156b917bcd7edaa`.
Scratch (ephemeral, outside the lane): `/tmp/w1-sct-held/`.

---

## 1. What is ALREADY HELD about general-option ownership

### 1.1 The 56 `getoption` claim→live pairs — held

`corpus/knowledge/hyprctl-verification-layer.md` (MADO-R2-1, `wc -l` = 308 lines):

| Held item | Anchor | What it already fixes |
|---|---|---|
| The 56 pairs, split 39 / 15 / 2 | §3.1 `:72`, §3.2 `:116`, §3.3 `:136` | Row counts re-derived from the markdown tables: **39 + 15 + 2 = 56 rows, 56 unique option keys** (a first regex pass returned 53 because `general:col.active_border`, `general:col.inactive_border`, `group:col.border_active` contain a dot — corrected with `[A-Za-z0-9_.]+`). Each row already carries: declaring chain (last wins), live value, `set` flag, and a class. |
| The divergence **vocabulary** | §2 `:37-58` | `agreement` / `agreement*` / `live-default` / `mismatch` / `config-only`, each with a falsifiable meaning; `set=false` ⇔ no declarer; "last declarer wins" as the resolution rule; chain aliases (D-LF, D-IN, D-EN, L-IN/L-MON/L-LF, T-WNG, TH). |
| The **include order** | §2 `:39` | defaults `L4–12` → theme `L13` → local `L16–20` → toggles glob `L23` → `ai-usage.conf` `L29`; plus the "last declarer wins" resolution rule and the 56-row class census (`:143-147`: 52 agreement of which 6 are `agreement*`, 4 `live-default`, **0 mismatch**). |
| The **toggle-beats-user proof** (6 ownership rows) | §5 `:163-176` | `general:gaps_in` / `gaps_out` / `border_size` → *toggle owns*; `input:kb_layout` → *local file owns*; `general:col.active_border` / `group:col.border_active` → *theme owns*. Each row names the earlier declarer, the later declarer, the live value and the verdict. This is the canonical ownership-proof set. |
| Config-only surface (non-getoption) | §6 `:178` | window rules, exec-once, env, include graph, other-consumer configs, commented monitor templates. |
| Live-probe recipe + unknowns | §8 `:216`, §10 `:249`, §11 `:270` | anti-claim branch; 8 open unknowns; 5 reproducible spot-checks. |
| Append-only errata | `:283` (round 4) | E2 (closure), E3 (`wlSocket` → `wl_socket`), plus the round-26 pointer to `animation-table-r26.md`. |

### 1.2 Include order and the who-owns-it table — held in `SKILL.md`

`SKILL.md` (`wc -l` = 2006 lines):

| Held item | Anchor | Note |
|---|---|---|
| **Config-plane map — who owns this key** | `:47-67` | Root is a pure orchestrator; the include-order arrow (defaults → theme → user files → toggles glob → `ai-usage.conf`); "include order *is* precedence — the last file to set a key wins"; the two measured ownership sentences (`gaps_out` → toggle-owned; `input:kb_layout` → user-owned); layer write rules (defaults tree read-only, `~/.config/` is the operator surface, toggles dir is tool-written, theme dir is rewritten by `omarchy theme set`). **Round-12 erratum at `:56`**: live is now **18 sources / 32 L, last include `gkeep.conf`**. |
| **Who-owns-it table** | `:69-91` | **19 data rows** (Intent → Owner file → Verify with → Anchors), re-counted from the table body. It is **intent-level** ("gaps / borders / rounding / animations / layout", "keyboard layout / repeat / touchpad", "env vars", "local window rules", …) — *not* a per-option key→owner table. |
| Four traps the table encodes | `:93-102` | (1) separate consumers; **(2) Toggle beats user file**; (3) bar needs restart; (4) `ai-usage.conf` is sourced last. |
| Claim → evidence-class routing | `:137-141` | File bytes license "who declares a key" but **bar** "the effective value"; hyprctl live read licenses "which declarer owns it (`agreement*` shadowing proof)". |
| Divergence vocabulary + severity | `:158-190` | The same five classes restated, plus S1/S2/S3; "any new mismatch falsifies" the 0-mismatch result. |
| Error pattern | `:359` | "The file says X, so X is live" → shadowing — later layers win. |
| Evidence trail | `:691-696` | Round-2 note cited as "56 `getoption` claim→live pairs + 9 non-getoption pairs; classes and ownership proofs". |

### 1.3 The static plane, the drift anchor and the grammar precedent — held

| Held note | Anchor | What it already fixes (relevant to C3) |
|---|---|---|
| `corpus/knowledge/hyprland-config-plane.md` (MADO-1, 267 L) | §3 `:38` root include graph with line anchors; §7 `:128` override-chain table (6 options: `gaps_in`, `gaps_out`, `border_size`, `rounding`, `layout`, `kb_layout`); §8 `:151` separate consumers; §9 `:170` version pins; §12 `:199` open items; errata round 2 `:220` | The **static** half: file inventory with sha256, include graph, effective values for 6 keys. |
| `corpus/knowledge/config-drift-r12.md` (MADO-R12-4) | `:76-80` live precedence spot-check; `:113-116` limits; `:160-170` SKILL erratum map | **The current include-order anchor**: 17 → **18 sources**, root 29 → **32 lines**, last include `gkeep.conf` at `:32` (`ai-usage.conf` remains `:29`); explicit limit — "`hyprctl getoption` checks only `general:gaps_out` and `input:kb_layout`; it does not independently establish all include precedence or source ownership". |
| `corpus/knowledge/hyprland-config-era-r12.md` (MADO-R12-2) | `:22-30` (S021–S030) | The syntax-era fence (hyprlang deprecated since 0.55, Lua is the forward surface; `configProvider: hyprlang` on this host) and the rule that include order and startup-file selection are two different precedence domains. |
| `corpus/knowledge/bind-table-r25.md` | §"Parse and source graph" `:5-17`; §"Variables and comments" `:19-23` | **The hyprlang grammar ground the option table reuses**: `source =` → `glob(absolutePath(…), GLOB_TILDE)`, `~`→`HOME`, relative paths resolve against the *including* file's dir, matches in `strcoll` order, depth-first traversal with the current path restored, directories/non-regular skipped, a no-match glob is an error; `$NAME` variables; `#` comment and `##` → one literal `#`. |
| `corpus/knowledge/executor-test-sufficiency.md` (MADO-R3-4) | `:62` declarer census for `general:gaps_out`; `:113-126` gap 2; `:133-136` gap 4 | The per-key declarer census shape (5 rows incl. the `group:groupbar:gaps_out` **namespace probe**); the named gap *"block-scope key namespacing not stated"* — nested blocks extend a key's path; and that **no-arg `hyprctl getoption` is not an enumeration surface** (per-key probes only). |
| `corpus/knowledge/config-health-report-r3.md` (MADO-R3-2) | `:48-50`, `:137-140`, Appendix A `:488` | The **re-measure** of the same 56 (+1) pairs: 57/57, **0 mismatch**, class census `{agreement*:6, agreement:46, live-default:4, extra:1}`; Appendix A is the 57-row live table with the round-2 class column. |
| `corpus/knowledge/animation-table-r26.md`, `workspace-rules-r27.md`, `keybind-rule-semantics.md` | resp. §"Local tool and counter", §"Measurement status" | The **shape precedent** for a tool+counter+note triple in this lane (static table → nested-instance oracle → note). The option table is the next sibling in that family. |
| `corpus/knowledge/arc-synthesis.md` §6 gap ledger; `remaining-planes-census.md` §0 | `:290-307`; §0 table | The frontier/plane bookkeeping that a new option-table note must fit under. |
| `corpus/README.md` | `:12`, `:15`, `:19`, `:37`, `:82` | Index rows for the four notes above; **55 index rows for 55 `corpus/knowledge/*.md` files** (`ls corpus/knowledge/*.md | wc -l` = 55; `grep -cE '^\| `knowledge/[^`]+\.md` ' corpus/README.md` = 55). A new note therefore needs **exactly one new index row** or `quality/check-index.py` fails. |

---

## 2. The NON-OVERLAP BOUNDARY (what C3 must add, and what it must not restate)

### 2.1 HELD — C3 must cite, not re-derive

1. **The 56 pairs and their classes** (`hyprctl-verification-layer.md` §3). C3 must not reprint them.
2. **The ownership-proof set of 6** (`…layer.md` §5) and the *toggle-beats-user* fact (`SKILL.md:97`). C3 must not re-argue it; it may show the tool reproduces it.
3. **The include order** (`SKILL.md:50-56` + round-12 erratum `:56`; `config-drift-r12.md`) and the "last file to set a key wins" rule (`SKILL.md:51`; `…layer.md:39`). C3 must not restate a host include order as a general law — and if it mentions an order, it must use the **current** one (18 sources, `gkeep.conf` last), not the 17-source/29-line MADO-1 form.
4. **The five divergence classes** (`…layer.md` §2; `SKILL.md:158-166`). C3 may *apply* them; it may not redefine them.
5. **The hyprlang source-graph and comment grammar** (`bind-table-r25.md:5-23`).
6. **The block-scope namespacing fact** (`executor-test-sufficiency.md:113-126`) and the "no-arg `getoption` is not an enumeration surface" note (`:133-136`).
7. **The per-key declarer-census shape** (`executor-test-sufficiency.md:62`).
8. **The sibling tool+counter+note shape** (`animation-table-r26.md`, `workspace-rules-r27.md`).
9. **The era fence** (`hyprland-config-era-r12.md`) — a Lua-era documentation page may not be promoted to a hyprlang grammar fact (QUALITY 15/16).

### 2.2 NOT HELD — C3's actual delta (the three deltas named in the task)

| Delta | Held today | Measured on the host tree (this seat) |
|---|---|---|
| **(a) Full-tree static option table** | Only **56 hand-picked live** pairs exist, and only **52** of them have a declarer. `config-drift-r12.md:114` states outright that the live layer "does not independently establish all include precedence or source ownership". | `tools/mado-options.py --home <tree>` → **79 static rows**, of which **70 are general options** and **9 are bind/windowrule-family rows that leak in** (see §3.1). Of the 70 general-option keys: **52 are held keys**, **18 are new** — `group:groupbar:{col.active, col.inactive, font_family, font_weight_active, font_weight_inactive, gaps_out, gradient_round_only_edges, gradient_rounding, gradients, indicator_gap, indicator_height, text_color, text_color_inactive}` (13), `group:col.border_inactive`, `group:col.border_locked_active`, `group:col.border_locked_inactive` (3), `misc:disable_scale_notification`, `misc:disable_splash_rendering` (2). The 4 held keys with no declarer (`decoration:dim_inactive`, `general:snap:enabled`, `input:accel_profile`, `input:touchpad:disable_while_typing`) are correctly absent from the static table and reappear as `live-default` in a merge. |
| **(b) Ownership resolution for ALL options** | Ownership is proven for **6 keys** (`…layer.md` §5) and censused for **1 key** (`executor-test-sufficiency.md:62`); the SKILL table is **19 intent rows**, not per-key. | The tool resolves owner = *file path relative to home* + *line* + *layer label* for **every** row, e.g. `general:gaps_out → .local/state/omarchy/toggles/hypr/window-no-gaps.conf:3 [toggles]`; `input:kb_layout → .config/hypr/input.conf:10 [user]`; `general:col.active_border → .config/omarchy/current/theme/hyprland.conf:4 [theme]`. These three agree with the held proof set rows-by-row — the **new** part is that the resolution generalizes to all 70 keys. |
| **(c) Vocabulary application (mechanical merge)** | The classes exist only as a **definition** (`…layer.md` §2, `SKILL.md:158-166`) plus a **hand-normalized** classification of 56 rows. | `--getoption <json>` merges a live dump into the static table and labels every row `agreement` / `agreement*` / `live-default` / `mismatch` / `config-only` with a deterministic comparator (`tools/mado-options.py:428-447` `values_equal`; `:468-492` `merge_rows`): numeric for int/float, boolean spellings, scalar-vs-tuple, else exact string. |

### 2.3 The boundary line, stated once

> **Held:** the *values*, the *6-row ownership proof*, the *include order*, the *class vocabulary*, the *hyprlang grammar*, and the *19 intent rows*.
> **C3 adds:** a *whole-tree static owner table* (key → owner file:line, layer), *ownership resolution generalised from 6 keys to every key*, and a *mechanical, reproducible application of the held vocabulary* to a static×live merge — plus the parser boundaries that make the static table a table and not a grep.

---

## 3. Boundary hazards the C3 entry must not walk into (measured)

These are findings about the **draft** entry at
`.ufo/waves/round-39/w1/ScrKnowledgeEntry/config-option-table-r39.md` (4013 B) and the
shipped tool it describes. They are inside my scope because they *are* the non-overlap
boundary: each is either a restatement of held ground or a claim the tool does not
support.

### 3.1 The draft's "excluding bind … and rule declarations" is not what the tool does

Draft text: *"The table includes ordinary general options (`key = value`), excluding bind,
animation, workspace, and rule declarations."*
Tool: `tools/mado-options.py:80-83` excludes by **exact trimmed-LHS match** against
`EXCLUDED` (`bind`, `binds`, `bindl`, `bindr`, `bindm`, `binde`, `bindn`, `bindd`,
`unbind`, `unmap`, `submap`, `animation`, `bezier`, `workspace`, `windowrule`,
`windowrulev2`, `exec`, `exec-once`, `monitor`, `env`, `layerrule`).

Measured on the host tree (`--home .ufo/waves/round-39/w1/ExecOptionsRealTree/host-tree`,
exit 0, 79 rows) the table **contains 9 rows that are not general options**:

* `binddr` (`.local/share/omarchy/default/hypr/bindings/utilities.conf:69`),
  `bindeld` (`…/bindings/media.conf:21`), `bindld` (`…/bindings/utilities.conf:10`),
  `bindmd` (`…/bindings/tiling-v2.conf:100`) — the source keyword is `bind` **plus flag
  suffixes**, so the exact-match exclusion never fires. (`bind-table-r25.md:27` holds that
  Hyprland parses `bind` with flag suffixes enabled, `ConfigManager.cpp:607-608`.)
* `windowrule:fullscreen`, `windowrule:idle_inhibit`, `windowrule:match:class`,
  `windowrule:name` (`…/apps/moonlight.conf:2-5`) and `windowrule:no_follow_mouse`
  (`…/apps/jetbrains.conf:4`) — the `windowrule { … }` **block** form puts members under
  a category, so the LHS is `name`/`match:class`/…, never `windowrule`.

Consequence for C3: the exclusion claim must be stated as the tool actually behaves
(exact-LHS verb exclusion + category-prefixed block members), or the entry overstates its
own instrument. `binds:hide_special_on_workspace_change` **is** a genuine option
(`binds { … }` category, `looknfeel.conf:142`) and **is** one of the held 56 — do not
sweep it out with the bind family.

### 3.2 The draft's "layers applied in this order … later layers override earlier" is not the tool's rule, and restates held ground

Draft text lists an ordinal layer order (1 built-in defaults → 2 theme → 3 user → 4 toggles
glob → 5 `ai-usage.conf`) with "later layers override earlier declarations".

Measured: the tool's precedence is **source-graph traversal order (last declarer in the
walk wins)**; the layer is a *label* only (`tools/mado-options.py:215-229` `layer_of`
derives it from the path; `:261-282` `declare` overwrites in walk order). Two scratch
fixtures in `/tmp/w1-sct-held/` show the ordinal reading is false:

* `defaults` sourced **after** `user` → owner = `.local/share/omarchy/default/hypr/d.conf`
  (layer `defaults`), value `99` — the defaults layer won because it came later.
* `toggles` sourced **before** `theme` → owner = `.config/omarchy/current/theme/hyprland.conf`
  (layer `theme`), value `33` — the theme layer won although the draft's ordinal puts
  theme *before* toggles.

Both runs exit 0. So the draft sentence is (i) a restatement of held host include order
(`SKILL.md:50-56`) and (ii) not the tool's mechanism. If C3 keeps an ordering sentence it
must attribute it to the host include graph (with the round-12 erratum: 18 sources,
`gkeep.conf` last), and must not present a layer ordinal as the resolver's rule.

### 3.3 The draft's `##` description diverges from both the tool and the held grammar note

Draft text: *"The parser recognizes the `##` section/comment convention as structural
context rather than treating those lines as settings."*
Held grammar (`bind-table-r25.md:23`, S172): `#` starts a comment and **`##` escapes to
one literal `#`**.
Measured in `/tmp/w1-sct-held/`: a whole-line `## a whole-line double hash = value`
produces **no row**; `name = x ## tail` yields value `x # tail` — i.e. the tool
*unescapes* `##` to a literal `#` inside a value, exactly as S172 says, and it does not
treat `##` as a "section convention". C3 should cite the held hyprlang grammar
(`bind-table-r25.md:19-23`) instead of introducing a competing description.

### 3.4 "Vocabulary application" must not claim the tool reproduces the held 0-mismatch census

Measured merge of the tool's static table against the round-39 synthetic 56-key dump
(`.ufo/waves/round-39/w1/ExecOptionsRealTree/getoption-synthetic.json`,
`custom_type`/`set`/`value` shape) → 83 merged rows, census
`{agreement: 41, agreement*: 6, live-default: 4, config-only: 27, mismatch: 5}`.
The **5 mismatches** are exactly the rows the held note classed `agreement (notation)` /
`agreement (truthy string parse)` / `agreement*` with hand normalization:
`animations:enabled` (`yes, please :)` vs `int: 1`), `decoration:shadow:color`
(`rgba(1a1a1aee)` vs `custom: ee1a1a1a 0deg`), `general:col.active_border`,
`general:col.inactive_border`, `group:col.border_active`. The tool's `agreement*` set is
therefore **not** the held proof set: it stars `decoration:rounding` and
`input:kb_options` (two declarers, identical value) where the note's §5 stars
`general:col.active_border` and `group:col.border_active`.

So C3 may claim: *the tool applies the held vocabulary mechanically and deterministically*.
It may **not** claim it reproduces the held classification of the 56 rows, nor cite the
0-mismatch census as a property of the tool. This is the single sharpest non-overlap
boundary: the held note's classes are *hand-normalized*, the tool's are *literal*.

### 3.5 Mechanics already available to C3 (no new claims needed)

* `tools/mado-options.py` — 1004 lines, sha256
  `cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e`; `--selftest` prints
  `MADO_OPTIONS_SELFTEST: 69/69 passed` (receipt:
  `.ufo/waves/round-39/w1/ExecOptionsRealTree/selftest.stdout`).
* `quality/counters/c3-r39-options.py` — sha256
  `16544cbde4ed67cfccc4c8cb4270a4a09250bbb2b63486d13b546ea16a101c35`; predicate
  `PRED-C3-r39-v1`; required row fields `{key,value,owner,layer,line,set}`.
* Fixture suite: `.ufo/waves/round-39/w1/ExecOptionsFixtures/run-fixtures.sh` → `fixtures=4/4`,
  exit 0 (from that seat's report).
* **C3's own counting counter `quality/counters/c4-r39-options-entry.py` does not exist yet**
  (`ls` → exit 2) and **no w1 seat is assigned to write it** — the w1 spec/dispatch
  mention `c4-r39-options-entry.py` only inside the shared context string, never in a
  seat task. C3's claim cannot be scored until that counter lands.
* SOURCES slots: `grep -cE '^\| S21[89] ' corpus/SOURCES.md` → **0** (exit 1); 211 rows
  total; ids up to S277/S258/S253 are taken, so **S218 and S219 are free**.

---

## 4. Commands run (this seat), with outcomes

```
read   corpus/knowledge/hyprctl-verification-layer.md        (308 L, full)
read   corpus/knowledge/hyprland-config-plane.md              (267 L, full)
read   SKILL.md:47-68, :69-104, :158-195, :353-380, :681-703, :719-746
read   corpus/knowledge/config-drift-r12.md, hyprland-config-era-r12.md,
       executor-test-sufficiency.md (head + :39-143),
       bind-table-r25.md (head), animation-table-r26.md (head),
       workspace-rules-r27.md (head), rule-attribution-r24.md (head),
       arc-synthesis.md (§6), remaining-planes-census.md (head)
read   .ufo/waves/round-39/registration.md (frozen claims)
read   .ufo/waves/round-39/w1-spec.json, w1-dispatch.json    (seat/task text)
read   .ufo/waves/round-39/w1/ScrKnowledgeEntry/config-option-table-r39.md (draft, 4013 B)
read   .ufo/waves/round-39/w1/ExecAssimFetches.md + S218.bin  (S218 quote located)
bash   wc -l SKILL.md corpus/knowledge/hyprctl-verification-layer.md  → 2006 / 308 / 267 / 1004
bash   grep -cE '^\| S21[89] ' corpus/SOURCES.md                → 0   (grep exit 1)
bash   grep -cE '^\| `knowledge/[^`]+\.md` ' corpus/README.md    → 55
bash   ls corpus/knowledge/*.md | wc -l                           → 55
bash   python3 tools/mado-options.py --home .ufo/waves/round-39/w1/ExecOptionsRealTree/host-tree
                                                              → exit 0, 79 rows
bash   python3 tools/mado-options.py --home /tmp/w1-sct-held     → exit 0 (fixtures below)
bash   ls quality/counters/c4-r39-options-entry.py               → exit 2 (absent)
bash   ls corpus/knowledge/config-option-table-r39.md            → exit 2 (absent at survey time)
bash   git rev-parse HEAD                                        → 457d1b125932c1e0d797061a2156b917bcd7edaa
bash   sha256sum tools/mado-options.py quality/counters/c3-r39-options.py
bash   git status --porcelain | head   (read-only; only round-39 wave files + new tool/counter untracked)
```

Fixture probes (all `python3 tools/mado-options.py --home /tmp/w1-sct-held`, exit 0):

| Fixture | Observed |
|---|---|
| `general { gaps_out = 10 }` on one line | key becomes the literal `general { gaps_out` — the block form must be multi-line |
| `general {` … `}` block | key `general:gaps_out` (nested block extends the path) |
| `# comment = value` | no row |
| `## literal hash line = value` | no row |
| `name = a ## b` | value `a # b` (`##` → one literal `#`) |
| `$W = 42` / `border_size = $W` | value `42` (variable expanded) |
| `gaps_out = {{ 10 - 4 }}` | value `6` (expression evaluated) |
| defaults sourced after user | owner = defaults file (walk order wins over any layer ordinal) |
| toggles sourced before theme | owner = theme file |

---

## 5. Confidence and remaining unknowns

**High confidence (measured from repo bytes in this seat):** the held-item inventory and
its anchors (§1); the 56/39+15+2 and 56-unique-key counts; the 19 who-owns-it rows; the
55 notes / 55 index rows; the 79/70/9 static-table arithmetic; the 5 mismatches and the
2-for-2 `agreement*` divergence; the 4 no-declarer held keys; the fixture behaviours in §4;
the absence of `c4-r39-options-entry.py` and of any w1 seat assigned to it; S218/S219 being
free SOURCES slots.

**Medium confidence:** that the 9 leaking rows are a *defect* rather than a deliberate
choice — the tool's own docstring says the table collects "`key = value` lines that are
not a bind/animation/workspace/windowrule/… directive" (`tools/mado-options.py:4-7`), which
the leak contradicts, so I read it as a mismatch between docstring and behaviour. If the
author intends the leak (flag-suffixed binds, `windowrule {}` block members), the docstring
must change instead. Either way the C3 entry must describe the observed behaviour.

**Open unknowns (not resolvable from repo bytes alone, out of my read-only scope):**
1. Whether the C3 entry is meant to *reproduce* the held 56-row classification (then the
   5 notation mismatches must be resolved in the comparator, e.g. `rgba()/rgb()` → the
   `custom` hex form, and `yes, please :)` → truthy) or to *apply the labels literally*
   (then the divergence must be stated as a stated limit). The registration does not say.
2. Whether the L1 wants the 9 leaked rows fixed in the tool (a C2 change, out of a scout's
   scope) or documented in the C3 entry.
3. Whether `c4-r39-options-entry.py` will be written this wave; without it C3's
   `admitted=1/1 verdict=TARGET_MET` predicate has no instrument, and the frozen
   registration counts on it.
4. Whether the round-39 lesson file (`corpus/lessons/round-39.md`) will carry the Gate
   lines the S218/S219 rows must bind to — it does not exist yet at survey time.

**Out of scope / not done:** no lane file edited except this report; no `corpus/`,
`corpus/SOURCES.md`, `corpus/README.md`, `SKILL.md`, `tools/`, `quality/` or
`registration.md` touched; no git/jj mutation; no compositor read verb run against the
live session (all option values used above come from committed bytes and the round-39
scratch receipts); no package transaction; no tool installed.
