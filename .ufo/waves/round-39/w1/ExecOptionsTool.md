# ExecOptionsTool — round-39 C2 tool seat report

Seat: `ExecOptionsTool` (leaf executor, w1). Scope: write ONLY
`tools/mado-options.py` (new file) in the lane repo and this report. No other
file was written. Read-only repo git ops were used for baseline context only.

## 1. Deliverable

`tools/mado-options.py` (new file, 1004 lines, Python stdlib only). File
sha256:

```
cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e  tools/mado-options.py
```

Behavior (per assignment spec):

- Reads `DIR/.config/hypr/hyprland.conf` from bytes only (bytes → UTF-8 with
  replacement, logical-line joining on trailing `\`, `# hyprlang if/endif`
  directives honored). No compositor, socket, network, or subprocess in the
  read path.
- Follows `source =` depth-first in line order: `~` expands to DIR; glob
  patterns expand sorted (lexicographic); relative paths join the sourcing
  file's directory (helpers::absolutePath semantics).
- Expands `$name` variables (longest-name-first like hyprlang, up to 100
  iterations), `{{ expr }}` float expressions (one binary op), `##` escapes
  (`##` → literal `#`), strips comments; `\` escapes in values.
- Collects every general option statement: `key = value` whose trimmed lhs is
  not in the directive/exclusion set (source, bind/binds/bindl/bindr/bindm/
  binde/bindn/bindd, unbind, unmap, submap, animation, bezier, workspace,
  windowrule, windowrulev2, exec, exec-once, monitor, env, layerrule). Keys
  are composed with the category stack (`general { gaps_out = 0 }` →
  `general:gaps_out`; nested categories join with `:`).
- Resolves the LAST declarer per key across layers; rows are `{key, value,
  owner, layer, line, set}` where `owner` is the path relative to DIR (when
  inside it), `layer` is the layer label, `line` is the 1-based physical line
  of the declaration, `set` is true (declared). Output is one JSON array on
  stdout, sorted by key, exit 0.
- Strict policy: every opened file must be regular (symlinks followed to
  regular targets). Missing/non-regular root, unresolved `source =` (no
  matches), glob match that is a non-regular file, and recursive-source loops
  are NAMED failures on stderr (exit 3), never silent skips.
- `--getoption FILE`: merges a live getoption JSON mapping (key → {value,
  custom_type, set}) and adds `agreement` per row using the lane's divergence
  vocabulary. Malformed/unreadable JSON is a named failure, exit 4.
- `--selftest`: writes ephemeral fixtures under a private temp dir
  (`tempfile.mkdtemp`), runs a byte-copy of itself as a child process
  (`python3 -I <copy> …`), and passes 69/69 assertions (>40 required). Prints
  `MADO_OPTIONS_SELFTEST: k/n passed`.

Exit map: 0 OK · 2 usage · 3 named config-read failure · 4 --getoption failure
· 1 failed selftest.

## 2. Selftest evidence

Command (run from the lane root):

```
python3 -I tools/mado-options.py --selftest
```

Output and exit code:

```
MADO_OPTIONS_SELFTEST: 69/69 passed
exit=0
```

Coverage of the 69 assertions: exact key-set equality on a fixture tree
(defaults tree + theme + user files + toggles glob + ai-usage.conf + gkeep +
root-level directives), last-declarer ownership per layer (owner path, layer
label, line numbers, values), directive exclusions, `~` expansion, relative
source join, sorted glob order (z.conf wins after a.conf), depth-first order
(parent line after nested source wins), variable expansion (incl. longest-name
order), `##` escape, trailing-comment stripping, continuation lines, nested
category keys, `{{ }}` expressions, strict-policy failures (source→directory,
unresolved source, root directory, root missing, broken symlink root, glob
with directory match — each named on stderr, exit 3), symlink-to-regular-file
acceptance, getoption merge agreement (agreement / agreement* / mismatch /
config-only / live-default), boolean and scalar-vs-tuple numeric normalization,
live-default rows, sorted merged output, missing/malformed getoption file
failures (exit 4), usage error exit 2.

