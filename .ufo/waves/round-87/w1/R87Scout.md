# R87Scout — mako(5) grammar digest and frozen C1 case set

Seat: R87Scout (scout), round 87 (hyaku run 15), wave 1.
Scope: pin the mako configuration grammar from the installed manual; author the frozen C1 case
set from the manual alone. No tool bytes were read (independence rule 5 honoured — I did not
open `tools/mado-mako.py` nor any other seat's round-87 file).

## 1. Source pinning

| item | value |
|---|---|
| package | `mako 1.11.0-1` (`pacman -Q mako`, read-only query, exit 0) |
| installed file | `/usr/share/man/man5/mako.5.gz` (only mako man page on the host) |
| **sha256 of `/usr/share/man/man5/mako.5.gz`** | `17ffc88c9950ba83a60a8d5bdf4cb528ca994adc6ba58e9386a81617b9db1670` |
| **sha256 of the decompressed manual** | `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba` |
| decompressed size | 17209 bytes, 644 lines (numbered with `nl -ba "$S/mako.5"`) |
| package integrity | `pacman -Qkk mako` → `mako: 33 total files, 0 altered files`; `pacman -Qi` → `Validated By: SHA-256 Sum  Signature` |

**Pin discrepancy (important — does not change the outcome).** The item asked me to verify
`sha256sum /usr/share/man/man5/mako.5.gz == f717848f…`. It does **not**: the `.gz` container
hashes to `17ffc88c…`. The value `f717848f…` is the digest of the **decompressed** manual
(`zcat … | sha256sum`), i.e. the pinned artifact is the manual *text*, not the gzip wrapper.
This is not tampering: `gzip -9 -n` of the decompressed text reproduces the installed `.gz`
**byte-for-byte** (`cmp` → identical), so the two digests are two views of one artifact. The
declaration's wording ("the host's installed mako 1.11.0 manual `/usr/share/man/man5/mako.5.gz`,
sha256 `f717848f…`") is therefore off by one layer of gzip: the digest it names belongs to the
man page source, not to the `.gz` file whose path it cites.

**Action for the L1:** the S493 row (and the C1 surface sentence) should quote the digest of the
manual *content* `f717848f…` and, if the `.gz` path is cited, cite the container digest
`17ffc88c…` alongside it — or cite the container path with the content digest and label the
scope "mako(5) manual text, mako 1.11.0-1". The *content* the grammar was read from is pinned
and verified; the S493 quote below uses the declaration's digest, which is the content digest.

Method: `zcat /usr/share/man/man5/mako.5.gz > "$S/mako.5"`, `nl -ba "$S/mako.5"` for line
numbers, and `groff -mandoc -Tutf8` rendering to disambiguate scdoc escapes (`\fB`, `\fI`,
`\(ti` → `~`, `\e` → backslash-space). All quotes below are checked against the numbered
source lines.

## 2. Grammar digest (every rule the tool must implement)

Line numbers are of the decompressed `mako.5`. Quotes are ≤ 25 words.

### 2.1 File location and top-level syntax

| rule | line | quote |
|---|---|---|
| config path | 16 | "The config file is located at ~/.config/mako/config or at" (XDG_CONFIG_HOME variant at 17) |
| option line form | 21 | "key=value" |
| comments and blank lines | 24 | "Empty lines and lines that begin with # are ignored." |

Line 24 states only that lines *beginning* with `#` are ignored. Whether a `#` mid-line starts
a comment is **not stated** — my case set only uses whole-line comments.

### 2.2 Global configuration options (top-of-file, before any section)

`max-history=n` (28; default 5, line 34), `sort=+/-time | +/-priority` (37; default `-time`,
42), `include=config path` (45; default none, 50). Line 45-50:

| rule | line | quote |
|---|---|---|
| include semantics | 47 | "Includes a config at the specified path. The path must be absolute" |
| include path form | 48 | "or otherwise start with ~/." |
| include default | 50 | "Default: none" |

The include path must be **absolute or start with `~/`** (48). The manual does **not** state
whether a relative path is relative to the including file's directory, nor what happens on a
missing target — see UNSTATED §4.

### 2.3 Criteria sections (INI-like)

| rule | line | quote |
|---|---|---|
| sections are criteria | 423 | "BINDING OPTIONS and STYLE OPTIONS. The sections, called criteria, are" |
| section syntax | 424 | "defined with an INI-like square bracket syntax. The brackets may contain any" |
| field list form | 428 | "[field=value field2=value2 ...]" |

A section header is `[field=value field2=value2 …]` (428): fields are space-separated inside one
bracket pair, each `name=value`. Section bodies hold BINDING OPTIONS and STYLE OPTIONS (423).

### 2.4 Matching semantics — AND, and what "match" means

| rule | line | quote |
|---|---|---|
| comparison | 431 | "When a notification is received, it will be compared to the fields defined in" |
| **AND** | 432 | "each criteria. If all of the fields match, the style options within will be" |
| unspecified fields ignored | 433 | "applied to the notification. Fields not included in the criteria are not" |
| multiple matches allowed | 434 | "considered during the match. A notification may match any number of criteria." |

**Combined criteria are AND, not OR** (432: "If **all** of the fields match"). Fields absent
from a criteria are not considered (433). A notification may match any number of criteria (434).

### 2.5 Precedence when several criteria match

| rule | line | quote |
|---|---|---|
| definition order | 435 | "This matching occurs in the order the criteria are defined in the config file," |
| last-wins | 436-437 | "meaning that if multiple criteria match a notification, the last occurrence of" / "any given style option will \"win\"." |

**Later-defined criteria win per style option** (435-437): the winner is decided *per key*, so a
later section that sets `output` does not erase an earlier section's `layer`. This per-option
granularity is what my cases c09 and c21 pin down.

### 2.6 Criteria field names and how each matches

| field | line | quote | match rule |
|---|---|---|---|
| app-name | 443 | "app-name (string)" | string equality of the notification's app name (no regex/exact qualifier is printed for this field, unlike summary) |
| summary | 447 | "summary (string): exact match on the summary of the notification. This" | exact |
| summary~ | 450 | "summary~ (string): a POSIX extended regular expression match on the summary" | POSIX ERE |
| urgency | 459 | "urgency (one of \"low\", \"normal\", \"critical\")" | one of three literals |
| mode | 469-470 | "mode (string): only apply style options in this section if the provided" / "mode is currently enabled." | gate: see §2.7 |

Also present but out of the C1 surface: `app-icon` (445), `body` (453), `body~` (456),
`category` (461), `desktop-entry` (463), `actionable` (465), `expiring` (467); second-pass
fields `grouped` (479), `group-index` (481), `hidden` (484), `output` (487), `anchor` (490);
boolean field spellings `true/false`, `0/1`, bare word, `!field` (510-518).

**Conflicts the manual states outright:** `summary` "conflicts with `summary~`" (448, and
`summary~` "conflicts with `summary`", 451); `body` conflicts with `body~` (454, 457). A
criteria naming both members of a conflicting pair is invalid by the manual's own words — this
is the one construct in my set that is a genuine refusal case (c22).

### 2.7 Mode criteria and makoctl

| rule | line | quote |
|---|---|---|
| mode is a gate | 616-617 | "mako supports applying style options conditionally via modes. A configuration" / "section with a mode criteria will only be applied if the current mode" |
| makoctl changes it | 618 | "matches. makoctl(1) can be used to change the current mode." |
| initial mode list | 620 | "The initial list of modes contains a single mode called \"default\". This is" |
| deprecation | 621 | "deprecated, in a future version the initial list of modes will be empty." |
| enabling a mode | 633 | "makoctl mode -a do-not-disturb will hide all notifications," |
| disabling a mode | 634 | "-r do-not-disturb will show them again." |

The mode list is a **set of enabled modes** (`-a` adds, `-r` removes; initial list contains
"default", 620). A section with a `mode` field applies only while that mode is enabled
(469-470, 617-618). So a `[mode=X]` section is a conjunction of "the mode is currently
enabled" and the other fields of the section (my c19/c20 pin the combined `app-name` + `mode`
case; c18 pins membership among several enabled modes).

