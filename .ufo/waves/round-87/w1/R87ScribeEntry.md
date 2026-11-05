# R87ScribeEntry — draft knowledge entry: mako configuration plane

Seat: R87ScribeEntry (leaf scribe, round 87, wave w1). Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin.
Target: corpus/knowledge/mako-criteria-resolution-r87.md (not written by this seat).
Method: read-only. `zcat /usr/share/man/man5/mako.5.gz` into scratch, `nl -ba`; host bytes via `readlink`, `ls`, `sha256sum`, `stat`, `grep`, `nl -ba`; `pacman -Q mako` and `pacman -Qo` (read-only queries). No makoctl, no D-Bus, no mako process, no live notification. Did not read other seats' reports or the case file.

## Findings for the L1

1. **BLOCKER — pin mismatch.** The frozen declaration (`claims-declaration-r87.md`, C1 Surface, line 28) pins the manual at sha256 `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba`. This host's `/usr/share/man/man5/mako.5.gz` hashes to `17ffc88c9950ba83a60a8d5bdf4cb528ca994adc6ba58e9386a81617b9db1670` (5779 B, mtime 2026-03-26 16:18:04 -0300, owned by `mako 1.11.0-1`). The draft cites the declared pin as the source sha, as the item requires, and states the mismatch in `## Pin status`. The mako.5 line numbers in the draft are for the observed file. The L1 must reconcile the pin before admission.
2. **BLOCKER — registry row absent.** `corpus/SOURCES.md` has zero rows `^| S493` at this read (last row S492, line 444). The declaration assigns the S493 row to the scout. The draft cites S493 and does not write the row.
3. **Scope note for PROVINCE.** The item asks for "reads the named config files only". The C1 spec makes the resolver follow `include=` into `core.ini`. The PROVINCE note therefore reads "the named config files and the `include=` targets they reach". This wording differs from the item by one clause; the L1 decides.
4. **Coverage ceiling (host-visible).** The declared CLI carries `--app-name`, `--urgency`, `--mode` only. Five `summary`/`summary~` criteria sections in omarchy `core.ini` (lines 24–38) therefore fall outside the modelled surface and are refused. This is a property of the declared tool, recorded in the draft's refusal list.
5. **Host state.** No key is defined in both the theme `mako.ini` and `core.ini`. The include-order question (Unknowns U3) therefore changes no value on today's bytes. Verified by grep of key names (OBS).
6. Dead steps: none. Installs: none.

## PROVINCE.md note (one table row, same column format as the existing `tools/mado-*.py` rows)

| `tools/mado-mako.py` | the bytes of the regular config file named by `--config`, the `include=` targets it reaches (absolute or `~/`, `~` = `--home`), and nothing else; `--app-name`, `--urgency`, repeatable `--mode` are caller arguments; no `makoctl`, no D-Bus, no process | nothing — stdout only (one JSON object of effective values and a `refusals` list); the operator applies any change | mado, round 87 (read-only effective-settings resolver for mako 1.11.0 criteria; refuses constructs it does not model; the operator applies changes) |

## corpus/README.md coverage-map row (one table row, same format as the existing rows)

| `knowledge/mako-criteria-resolution-r87.md` | The notification-daemon configuration plane for mako 1.11.0, read from the manual and host bytes only: grammar and precedence of `~/.config/mako/config` and its `include=` chain into omarchy `core.ini`; mode and criteria rules; the resolver's refusal list; the two do-nothing controls; host bytes today (sha-anchored). Effective values are rule-derived and measured by the C1 counter; no live `makoctl` or D-Bus state is claimed. | S493; round-87 frozen controls and receipts |

## Draft entry (the whole text of corpus/knowledge/mako-criteria-resolution-r87.md)

````markdown
source: S493 — mako 1.11.0 configuration manual `mako.5` (scdoc output; package `mako 1.11.0-1`), locator `/usr/share/man/man5/mako.5.gz`, sha256 `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba` (declared pin; host bytes differ, see `## Pin status`); `mako.5:N` below is line N of `zcat /usr/share/man/man5/mako.5.gz`; host bytes at `~/.config/mako/config` and the omarchy `core.ini` named in `## Host bytes today`
verified-at: 2026-11-05 at revision [[REV]]
recheck: 90d

# mako configuration: effective settings for one notification

