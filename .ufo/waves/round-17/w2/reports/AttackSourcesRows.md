# AttackSourcesRows — rows S056–S070 against SOURCES contract v1

Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`, lane HEAD `988b858bd6049bc709807534fd725c05264f7e60` (pushed).
Rows measured: `corpus/SOURCES.md:68-82` (S056–S070) plus the shape of the file they land in
(`## Paths`, `## Search log`) and the round-17 `## Gate` that must ground them
(`corpus/lessons/round-17.md:22-66`).

Install: **none**. No pacman/sudo/systemctl/probe; web sources fetched with curl only and hashed
locally; host files read as bytes; git read verbs only.

**Measurement-state caveat (read this first).** At review time the lane working tree was *dirty*
and moving: `corpus/SOURCES.md`, `corpus/knowledge/terminal-route-r17.md` and
`corpus/lessons/round-17.md` had mtimes 11:56:37–11:57:09 (now 11:57:44) and `git status` showed
` M` on all three. The SOURCES delta is exactly one added row, **S071**, after S070
(`git diff corpus/SOURCES.md` = 1 insertion), plus knowledge-entry edits (“corrected in round-17
wave 2”). Every finding below was measured against **HEAD 988b858**; I re-checked that rows
S056–S070 are byte-identical in HEAD and in the dirty tree, so no finding here depends on the
in-flight edit. S071 is discussed separately at the end because it is uncommitted and has no Gate row.

---

## Verdict

Three anchor claims fail outright; one required document section was not written for the round;
one rejected row's `flip:` is unsatisfiable as written; three low-severity grounding/precision
defects. The rows' *substance* — digests, tag refs, line content, used-by integrity, tier scoping,
11-column shape, append-only — survived a byte-level attack almost completely.

| # | Row / file | Severity | Finding |
|---|---|---|---|
| F1 | S066 row + Gate | High | Anchor digest is wrong by one hex character; actual upstream bytes hash to a different value |
| F2 | S062 row + Gate | High | Cited anchor lines `:51`/`:247` do not exist in the digested 145-line artifact; the quoted text is at lines 1 and 146 |
| F3 | S070 row + Gate | High | “raw sha256” is not reproducible: the page returns a different digest per request (per-request RSC chunk id); claimed digest matches no observed response |
| F4 | `SOURCES.md` | Medium | Round 17 added 15 rows and **no** `## Paths` bullet and **no** `## Search log` note (rule 5 unmet) |
| F5 | S061 `teaches` | Medium | `flip:` (“if the rubric ever admits tier C”) is unsatisfiable — contract v1 admits tier C; C2's bar is tier **A**. Reason text also confuses kind (`docs`) with tier (`community`) |
| F6 | S060 Gate | Low | Gate quote (line 3 path comment) does not ground `teaches` (exclusions/execargs live at lines 6–25) |
| F7 | S063 Gate | Low | Gate quote `[HW:6]` (config-file path) does not ground `teaches` (key meanings begin `[HW:13]`) |
| F8 | S059 anchor | Low | `alacritty.toml:1-27` on a 28-line file; anchor also pins two artifacts `source` does not name |
| F9 | S059 anchor / entry | Low | “`.bak` not referenced” is a negative claim with a digest but no sweep command |

---

## Findings

### F1 — S066 (hypridle `Hypridle.cpp`) anchor digest is falsified

`corpus/SOURCES.md:79` and `corpus/lessons/round-17.md:53` both carry:

```
sha256 2dd4d73d4f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75
```

Actual bytes at the cited tag (`https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp`,
29880 bytes), fetched twice in one session:

```
2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75
```

The strings differ at exactly one character, index 8: claimed `4`, actual `6`. A one-nibble
difference cannot be “a different revision” — a real content change avalanches the whole digest —
so this is a transcription error, not a source-state disagreement. Commands:

```sh
curl -sSL https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp | sha256sum   # twice, identical
```

Blast radius: the row's *line* anchors are correct — `:473` is `if (MEMBER == "Lock") {`, `:301`
is the inhibit gate, `:327` is `spawn(pListener->onTimeout);`, `:346-352` is the on-resume guard,
`:600`/`:626` are `ignore_dbus_inhibit` and the ScreenSaver registration — so the fix is the 64-hex
string in two files, not the row's content. Contract v1: the anchor is “exact section / heading /
page / line **plus revision**”; a digest that does not match the bytes at the named revision is
not an anchor. A non-author verifier re-computing the digest gets a mismatch and must reject the
row, exactly as the contract's rule 1 intends.

