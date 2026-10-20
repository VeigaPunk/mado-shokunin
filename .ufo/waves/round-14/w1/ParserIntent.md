# Parser intent and source-order surface — Mado R14

**Axes:** coverage; operability.  
**Scope:** the gate's Hyprland root-source extraction, source membership/order, target resolution, and the associated R12/R13 history. This is not a general Hyprlang parser redesign.

## Reconstructed contract

### Gate-supported syntax (not full Hyprlang)

The gate first treats `hyprland.conf` as a pure orchestrator: blank lines and ordinary comments are ignored, `source` assignment lines are extracted, and other active lines make `hypr.root.orchestrator` FAIL. A comment matching the gate's `# hyprlang...` probe is specifically rejected because conditional source semantics are not modeled (`tools/mado-verify.sh:2321-2332`; the N8 fixture at `:1153-1169`). This is a line-oriented gate contract, not a promise to parse Hyprland's full grammar.

The extractor recognizes lines matching `^[[:space:]]*source[[:space:]]*=`. It keeps the remainder after the first `=` after trimming whitespace at the start and end (`:2371-2372`). It does not tokenize shell-like quoting, unescape text, interpret inline comments, or assemble continuations. A blank `source =` is captured as an empty member and fails the exact-set rows as `extra: ''`; N7 guards against a crash (`:1136-1151`).

For target checks, the current path mapping substitutes `$ROOT` only for a leading `~`. The declared toggle entry is the literal `~/.local/state/omarchy/toggles/hypr/*.conf`; the current resolver asks `compgen -G` for that pattern when `*` occurs (`:2352-2370`, `:2416-2425`). This means at least one toggle match is required, but its concrete filenames are not an independently declared expected set. R12's correction says this explicitly (`config-drift-r12.md:163-170`). Do not expand this into support for environment variables, arbitrary Hyprlang expressions, or a general glob inventory.

### Exact set, exact order, and row ownership

`EXPECT` is the pinned source-declaration list. `hypr.root.include_graph` checks the observed source count and positional sequence; R13 added set-delta reporting so missing/extra declarations are named too (`tools/mado-verify.sh:2352-2402`). `hypr.root.sources_resolve` separately checks the declared/observed member set and resolves each expected target (`:2404-2437`). These are distinct facts and rows:

- A same-set source reorder is an `include_graph` failure; target resolution remains independently checkable.
- A missing/extra source declaration is named by the exact-set diagnostics, even where the replacement target exists.
- A target-type/resolution failure belongs to `hypr.root.sources_resolve`; it must not be reported as an order defect.

The order verdict is already implemented. An isolated source-order negative fixture is a regression guard, not a newly added capability: swap two existing source lines while preserving the declaration multiset and target files, then expect `hypr.root.include_graph` FAIL and `hypr.root.sources_resolve` PASS. Do not describe this as an improvement to source-order detection.

### Directory and symlink policy

**Baseline divergence:** the current resolver treats any existing direct path as resolved via `-e`; a glob is accepted if `compgen -G` finds any match (`:2420-2424`). Neither branch checks that the target is a regular file. Thus a direct directory, a directory symlink, or directory entries matched by a glob can currently satisfy this target-existence test. The mixed regular-file/directory glob is also not rejected by the baseline logic.

**R14 contract:** a source target must be a regular file, tested while following file symlinks (`.ufo/waves/round-14/w1/spec.json`, `GateImplement` prompt). Consequently:

- A direct regular file is accepted; a direct directory is rejected.
- A symlink resolving to a regular file is accepted; `-f` follows the link. A symlink to a directory or a dangling link is not a regular-file target and is rejected.
- A glob must have at least one match, and every matched object must pass the regular-file test. All-directory and mixed file/directory matches fail; name each non-regular target in the stable owning row `hypr.root.sources_resolve`.
- Preserve existing `missing:` / `extra:` membership diagnostics and source-order behavior. The new type failure is not a reason to broaden parsing or to change the expected toggle filename set.

The existing builder writes all source-target fixture files as regular files (`:245-298`); the two fixture symlinks at `:312-313` are theme-background and mako links, not source-target cases. Therefore the existing fixture is compatible with regular-file targets but, by itself, does not establish source-symlink behavior. The explicit R14 contract supplies that policy.

## Evidence chain and history