Tags: MAN = stated in the manual (line cited). INF = derived by a rule in this entry from MAN lines; not observed live. OBS = host bytes (path:line or command). UNK = not stated; the resolver refuses rather than guesses (see `## Unknowns`).

## Scope and boundary

- Owned surface: `~/.config/mako/config`, a symlink to `/home/vgpnk/.config/omarchy/current/theme/mako.ini` (OBS: `readlink -f ~/.config/mako/config`); the theme file's `include=` line chains into `/home/vgpnk/.local/share/omarchy/default/mako/core.ini` (OBS: `mako.ini:1`). The manual names the path at `mako.5:16-17`.
- Read-only. Drafted from the manual and host file bytes. No `makoctl`, no D-Bus call, no mako process, no live notification. Live effective values are UNK.
- Resolver: `tools/mado-mako.py`. It reads the regular config file named by `--config`, the `include=` targets it reaches, and nothing else; `--home` maps `~`. Arguments: `--app-name`, `--urgency {low,normal,critical}`, repeatable `--mode`. Output: one JSON object of effective values and a `refusals` list. It writes nothing.
- C1 counter (run by the L1 at [[REV]]): `python3 -I quality/counters/c1-r87-mako-criteria.py --repo . --rev [[REV]] --cases .ufo/waves/round-87/controls/mako-cases-r87.json --scratch-root DIR`.
- Registry: S493 census before/after `[[CENSUS]]`.

## Grammar

Line numbers are `mako.5:N`.

| Rule | Manual line | What the resolver does |
|---|---|---|
| Config path `~/.config/mako/config` or `$XDG_CONFIG_HOME/mako/config` | 16–17 (MAN) | Reads the path the caller names (`--config`); `~` maps to `--home`. Which path wins when both exist: UNK (U1). |
| Option line `key=value` | 16–18 (MAN) | Splits at `=`; value runs verbatim to end of line. Spaces around `=` on top-level lines: UNK (U7). |
| Empty lines and lines starting with `#` are ignored | 24 (MAN) | Skipped. Inline `#` comments: UNK, refused (U8). |
| Lines before the first `[header]` are the global section; criteria sections follow | 421–422 (MAN) | Global keys form the base layer. |
| Global keys: `max-history`, `sort`, `include`, plus style and binding options | 28–50 (MAN) | Parsed into the base layer. |
| `sort=+/-time` or `+/-priority` | 37–42 (MAN) | Enumerated; any other value refused. |
| `include=PATH`; PATH absolute or starting `~/` | 45–48 (MAN) | `~/` maps to `--home`; the target is read as a regular file. Relative paths refused (U5). Nested includes: UNK (U4). |
| Binding options `on-button-left`, `on-button-middle`, `on-button-right`, `on-touch`, `on-notify` | 59–93 (MAN) | Value kept as an opaque string. |
| Binding actions: `none`, `dismiss [--no-history]`, `dismiss-all`, `dismiss-group`, `invoke-action <action>`, `invoke-default-action`, `exec <command>` | 96–161 (MAN) | Action text kept verbatim. `exec` is never run; the POSIX-shell execution is not modelled (`mako.5:143`). |
| Style options with typed values and defaults | 164–416 (MAN) | Value sets and defaults in `## Defaults`. Values outside a stated set refused (U22). |
| Colours `#RRGGBB` or `#RRGGBBAA` | 555–557 (MAN) | Exactly 6 or 8 hex digits; other forms refused (U24). |
| Directional values: 1 to 4 comma-separated entries | 559–583 (MAN) | 1 → all edges; 2 → vertical,horizontal; 3 → top,horizontal,bottom; 4 → top,right,bottom,left (`mako.5:570-573`). 5 or more refused (U25). |
| `progress-color=[over \| source] COLOR` | 252–263 (MAN) | `over` or `source` attribute plus colour; other attribute refused (U22). |
| Booleans `0`/`1`; in criteria also `true`/`false` and bare words; `!word` negates | 266–270, 510–518 (MAN) | Mapped to 0/1. |
| Criteria header `[field=value field2=value2 ...]` | 425–428 (MAN) | Parsed as a conjunction of fields. |
| Quoting in criteria values: `"..."`; backslash escapes; `\\` is a literal backslash; escaped quotes inside quotes | 497–508 (MAN) | Parsed as stated. The manual's `[app-name=Google\e Chrome]` (line 503) is roff for a backslash; the resolver reads the escape as stated in 506–508 (U26). |
| No spaces around `=` in a criteria header | 507 (MAN) | A header containing spaces around `=` is refused. |
| Format string `format=` | 337–347, 585–612 (MAN) | Kept verbatim. Specifier expansion is performed at display time, not by the resolver; unknown `%` escapes UNK (U27). |