### 2.8 Value quoting and escaping

| rule | line | quote |
|---|---|---|
| escape or quote | 497-498 | "If a field's value contains special characters, they may be escaped with a" / "backslash, or quoted:" |
| quoted example | 501 | "[app-name=\"Google Chrome\"]" |
| escaped example | 503 | "[app-name=Google\ Chrome]" |
| nested quotes / literal backslash | 506-507 | "Quotes within quotes may also be escaped, and a literal backslash may be" / "specified as \\." |
| **no spaces around `=`** | 507 | "No spaces are allowed around the equal sign." |
| `=` inside a value needs no escape | 507-508 | "Escaping equal signs within values is unnecessary." |

Two consequences the tool must implement: (i) a value may be quoted or backslash-escaped, and
the escapes are removed before comparison (497-498, 501, 503); (ii) `=` occurring *inside* a
value is literal and must not be treated as another field separator (507-508) — hence
`[app-name=foo=bar]` is one field whose value is `foo=bar`.

### 2.9 The always-present criteria

| rule | line | quote |
|---|---|---|
| three criteria always first | 519 | "There are three criteria always present at the front of the list:" |
| empty criteria = defaults + global section | 522-523 | "An empty criteria which matches all notifications and contains the defaults" / "for all style options, overwritten with any configured in the global section." |
| override them | 531 | "These options can be overridden by simply defining the criteria yourself and overriding them." |