1. **R12 re-anchor.** The round-12 note records the observed source-list addition of `~/.config/hypr/gkeep.conf` after `ai-usage.conf`, and its gate erratum records 17→18 source lines (`config-drift-r12.md:82-91`). R12 retained the older 12-name `LOCAL` inventory: `gkeep.conf` was already in `EXPECT` and checked by `sources_resolve`; the attempted local-list widening lacked a behavioural fixture and was dropped (`:84-89`; `corpus/lessons/round-12.md:104-112`). This records membership/order and provenance, not gkeep ownership or operator intent.
2. **R12 residual.** At that stage, `include_graph` compared source order/count, but `sources_resolve` checked expected target existence without comparing the observed source set; the local list was not a directory census (`config-drift-r12.md:86-89`). The later erratum explicitly narrows the toggle glob claim to “at least one target,” not a set of filenames (`:163-170`).
3. **R13 correction.** Current gate comments mark the R13/M13 widening: source declarations and local regular `*.conf` members became exact-set comparisons with named missing/extra values, while `EXPECT` stayed at the recorded ordered list and the positional walk remained the PASS criterion (`tools/mado-verify.sh:2343-2402, 2444-2456`). The N2 fixture demonstrates why existence alone is insufficient: it replaces one source with a different existing target and expects both exact-set rows to name the delta (`:1080-1102`). N4 keeps the prior missing-gkeep target failure observable (`:1121-1134`); N7 and N8 guard empty-member safety and the unsupported conditional boundary (`:1136-1169`). These are source-code fixture assertions; none were executed for this assignment.
4. **Maintenance authority.** R12's source note later corrected its authority citation: the gate's governing rule is `gate-standing-use.md` §5 rule 4 — report a moved pin, re-verify, append an erratum — not the unrelated omarchy drift-watch protocol (`corpus/lessons/round-12.md:109-112`; `corpus/knowledge/gate-standing-use.md:222-226`). This history is not a reason to widen or rewrite the parser.

## Divergences and limits

- Current target resolution is existence-based, not regular-file-based; the direct and glob directory false-greens are the bounded operability issue to close.
- Existing declaration set/order semantics are not the issue and should remain unchanged. The order negative fixture only locks down that existing behavior.
- A clean declaration/list comparison does not imply an expected set of concrete toggle files; the toggle pattern remains “one-or-more matches,” now constrained so every match is a regular file.
- No claim is made about Hyprland runtime loading, source evaluation, gkeep intent, or effects of included configuration.

## Evidence provenance and confidence

- `file:///home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` — worktree source read 2026-10-20; repository `HEAD` context observed as `873ff081b2ac363df771261b0ed950cba50d8988` (this is not a claim that the in-flight worktree file equals that commit). Located quote, `:2374-2377`: “The positional walk below stays the PASS criterion (MADO-1 §3 order).” **Tier/scope:** direct static implementation/comment evidence for gate behavior. **Admit:** extraction, row separation, exact-set/order design. **Reject:** full Hyprlang semantics or runtime behavior. **Flip:** only on a newer source/fixture contract or measured implementation change.
- `file:///home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/config-drift-r12.md` — worktree record read 2026-10-20; same HEAD context qualifier. Located quote, `:163-167`: “Toggle glob expansion requires at least one target; it is not an expected set of toggle filenames.” **Tier/scope:** historical record of R12/R13 source-inventory correction, not a new host measurement. **Admit:** recorded chronology and bounded toggle-set interpretation. **Reject:** current live source contents or ownership. **Flip:** an append-only later erratum or fresh pinned source measurement.
- `file:///home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/spec.json` — assignment contract read 2026-10-20; `GateImplement` prompt at item 1. Located quote: “use regular-file check following file symlink.” **Tier/scope:** this round's requested policy, not evidence that implementation has landed or been exercised. **Admit:** the source-symlink rule for this change. **Reject:** any claim that baseline code already enforces it. **Flip:** a superseding explicit task contract.
- `lsp` was unavailable: `read xd://lsp` returned “No such tool” and listed the mounted devices. Search output was used only to locate passages; semantic findings above are based on direct selected-file reads. No LSP result is represented as evidence.

**Confidence:** high for the line-oriented baseline and recorded R12/R13 history; high that the R14 task contract requires regular-file targets with file-symlink following; not yet verified in the edited implementation or by running fixtures. No tests, builds, linters, formatters, smoke runs, or runtime actions were performed. The only shell command was read-only `git rev-parse HEAD`; no tools were installed.