### Criteria fields

| Field | Manual line | Resolver |
|---|---|---|
| `app-name` (string) | 443 (MAN) | Compared to `--app-name`. Comparison type (case, exact): UNK (U12). |
| `urgency` (`low`, `normal`, `critical`) | 459 (MAN) | Compared to `--urgency`. |
| `mode` (string) | 469–471 (MAN) | Modes rule M1. |
| `summary` (exact), `body` (exact) | 447–448, 453–454 (MAN) | No `--summary` or `--body` argument exists: refused as not supplied. |
| `summary~`, `body~` (POSIX extended regex) | 450–451, 456–457 (MAN) | Regex not modelled: refused (U13). |
| `app-icon`, `category`, `desktop-entry`, `actionable`, `expiring` | 445, 461, 463, 465, 467 (MAN) | Not supplied by the caller: refused. |
| `grouped`, `group-index`, `hidden`, `output`, `anchor` (second pass) | 479–491 (MAN) | Grouping is not modelled: refused. |

Field conflicts: `summary` with `summary~`, or `body` with `body~`, in one header is refused (`mako.5:447-448`, `453-457`).

## Precedence

- P1 (MAN, INF). Values for one notification are layered in this order: (a) built-in defaults (`## Defaults`); (b) global-section keys override defaults (`mako.5:520-522`); (c) every criteria section whose fields all match applies, in file order; when several set the same style option, the last occurrence wins (`mako.5:431-437`).
- P2 (MAN). Three criteria sit at the front of the list: the empty criteria (defaults overwritten by global keys, `520-522`), `[grouped]` and `[group-index=0]` (`524-528`). The last two depend on grouping; grouping is not modelled, so their effect is not reported.
- P3 (MAN). Two passes per notification; second-pass criteria cannot reposition a notification (`494-495`).
- P4 (UNK). Whether a key present in both the included file and the including file is overridden, and in which direction, depends on the include processing order, which the manual does not state (U3). On today's bytes no key is in both (OBS, see `## Host bytes today`), so P4 does not change any host value.
- P5 (UNK). Duplicate top-level keys within one file: the manual states last-wins only for criteria (`435-437`) (U9).

## Modes

- M1 (MAN). `[mode=X]` applies only if X is currently enabled (`mako.5:469-471`). It conjoins with the other fields (`431-433`).
- M2 (INF). The enabled set is exactly the caller's `--mode` values. The resolver never reads `makoctl` state.
- M3 (MAN, UNK). The initial list "contains a single mode called `default`", deprecated, and "in a future version the initial list of modes will be empty" (`mako.5:620-621`). Whether `default` is enabled before any `makoctl` change is UNK (U16). A `[mode=default]` header is therefore refused until measured.
- M4 (MAN). `makoctl mode -a X` enables and `-r X` disables a mode at runtime (`mako.5:633-634`). Not modelled.
- M5 (MAN). Example from the manual: `[mode=do-not-disturb]` with `invisible=1` hides all notifications while the mode is enabled (`mako.5:623-631`). `invisible=true` is an equivalent boolean spelling (`510-516`).

## Refusal list

The resolver refuses, and does not guess, these constructs. A refused construct is listed in `refusals` with its file line. The keys a refused section would set are not reported as effective values.

