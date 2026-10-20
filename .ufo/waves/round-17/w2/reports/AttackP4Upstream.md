# AttackP4Upstream — `corpus/knowledge/terminal-route-r17.md` § Upstream contract

Target: `corpus/knowledge/terminal-route-r17.md` lines 18-62 (§ Upstream contract).
Lane HEAD: 988b858bd6049bc709807534fd725c05264f7e60.

**Bytes reviewed:** the worktree file at sha256
`f5ab1092112f950420ba4363caef3a341254a13a95f578d3b38626acfb6268d4` (323 lines).
The file moved once during this review: a sibling lane inserted the
`README.md:259-262` compliance clause at lines 45-46 (+1 line after line 45) and
corrected three Host-declaration rows. I re-read the section and re-verified the
new clause against the fetched README before writing this report; all doc line
references below are against the hash above, not against HEAD `a9998d1`.

**Verdict: the attack failed.** Every quotation in the section is a literal
substring of the pinned bytes, every substantive reading holds at the pinned
tags, and the tag/commit provenance claims are exactly right. Three low-severity
defects were found (F1-F3: two anchor-range/label errors and one incomplete
default-source statement); each leaves its conclusion intact. No false claim was
found in the section.

## Probe provenance (all read-only; no installs, no execution of the route)

Pinned bytes, fetched with `curl` from `raw.githubusercontent.com` at the tag
**and** independently at the claimed commit SHA; digests identical in both
fetches:

| artifact | bytes | sha256 |
|---|---|---|
| `README.md` @ v0.14.3 | 14762 | `c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40` |
| `xdg-terminal-exec` @ v0.14.3 | 44020 | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` |
| `xdg-terminals.list` @ v0.14.3 | 1053 | `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034` |
| `extra/man/alacritty.5.scd` @ v0.17.0 | 28787 | `e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107` |

All four values match the document's line 20-21 / 51-53 / 83-86 table exactly,
including byte counts. GitHub's JSON API returned HTTP 403 (rate limit), so tag
identity was resolved instead from the smart-HTTP ref advertisement
(`…/info/refs?service=git-upload-pack`), which is authoritative and curl-only:

```
003f065925df9f419008159258ae169018bfd23df71b refs/tags/v0.14.3
003fdc946285396bd3e251b6942af7e9961b74f76bee refs/tags/v0.17.0
004294e7c8874e526b1e67b349d9ba30ddf81669119e refs/tags/v0.17.0^{}
```

- xdg-terminal-exec: one line, **no `^{}` peel** → lightweight tag whose ref
  object is the commit `065925d…`. Doc line 20-21 exact.
- alacritty: peel line present → annotated **tag object** `dc9462…` peeling to
  **commit** `94e7c8…`. Doc line 51-53 exact.
- Differential cross-check: `raw.githubusercontent.com` serves content at both
  commit SHAs (HTTP 200) and returns 404 at the alacritty tag-object SHA, the
  behaviour expected of a non-commit object.

Nothing from the route was executed: no `alacritty`, no `xdg-terminal-exec`, no
launcher/compositor/device probe, no package query. Directory contents were read
with `grep`/`awk`/`sha256sum`; `find`/`ls` were used only as existence checks on
config trees.

## Anchor-by-anchor result (all 18 anchors in § Upstream contract)

| Doc anchor | Cited claim | Result |
|---|---|---|
| README.md:100-101 | file naming | ✓ quote literal |
| README.md:115-118 | user file after `${desktop}` sibling, before `/etc/xdg/` | ✓ |
| xdg-terminal-exec:148-162 | same sequence from `XDG_CONFIG_HOME`/`XDG_CONFIG_DIRS`, then data dirs | ✓ |
| README.md:120-123 | system-data copy lowest priority | ✓ |
| README.md:131 | format quote | ✓ |
| README.md:133 | `#` lines ignored | ✓ (line also covers empty lines/trimming) |
| README.md:153-166 | list composed highest-priority first, then checked | ✓ |
| README.md:166 | applicability quote | ✓ literal |
| xdg-terminal-exec:106 | `--dir=workdir` / "set workdir of terminal." | ✓ literal |
| xdg-terminal-exec:1252 | "the option parser" | **F1** |
| xdg-terminal-exec:919 | `X-TerminalArgDir`/`TerminalArgDir` key | ✓ |
| README.md:264 | compliant-terminals quote | ✓ literal |
| README.md:259-262 (added mid-review) | compliance defined as `-e` argument handling | ✓ (261-262: "IMHO `xterm -e` handling of arguments is the golden standard, any terminal that fails to do so should be bugreported.") |
| xdg-terminal-exec:402-413 | `/execarg_default` directive handler | ✓ (F3 on the surrounding sentence) |
| alacritty.5.scd:31 | `import` option | ✓ |
| alacritty.5.scd:35-37 | import-order quote | ✓ literal |
| alacritty.5.scd:39-40 | three accepted path forms | **F2** (third form completes on 41) |
| alacritty.5.scd:57-61 | `live_config_reload` + "Default: true" | ✓ literal |

