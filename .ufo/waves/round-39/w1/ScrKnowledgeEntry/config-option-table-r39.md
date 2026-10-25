source: S218, S219
verified-at: 2026-10-25
recheck: on-release

# Reading a static general-option ownership table

A config-tree option table answers a bounded question: among the files visited by the resolver, which declaration is the final declaration for each ordinary `key = value` setting? It is a reproducible static view, not a report of compositor health.

## Source graph and precedence

The resolver starts from the selected Hyprland configuration root and follows the configuration's source graph: the main file and its sourced files, with paths interpreted relative to the containing configuration context. Its table layers are applied in this order:

1. built-in defaults;
2. theme files;
3. user configuration files;
4. files selected by the toggles glob;
5. `ai-usage.conf`.

Later layers override earlier declarations for the same key. Within the traversed graph, the last declarer owns the resulting static row; an earlier declaration remains part of the source history but is not the selected value. This is an ordering rule of this resolver, not a claim that every Hyprland runtime release loads every user's files in exactly this order. Check the actual graph and options-tool output for the tree being examined.

A falsifiable consequence: if a key has a value in a theme file and a later declaration in `ai-usage.conf`, the table should attribute the selected value to `ai-usage.conf`; changing/removing that later declaration should expose the earlier value, assuming no still-later declaration.

## Parsing boundaries

The table includes ordinary general options (`key = value`), excluding bind, animation, workspace, and rule declarations. Variable assignments and references are relevant to interpreting values: a setting may contain a variable reference whose meaning depends on the config context, so the displayed text should not be mistaken for an independently expanded runtime value unless the resolver explicitly reports expansion.

Comments are not option declarations. The parser recognizes the `##` section/comment convention as structural context rather than treating those lines as settings; ordinary comment text likewise does not become a row. A declaration-looking string inside a comment therefore does not become an option owner. This is a static parser boundary, not a complete implementation of every hyprlang syntax feature.

## Merging a live getoption dump

An optional live `getoption` JSON dump can be merged with the static table. The vocabulary distinguishes:

- `agreement`: static and live values agree;
- `agreement*`: agreement with a qualification/normalization marker from the comparison;
- `live-default`: a live value is reported as the default rather than as a matching configured declaration;
- `mismatch`: static and live values differ;
- `config-only`: a static config row has no corresponding live option in the supplied dump.

These labels describe the comparison of the supplied inputs. They do not prove why a mismatch occurred, that the dump is current, or that the compositor is healthy. Missing dump entries are not evidence that the static declaration is active.

## Evidence and limits

**OBS S218:** The round-39 opened Hyprland configuration/hyprlang option-syntax source is the syntax reference for interpreting option assignments and comment/section lines; consult its located Gate quote and bound receipt when checking parser assumptions.

**OBS S219:** The round-39 opened own-work source records the options resolver; its located Gate quote describes the static config-tree table and optional `getoption` merge.

The resolver is deliberately static: it reads configuration files and does not contact a compositor, socket, or network. Its output can support ownership analysis and can be compared with a separately acquired live dump, but static parsing alone is not live health, runtime state, or proof that the compositor accepted the files. Behavior outside the resolver's supported input and syntax boundaries remains unverified.
