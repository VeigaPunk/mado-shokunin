# Parser intent and source-order surface — Mado R14

**Axes:** coverage; operability.  
**Scope:** Hyprland root-source extraction, membership/order, resolution, and R12/R13 history only. No general parser redesign.

## Contract

- The gate's accepted syntax is a line-oriented subset, not a full Hyprlang parser. It extracts lines matching `^[[:space:]]*source[[:space:]]*=`, trims the right-hand text, permits blank/comment lines, and fails on other active root lines. It does not interpret quoting, escapes, inline comments, or line continuations. The `# hyprlang...` probe rejects conditional source semantics as unsupported (`tools/mado-verify.sh:2321-2332, 2371-2372, 1153-1169`).
- Leading `~` maps under `$ROOT`; the expected toggle source is literal `~/.local/state/omarchy/toggles/hypr/*.conf`, expanded through `compgen -G` when `*` occurs. Its contract is one-or-more matches, not an expected set of concrete toggle filenames (`:2352-2370, 2416-2425`; `config-drift-r12.md:163-170`).
- `hypr.root.include_graph` owns ordered source declarations and exact-set diagnostics. `hypr.root.sources_resolve` owns declared/observed membership and target resolution (`tools/mado-verify.sh:2374-2437`). Order detection already exists. An isolated permutation fixture should preserve set and targets, assert `include_graph` FAIL and `sources_resolve` PASS, and be described as a regression guard—not an improvement.

## Directory and symlink boundary

The baseline accepts any existing direct path through `-e`, and any glob with at least one `compgen -G` match (`:2420-2424`); neither branch checks object type. Direct directories and directory matches, including mixed file/directory glob results, can therefore pass the current existence-only resolution.

The R14 task contract requires regular-file checks following file symlinks. A symlink to a regular file is valid; a directory, symlink to a directory, or dangling symlink is not. Glob acceptance requires at least one match and every match regular; on failure name non-regular targets in `hypr.root.sources_resolve`, preserving existing `missing:` / `extra:` diagnostics and order/set behavior. This is the bounded source-target fix, not a parser redesign.

The existing fixture writes source targets as regular files (`:245-298`). Its `:312-313` symlinks are theme-background and mako links, not source targets; therefore the fixture itself does not define source-symlink semantics. The R14 contract does.

## History and evidence chain

- R12 records gkeep appended after ai-usage (17→18 source lines) while retaining the earlier 12-name `LOCAL` set; the source target was already part of `EXPECT` and checked by `sources_resolve` (`config-drift-r12.md:82-91`). The retained list did not assert gkeep ownership or operator intent.
- R12's source resolver checked expected target existence but did not compare the observed source set; R13/M13 added exact-set membership diagnostics while keeping positional order as the PASS criterion (`config-drift-r12.md:86-89`; `tools/mado-verify.sh:2343-2402`). The toggle glob is still one-or-more matches, not a filename census (`config-drift-r12.md:163-170`).
- Existing fixture assertions cover an existing-target substitution (N2), removed gkeep target (N4), empty source member (N7), and unsupported conditional source syntax (N8) (`tools/mado-verify.sh:1080-1169`). They were read, not executed.
- R12's later correction points gate maintenance to `gate-standing-use.md` §5 rule 4: report/re-verify/appended erratum for moved pins, rather than cite the unrelated drift-watch rule (`corpus/lessons/round-12.md:109-112`; `corpus/knowledge/gate-standing-use.md:222-226`).

## Provenance, divergence, confidence

Local sources opened 2026-10-20 from the worktree; repository `HEAD` context was read as `873ff081b2ac363df771261b0ed950cba50d8988`, not asserted as the exact commit content of the in-flight worktree. The gate quote at `:2374-2377` is “The positional walk below stays the PASS criterion (MADO-1 §3 order).” It is admitted for static gate behavior, not full Hyprlang or runtime semantics. The R12 quote at `config-drift-r12.md:163-167` is “Toggle glob expansion requires at least one target; it is not an expected set of toggle filenames.” It is admitted as historical record, not current live state. The R14 assignment quote is “use regular-file check following file symlink”; it establishes requested policy, not landed behavior.

**LSP:** unavailable (`read xd://lsp` returned “No such tool” and enumerated mounted devices). Search was navigation only; findings rely on direct selected-file reads.

**Confidence:** high for the observed line-oriented gate and recorded history; high for the task's intended regular-file/symlink policy; not verified in landed implementation or by running fixtures. No tests, builds, linters, formatting, smoke runs, or runtime actions. Only shell command: read-only `git rev-parse HEAD`. No tools installed.