### F2 — S062's anchor lines are impossible in the artifact it digests

`corpus/SOURCES.md:74` says `` `:51` and `:247` place TOML at 0.12 ``; `corpus/lessons/round-17.md:49`
cites “line 247”. The row's abbreviated digest (`08608a0b…bec2c653`) matches my fetch of
`https://linuxjunkies.org/guides/configure-alacritty` exactly:

```
90051 bytes, sha256 08608a0bafb9bb7b4cea2a7970dbc2f926946976c7f9eb23a1d30249bec2c653
```

In **those** bytes:

```
$ wc -l                             -> 145      (one final unterminated line; max line = 146)
$ grep -n "Starting with 0.12"      -> 1:<!DOCTYPE html>…   and  146:<p>…FAQ…
$ sed -n '51p'                      -> sudo pacman -S ttf-firacode-nerd</code></pre>
$ sed -n '247p'                     -> (no such line)
```

The claim is present twice — inline in the JSON-LD on line 1 and in the body FAQ on line 146 — but
line 247 cannot exist in a 145-newline document, and line 51 is a font-install command. So the row
and the Gate quote point at text that is not there.

The rejection *verdict* is independently true, which is why this is an anchor defect and not a
verdict defect: `v0.13.0/CHANGELOG.md:36` reads exactly
`- Configuration file now uses TOML instead of YAML`, and `v0.12.0/CHANGELOG.md` contains
`grep -ci toml` = **0**. Fix is to cite lines 1/146 (or the FAQ heading) against the same digest.

### F3 — S070's “raw sha256” is unreproducible by construction

`corpus/SOURCES.md:82` and `corpus/lessons/round-17.md:57` claim
`raw sha256 bf875a25…350ab90a`. Three fetches of the same URL, same day:

| fetch | bytes | sha256 |
|---|---|---|
| plain curl | 179614 | `da06684a2243d5fa91fb8edc32c1821feb1ed8e78734de183feeab0a42b26f4e` |
| curl + Mozilla UA | 179317 | `fcbc6cc476879233e45aba2ed8f33f8ad379c1696308cbfd50b6726a8ce375b2` |
| curl + Mozilla UA | 179317 | `7d7a65bbba170a72b65a5177288105a7b812073e7e87edcec450774ff0a1feae` |

The two 179317-byte responses are the same length but differ at offset 70751 —
`16:I[41651,[…]]` versus `16:I[80622,[],…]` — a per-request Next.js RSC chunk id. The claimed
digest matches neither the prefix nor the suffix of any observed response. So a re-verifier cannot
confirm that the row's author opened these bytes, and no future verifier can either. The row's
revision binding (“published 2024-12-24, modified 2026-04-05”) sits in `scope`, not in `anchor`,
so the anchor is *only* the unstable digest.

The rejection itself holds up: content probes on the fetched page return
`hypridle.conf` ×2, `lock_cmd` ×3, `before_sleep_cmd` ×2, `timeout = 600/900/1800` ×2 each, and no
project-version token (the decimal tokens present — `1.75`, `3.573`, `9.104` — occur inside SVG path
coordinates and asset markup, not as `hypridle`/`hyprlock`/`Hyprland` versions).
Recommendation for Main: replace the digest with a citable, stable locator (section heading +
retrieval date) or admit that a mutable third-party page cannot carry a byte anchor.

### F4 — Round 17 wrote rows but no Paths bullet and no Search-log note

`git diff a9998d1^..HEAD -- corpus/SOURCES.md` yields 15 added lines (S056–S070) and **zero**
deleted or modified lines. Consequently:

- `## Paths` still ends at the round-16 bullet (`Waybar module observation boundary (U7, round 16) — S053 → S054`,
  `corpus/SOURCES.md:111`). There is no P4 (`S056 → S060`) or P6 (`S063 → S069`) sequence,
  although both are new documentary routes and every earlier round that mined a surface appended one.
- `## Search log`'s last round note is `Round 16 (2026-10-20)` (`corpus/SOURCES.md:225`). No
  round-17 note exists: no question, no query, no identified/screened/included/excluded counts, no
  exclusion reasons, no stop rationale. The lesson's Gate substitutes a prose sentence
  (“Candidates considered: …”, `round-17.md:24-29`) that contains none of the rule-5 quantities.

Contract v1 shape lists both sections as part of the file and rule 5 says “one prose note per
bounded search” with counts, exclusion reasons and stop rationale. Round 17 performed at least one
bounded search (the rejection sweep that produced S061/S062/S070) and mined two surfaces, so the
omission is not “no search happened”. This is the only defect that survives the in-flight repair —
the dirty tree still lacks both additions.