Substance also holds, not just anchors: the lookup sequence built at
`xdg-terminal-exec:148-154` and `:157-163` reproduces README:113-123 in
decreasing priority; the applicability decision is the `Categories` scan for
`TerminalEmulator` at `:816-827`; `--dir=` is parsed at `:1252-1259` and applied
at `:1400-1411` (`--working-directory=<val>` concatenation for a trailing `=`),
with a documented `cd` fallback at `:1494-1496`; the upstream list contains no
Alacritty line and no Alacritty `/execarg_default` (all 25 lines are comments,
`-` exclusions, or `/execarg_default` for other terminals).

## Findings (actionable)

### F1 — Low. `terminal-route-r17.md:40` calls the `--dir=` case arm "the option parser"

Evidence (`xdg-terminal-exec`):
```
1224: while [ "$#" -gt "0" ]; do
1225:   case "$1" in
...
1252:   --dir=*)
```
Line 1252 is the `--dir=` arm, not the parser. A reader following 1252 finds the
option handling, so the conclusion is unaffected, but the sentence as written
misdescribes the anchor.
Fix: "the `--dir=` arm is at `xdg-terminal-exec:1252` (parser loop begins at
`:1224`)."

### F2 — Low. `terminal-route-r17.md:58` cites `alacritty.5.scd:39-40` for three path forms

Evidence (scd 39-41):
```
39:  All imports must either be absolute paths starting with _/_, paths relative
40:  to the user's home directory starting with _~/_, or paths relative from the
41:  current config file.
```
The third form asserted by the document ("paths relative to the importing file")
is completed by line 41. `39-40` supports only the first two.
Fix: `alacritty.5.scd:39-41`.

### F3 — Low. `terminal-route-r17.md:47-48` presents `/execarg_default` as the sole source of `TerminalArgExec` defaults

Evidence: `get_default_execarg` falls back to the built-in value:
```
1126:   $XTE__EXECARG_DEFAULTS
1128: XTE__DEFAULT_EXECARG='-e'
```
and is applied only when the entry declared no `TerminalArgExec`
(`:1092-1096`); `reset_keys` also seeds `XTE__EXECARG='-e'` (`:746`). So "no
Alacritty entry in the upstream list" means *no Alacritty-specific override*,
not "no default": the built-in `-e` is what an Alacritty entry without its own
key would receive. Consequence for this route is nil — the host entry declares
`X-TerminalArgExec=-e` itself — which is why this is Low.
Fix: "defaults come from `/execarg_default:` directives, with a built-in `-e`
fallback (`:402-413`, `:1128`)."

## Observations (no correction required)

