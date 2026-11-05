source: S493 (mako(5) manual text of the installed mako 1.11.0-1; locator /usr/share/man/man5/mako.5.gz, container sha256 17ffc88c9950ba83a60a8d5bdf4cb528ca994adc6ba58e9386a81617b9db1670, decompressed text sha256 f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba), S494 (upstream mako v1.11.0 source: criteria.c sha256 22767742365ea632351751c46d3d5241c340fcf60f376028eb050797b422d76c, types.c sha256 c2f3398d45877c10ae94a61634629c22b1c4c472b526a4963d45f7981c4734de, config.c sha256 94c3a4e7b0bc7304dd9011c1e44d91cfffe417fe03aa3fa864205204f968ca12, all fetched from https://raw.githubusercontent.com/emersion/mako/v1.11.0/<file>), S495 (path_resolution(7), locator /usr/share/man/man7/path_resolution.7.gz, container sha256 2a21ab674e6f2c51f74c15b3709e2155873734cf867f8ffd2d1b3dec14d41077, decompressed text sha256 2072681115cb012523b968eb243c5ba306ac68fca7f92d9e378949108921dc12), host bytes `~/.config/mako/config` (symlink to the omarchy theme `mako.ini`) and `~/.local/share/omarchy/default/mako/core.ini`
covers: the twelve first-pass criteria fields of mako 1.11.0 and which the round-88 resolver models; the upstream boolean grammar and its style-option consequence; the lane's include-containment stance and its named limits
verified-at: `<L1: measured revision>` (round 88)
recheck: 90d

# mako criteria fields, boolean grammar, and include containment

Round 88 moves the notification-daemon plane from three modelled criteria fields to ten of the twelve the
manual lists, and states a containment stance for `include=`. The read-only resolver is `tools/mado-mako.py`;
its round-87 predecessor modelled `app-name`, `urgency` and `mode` only
(`tools/mado-mako.py` at 24ba2a9ddac21c1211579231e6ee1d98963f9988:75, `MODELLED_FIELDS = ("app-name", "urgency", "mode")`).

Scope: read-only resolution over the config bytes a caller names. Not in scope: `makoctl` state (a mode or a
notification input the caller supplies), D-Bus ownership, a live notification, rendering, and the layout mako
computes at runtime.

## 1. The twelve first-pass fields: what is modelled and what is refused

The manual lists the first-pass fields at L443-469, one bullet each; the second-pass fields start at L474 and are
outside this entry. Upstream `criteria.c` `match_criteria` (61-140) applies one test per field.

| field | manual line | upstream test (criteria.c v1.11.0) | round-88 resolver |
|---|---|---|---|
| `app-name` | 443 | `strcmp` at 76 | modelled (string equality) |
| `app-icon` | 445 | `strcmp` at 81 | modelled (string equality) |
| `summary` | 447 | `strcmp` at 111 | modelled (string equality) |
| `summary~` | 450 | `regexec` POSIX ERE at 116 | **refused** — named limit |
| `body` | 453 | `strcmp` at 123 | modelled (string equality) |
| `body~` | 456 | `regexec` POSIX ERE at 128 | **refused** — named limit |
| `urgency` | 459 | enum compare at 96 | modelled (r87) |
| `category` | 461 | `strcmp` at 101 | modelled (string equality) |
| `desktop-entry` | 463 | `strcmp` at 106 | modelled (string equality) |
| `actionable` | 465 | boolean at 86 (`wl_list_empty(&notif->actions)`) | modelled (boolean) |
| `expiring` | 467 | boolean at 91 (`requested_timeout != 0`) | modelled (boolean) |
| `mode` | 469 | `has_mode` at 155 | modelled (r87) |

Ten of twelve are modelled; `summary~` and `body~` stay refused because the manual names a POSIX extended regular
expression (450, 456) and the resolver does not implement one — Python `re` is not POSIX ERE, so modelling them
with `re` would answer a different question. The refusal is a refusal, never a silent `re` match.

A field whose notification input is not supplied is refused, never guessed: the manual's "Fields not included in
the criteria are not considered" (433) is about the header, not about a missing input, and the resolver keeps the
r87 rule that an undecidable section is refused with the missing input named.

## 2. Boolean grammar: the manual's `0|1`, upstream's `parse_boolean`, and the host's own config

The manual documents boolean criteria values as `true/false`, `0/1` or a bare word, with `!` for negation
(L510-516), and documents every boolean style option as `0|1` (for example `icons=0|1` at 266 and
`invisible=0|1` at 545).

Upstream parses both through one function, `types.c` `parse_boolean` (19-29):

- `strcasecmp(string, "true") == 0` or `strcmp(string, "1") == 0` → true (20);
- `strcasecmp(string, "false") == 0` or `strcmp(string, "0") == 0` → false (23);
- anything else → the parse fails (28).

So the accepted spellings are `true`/`false` in any case and the exact strings `1`/`0` — for criteria fields
(`criteria.c` 369-400 calls `parse_boolean` for `actionable`, `expiring`, `grouped`, `hidden`) and for style
options alike (`config.c` 648-649: `invisible` → `parse_boolean`). A bare criteria token is turned into a value
before parsing: `criteria.c` 283-289 maps `!field` to `"false"` and a bare `field` to `"true"`.

**Consequence the r87 resolver got wrong.** The manual's `0|1` is a documentation shorthand, not the accepted
set — the manual's own do-not-disturb example writes `invisible=1` (L628-629), and the host's config writes the
other accepted spelling for the same option. The host's own do-not-disturb configuration writes `invisible=true` (core.ini:15, section
`[mode=do-not-disturb]`) and `invisible=false` (core.ini:18, section
`[mode=do-not-disturb app-name=notify-send]`). The r87 resolver validated style booleans against `("0", "1")`
only (`tools/mado-mako.py` at 24ba2a9d:113-114, message `expects 0 or 1`), so it refused both lines. Replayed on
this host at that revision, it reports seven refusals, two of them those lines, and resolves `invisible` to `"0"`:
the host's DND state is not resolvable by r87 (`.ufo/waves/round-88/w1/receipt-base-host-config-r88.txt`, base
tool sha256 `67a955a5…`). The round-88 resolver accepts the upstream grammar and still reports the effective value
in the manual's `0|1` form, so the output shape does not change.