| # | Construct | Basis |
|---|---|---|
| R1 | `include=` path neither absolute nor `~/` | `mako.5:47-48` |
| R2 | criteria field the caller does not supply (`summary`, `body`, `app-icon`, `category`, `desktop-entry`, `actionable`, `expiring`) | `mako.5:443-467`, caller args `--app-name`/`--urgency`/`--mode` only |
| R3 | second-pass fields `grouped`, `group-index`, `hidden`, `output`, `anchor` in a header | `mako.5:474-491` |
| R4 | `summary~` or `body~` (regex) | `mako.5:450-451`, `456-457` (U13) |
| R5 | `summary` with `summary~`, or `body` with `body~`, in one header | `mako.5:447-457` |
| R6 | criteria matching `grouped` or `group-index` that set `anchor`, `output` or `group-by` | `mako.5:534-536` |
| R7 | `invisible` in the global section | `mako.5:545-552` (criteria-only) |
| R8 | `max-history`, `sort` or `include` in a criteria header | `mako.5:421-423`, `439-471` (U10) |
| R9 | `[mode=default]` | `mako.5:620-621` (M3) |
| R10 | unknown key, unknown field, or value outside an enumerated set | UNK (U6, U22) |
| R11 | spaces around `=` in a criteria header | `mako.5:507` |
| R12 | colour with other than 6 or 8 hex digits; directional value with 5 or more entries | `mako.5:557`, `559-583` (U24, U25) |
| R13 | `exec` or `invoke-action` payload evaluated by the resolver | never run: `mako.5:139-149` |
| R14 | integer px or ms field with a non-integer value | `mako.5:187-199`, `355-360` (U23) |
| R15 | inline `#` comment, or an unclosed `[` header | `mako.5:24` (U8) |

## Do-nothing controls

Defined in the frozen declaration (`claims-declaration-r87.md`, C1 "Do-nothing controls"). Each must score strictly below N in the counter.

- `naive-toplevel`: reads only the `--config` file. It ignores `include=` and every criteria section. Output: top-level keys over defaults.
- `globals-include`: follows `include=` and applies global keys from both files. It ignores every criteria section.

Neither control applies the mode or criteria rules P1–P3 or M1–M3. Their scores are in `## Measurements`.

## Defaults

Default values as stated by the manual (MAN). Line numbers are `mako.5:N`.

| Option | Default | Line |
|---|---|---|
| `max-history` | 5 | 34 |
| `sort` | -time | 42 |
| `include` | none | 50 |
| `on-button-left` | invoke-default-action | 63 |
| `on-button-middle` | none | 70 |
| `on-button-right` | dismiss | 77 |
| `on-touch` | dismiss | 84 |
| `on-notify` | none | 91 |
| `font` | monospace 10 | 170 |
| `background-color` | #285577FF | 177 |
| `text-color` | #FFFFFFFF | 184 |
| `width` | 300 | 191 |
| `height` | 100 | 199 |
| `outer-margin` | 0 | 208 |
| `margin` | 10 | 219 |
| `padding` | 5 | 227 |
| `border-size` | 2 | 234 |
| `border-color` | #4C7899FF | 241 |
| `border-radius` | 0 | 249 |
| `progress-color` | over #5588AAFF | 263 |
| `icons` | 1 | 270 |
| `max-icon-size` | 64 | 277 |
| `icon-path` | "" | 293 |
| `icon-location` | left | 301 |
| `icon-border-radius` | 0 | 308 |
| `markup` | 1 | 317 |
| `actions` | 1 | 325 |
| `history` | 1 | 334 |
| `format` | `<b>%s</b>\en%b` (grouped: `(%g) <b>%s</b>\en%b`) | 343, 345 |
| `text-alignment` | left | 352 |
| `default-timeout` | 0 (ms; 0 disables) | 360 |
| `ignore-timeout` | 0 | 368 |
| `group-by` | none | 378 |
| `max-visible` | 5 (-1: all visible) | 386 |
| `output` | "" | 397 |
| `layer` | top | 407 |
| `anchor` | top-right | 416 |
| `invisible` | 0 (criteria-only) | 552 |

## Precedence and host values: summary

On this host the effective `width` is 420, not the default 300: `core.ini:4` overrides `mako.5:191`. The same holds for `default-timeout` (core.ini:3 gives 5000 over `mako.5:360`), `outer-margin` (core.ini:5 gives 20 over `mako.5:208`), `padding` (core.ini:6 gives 10,15 over `mako.5:227`), `max-icon-size` (core.ini:8 gives 32 over `mako.5:277`), and `font` (core.ini:9 gives sans-serif 14px over `mako.5:170`). These are global-layer overrides (P1 layer b) and do not depend on the include-order question.

## Host bytes today

Observed 2026-11-05 by read-only commands. Anchors are host path:line or the command shown.