## 3. Real-tree cross-validation (read-only bytes)

Static run against the host tree (`--home /home/vgpnk`): exit 0, 79 rows.
Spot rows agree with the lane's recorded measurements (hyprctl-verification-
layer.md §3; hyprland-config-plane.md §7):

| key | value | owner | layer | record |
|---|---|---|---|---|
| general:gaps_out | 0 | .local/state/omarchy/toggles/hypr/window-no-gaps.conf:3 | toggles | toggle owns (MADO-1 §7; executor-test-sufficiency.md:51) |
| general:border_size | 0 | window-no-gaps.conf:5 | toggles | toggle owns (hyprctl-verification-layer.md:78) |
| decoration:rounding | 0 | window-no-gaps.conf:9 | toggles | toggle owns (hyprctl-verification-layer.md:84) |
| input:kb_layout | br | .config/hypr/input.conf:10 | user | L-IN:10 = br (hyprctl-verification-layer.md:120) |
| general:layout | dwindle | .local/share/omarchy/default/hypr/looknfeel.conf:24 | defaults | D-LF:24 = dwindle (hyprctl-verification-layer.md:83) |
| input:touchpad:natural_scroll | false | .local/share/omarchy/default/hypr/input.conf:14 | defaults | D-IN:14 = false (hyprctl-verification-layer.md:128) |
| input:repeat_rate | 40 | .config/hypr/input.conf:14 | user | L-IN:14 = 40 (hyprctl-verification-layer.md:132) |

No host file was opened for writing; no state mutated.

## 4. Divergences / documented decisions

- Layer labels: the spec names four layers (defaults tree, user files, toggles
  glob, ai-usage.conf). The tool emits those labels plus `root` (the
  orchestrator file itself), `theme` (the omarchy theme include), and `other`
  for any other resolved path; labels are derived from resolved paths relative
  to DIR (defaults = `.local/share/omarchy/default/hypr/`, toggles =
  `.local/state/omarchy/toggles/hypr/`, ai-usage = basename `ai-usage.conf`,
  theme = `.config/omarchy/current/theme/`, user = `.config/hypr/`).
- `agreement` equality semantics were unspecified; implemented deterministic
  normalization: numeric equality for int/float live types when the declared
  value parses; boolean spellings (true/yes/on/1 vs false/no/off/0) against
  live `1`/`0`/`true`/`false`; scalar-vs-tuple equivalence (`0` ==
  `0 0 0 0`); trimmed string equality otherwise. `agreement*` when the key
  was declared more than once (an earlier declarer is shadowed); `mismatch`
  when live differs or live `set` is false despite a declarer; `config-only`
  when declared but absent from the live map; `live-default` rows (owner/
  layer/line null, `set` from live) are appended for live keys with no
  declarer so the full vocabulary is reproducible.
- Recursive-source loops (a source cycle) are a named failure, not a silent
  skip; hyprlang category scoping is per-file (the parent category stack is
  restored after a nested source returns).
- `--getoption` schema: each entry must carry `value`, `custom_type`, `set`;
  anything else is a named exit-4 failure.

## 5. Safety

No writes outside `tools/mado-options.py` and this report; scratch only under
`/tmp` (`tempfile.mkdtemp`, cleaned in `finally`). No pacman/package
transactions (none needed — Python stdlib only), no host service mutation, no
socket connects, no git/jj mutation (no add/commit/checkout was run). No tools
installed. The selftest runs only its own ephemeral fixture copy as a child
process.

Main agent: run `python3 -I tools/mado-options.py --selftest` (expect
`MADO_OPTIONS_SELFTEST: 69/69 passed`, exit 0) and the C2 counting command
once `quality/counters/c3-r39-options.py` exists.