The same replay shows the five `[summary~="…"]` click-action sections (core.ini:24, 27, 30, 33, 36) still refused
by round 88: `summary~` is a named limit (§1), so those sections' `on-button-left` bindings remain outside the
model. A caller resolving the host config gets the global style options and the `mode`/`app-name` sections, not the
click actions.

## 3. Include containment: a lane stance, not a mako rule

mako opens any absolute `include=` path (`config.c` 545-548 → `expand_config_path` 505-522, which accepts a leading
`/` or `~/` and refuses anything else); the manual states the same at L45-48 and says nothing about a trust
boundary. Containment is therefore **the lane's stance**, not a mako rule, and the entry says so rather than
implying mako refuses escapes.

Stance: an `include=` target is read only when its fully resolved path (every symlink and `..` resolved) lies
inside a declared read root — `--home` and each `--read-root DIR`; otherwise it is refused before it is stat'ed or
opened, and the resolved path is what is opened. The `--config` file itself is named by the caller and is not
subject to the roots.

Basis, path_resolution(7) (S495):

- a symbolic link component is resolved during the walk, recursively, with a bounded depth and a maximum of 40
  links followed, `ELOOP` beyond (77-99, 105-117);
- `.` and `..` are resolved by convention, and `/..` is `/` (136-145);
- mount points are crossed by ordinary resolution, and `RESOLVE_NO_XDEV` is what would block that traversal —
  including bind mounts (146-161);
- whether the final component's symlink is followed depends on the system call: `lstat` sees the link, `stat` sees
  the target (169-178).

Named limits (each is a limit of the stance, not a claim about mako):

- **TOCTOU.** The containment decision is made on a resolved path, and the open follows it; a component swapped
  between the two steps is not detected. The window is the tool's own runtime, and the tool is read-only, but the
  stance does not close it.
- **Bind mounts and hardlinks are not symlinks.** A bind mount that makes an outside tree appear under a declared
  root resolves to a path inside the root, and a hardlink is the same inode under another name; neither is
  detected by a realpath test. `path_resolution(7)` 146-161 is the basis for the mount half of this limit.
- **The `--config` file is trusted as named.** The caller's own file is not containment-checked; a caller who
  names an outside config has declared it trustworthy by naming it.
- **A refused include is refused, not followed partially.** The tool does not read the target and then discard it.

What `--read-root` changes: it adds one directory to the set of roots an `include=` may resolve into, so a config
tree kept outside `$HOME` (a system-wide or repo copy) can be resolved without widening `--home`. It does not
change the `--config` rule, and it does not make a symlink into an undeclared tree readable.

## 4. Decision table

| question | command (lane root) | what the answer means |
|---|---|---|
| which fields can this resolver decide? | `python3 -I tools/mado-mako.py --help` and §1 above | ten of twelve; a `summary~`/`body~` section is refused, so its options never apply |
| what does the host's DND mode resolve to? | `python3 -I tools/mado-mako.py --config ~/.config/mako/config --home "$HOME" --mode do-not-disturb --app-name notify-send` | the effective `invisible` for a notify-send notification while DND is on; `refusals` lists every line the resolver would not decide |
| is a `true`/`false` style value accepted? | same command; read `refusals` | no refusal for `invisible=true|false` means the upstream grammar was applied; the effective value is still printed `0|1` |
| may this include be read? | same command with `--read-root DIR` added | a refusal naming the include means its resolved path is outside every declared root; adding the root is the caller's decision |
| is the answer about mako or about the lane? | §3 first paragraph | containment is the lane's stance; mako itself opens any absolute include |

## 5. What this entry does not certify

- It resolves the grammar the manual and the upstream source state. It does not verify that the running mako
  behaves as its source says; no notification was sent.
- `summary~` and `body~` are refused, so a host config that relies on them is only partially resolved (the host's
  five click-action sections are in that class).
- A mode is a caller input. A stale or wrong mode set produces a wrong answer that the tool cannot detect.
- The containment stance is not a sandbox: the named limits in §3 stand.

## 6. Unknowns

- Whether `include=` paths are resolved relative to the including file: the manual says absolute or `~/`
  (L47-48) and upstream refuses anything else (`config.c` 510-513), so the relative form is refused, not modelled.
- Whether a missing include is an error at runtime: the manual is UNSTATED; upstream returns the load result
  (`config.c` 547), and the resolver refuses a missing target by design.
- The runtime handling of an include cycle: UNSTATED; refused by design.
- Whether `mode` criteria are re-evaluated on every `makoctl mode` change: UNSTATED beyond L617-618.

## Measurements (round 88)

- C1 (`quality/counters/c1-r88-mako-fields.py`): `<L1: cases, correct, mutants killed, controls, score>`.
- C2 (`quality/counters/c2-r88-include-containment.py`): `<L1: cases, correct, mutants killed, controls, score>`.
- Base-tool host replay: `receipt-base-host-config-r88.txt` (7 refusals, `invisible` resolves to `"0"`), base tool
  sha256 `67a955a5fa06135c2748855b7e452bd3f0792c540002009ec90842ee5c986698`.
