# MadoA4CritEntry — round-48 C2 entry attack

Axes: repair presence; truth against pinned bytes; runtime/receipt alignment.

## Finding

No sampled false or overclaiming sentence found; no release-blocking predicate break identified. Repairs enumerated by registration-v2 §C2 are present, including step-9 severity split (entry:44), unknown model result (42), second WARNING (94), three regular ruleset files plus `xorg` symlink (38), include-path precedence attribution (28), model wildcard gloss (39), `kb_file` wording (112), README locator (17), recheck triggers/pin count (16), S340/S349 locators (3,12), and S351 (14,67).

## Evidence

Pinned-source sampling:

- `fetch/xkbcommon-rules.c:520-535` confirms more layouts than variants emits WARNING only if a variant was supplied, while fewer layouts emits ERROR; step 9 accurately distinguishes them.
- `fetch/xkbcommon-context.c:243-280,282-319,330-337` confirms user XDG/HOME paths precede extra, extensions, then root, and legacy-root fallback follows an unavailable canonical root.
- `fetch/xkbcommon-keymap.c:173-189` confirms failed internal construction unrefs and returns NULL, and `xkb_keymap_new_from_names` wraps the names2 API.
- `fetch/xkeyboard-config-rules-evdev:55-59,109-175` supports named model rows plus catch-all and symbols wildcard descriptions.
- `fetch/xkbcommon-messages-codes.h:116,150` supports S349 IDs 338 and 595; remaining ID claims were not independently sampled.

Runtime probes (all `/usr/bin/xkbcli compile-keymap --test`, HOME/XDG paths in scratch):

| Arguments | rc | stderr result |
|---|---:|---|
| `--layout br --options compose:caps` | 0 | empty |
| `--layout zz` | 1 | XKB-338, XKB-661, XKB-769, XKB-822 |
| `--layout br --variant nope` | 1 | XKB-661, XKB-769, XKB-822 |
| `--layout br --options nope:nope` | 0 | XKB-595 ignored-option diagnostic |
| `--layout br --model nope` | 0 | empty |
| `--layout br --rules nope` | 1 | XKB-338, XKB-595, XKB-822 |

These agree with receipt `receipts/xkbcli-compile-keymap-r48.txt` on rc and diagnostic classes (receipt lines 120-210). Because the run used scratch HOME, the path strings in XKB-338 census differ from the receipt's host paths; no mismatch in the described failure behavior.

## Execution constraint

The required full clone under `ulimit -f 2048` failed checkout because tracked files exceeded the 1 MiB per-file limit. A `--no-checkout` clone succeeded for probe execution. Both scratch directories were removed by exit traps. No tools installed. Largest output file was not measured; probe output files were small. No tracked lane files changed.