### F5 — S061's flip condition contradicts the contract it is graded against

`corpus/SOURCES.md:73` (`kind=docs`, `tier=C`) says:

> REJECTED: community tier cannot support a C2-covered entry; … flip: oldid-pinned tier-C
> cross-check only, if the rubric ever admits tier C

Two problems:

1. C2's actual bar, from the round's own pre-registration
   (`.ufo/waves/round-17/w1/spec.json`, context line 3), is: “Covered = knowledge entry whose first
   15 lines have `source:` citing a **mined tier-A** SOURCES row whose used-by names that entry”.
   The operative exclusion is tier **A**, not “community tier”; and `community` is a *kind*
   (this row's kind is `docs`), never a tier. The sentence mixes the two enums.
2. Contract v1 **does** admit tier C rows — “C: lead only — never sole support for an admitted
   entry” — and this registry already carries six C rows at HEAD (three at baseline). So “if the
   rubric ever admits tier C” is a condition that is already true of the registry and can never be
   the thing that flips this verdict. The flip that would actually matter is a tier-A primary on the
   same scope (e.g. the Alacritty v0.16.0 man page itself), or a rubric that admits a C row as a
   *cross-check* rather than sole support.

The substantive rejection ground is true and I verified it end to end: v0.16.0
`alacritty/src/config/mod.rs:371` is `/// 5. /etc/alacritty/alacritty.toml` and `:395` is
`PathBuf::from("/etc/alacritty")…`; v0.14.0 and v0.15.0 contain **0** occurrences of
`/etc/alacritty`; Arch-wiki revid 869789 (2026-03-23) is the page's latest revision, its raw digest
is `c39c563d…c4600bb`, and its lines 22/24 are exactly `` * {{ic|/etc/alacritty/alacritty.toml}} ``
and “Versions before 0.13.0 used a YAML configuration file.” So only the `teaches` wording is wrong.

### F6 — S060's Gate quote grounds the source's identity, not its `teaches`

`corpus/lessons/round-17.md:47` quotes `line 3 "# i.e. /usr/share/xdg-terminal-exec/xdg-terminals"`.
The row's `teaches` is “fallback exclusions and execarg defaults; no Alacritty entry; installing
package and version [UNK]”. Line 3 is a comment about the intended install path; the exclusions are
lines 5–11 (`-org.kde.yakuake.desktop` … `-footclient.desktop`), the execarg defaults are lines
15–25, and the absence of Alacritty is a property of the whole 25-line file. Rule 1 requires the
Gate's ≤25-word quote to *ground `teaches`*; this one grounds only which file it is. (The row's own
content is otherwise exact: 1053 bytes, sha `a2b5…f034`, and the host file is byte-identical to
upstream `v0.14.3/xdg-terminals.list` — I fetched the upstream file and got the same digest.)

### F7 — S063's Gate quote grounds a different fact than its `teaches`

`corpus/lessons/round-17.md:50` quotes `[HW:6] "Configuration is done via the config file at
~/.config/hypr/hypridle.conf."` The row's `teaches` is “documented meaning of lock_cmd,
before/after_sleep_cmd, on-timeout/on-resume, inhibit_sleep 0-3; not version-pinned to v0.1.8”.
`[HW:6]` is none of those; the key meanings begin at `[HW:13]` and the inhibit modes at
`[HW:22-26]`. The quote is accurate and correctly located — it just does not do rule 1's job for
this row. (`S064`'s quote does ground the second half of its `teaches`, the no-config-no-lock
warning, so I do not file the same finding there.)

### F8 — S059's `alacritty.toml:1-27` is one line short, and `source` under-names the anchor

`corpus/SOURCES.md:71` anchors `alacritty.toml:1-27`. The file is 28 lines (`wc -l` = 28), and line
28 is `]`, the close of the `[keyboard] bindings` array that lines 23–28 open. The citing entry at
HEAD repeats “lines 3-27” (`terminal-route-r17.md:73`), so the slip is consistent across files; the
dirty tree's in-flight edit already changes it to “3-28”, which confirms the off-by-one rather than
contesting it. Separately, the anchor pins five artifacts (three `source` files plus the omarchy
theme import target and the `.bak`) while `source` names only three; the extra digests are labelled
in the anchor so this is cosmetic, but it is the reason a reader cannot tell from `source` alone
what the row opened.

### F9 — the `.bak` negative claim has no sweep