- **Preamble vs body on version.** `:10-11` says the note "does not establish …
  the installed Alacritty version", but § Unexercised behavior binds
  `installed alacritty (0.17.0-1)` from `pacman.log:639` and states the tags
  match "the last logged pkgver". The body is properly hedged (`[UNK]` the
  running binary and unlogged changes); the abstract's phrase would be exact as
  "the *running* binary's version". I did not count this as a defect because the
  body's evidence is a documentary lower bound, not a runtime claim.
- **`live_config_reload`.** The line the section quotes is literally "Live
  config reload (changes require restart)" — the parenthetical cuts against the
  "reload" reading. The `[UNK]` in § Unexercised behavior is the honest
  treatment; a half-sentence noting that the parenthetical most plausibly
  refers to changing the *setting* would remove the apparent contradiction.
- **`148-162` boundary.** The `for … done` that builds `XTE__CONFIGS` closes at
  `:163`, so the cited range ends one line inside the loop. I checked and did
  **not** count it: the asserted sequence is fully visible in 148-162, unlike F2
  where the asserted content is truncated.
- **Format bullet completeness.** `:32-33` states only the `#` rule, but the
  list grammar also has `+entry` (prevent fallback exclusion, `:445-454`) and
  `-entry` (exclude, `:455-464`) plus `/directive` lines (`:369-469`). This is
  mitigated because the system list the section points to ("see S060 below") is
  described in `SOURCES.md` S060 as "fallback exclusions and execarg defaults",
  so the information is reachable one hop away. Not a defect.

## Residual risk / verification gaps

- The section is `[INF-docs]` throughout and says so. Nothing here establishes
  that `xdg-terminal-exec` is the binary that runs, nor which Alacritty build is
  executing; those remain runtime claims this note cannot carry, and the note
  states that correctly.
- The host-side step (that `~/.config/xdg-terminals.list` is the
  highest-priority existing selection file) depends on the runtime values of
  `XDG_CONFIG_HOME`, `XDG_CONFIG_DIRS`, `XDG_DATA_DIRS` and
  `XDG_CURRENT_DESKTOP`. Those are environment values, not file bytes, and no
  probe was permitted. Mitigation observed by filename scan: no
  `*-xdg-terminals.list` exists anywhere in `~/.config`, `/etc/xdg`,
  `/usr/share/xdg-terminal-exec` or `/usr/local/share/xdg-terminal-exec`
  (`/usr/local/share/xdg-terminal-exec` does not exist), so no desktop-prefixed
  file can displace the user list *within those trees* regardless of the
  desktop name. A non-default `XDG_CONFIG_HOME` directory would not have been
  searched. The upstream-contract section itself is not affected by this — it
  claims only the documented order.
- `uwsm-app` is outside the section's named sources and is not addressed by it;
  no claim about it was verifiable here.
- The upstream list's exact provenance on this host (which package installed
  `/usr/share/xdg-terminal-exec/xdg-terminals.list`) stays `[UNK]`, as the note
  says; the byte identity with upstream is confirmed.

## Host bytes re-checked (corroboration, outside the named section)

Because the section's chain rests on the Host declaration table, I re-hashed it:
all six SHA-256 values match on disk, and each row's quoted content matches the
bytes as they now stand — `bindings.conf:2` now quotes the full
`--dir="$(omarchy-cmd-terminal-cwd)"` (the truncated form I first read was
corrected mid-review), line 3 matches verbatim,
`~/.config/xdg-terminals.list` is comment/comment/`Alacritty.desktop` and is
byte-identical to `~/.local/share/omarchy/config/xdg-terminals.list`
(`d035da57…`), `Alacritty.desktop:7,14-17` match and the file is byte-identical
to `~/.local/share/omarchy/applications/Alacritty.desktop` (`713703ba…`, S071
exists in `SOURCES.md`), `alacritty.toml` is 28 lines with `:1` matching and
zero `live_config_reload` keys, and `/usr/share/applications/Alacritty.desktop`
has 0 `X-Terminal` keys.

## Installs

None.
