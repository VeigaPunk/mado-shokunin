# WikiTags source-opener report

**Verdict:** Opened and hashed two pinned Hyprland wiki pages. Six proposed claim rows passed the local quote/topic/anchor subchecks against the fetched bytes. The requested literal `tagwindow` did not occur in the pinned wiki `content/` sweep; the pages document `hl.dsp.window.tag` instead. The C1 integration counter and overall target were not run.

## Findings and behavior

- `content/configuring/core/rules/window-rules.md:178` documents the `tag` rule effect: `+`/`-` prefixes set or unset, and no prefix toggles.
- Lines 231–238 distinguish static and dynamic tags, say dynamic tags have a `*` suffix, direct users to `hyprctl clients` to check window tags, and state that the `tag` rule manipulates dynamic tags while the `hl.dsp.window.tag` dispatcher works with static tags.
- Lines 296–302 give examples including a `footclient` rule whose comment says it adds dynamic tag `term*`, plus tag-based matches and effects.
- `content/configuring/core/dispatchers.md:92–126` documents the Lua `hl.dsp.window.` method namespace and includes `tag({ window?, tag })`; line 100 lists the tag-clearing operation.
- **Inference:** These passages support a user-chosen tag as an inspectable marker: a rule can add one and the docs direct users to `hyprctl clients` to inspect tags. They do not establish that client output identifies which rule created a tag or which rule caused an applied effect. Host-side behavior remains **[UNK]**; no host query was made.
- The recursive pinned-content search for `tagwindow` returned no matches. This is limited to that spelling in this wiki snapshot; it is not evidence that no such command exists elsewhere.

## Proposed claim rows

`S?` ids are provisional for integration. `A1`–`A6` are local draft labels and may be renumbered by the integrator.

| A1 | Applies a tag. Use prefix `+`/`-` to set/unset; no prefix toggles it. | S? | "Applies a tag. Use prefix `+`/`-` to set/unset, or no prefix to toggle" |
| A2 | Check window tags with `hyprctl clients` is the documented way to inspect windows' tags. | S? | "Check window tags with `hyprctl clients`." |
| A3 | The `tag` rule can only manipulate dynamic tags. | S? | "The `tag` rule can only manipulate dynamic tags" |
| A4 | The footclient rule example's comment is: Add dynamic tag `term*`. | S? | "Add dynamic tag `term*`" |
| A5 | "Clear all tags from a window" describes a tag-clearing operation for a window. | S? | "Clear all tags from a window" |
| A6 | The signature contains `window?` as its window-parameter notation alongside a `tag` argument. | S? | "tag({ window?, tag })" |

The local Python check used the frozen C1 v2 topic pattern and anchor logic. All six rows had a whitespace-collapsed quote present in the fetched bytes, a quote of at most 25 words with a rule-topic word, a claim of at least 8 words, and either a four-word quote run or a matching backticked token. This is only the row-content subcheck; it does not establish `PASS_ROW` because the rows and source entries are not integrated at a revision.

## Draft SOURCES rows

| S? | Window rules — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/window-rules.md | docs | A | Window-rule tag effect, tag semantics, client inspection cue, and examples | content/configuring/core/rules/window-rules.md:178,229-238,296-302 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95, 16200 B | the tag rule's set/unset/toggle behavior, its dynamic-tag scope, checking tags with hyprctl clients, and the footclient example | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Window dispatchers — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/dispatchers.md | docs | A | Lua window-dispatcher namespace and tag-related method entries | content/configuring/core/dispatchers.md:92-126 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:80fccbf1ec5632d0979125d6df7f7a395391af85760952733bd2134c6dffe6ff, 12860 B | the documented window dispatcher namespace, tag method signature, and tag-clearing operation | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Provenance and exact commands

Pinned source revision: hyprland-wiki commit `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`.

The read-only discovery search was `functions.grep(pattern="tagwindow", path="/fast/scratch/hyaku/mado-r24/src/hyprland-wiki/content", case=false, gitignore=false, skip=0)`; output: `No matches found`. A second discovery search used `pattern="tag|tagwindow|tag rule|tags"` in `content/configuring/` and surfaced the two cited pages. No shell `grep` or writes to the clone were used.

The fetch/hash/size command was:

```sh
timeout 30s curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/window-rules.md' -o '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiTags-1.bin' && timeout 30s curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/dispatchers.md' -o '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiTags-2.bin' && sha256sum '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiTags-1.bin' '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiTags-2.bin' && wc -c '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiTags-1.bin' '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiTags-2.bin'
```

Observed output:

```text
9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiTags-1.bin
80fccbf1ec5632d0979125d6df7f7a395391af85760952733bd2134c6dffe6ff  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiTags-2.bin
16200 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiTags-1.bin
12860 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiTags-2.bin
29060 total
```

The frozen predicate was read from `.ufo/waves/round-24/c1/count.py`; Python read the fetched bytes, decoded UTF-8, whitespace-collapsed quotes, and applied the predicate's `TOPIC_RE` and `anchored()` logic. The resulting six row-subcheck results were all `PASS_ROW_SUBCHECK=True` (A1–A4 from `window-rules.md`, A5–A6 from `dispatchers.md`). No C1 counter, C2 counter, tests, or host commands were run.

## Surfaces, gates, and limits

- Files written: `.ufo/waves/round-24/fetch/w1/WikiTags-1.bin`, `.ufo/waves/round-24/fetch/w1/WikiTags-2.bin`, and this report.
- No product code, `corpus/SOURCES.md`, knowledge entry, README, or local wiki clone file was changed. No packages or tools were installed or updated.
- The overall C1 gate remains untested and unmet by this report alone: the source rows/claims are provisional, not committed into the required surfaces; the target also requires at least six counted rows from at least three distinct source rows and a README coverage-map index. This seat contributes two source candidates.
- C2, runtime tag behavior, rule provenance in actual client output, and any claim about a literal `tagwindow` dispatcher beyond the pinned wiki search are out of scope or **[UNK]**.

Report artifact: `.ufo/waves/round-24/w1/reports/WikiTags.md`.