`corpus/SOURCES.md:71` records “`.bak` not referenced (ea3e0fa0…1207a)” and
`terminal-route-r17.md:76` repeats “not referenced by the live file; not read”. `ea3e0fa0…` is the
digest of the `.bak` itself (873 bytes, verified), which says nothing about whether anything
references it. The corpus rule is explicit: “A negative claim carries its sweep.” The same entry
demonstrates the missing form one row earlier — “no `live_config_reload` key (grep count 0)” — so
the convention is known and was simply skipped here. A one-line `grep -rn "alacritty.toml.bak"
~/.config ~/.local/share/omarchy` would close it.

---

## What survived (attacks that failed)

I state these as failures of the attack, with the measurement that killed each one.

**11-column shape and enums.** All 70 registry rows at HEAD have `NF=13`
(`awk -F'|' '… && NF!=13' corpus/SOURCES.md` prints nothing); `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`
= 70; no duplicate ids; every `kind`/`tier`/`status` value is in the v1 enum; no `community`+`A`
inflation. The maintained census agrees: `scripts/sources-census.sh validate … mado` → `ok`, with
only the three pre-existing, documented W04 URL-collision warnings (S030, S042, S045). No row in
S056–S070 introduces a `|` inside a cell.

**Tier scoping.** All 12 new A rows are scoped, not global: S056/S057/S058 are tag-pinned upstream
docs/script/man-page, S065–S069 are tag-pinned README/src, S059/S060 are this host's bytes, and
S063/S064 are the official wiki *scoped to “Latest git”* with the version non-pinning stated in the
cell. The three community/third-party rows are C. No NATO/GRADE labels.

**Digests.** Verified byte-for-byte against fresh fetches: S056 14762 B `c7a1…9d40`; S057 44020 B
`89f2…27ac`; S058 28787 B `e444…4107`; S059's five artifacts — bindings 2879 B `e574…0581`,
`xdg-terminals.list` 127 B `d035…b71b`, `alacritty.toml` 876 B `6953…24f8`, theme import target
772 B `8c3d…9139`, `.bak` 873 B `ea3e…207a`; S060 1053 B `a2b5…f034`; S063 254750 B `b45c…f640`;
S064 291777 B `f69c…ebf5`; S065 2598 B `f5b8…81f6`; S067 3611 B `f9e4…a2b8`; S068 2587 B
`379b…2a38`; S069 1458 B `8309…f0f3`. S061 `c39c…4600bb` and S062 `0860…c653` also matched as
prefix+suffix. Only S066 failed (F1) and S070 is unverifiable (F3).

**Revision bindings.** Read from the smart-HTTP ref advertisement (api.github.com is blocked in this
sandbox): `xdg-terminal-exec v0.14.3` → `065925df9f419008159258ae169018bfd23df71b` (S056's stated
ref, exact); `alacritty v0.17.0` → tag object `dc946285396bd3e251b6942af7e9961b74f76bee`, peeled
commit `94e7c8874e526b1e67b349d9ba30ddf81669119e` (S058 states both, exact). Arch-wiki revid 869789
is confirmed by the MediaWiki API as the page's latest revision, timestamp 2026-03-23, comment
“/* Configuration */ Add system-wide configuration location” — the row's “the edit that added it
cites no source” is literally true.

**Line anchors.** Spot-checked against the digested bytes and all exact: S056 line 166 is
“Each entry from the explicit selection list is checked for applicability:”; S057 line 106 is
`--dir=workdir  set workdir of terminal.`, 148–162 is the config/data sequence, 402–413 the
`execarg_default` handling, 919 `TerminalArgDir`, 1252 `--dir=*)`; S058 35–41 is the import order +
“loaded last” + relative-path rule and 57–61 `live_config_reload` default true; S065 line 5
`ext-idle-notify-v1`, line 6 the dbus loginctl trio, line 62 `exec-once = hypridle`; S066 lines
301/327/346–352 as above; S067 lines 23/26 `ignoreInhibit`/`conditionRetry`; S068 55–63 the CRIT
branch that ends in `return 1` before `init()`/`run()` — so “fatal, not a silent default” is
accurate; S069 lines 5/19.

**S063/S064 derived-line convention.** I tried to break the “lines of the tag-stripped `<article>`
text” anchor and could not. Implementing the convention documented in the entry (“one line per
block, empty lines dropped”) reproduces the Gate quotes exactly: `[HW:6]` is the config-file
sentence, `[HW:13]` the `lock_cmd` row, `[HW:22-26]` the inhibit modes, `[HW:33]` the “wait until
locked” sentence, `[HW:51]` `ignore_inhibit`, `[HW:78-107]` the full example; `[LW:7]` the
no-config warning, `[LW:16]` `--grace`, `[LW:37/38]` the two defaults, `[LW:49]` `fail_timeout`
2000 ms. Under that transform S063's article is 121 non-empty lines (row range 6–120) and S064's is
340 (row range 6–85), so the stated ranges are honest and cover every citation in the entry.

