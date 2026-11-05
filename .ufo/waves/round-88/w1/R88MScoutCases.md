# R88MScoutCases — round-88 C1 superseding case set

Seat: scout (authoring seat, no tool access). Scope: author
`.ufo/waves/round-88/controls/mako-cases-r88.json` (schema `mako-cases-r88-v1`) from the
manual and the upstream source alone. No candidate tool was opened or run: the working-tree
`tools/mado-mako.py`, `.ufo/waves/round-88/build/`, and every other seat's file under
`.ufo/waves/round-88/w1/` were left unopened. No counter was run against the candidate or the
base tool over this case file; the counter module was imported only for its schema loader
(`load_cases`) and its `canon`/`carried_count` helpers — no tool execution.

## Deliverable

| item | value |
|---|---|
| file | `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-88/controls/mako-cases-r88.json` |
| schema | `mako-cases-r88-v1` |
| N | 59 (22 carried from r87 + 37 new, ids `c23`..`c59`) — inside the declared 40..64 |
| sha256 | `222d7b014549923d5edc76da877b12bb934643955abd1f29972d324d00f4c1ed` |
| indent | 2-space JSON, one trailing newline |
| top-level `notes` | present (provenance, digests, expectation model) |

## Source digests (all read this round)

| source | sha256 |
|---|---|
| `/usr/share/man/man5/mako.5.gz`, decompressed to `mako.5`, numbered `zcat \| nl -ba` | `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba` (matches the pinned value) |
| upstream `mako` v1.11.0 `criteria.c` | `22767742365ea632351751c46d3d5241c340fcf60f376028eb050797b422d76c` |
| upstream `mako` v1.11.0 `types.c` | `c2f3398d45877c10ae94a61634629c22b1c4c472b526a4963d45f7981c4734de` |
| upstream `mako` v1.11.0 `config.c` | `94c3a4e7b0bc7304dd9011c1e44d91cfffe417fe03aa3fa864205204f968ca12` |
| host `~/.local/share/omarchy/default/mako/core.ini` (read-only) | `255e30c44d49c4195882c6b9ce491cdf9feccccfa803903da5fc18508d76e450` |

Upstream fetched with `curl -sSfL` from `https://raw.githubusercontent.com/emersion/mako/v1.11.0/<file>`.
Only the two `[mode=do-not-disturb]` sections and their lines were copied from the host file into
the fixture; the host's global section and its other sections were not copied.

## Expectation model used (the seat brief's stated contract, cross-checked against upstream)

- `effective` starts from every option's manual `Default:` value; the global section overrides it;
  every **matching** criteria section applies in file order, last occurrence wins per option.
- Values are the strings exactly as written in the config, except the style boolean options
  (`icons`, `markup`, `actions`, `history`, `ignore-timeout`, `invisible`), reported in the manual's
  `0|1` form (manual L266/L311/L545; upstream `config.c` L590-593/L620-621/L648-649 route every
  one of them through `types.c parse_boolean`).
- A refused section contributes no options; a decided mismatch contributes no options and no
  refusal; a supplied-but-differing field decides the section (upstream `criteria.c` L75-141
  `match_criteria` returns false on the first differing field).
- `expect.effective` asserts only the listed keys (the counter's `tool_verdict` checks presence and
  value of those keys only).
- **Robustness choice:** where a refusal is expected, the global section repeats the *manual
  default* of the option the refused section would have set (`anchor=top-right`, `layer=top`), so
  the expectation is identical whether the refusal drops only that section or the whole file.

## Pins table (source lines used)