| File | Bytes | sha256 | Anchor |
|---|---|---|---|
| `~/.config/mako/config` | symlink; target below | — | `readlink -f`; `ls -la ~/.config/mako/` |
| `/home/vgpnk/.config/omarchy/current/theme/mako.ini` | 119 | `95bf0c86c955cc813d1b60d18e738567c7f135885c5f02a6acfbbb38946e3bec` | `mako.ini:1,3,4,5` |
| `/home/vgpnk/.local/share/omarchy/default/mako/core.ini` | 1053 | `255e30c44d49c4195882c6b9ce491cdf9feccccfa803903da5fc18508d76e450` | `core.ini:1-38` |

Theme file (`mako.ini`):

- `:1` `include=~/.local/share/omarchy/default/mako/core.ini` (MAN: `~/` form, `mako.5:48`).
- `:3` `text-color=#bebebe`; `:4` `border-color=#e68e0d`; `:5` `background-color=#121212` (six-digit colours, `mako.5:557`). No criteria sections (OBS).

Default layer `core.ini` (lines with rule annotations):

| Lines | Content | Resolver status |
|---|---|---|
| 1–9 | globals: `anchor=top-right` (1, default), `group-by=app-name,summary,body` (2), `default-timeout=5000` (3), `width=420` (4), `outer-margin=20` (5), `padding=10,15` (6), `border-size=2` (7, default), `max-icon-size=32` (8), `font=sans-serif 14px` (9) | Modelled (P1 b). `group-by` makes grouping possible; grouped state unmodelled (R3). |
| 11–12 | `[app-name=Spotify] invisible=1` | Modelled (`app-name` supplied). |
| 14–15 | `[mode=do-not-disturb] invisible=true` | Modelled (M1). |
| 17–18 | `[mode=do-not-disturb app-name=notify-send] invisible=false` | Modelled (M1, field conjunction). INF: with `do-not-disturb` and `notify-send`, `invisible=0` wins over line 15 by last-occurrence (`mako.5:435-437`). Not observed live. |
| 20–22 | `[urgency=critical] default-timeout=0 layer=overlay` | Modelled. `layer=overlay` may still show at `top` depending on compositor (`mako.5:403-405`, UNK U31). |
| 24–25 | `[summary~="Setup Wi-Fi"] on-button-left=exec ...` | Refused: R2/R4. |
| 27–28 | `[summary~="Update System"] on-button-left=exec ...` | Refused: R4. |
| 30–31 | `[summary~="Learn Keybindings"] on-button-left=exec ...` | Refused: R4. |
| 33–34 | `[summary~="Install Dictation with Voxtype"] on-button-left=exec ...` | Refused: R4. |
| 36–38 | `[summary~="Screenshot copied & saved"] max-icon-size=80 format=<b>%s</b>\n%b` | Refused: R4. `\n` is the manual's new-line escape (`mako.5:594`). |

Key overlap: the key names in `mako.ini` (`include`, `text-color`, `border-color`, `background-color`) do not appear in `core.ini` (OBS: `grep -o '^[a-z-]*='` on both files).

Package: `pacman -Q mako` → `mako 1.11.0-1`; `pacman -Qo /usr/share/man/man5/mako.5.gz` → owned by `mako 1.11.0-1` (OBS, read-only query).

## Pin status

- Declared pin (frozen declaration, C1 Surface): `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba`.
- Observed 2026-11-05 (`sha256sum /usr/share/man/man5/mako.5.gz`): `17ffc88c9950ba83a60a8d5bdf4cb528ca994adc6ba58e9386a81617b9db1670`; 5779 B; mtime 2026-03-26 16:18:04 -0300.
- **Open: the declared pin does not match the observed file.** Every `mako.5:N` line in this entry is for the observed file. Admission is blocked until the pin is reconciled.
- The `source:` row S493 is not present in `corpus/SOURCES.md` at drafting time (OBS: `grep -c '^| S493'` → 0).

## Measurements

[[MEASURE]]
[[MEASURE]]
[[MEASURE]]
[[MEASURE]]

## Unknowns

Every point the manual leaves unstated, and the rule the resolver takes in its place. All are UNK; the resolver refuses rather than guesses.