The empty criteria matches **every** notification and carries the defaults for all style
options, overwritten by the global section (522-523). Practical consequence: a notification that
matches no user criteria still gets the global-section values — that is why my c03/c05/c12/c20
expect the global `anchor` rather than an empty map.

### 2.10 Defaults the tool may need

Style-option defaults are printed in the manual next to each option (e.g. `width` 300 at 191,
`height` 100 at 199, `border-size` 2 at 234, `border-color` `#4C7899FF` at 241, `background-color`
`#285577FF` at 177, `text-color` `#FFFFFFFF` at 184, `icons` 1 at 270, `max-icon-size` 64 at 277,
`font` `monospace 10` at 170, `format` `<b>%s</b>\en%b` at 343, `text-alignment` left at 352,
`default-timeout` 0 at 359, `ignore-timeout` 0 at 367, `group-by` none at 378, `max-visible` 5 at
386, `output` `""` at 397, `layer` top at 407, `anchor` top-right at 416, `icon-path` `""` at 293,
`icon-location` left at 301, `icon-border-radius` 0 at 308, `markup` 1 at 318, `actions` 1 at 325,
`history` 1 at 334, `progress-color` `over #5588AAFF` at 263, `outer-margin` 0 at 208,
`margin` 10 at 219, `padding` 5 at 227, `border-radius` 0 at 249, `invisible` 0 at 552,
`max-history` 5 at 34, `sort` `-time` at 42).

My cases deliberately assert **only keys the fixture sets** (plus the global-section key), so a
default-valued key never appears in an `expect.effective` map unless the fixture set it. This
keeps every expectation derivable from the fixture text and one pinned manual line, and keeps
the comparison type-stable (all asserted values are strings).

### 2.11 What the manual says about invalid keys and errors

The manual **never** describes an error-reporting mechanism. The only normative statements
about invalid constructs are:

- 47-48: the include path "must be absolute or otherwise start with ~/".
- 507: "No spaces are allowed around the equal sign."
- 448 / 451 / 454 / 457: `summary`/`summary~` and `body`/`body~` conflict.
- 535-537: criteria matching `grouped` or `group-index` "are not allowed to change the anchor,
  output, or group-by, as this would invalidate the grouping."

