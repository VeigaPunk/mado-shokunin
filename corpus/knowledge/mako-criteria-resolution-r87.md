source: S493 (mako(5) manual text of the installed mako 1.11.0-1; locator /usr/share/man/man5/mako.5.gz, container sha256 17ffc88c9950ba83a60a8d5bdf4cb528ca994adc6ba58e9386a81617b9db1670, decompressed text sha256 f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba), host bytes `~/.config/mako/config` (symlink to the omarchy theme `mako.ini`) and `~/.local/share/omarchy/default/mako/core.ini`
verified-at: 2026-11-05 at [[REV]] (round 87, attempt 1)
recheck: 90d

# mako effective settings for one notification: include chain, criteria, mode

Round 87 frontier-to-core move on the notification-daemon plane. Before this entry, `corpus/knowledge/waybar-walker-plane.md` §4
recorded the mako chain by hand (`core.ini:1-37` read as OBS), but no note resolved the effective value of a
style option for one notification. This entry states the grammar the resolver implements, with the manual line that
decides each rule, and the read-only tool that implements it: `tools/mado-mako.py`.

Scope: read-only resolution over the config bytes a caller names. Not in scope: `makoctl` state (a mode is an input the
caller supplies), D-Bus ownership, a live notification, rendering, and the layout mako computes at runtime.

## 1. Grammar and the manual lines that decide it

| rule | manual line (mako.5) | resolver behaviour |
|---|---|---|
| config path `~/.config/mako/config` or `$XDG_CONFIG_HOME/mako/config` | 16-17 | the caller passes `--config`; the tool does not search |
| `key=value` option lines | 21 | parsed as key=value |
| blank lines and lines beginning with `#` ignored | 24 | ignored; a `#` mid-line is UNSTATED, not treated as a comment |
| `include=` path absolute or starting `~/` | 47-48 | `~/` resolved under `--home`; a relative path is refused, not guessed |
| `include=` default none | 50 | absent include is no include |
| criteria sections `[field=value ...]`, INI-like | 423-428 | parsed into a section; fields space-separated inside one bracket pair |
| all fields of a criteria must match (AND) | 431-433 | a section applies only when every field matches |
| fields not in a criteria are not considered | 433 | a field absent from the header imposes no condition |
| a notification may match any number of criteria | 434 | several sections may apply |
| definition order decides; the last occurrence of a style option wins | 435-437 | the winner is chosen per option key, not per section |
| `app-name` string equality | 443 | exact string equality |
| `urgency` one of low, normal, critical | 459 | exact literal |
| `mode` applies only while the mode is enabled | 469-470 | the mode set is an input; the section applies when the named mode is in it |
| initial mode list contains `default` | 620 | the resolver starts from {default}; deprecation at 621 is noted |
| `makoctl mode -a/-r` changes the set | 633-634 | modelled as the caller-supplied set; not invoked |
| `summary` and `summary~` conflict; `body` and `body~` conflict | 448, 451, 454, 457 | a header naming both members of a pair is refused |
| escaping and quoting in values | 497-508 | values with spaces or `=` are parsed; spaces around `=` are refused (507) |
| boolean spellings `true/false`, `0/1`, bare word, `!field` | 510-518 | `true/false` and `0/1` are values; bare tokens are outside the model and refused |

## 2. Refusals (constructs the resolver names and does not guess)

- a relative `include=` path (47-48);
- a missing or unreadable include target, and a non-regular include target (the manual is silent on both; refused by design);
- an include cycle (the manual is silent on cycles; refused by design);
- an `include=` inside a criteria section (`include` is a global key, 45-50);
- a criteria field outside the modelled set (`summary`, `body`, `grouped`, `actionable`, and the rest of the second-pass
  fields at 443-490), and a repeated field in one header;
- a `summary` with `summary~`, or a `body` with `body~` (448-457);
- bare boolean tokens (510-518);
- an out-of-domain value for an enumerated, integer, directional, colour or action-typed key.

## 3. Do-nothing controls (defined so the claim can fail)

- `naive-toplevel`: reads only the top-level `--config` file's own global key=value lines, ignoring `include=` and every
  section.
- `globals-include`: follows `include=`, applies the global lines of every file reached, ignores every section.

Both controls are implemented in the counter `quality/counters/c1-r87-mako-criteria.py`, not in the tool.

## 4. Host bytes (OBS, read at [[REV]])

- `~/.config/mako/config` is a symlink to `~/.config/omarchy/current/theme/mako.ini`, which holds `include=` and
  three colour keys (`text-color`, `border-color`, `background-color`).
- `core.ini` holds the global options (anchor top-right, default timeout 5000, width 420) and the criteria sections
  `[app-name=Spotify] invisible=1`, `[mode=do-not-disturb] invisible=true`,
  `[mode=do-not-disturb app-name=notify-send] invisible=false`, `[urgency=critical] default-timeout=0 layer=overlay`,
  and several `[summary~="…"]` click-action sections, as recorded in `waybar-walker-plane.md` §4.
- The mode the host is in is read by `makoctl mode` in that note; this entry does not re-read it.

## 5. What the resolver does not certify

- It resolves the grammar the manual states. It does not verify that mako 1.11.0 behaves as the manual says; the
  manual is the stated source and no notification was sent.
- A mode is a caller input. A stale or wrong mode set produces a wrong answer that the tool cannot detect.
- Escaped and quoted values follow 497-508; other quoting forms are refused, not interpreted.
- The `#` mid-line comment question is UNSTATED (see §1); the case set avoids it.

## 6. Unknowns

- Whether `include=` paths are resolved relative to the including file: the manual says absolute or `~/`, so the
  relative form is refused, not modelled.
- Whether a missing include is an error at runtime: UNSTATED.
- The runtime handling of an include cycle: UNSTATED; refused by design here.
- Whether `mode` criteria are re-evaluated on every `makoctl mode` change: UNSTATED beyond 617-618.

## Measurements

[[MEASURE]]