**used-by integrity / C2's mechanical condition.** Every mined row's `used-by` path exists at HEAD
and names the row in its `source:` line: `terminal-route-r17.md:1` cites S056–S060 (and
`surface: P4`), `idle-lock-route-r17.md:1` cites S063–S069 (`surface: P6`). C2's stated test
(“first 15 lines … mined tier-A row whose used-by names that entry”) therefore passes on its own
terms for both new surfaces. Rejected rows carry `—`, matching registry-wide convention — though
`terminal-route-r17.md:131` does name S061/S062, so the `—` is convention, not a literal inventory.

**Append-only (rule 2).** The round's SOURCES diff has zero `-` lines, so no existing row's
`status`/`recheck`/`used-by` was edited in place; the Gate's “Status/recheck/used-by changes to
existing rows: none (old→new: none)” is true.

**Gate histograms.** Recomputed at HEAD and at `a9998d1^`: rows 55 → 70; tier A 51 → 63, B 1 → 1,
C 3 → 6; status mined 43 → 55, rejected 4 → 7, queued 8 → 8. Every number in the lesson matches.
The Gate also covers all 15 new rows with URL, access date (“all opened 2026-10-20”) and a ≤25-word
quote, as rule 1 requires — the quotes' *grounding* is where F6/F7 land, not their presence.

**Rejected-row shape.** All three rejected rows read `REJECTED: <reason>; flip: <…>` and the reasons
are substantive; S061's and S062's grounds survived independent verification (F5/F2), and S070's
ground survives even though its anchor does not (F3).

---

## S071 and the dirty tree (outside my row scope, flagged for Main)

The working tree adds a 71st row, `S071` (host `~/.local/share/applications/Alacritty.desktop`,
`code`, `A`, mined, used-by `corpus/knowledge/terminal-route-r17.md`), and edits the knowledge entry
to cite it. That row has **no Gate entry** — the Gate table still ends at S070 and still states
“Rows before→after: 55 → 70”. If S071 is committed as-is, rule 1's per-new-row Gate record is
missing for it and the lesson's counts become 71. It is uncommitted right now, so I did not treat it
as a defect of the landed C2 commit; I note it because the numbers in this report (70 rows, A=63,
C=6) are the HEAD numbers, and the in-flight state already differs.

The same in-flight knowledge edit also fixes two slips I measured independently at HEAD: the
`bindings.conf:2` quote gains `"$(omarchy-cmd-terminal-cwd)"` (the HEAD quote truncated the line)
and `alacritty.toml` “lines 3-27” becomes “3-28” (F8). Both repairs match the bytes; neither is
committed.

## Residual risk / verification gaps

- **S070's “339 extracted lines”** is unreproducible: the transform is unstated and the page is
  nonce-unstable, so the count cannot be re-derived even in principle. The rejection still stands on
  the content probes, but the quantitative clause should not be relied on.
- **S061's anchor is date-coupled**: it pairs a stable `revid 869789` with the *current* raw digest.
  Today the latest revision is 869789 and raw == revid; after the next wiki edit the same raw URL
  will hash differently while the revid still names 869789. The anchor's two halves will silently
  diverge unless the verifier pins `oldid=` (which currently answers with an Anubis bot challenge
  to plain curl, so a verifier needs the API or a browser).
- **C2's P4/P6 “coverage” rests on documentary tier-A rows**: S063/S064 are scoped to the wiki's
  “Latest git” and are explicitly *not* version-pinned to the installed v0.1.8/v0.9.6, and S059/S060
  are host declarations, not observations of which binary launches. The rows say this honestly in
  their `teaches` cells; the risk lives in reading C2's “documented route” as behavioural coverage.
- **S060 says “installing package and version [UNK]”** while the Gate's version-binding paragraph
  reads `xdg-terminal-exec 0.14.3-2` from `pacman.log:2935`. I did not score this as a defect — a
  log line does not prove the file's owning package or the running binary — but the two sentences
  pull in opposite directions and a reader may take the row's `[UNK]` as an admission that the
  package is unknown when the log does name one.
- GitHub's API is blocked here; all repo identity checks used the git smart-HTTP advertisement
  (`info/refs?service=git-upload-pack`), which serves the same tag objects and peeled commits.