There is no sentence anywhere in the manual containing "error", "invalid", "unknown",
"unrecognized", "warn" or "fail" (grepped the whole file). Hence the tool's `refusals` list is a
**tool-side convention** (the tool spec says it "Refuses, never guesses"), not a manual-defined
output. My case set therefore marks `refusals: "present"` only for c22, where the manual states
the conflict outright (448). Everything else is `refusals: "none"`.

## 3. UNSTATED (the manual does not say it — not filled from memory)

1. **app-name matching mode.** 443 prints `app-name (string)` with no "exact match" /
   "POSIX extended regular expression" qualifier, unlike summary (447) and summary~ (450).
   The manual does not state whether app-name is compared literally or as a regex, nor whether
   it is case-sensitive. My cases use plain literals (`alpha`, `beta`, `Google Chrome`,
   `foo=bar`) that behave identically under either reading.
2. **Include resolution base.** 47-48 fix the path *form* (absolute or `~/`) but not whether a
   relative path is resolved against the including file's directory, nor the behaviour when the
   target is missing, unreadable, or a directory.
3. **Include ordering vs. file order.** Whether the included file's sections participate in the
   "order the criteria are defined in the config file" sequence (435) is not stated. The
   declaration's own `globals-include` control follows includes for *global* keys only, which
   suggests the lane treats included files as contributing globals — but that is the counter's
   model, not the manual's words.
4. **Which file wins on conflict.** The manual states last-occurrence-wins *within* the config
   file (435-437). It says nothing about a value in the including file overriding the same value
   in an included file. My cases avoid that question: c13 has the two files set **different**
   keys (`anchor` in the including file, `output` in the included one), so no precedence claim is
   smuggled in. The item asked for "a value set by the including file overriding the included one
   only where the manual says so" — the manual does not say so, so no such case exists.
5. **Whether the mode list is a set or a stack**, and whether "default" is enabled implicitly
   when a config is read outside `makoctl`. 620-621 and 633-634 imply a set with add/remove, but
   the default-mode question is not settled by the text. My cases always state the enabled modes
   explicitly through `modes`, so no case depends on it.
6. **Grouping / second-pass fields** (474-495) are a two-pass mechanism whose interaction with a
   single-notification resolution is not spelled out.
7. **Comment syntax in the global section vs. inside a section**, and whether `#` may appear
   mid-line (only "lines that begin with #" is stated, line 24).
8. **Trailing whitespace, duplicate keys within one section, and `key = value` in the global
   section.** Line 507's "no spaces around the equal sign" is stated inside the criteria
   discussion; the manual does not say whether the same rule governs top-level `key=value` lines.
9. **Empty criteria header `[]`** and **an empty value** (`key=`) are not addressed.

## 4. The frozen case set

File: `.ufo/waves/round-87/controls/mako-cases-r87.json`
schema `mako-cases-r87-v1`, **N = 22 cases** (counter accepts 20–24), sha256 of the written file
`0a9558743a721f70bb64b48d188b375f1468a140b00ca75ac93ab59c316d5fe3`.

Each case carries its own HOME fixture (`home_files`), its own `--config` path relative to HOME,
the notification fields, the expected `effective` map, and a `pin` naming one manual line and a
≤ 25-word quote. Every pin was re-verified programmatically as a verbatim substring of that
`nl -ba` line of `mako.5` (all 22 match; max quote length 14 words).