- U1. Which of `~/.config/mako/config` and `$XDG_CONFIG_HOME/mako/config` wins when both exist (`mako.5:16-17`).
- U2. Whether mako itself expands `~` and how `$XDG_CONFIG_HOME` is read (`mako.5:16-17`, `48`). Observed here: `XDG_CONFIG_HOME=/home/vgpnk/.config` (OBS, shell env).
- U3. Processing order of an `include=` line relative to keys in the including file (`mako.5:45-50`).
- U4. Whether `include=` is recursive, how cycles are handled, and whether it may sit inside or after a criteria section (`mako.5:45-50`, `419-430`).
- U5. Behaviour of a relative `include=` path; only the requirement is stated (`mako.5:47-48`).
- U6. Behaviour for unknown keys, unknown field names and unknown enumerated values (silent).
- U7. Whether spaces are allowed around `=` on top-level lines. `mako.5:581` shows `margin = 10,20,5`; `507` forbids spaces only in criteria.
- U8. Inline `#` comments and comments after a value (`mako.5:24` covers whole lines only).
- U9. Which occurrence of a duplicate top-level key wins (`mako.5:435-437` covers criteria only).
- U10. Whether `max-history`, `sort` and `include` may appear in a criteria header (`mako.5:421-423`, `439-471` silent).
- U11. Whether an empty header `[]` is valid, and whether a field may repeat within one header (silent).
- U12. Comparison type for `app-name` and `urgency` (exact or case-insensitive). `summary` and `body` are stated exact (`mako.5:447-454`); the others are not (`443`, `459`).
- U13. Regex flavour details and anchoring for `summary~` and `body~`: the manual says POSIX extended only (`mako.5:450-451`, `456-457`).
- U14. Whether `summary` with `summary~` is rejected or the first is used (`mako.5:447-448` states only the conflict).
- U15. Whether `urgency` values outside `low`, `normal`, `critical` are rejected (`mako.5:459`).
- U16. Whether `default` is enabled before any `makoctl` change (`mako.5:620-621`).
- U17. Mode-name matching: case, whitespace, and multiple `mode=` fields in one header (`mako.5:469-471`, `616-618` silent).
- U18. Whether runtime mode state survives a mako restart (silent).
- U19. Value applied by `[grouped]` and `[group-index=0]` when grouping is off (`mako.5:524-528`).
- U20. Meaning of the `group-by` default text `none` (`mako.5:378`), and the matching rule beyond "exactly equal" (`371-376`).
- U21. How criteria on `anchor` or `output` compare against the first-pass value (`mako.5:487-491` silent on comparison).
- U22. Behaviour for values outside enumerated sets: `anchor` (`413-415`), `layer` (`402-405`), `text-alignment` (`348-352`), `icon-location` (`298-301`), `sort` (`39-42`), `progress-color` attribute (`252-258`).
- U23. Units: whether `width`, `height`, `margin`, `font` accept units other than px or pt (`mako.5:164-199`); whether `default-timeout` accepts units other than ms (`355-357`).
- U24. Whether short hex (`#RGB`) or named colours are accepted (`mako.5:555-557` gives two forms only).
- U25. Behaviour of directional values with 5 or more entries, or with whitespace separators (`mako.5:559-583`).
- U26. Escape semantics inside criteria values beyond what `mako.5:506-508` states; the manual's example at `503` is roff, not the raw character.
- U27. Format-specifier handling of unknown `%` escapes (`mako.5:585-612`).
- U28. What "opened" means for `on-notify` (`mako.5:87-89`).
- U29. `icon-path` search beyond the one sentence on the search (`mako.5:280-293`).
- U30. Out-of-range `progress` hint values (`mako.5:259-261` gives 0–100 inclusive only).
- U31. Whether `layer=overlay` shows above fullscreen windows is compositor-dependent (`mako.5:403-405`).
- U32. Whether `output` needs `xdg-output-unstable-v1` version 2 in the compositor (`mako.5:389-397`), and what happens without it.
- U33. Whether the manual body describes exactly mako 1.11.0. The manual's date line is `.TH "mako" "5" "2026-03-26"` (`mako.5:8`); the package link is host evidence only (`pacman -Qo`).
- U34. Timing of the "future version" change to an empty initial mode list (`mako.5:620-621`).
- U35. Interaction of `ignore-timeout` with a criteria `default-timeout` (`mako.5:355-368`).
- U36. Whether a matched criteria section may set `on-*` bindings, and when a bound `exec` fires (`mako.5:59-161` silent on criteria).
- U37. Whether `text-color`, `background-color` and `border-color` are valid inside criteria (MAN lists style options generally at `164-416`; no statement on criteria validity per key).
````
