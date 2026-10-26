# SKILL.md insertion text — round 43 (seat `ScrSkillProvince`)

Draft only. Nothing here edits `SKILL.md` (sha256 `8264434c43da1a90cecf90cfc9f08af0512e5db1c09c8ed588f0cf4eedf27e26`
at this seat's read, 2026-10-26, working tree clean for that file: `git status --porcelain=v1` names only `M LOG.md`).
The L1 integrates. Three items, each with its neighbouring lines.

Note on the escaped pipe: a markdown table splits on `|` even inside a code span, so the command cell carries `\|`
where the shell pipe is. The text below is literal insertion text — copy it verbatim.

---

## 1. Probe row

**Insert as a new line after line 223** (`| python3 tools/mado-globals.py --journal-file <journal>` …), i.e. as the new
last row of the `### Read-only probes` table (header line 205, separator 206, last row 223); line 224 is blank and line
225 is `### Advertised Wayland globals`, which keeps its place.

```markdown
| `hyprctl clients -j \| python3 tools/mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf` | whether a `windowrule = size W H, match:class RX` line's size matches the size the compositor reports for the client that line matches: a read-only join of config bytes and one `clients` dump, per matched client AGREE / DIFFER / TILED / BADSIZE; `--selftest` | host run 2026-10-26 (no gkeep window open): `MADO_GEOMETRY: rules=1 float_rules=1 other=1 unsupported=0 clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT`, rc 3; the size line it parsed: `MADO_GEOM_RULE: n=2 file=1 effect=size arg=420x500 class=^(org.omarchy.gkeep)$`; per-verdict licence in § "Rule size versus reported size" |
```

The sample line and the rule line are copied from this seat's own host run (receipt
`.ufo/waves/round-43/w1/ScrSkillProvince/receipts/geometry-host-run.txt`, command and rc in the same file); the same
summary line appears in the L1's independent receipt `.ufo/waves/round-43/receipts/live-geometry-host.txt:9`.

---

## 2. Decision row

**Insert as a new line after line 157** (the `Which Wayland globals …` row), i.e. as the new last row of the
`### Claim-first routing (what am I trying to settle?)` table (header 144, separator 145, last row 157); line 158 is
blank and 159 is `### Divergence vocabulary and severity taxonomy`.

```markdown
| Does the size a window rule asks for match the size the compositor reports for that client? | two read-only inputs, no new verb: file bytes (the `size` rule line) + hyprctl live (`clients`, which prints the animation goal box) | `hyprctl clients -j \| python3 tools/mado-geometry.py --clients - --rules <file>`; per-verdict licence and exit map in § "Rule size versus reported size" | `[OBS]` for both printed sides (the rule text and the goal box); rendered size, the client's own request and rule attribution stay `[UNK]` |
```

---

## 3. Subsection `### Rule size versus reported size`

**Insert after line 243** (the blank line closing `### Advertised Wayland globals`, which runs 225-243), before line 244
`### Mutating commands — operator only, mado never runs`. Keep one blank line on each side, as below.