| id | what it pins | manual pin |
|---|---|---|
| c01-global-section-values | global section applies to every notification | 523 |
| c02-criteria-overrides-global | a matching criteria section overrides the global value | 437 |
| c03-no-criteria-matched | no criteria matched → global value stands | 432 |
| c04-urgency-critical-matches | `urgency=critical` matches | 459 |
| c05-urgency-critical-not-matched | `urgency=critical` does not match a normal notification | 432 |
| c06-urgency-low-matches | `urgency=low` matches | 459 |
| c07-mode-criteria-active | mode enabled → section applies | 618 |
| c08-mode-criteria-inactive | mode not enabled → section does not apply | 470 |
| c09-two-sections-per-option-last-wins | last-wins is **per option**, not per section | 437 |
| c10-two-sections-only-first-matches | a non-matching later section does not apply | 435 |
| c11-combined-fields-all-match | combined criteria are AND (both match) | 432 |
| c12-combined-fields-one-miss | combined criteria are AND (one misses) | 432 |
| c13-include-globals-under-home | `~/`-relative include resolved under HOME | 47 |
| c14-comments-and-blank-lines | `#` lines and blank lines ignored | 24 |
| c15-quoted-field-value | quoted field value | 501 |
| c16-backslash-escaped-space | backslash-escaped field value | 503 |
| c17-equal-sign-inside-value | `=` inside a value is literal | 508 |
| c18-mode-criteria-among-several-modes | mode membership among several enabled modes | 469 |
| c19-combined-mode-and-app-name | mode gate + app-name, both satisfied | 432 |
| c20-combined-mode-and-app-name-mode-inactive | mode gate + app-name, mode inactive | 470 |
| c21-two-matching-sections-last-wins | later of two matching sections wins | 436 |
| c22-refusal-summary-conflicts-summary-tilde | manual-named conflict → refusal | 448 |

Design notes for the tool author:

- **The two do-nothing controls score strictly below N.** I re-implemented the counter's
  `naive_values` and `globals_values` readers (as a scratch re-implementation, not by running
  the counter) and scored them against this case set: `naive_correct = 7`, `globals_include_correct
  = 8`, against N = 22. Both are strictly below N, as the predicate requires. The controls fail
  c02–c07, c09–c13, c15–c19, c21–c22 (criteria sections, mode gating, quoting and refusals) and
  pass only the cases whose answer the global section alone already gives.
- **Every asserted value is a literal in the fixture.** `expect.effective` never contains a
  default-valued key, so no case depends on the tool reproducing the manual's default table; the
  asserted key always appears verbatim as `key=value` in the case's own `home_files`. All values
  are strings, matching the manual's text form.
- **Case isolation.** Every case writes its own HOME; no case depends on another's files, and
  none uses host paths. The two `include` cases use `~/.config/mako/core.ini` (home-relative),
  which is the one include form the manual licenses (48). The `include` chain is exercised with
  *different* keys per file to avoid asserting the undocumented include-vs-file precedence.
- **No host bytes were copied.** The fixture values are invented placeholders (`alpha`, `beta`,
  `HDMI-1`, `DP-2`, `bottom-left`, `bottom-center`, `bottom`, `overlay`) chosen so that every
  asserted value is distinguishable from the manual's defaults and from the sibling value in the
  same case.

## 5. S493 gate draft (for the L1 / scribe)

```
id:      S493
source:  mako(5) manual — installed mako 1.11.0-1
kind:    docs (host-installed manual page)
tier:    A
scope:   mako config grammar on this host version
locator: file:///usr/share/man/man5/mako.5.gz
accessed: 2026-11-05
sha256:  f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba
         (digest of the decompressed manual text; the .gz container itself is
          17ffc88c9950ba83a60a8d5bdf4cb528ca994adc6ba58e9386a81617b9db1670 and
          gzip -9 -n of the text reproduces it byte-for-byte)
quote:   mako.5 line 435-437: "This matching occurs in the order the criteria are defined in
          the config file, meaning that if multiple criteria match a notification, the last
          occurrence of any given style option will \"win\"."
teaches: mako resolves one notification's effective settings by matching every criteria section
          whose fields all match (AND), then applying the sections in file order so that the
          last occurrence of each style option wins, with the global section as the always-first
          baseline and `include=` pulling in further config files.
status:  mined
used-by: corpus/lessons/round-87.md, .ufo/waves/round-87/controls/mako-cases-r87.json
```