| source | line | text |
|---|---|---|
| mako.5 | 47 | Includes a config at the specified path. The path must be absolute |
| mako.5 | 170 | Default: monospace 10 |
| mako.5 | 234 | Default: 2 |
| mako.5 | 266 | icons=0\|1 |
| mako.5 | 311 | markup=0\|1 |
| mako.5 | 407 | Default: top |
| mako.5 | 432 | each criteria. If all of the fields match, the style options within will be |
| mako.5 | 443 | app-name (string) |
| mako.5 | 445 | app-icon (string) |
| mako.5 | 447 | summary (string): exact match on the summary of the notification. |
| mako.5 | 450 | summary~ (string): a POSIX extended regular expression match on the summary |
| mako.5 | 461 | category (string) |
| mako.5 | 463 | desktop-entry (string) |
| mako.5 | 465 | actionable (boolean) |
| mako.5 | 467 | expiring (boolean) |
| mako.5 | 510 | boolean values may be specified using any of true/false, 0/1, or |
| mako.5 | 514 | [actionable=true] [actionable=1] [actionable] |
| mako.5 | 516 | [actionable=false] [actionable=0] [!actionable] |
| mako.5 | 545 | invisible=0\|1 |
| mako.5 | 618 | matches. makoctl(1) can be used to change the current mode. |
| mako.5 | 620 | The initial list of modes contains a single mode called "default". |
| mako.5 | 623 | For example, to hide all notifications if the mode "do-not-disturb" is |
| mako.5 | 628 | [mode=do-not-disturb] |
| mako.5 | 629 | invisible=1 |
| criteria.c | 76 | strcmp(criteria->app_name, notif->app_name) != 0 |
| criteria.c | 81 | strcmp(criteria->app_icon, notif->app_icon) != 0 |
| criteria.c | 86 | criteria->actionable == wl_list_empty(&notif->actions)) { |
| criteria.c | 91 | criteria->expiring != (notif->requested_timeout != 0)) { |
| criteria.c | 101 | strcmp(criteria->category, notif->category) != 0 |
| criteria.c | 106 | strcmp(criteria->desktop_entry, notif->desktop_entry) != 0 |
| criteria.c | 111 | strcmp(criteria->summary, notif->summary) != 0 |
| criteria.c | 123 | strcmp(criteria->body, notif->body) != 0 |
| criteria.c | 230 | Unmatched quote in criteria definition |
| criteria.c | 233 | Trailing backslash in criteria definition |
| criteria.c | 267 | bool apply_criteria_field(struct mako_criteria *criteria, char *token) { |
| criteria.c | 283 | if (*key == '!') { |
| criteria.c | 286 | value = "false"; |
| criteria.c | 288 | value = "true"; |
| criteria.c | 332 | } else if (strcmp(key, "summary~") == 0) { |
| criteria.c | 344 | } else if (strcmp(key, "body~") == 0) { |
| criteria.c | 370 | if (!parse_boolean(value, &criteria->actionable)) { |
| criteria.c | 378 | } else if (strcmp(key, "expiring") == 0){ |
| criteria.c | 403 | Invalid boolean criteria field '%s' |
| criteria.c | 405 | Invalid criteria field '%s' |
| types.c | 19 | bool parse_boolean(const char *string, bool *out) { |
| types.c | 20 | if (strcasecmp(string, "true") == 0 \|\| strcmp(string, "1") == 0) { |
| types.c | 23 | } else if (strcasecmp(string, "false") == 0 \|\| strcmp(string, "0") == 0) { |
| types.c | 221 | Unknown criteria field '%s' |
| config.c | 590 | } else if (strcmp(name, "icons") == 0) { |
| config.c | 592 | return spec->icons = |
| config.c | 593 | parse_boolean(value, &style->icons); |
| config.c | 620 | } else if (strcmp(name, "markup") == 0) { |
| config.c | 648 | } else if (strcmp(name, "invisible") == 0) { |

Every pin in the file was checked mechanically: after stripping roff escapes (`\fB`, `\fI`, `\fR`,
`\&`, `\(ti`, `\e`) the quoted text is a substring of the cited source line, and every quote is
≤ 25 words. Checker output: `pin problems: 0`.

## New cases (37): id → behaviour → pin

| id | behaviour | pin |
|---|---|---|
| c23-include-relative-path-refused | relative `include=` refused, target not read (`layer` stays default `top`) | mako.5 line 47 |
| c24-mode-default-section-applies | `[mode=default]` applies with no `--mode` (initial mode list) | mako.5 line 620 |
| c25-default-font-unconfigured | `font` reported at manual default `monospace 10` | mako.5 line 170 |
| c26-default-layer-unconfigured | `layer` reported at manual default `top` | mako.5 line 407 |
| c27-default-border-size-unconfigured | `border-size` reported at manual default `2` | mako.5 line 234 |
| c28-appname-criteria-missing-input-refusal | criteria `app-name` with no `--app-name` → refusal, option not applied | criteria.c line 76 |
| c29-unterminated-quote-header-refusal | unterminated quote in header → refusal, option not applied | criteria.c line 230 |
| c30-app-icon-match | `app-icon` matches → section applied | criteria.c line 81 |
| c31-app-icon-mismatch | `app-icon` differs → section not applied, no refusal | criteria.c line 81 |
| c32-summary-match | `summary` exact match → section applied | criteria.c line 111 |
| c33-summary-mismatch-case-sensitive | `summary` differs only in case → not applied | mako.5 line 447 |
| c34-body-match | `body` exact match → section applied | criteria.c line 123 |
| c35-body-mismatch | `body` differs → not applied | criteria.c line 123 |
| c36-category-match | `category` exact match → section applied | criteria.c line 101 |
| c37-category-mismatch | `category` differs → not applied | criteria.c line 101 |
| c38-desktop-entry-match | `desktop-entry` exact match → section applied | criteria.c line 106 |
| c39-desktop-entry-mismatch | `desktop-entry` differs → not applied | criteria.c line 106 |
| c40-summary-missing-input-refusal | `summary` input not supplied → refusal, option not applied | criteria.c line 111 |
| c41-app-icon-missing-input-refusal | `app-icon` input not supplied → refusal, option not applied | criteria.c line 81 |
| c42-boolean-true-literal | `[actionable=true]`/`[expiring=true]` match true flags → applied | mako.5 line 514 |
| c43-boolean-one-literal | `[actionable=1]`/`[expiring=1]` match true flags → applied | mako.5 line 514 |
| c44-boolean-false-literal | `[actionable=false]`/`[expiring=false]` match false flags → applied | mako.5 line 516 |
| c45-boolean-zero-literal | `[actionable=0]`/`[expiring=0]` match false flags → applied | mako.5 line 516 |
| c46-boolean-bare-word | bare `[actionable]`/`[expiring]` mean true → applied | criteria.c line 288 |
| c47-boolean-negated-bare-word | `[!actionable]`/`[!expiring]` mean false → applied | criteria.c line 286 |
| c48-boolean-uppercase-word | `TRUE`/`FALSE` accepted case-insensitively → applied | types.c line 20 |
| c49-boolean-mixed-case-word | `True`/`FaLsE` accepted case-insensitively → applied | types.c line 23 |
| c50-boolean-invalid-value-refusal | `actionable=yes`/`expiring=maybe` invalid → refusal, options not applied | criteria.c line 370 |
| c51-boolean-mismatching-flag | flag differs → not applied, no refusal | criteria.c line 86 |
| c52-boolean-missing-input-refusal | boolean input not supplied → refusal, options not applied | criteria.c line 86 |
| c53-summary-tilde-refused | `summary~` outside the modelled field set → refusal | mako.5 line 450 |
| c54-style-boolean-true-normalized | `invisible=true` reported as `1` | mako.5 line 545 |
| c55-style-boolean-false-normalized | `markup=false` reported as `0` | types.c line 23 |
| c56-style-boolean-invalid-option-value-refused | `icons=yes` invalid → refusal, default `1` kept | config.c line 593 |
| c57-host-dnd-notify-send-invisible | host DND pair: `notify-send` → `invisible=0` (last matching section wins) | mako.5 line 623 |
| c58-host-dnd-other-app-invisible | host DND pair: another app in dnd mode → `invisible=1` | mako.5 line 628 |
| c59-mismatch-beside-undecided-no-refusal | decided mismatch next to an undecided field → no refusal, section not applied | mako.5 line 432 |

## Coverage map against the seat item's required list

| required | cases |
|---|---|
| (a) relative include= path refused | c23 |
| (b) `[mode=default]` applies with no `--mode` | c24 |
| (c) unconfigured option reported at manual Default (font, layer, border-size) | c25, c26, c27 |
| (d) criteria `app-name` with no `--app-name` → refusal, option not applied | c28 |
| (e) unterminated quote in criteria header → refusal, option not applied | c29 |
| (f) match + mismatch for app-icon / summary / body / category / desktop-entry | c30-31, c32-33, c34-35, c36-37, c38-39 |
| (f) missing-input for ≥2 of them | c40 (summary), c41 (app-icon) |
| (f) summary exact match is case-sensitive | c33 |
| (g) actionable+expiring: `=true`, `=1`, `=false`, `=0`, bare, `!bare`, upper-case, mixed-case, invalid, mismatching, missing | c42-c52 |
| (h) summary~ refused | c53 |
| (i) style booleans true/false → 1/0; invalid boolean option value refused, default kept | c54, c55, c56 |
| (j) host do-not-disturb pair (notify-send and another app) | c57, c58 |
| (k) mismatching field next to an undecided field → no refusal, not applied | c59 |

All 37 new cases are accounted for by that map.

## Constraint compliance

- Every `include=` target stays inside HOME: the only two include values in the whole file are
  `relative.ini` (relative, refused — the case that must exist) and `~/.config/mako/core.ini`
  (carried r87 case c13). No absolute include path is used anywhere.
- New case ids are lowercase `[a-z0-9-]`, unique, and match the counter's `ID_RE`
  (`^[a-z0-9][a-z0-9-]{0,63}$`).
- `args` keys are drawn only from the r88 loader's `ARG_NAMES`
  (`app-name, app-icon, summary, body, category, desktop-entry, urgency, actionable, expiring, mode`);
  `actionable`/`expiring` are `"true"`/`"false"` only; `mode` is a list of strings.
- The 22 round-87 cases are carried byte-equal: `carried_count` from the r88 counter returns
  `(22, 22)`, and an independent comparison of `json.dumps(..., sort_keys=True)` over the raw case
  objects also returns 22/22.
- Every `home_files` key is a safe relative path under HOME (`safe_relpath` accepts them all —
  confirmed by the counter's `load_cases` succeeding).

## Commands run (each exit code)

| command | exit |
|---|---|
| `zcat /usr/share/man/man5/mako.5.gz > $S/mako.5; sha256sum $S/mako.5` | 0 (digest matches the pinned value) |
| `curl -sSfL …/v1.11.0/{criteria.c,types.c,config.c}` + `sha256sum` | 0 (3 files fetched) |
| `python3 $S/gen_cases.py` | 0 (writes the case file) |
| `python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print(len(d["cases"]))' <file>` | 0 → `59` |
| `sha256sum <file>` | 0 → `222d7b014549923d5edc76da877b12bb934643955abd1f29972d324d00f4c1ed` |
| r88 counter `load_cases(raw)` (schema only, no tool run) | 0 → `N = 59`, in 40..64 |
| r88 counter `carried_count(cases, r87_raw)` | 0 → `(22, 22)` |
| independent carried-equality comparison | 0 → `22/22` |
| pin verifier (normalised substring + ≤25 words) | 0 → `pin problems: 0` |
| coverage-matrix verifier | 0 → 28 rows, 37/37 new cases accounted |

## Scratch

`$HYAKU_SCRATCH/mado-r88/R88MScoutCases` (default `/fast/scratch/hyaku`) held the decompressed
manual, the three upstream files, and `gen_cases.py`; removed on exit.

## Notes for the L1

- The case file's sha256 to pin in the freeze is
  `222d7b014549923d5edc76da877b12bb934643955abd1f29972d324d00f4c1ed`.
- `expect.effective` deliberately asserts only the listed keys. If the candidate tool reports the
  full default set, that is consistent with every case here; if it reports a smaller set, the
  listed keys are still the ones the case is about.
- The refusal cases are written so that the global section repeats the manual default of the
  refused section's option. This is deliberate: it makes each refusal case assert "refused and
  not applied" without depending on whether the tool's refusal is scoped to the section or to the
  whole file.
- `summary~` (c53) and `body~` are outside the modelled field set, so they are refused rather than
  matched; c53 pins the manual's own `summary~` line for the field's existence.
- No install or upgrade was performed by this seat (nothing in the task required one); no tooling
  change to record.