```markdown
### Rule size versus reported size

`python3 tools/mado-geometry.py --clients <dump|-> --rules <file>…` joins two caller-supplied read-only inputs: the
`windowrule = size W H, match:class RX` and `windowrule = float on|off, match:class RX` lines of Hyprland config files,
and one `hyprctl clients -j` dump. It starts no process, opens no socket and reads no config tree of its own — the caller
runs `hyprctl clients -j | python3 tools/mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf`. Output: one
`MADO_GEOM_RULE:` line per supported rule, one `MADO_GEOM_CLIENT:` line per matched client, then a `MADO_GEOMETRY:` summary.

What the reported size is. The `clients` reply prints `"size": [{}, {}]` (`Hyprland-HyprCtl.cpp:395`, command
registered at `:2007`) from `w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL)` (`:427-428` in the JSON format, `:448`
in the plain one), and `GEOMETRIC_GOAL` is `m_realSize->goal()` while `GEOMETRIC_CURRENT` is `m_realSize->value()`
(`Hyprland-GeometricMovableAnimated.cpp:19-20`): the dump is the animation's target box, not the value on screen. A rule's
`size` reaches that box only on the floating path: the default floating algorithm reads `m_ruleApplicator->static_.size`
for a window on its first map and takes the box from `calculateExpression` (`Hyprland-DefaultFloatingAlgorithm.cpp:49,55-56`);
the applicator stores the parsed `Math::SExpressionVec2` (`Hyprland-WindowRuleApplicator.cpp:426`). The class match is
anchored upstream — `re2::RE2::FullMatch` (`Hyprland-RegexMatchEngine.cpp:16`, `negative:` prefix at `:7-8`) — which is
why the tool uses `re.fullmatch`.

Per-verdict licence — a verdict reads two printed values, it never calls a fault:

| Verdict | Licenses | Does not license |
|---|---|---|
| AGREE | the reported goal box equals the rule's `size` for that client: the rule's size reached this client's goal | that the window renders at that size (the dump prints the goal, not the current value); that the rule is the only writer (a resize, a center or a later effect can set the same value); that the client asked for it |
| DIFFER | the goal box differs from the rule's `size` | a defect or a cause: a user resize, a compositor clamp or a later effect all produce it — a report, not a fault |
| TILED | the matched client is not floating, so the first-map floating branch that reads `static_.size` never ran for it: the rule's size is inert for this client | that the rule is inert for the class — a later floating instance of the same class reads it |
| BADSIZE | only that there was no size to compare (no `size` value, or not two integers) | any agreement claim |
| NO_MATCHING_CLIENT (rc 3) | no mapped client matched any supported `size` rule — a null observation | that the rule works, or that the file declares none |
| NO_SIZE_RULES (rc 4) | the rules files carry no supported `size` line | anything about a `float`-only or unsupported-grammar file |

Exit map: 0 `OK` · 1 `DIFFER` (at least one matched client differs) · 2 `SETUP` (usage | unreadable | too_large |
bad_json) · 3 `NO_MATCHING_CLIENT` · 4 `NO_SIZE_RULES`.

Host run 2026-10-26, no gkeep window open: the gkeep rule file declares `size 420 500` and the dump holds four tiled
clients, so nothing matches.

    $ hyprctl clients -j | python3 tools/mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf
    MADO_GEOM_RULE: n=1 file=1 effect=float arg=on class=^(org.omarchy.gkeep)$
    MADO_GEOM_RULE: n=2 file=1 effect=size arg=420x500 class=^(org.omarchy.gkeep)$
    MADO_GEOMETRY: rules=1 float_rules=1 other=1 unsupported=0 clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT

NO_MATCHING_CLIENT is not "the rule works": it says only that no mapped window carried the class. What a live gkeep
window would report needs that window open — an operator act, not a mado probe, and the rendered size after the
animation stays `[UNK]` either way.
```

---

## Provenance of every quoted line

| Quote | Where it was read | Receipt |
|---|---|---|
| the `MADO_GEOM_RULE:` / `MADO_GEOMETRY:` lines | this seat's host run of the reference at `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (copied to scratch, sha256 `e3c2e471…`) | `w1/ScrSkillProvince/receipts/geometry-host-run.txt` |
| `"size": [{}, {}]` at `Hyprland-HyprCtl.cpp:395`; `GEOMETRIC_GOAL` at `:427-428`, `:448`; `clients` at `:2007` | pinned fetch `.ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp` (sha256 `798b7c6c…`) | `w1/ScrSkillProvince/receipts/source-quotes.txt` |
| `m_realSize->goal()` / `m_realSize->value()` at `Hyprland-GeometricMovableAnimated.cpp:19-20` | pinned fetch (sha256 `649f1a8d…`) | same |
| `static_.size` / `calculateExpression` at `Hyprland-DefaultFloatingAlgorithm.cpp:49,55-56`; `static_.size = expr` at `Hyprland-WindowRuleApplicator.cpp:426` | pinned fetches (sha256 `f05f2561…`, `fec33f9a…`) | same |
| `re2::RE2::FullMatch` at `Hyprland-RegexMatchEngine.cpp:16`, `negative:` at `:7-8` | pinned fetch (sha256 `8ca65533…`) | same |

Each quote is ≤ 25 words and is re-found by
`python3 -I .ufo/waves/round-43/w1/ScrSkillProvince/verify-quotes.py`, which greps the receipts above and exits non-zero
on a miss.