Quote length check: 31 words for the two-line quote above — **over the ≤ 25-word limit** for a
single-line quote. The one-line form to use instead:

```
quote:   mako.5 line 437: "any given style option will \"win\"."   (6 words)
```

That is the pinned quote for S493 (line 437). The preceding two-line phrasing at 435-436 is
reproduced in §2.5 of this report for context but is not the gate quote.

## 6. Verification performed

| check | command / method | result |
|---|---|---|
| package version | `pacman -Q mako` | `mako 1.11.0-1` (exit 0) |
| container digest | `sha256sum /usr/share/man/man5/mako.5.gz` | `17ffc88c…` |
| content digest | `zcat … \| sha256sum` | `f717848f…` = the pinned value |
| gzip reproducibility | `gzip -9 -n -c mako.5 \| cmp - /usr/share/man/man5/mako.5.gz` | identical |
| package integrity | `pacman -Qkk mako` | 33 files, 0 altered |
| manual rendered | `groff -mandoc -Tutf8` | renders cleanly; `\(ti`→`~`, `\e`→`\ ` |
| case file parses | `python3 -c "json.load(...)"` | valid JSON, schema `mako-cases-r87-v1` |
| case count | counter range check replicated | 22 ∈ [20, 24] |
| pins verbatim | programmatic substring check of all 22 pins against `nl -ba mako.5` | 22/22 match, max 14 words |
| loader schema | replicated `load_cases` rules (id regex, relpath safety, arg names, expect shape, refusals enum) | no violations |
| controls below N | re-implemented `naive_values`/`globals_values` readers | naive 7, globals-include 8, N = 22 |

Not run (per the item: the L1 runs the lane counters after the wave): the r87 C1/C2 counters,
the mutant harness, and `tools/mado-mako.py` (never opened, for independence).

## 7. Files written

- `.ufo/waves/round-87/controls/mako-cases-r87.json` — the frozen C1 case set (22 cases,
  sha256 `0a9558743a721f70bb64b48d188b375f1468a140b00ca75ac93ab59c316d5fe3`).
- `.ufo/waves/round-87/w1/R87Scout.md` — this report.

No other file was created or modified. Scratch `S=$HYAKU_SCRATCH/mado-r87/R87Scout` was removed
on exit (`rm -rf`), so nothing of mine is left on disk under the scratch root.

## 8. Installations

None. The task needed only `zcat`, `sha256sum`, `nl`, `grep`, `sed`, `groff` (all already
present in the base image; `groff` was used read-only to render the manual, no install performed).
No pacman transaction was attempted (host-wide pacman pause respected).

## 9. Handoff notes for the L1

1. **Digest layering (must-fix in the S493 row and in the C1 surface sentence).** `f717848f…` is
   the sha256 of the *decompressed* manual; the installed `.gz` is `17ffc88c…`. Both digests are
   reproducible and mutually consistent (gzip -9 -n reproduces the container byte-for-byte), so
   the manual content is pinned and authentic — but the declaration's sentence attributes the
   content digest to the `.gz` file. Either cite the `.gz` with its own digest, or cite the
   content digest and say "manual text". Flagging rather than silently choosing, because the
   declaration is a frozen contract and the L1 owns the row.
2. **Schema conformance.** The case file uses `args` keys `app-name` / `urgency` / `mode` and
   lowercase hyphenated case ids, matching `quality/counters/c1-r87-mako-criteria.py`'s
   `ARG_NAMES` and `ID_RE`. The item's illustrative schema (`app_name`, `modes`) would have been
   rejected by that loader, so I followed the loader that will actually consume the file.
3. **Only c22 expects a refusal.** It is the single construct the manual itself calls invalid
   (448). If the tool's refusal vocabulary differs, c22 is the one case to renegotiate; the
   other 21 are pure resolution behaviour and are independent of that choice.
