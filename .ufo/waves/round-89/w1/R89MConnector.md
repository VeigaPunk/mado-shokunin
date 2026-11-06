# R89MConnector — sibling overlap, assimilation, considerthese, and C1↔C2 coupling

Seat: connector (leaf, no dispatch). Round 89 w1, base `af998dcc41d48618ffe7afe0efc9354755a9244e`.
Read-only: no counter, no fixture, no clone, no write outside this file. Every command below was run
from the fleet root `/home/vgpnk/Projects/shokunin` or the lane root, 2026-11-06.

## 1. Sibling-lane hit list

Exact scan (the item's command):

```
grep -rlI -e 'regcomp' -e 'POSIX extended' -e 'REG_EXTENDED' -e 'setlocale' \
     /home/vgpnk/Projects/shokunin/*-shokunin/corpus --include=*.md
```

→ 4 files, rc 0 (matches found):

| # | path | which term | relevance |
|---|---|---|---|
| 1 | `mado-shokunin/corpus/knowledge/mako-fields-containment-r88.md` | POSIX extended | **direct antecedent** — the entry whose §1 marks `summary~`/`body~` "refused — named limit" and whose §2 counts the host's five `[summary~="…"]` sections |
| 2 | `mado-shokunin/corpus/lessons/round-88-verifier-spotcheck.md` | regcomp | **direct antecedent** (via the reject table it relays) — the routed R1–R5 defect list C2 answers |
| 3 | `mado-shokunin/corpus/knowledge/hyprland-config-autoreload-r56.md` | setlocale | weak precedent: the lane already states a libc-locale dependency instead of assuming it |
| 4 | `kaidoku-shokunin/corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md` | setlocale | **false positive** — `setlocale` appears only as an ELF import name (`setlocale@GLIBC_2.2.5`) in jq's GOT |

The item asks for the top 5; the exact scan yields 4. A widened phrasing scan found the fifth
(`grep -rlI -e 'POSIX ERE' -e 'POSIX extended regular' -e 'extended regular expression' -e 'REG_NOSUB'`
over `*-shokunin/{corpus,quality,tools}`, rc 0, 18 hits — 13 are `.c`/man/html sources in audio, mori,
kengaku, kagi and are unrelated), of which the lane-relevant fifth is:

| 5 | `mado-shokunin/corpus/lessons/round-88.md:96` | extended regular expression | **direct antecedent** — the "Candidates considered" row: `summary~`/`body~` modelled with Python `re` → **reject**, with the follow-on stated verbatim as "a resolver that implements POSIX ERE" |

### What each opened hit says, and what it means for this round

1. **`mako-fields-containment-r88.md`** (opened in full). §1's table gives `summary~` (manual 450,
   `regexec` POSIX ERE at `criteria.c:116`) and `body~` (456, `criteria.c:128`) as the only two of the
   twelve first-pass fields the round-88 resolver refuses; §2 states "the five `[summary~="…"]`
   click-action sections (core.ini:24, 27, 30, 33, 36) still refused by round 88". **C1 lifts exactly
   this limit.** The round-89 knowledge entry must supersede/extend this file (a dated amendment or a
   new entry citing it), not restate §1 — and the count "five" and the line list 24/27/30/33/36 are the
   numbers to reuse, so they stay single-sourced.
2. **`round-88-verifier-spotcheck.md`** (opened in full). §5 routes R1 (four C1 survivors: RM2C1,
   RM3C1, RM5C1, RM7C1), R2 (three C2 survivors: RM3C2, RM4C2, RM5C2) and R3 (RM6C2, "not in the
   report's routing list"); RM2C2 is ruled a confirmed named limit. 4 + 3 + 1 = the 8 survivors in
   `survivor-mutants-r89.json`. **C2's eight are a faithful, complete transcription of that routing** —
   worth citing by §5 R1/R2/R3 rather than re-deriving.
3. **`hyprland-config-autoreload-r56.md:70`** (opened; the quote is in the "Glob semantics" paragraph):
   "Whether Hyprland calls `setlocale` and which libc it links are not in the pins. The watch-plan model
   sorts bytewise; that is a declared divergence". Relevance is **stylistic, not evidential**: it is the
   lane's precedent for naming a libc-locale dependency as a declared stance. C1's C-locale argument must
   rest on its own evidence (no `setlocale` call in the mako v1.11.0 tree), not on this entry.
4. **kaidoku `2026-10-13-r5-02-call-targets-jq.md:69,165`** (opened). `setlocale` is a symbol name in a
   Ghidra call-target table (`0x10206a` → `0x109220`). No regex, no locale semantics, no shared surface.
   **Do not cite; nothing to duplicate.**
5. **`corpus/lessons/round-88.md:96`** — the round-88 lesson row explicitly names round 89's work.
   C1 is the predicted follow-on; citing this line turns the claim into a discharged prediction rather
   than a new direction.

Supplementary scan outside the corpus (`*/quality`, `*/tools`, rc 0): the only file matching
`regcomp|REG_EXTENDED|POSIX extended|setlocale` in any sibling lane's tooling is the lane's own new
`quality/counters/c1-r89-mako-regex.py`. **No sibling lane is building a POSIX ERE engine; no overlap
to avoid.**

## 2. Assimilation verdict

Read `/home/vgpnk/Projects/shokuknow/merge/mado/MERGE-REPORT.md` (18 KB; 147 proposed rows, 69 proposed
knowledge entries, rounds 1–16, staged 2026-10-24, "Nothing was written into the lane repo"). Greps over
the whole `merge/mado` tree:

- `grep -rn -i 'mako'` → 3 lines: `SOURCES.append.md:42` (S238, the omarchy notification-silencing bar
  indicator running `makoctl mode`) and `knowledge/corpus/knowledge/host-producer-outputs-r29.md:25,32`
  (the same chip; "`makoctl mode` reports `default`").
- `grep -rn -e regcomp -e REG_EXTENDED -e 'summary~' -e 'body~' -e POSIX` → **0 lines**.
- `grep -rn setlocale` → **0 lines**.

**`Assimilation: none`.**

Reason: the package's entire mako content is one bar producer that *queries* `makoctl mode` at runtime.
That is the mode-set input the resolver takes from the caller, not the criteria grammar, not
`summary~`/`body~`, and not regex. It fits neither C1 (POSIX ERE coverage) nor C2 (survivor kills), and
the one-theme/1–3-entry rule would force a false fit. The package also predates rounds 65–88, so it
cannot carry the r87/r88 mako material either, and it is staged-only (unadopted). If the operator ever
adopts it, the mako touch is a duplicate of the already-mined lane entry `host-producer-outputs-r29.md`
— one more reason not to open a theme for it.

## 3. considerthese mapping (`considerthese/2026-11-06.md`)

**Proposal 1 — "carry a survivor ledger … report the first later commit that kills one".**
C2 answers it in the strongest form available: the 8 routed survivors are re-expressed with anchors,
7 are killed over B ∪ S, `RM6C2` is declared crash-only *before* data with an argument, `RM2C2` is
excluded as the confirmed TOCTOU named limit, and the do-nothing control (B alone) kills 0/7 — so the
kill is attributable to the new cases, not to existing coverage. The "first later commit that kills one"
is the measured C2 revision. **Stays open:** no *durable* ledger artifact exists — the kill is a one-shot
receipt, so a later daily reflection still cannot read a live list; and the reflection's other open rows
(r86 forgery classes, r85 C2 survivors) are untouched by this round.

**Proposal 3 — "read-only live check of `mado-mako.py` against João's real theme files".**
Answered inside the wave, not in the declaration: seat `R89MExecHostDiff` ("Host coverage receipt for
C1 (read-only)") runs base vs candidate on `~/.config/mako/config --home "$HOME"` for the five host
`summary~` patterns plus a non-matching control, and against the oracle; C1's case `r01-host-setup-wifi`
is derived from `core.ini:24`. **Stays open:** agreement with the *running* daemon (`makoctl`, a live
notification) is still not claimed — the manual and the tag-pinned source remain the stated authority, so
the proposal's "test whether the refusals match mako 1.11.0 behaviour" is answered at source level only.
The five click-action sections become *decidable* by C1, but no round-89 artifact resolves them end to end
in one receipt (the host-diff grid does, as a draft).

## 4. C1 ↔ C2 coupling (claim separation cross-check)

Facts found in the files (each verified by a command, rc 0):

1. **Same measured path, different revisions.** Both claims score `tools/mado-mako.py`. C2 is measured at
   the freeze revision; at the base revision the tool's sha256 is
   `c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237`
   (`git show af998dcc:tools/mado-mako.py | sha256sum`), exactly the round-88 measured tool. So the
   separation is **temporal (revision)**, not material: one file, one failure point.
2. **Same carried case corpus.** C1's 91 cases = 61 carried + `r01`–`r30`. Comparing C1's carried block
   against `round-88/controls/mako-cases-r88.json` (62 cases) by id and JSON: **0 differences over the 61
   shared ids**, `c53-summary-tilde-refused` absent from the r89 file. C2's B is the *same* round-88 file
   minus `c53` by id filter (`EXCLUDED_B`). The two claims therefore share one case corpus but exclude
   `c53` by **two different mechanisms** (deletion from a copy vs a runtime filter).
3. **Same anchors.** All 8 survivor `old` strings and all 32 C1 mutant `old` strings occur **exactly once**
   in `build/mado-mako.c1.py` (counts printed 1..1 for every id). So a C1 refactor that moves any of those
   lines converts C2's mutant application into a setup error (rc 2), not a scored miss — and the
   declaration's sentence "C2's eight anchors occur exactly once in the C1 candidate too" is confirmed,
   not merely asserted.
4. **The c1side supplementary cases test code C1 edits.** `s1-appname-case-differs`,
   `s1-bang-string-field`, `s1-mode-case-differs`, `s1-include-in-criteria` exercise
   `parse_criteria`/`match_criteria` — the same functions the regex work touches. And B keeps
   `c22-refusal-summary-conflicts-summary-tilde` (expects `refusals: present`), which asserts the
   "Cannot set both" rule C1 newly implements. So C2's harm re-run at the C1 revision is **partly a test
   of C1's new code**: the dependence is one-directional (C2 does not depend on C1 to be measured, but
   C1's harm evidence depends on C2's corpus).
5. **Shared frozen machinery.** Both counters sha-pin the round-88 counters (C1 pins
   `c1-r88-mako-fields.py` `3678425a…`; C2 pins both r88 counters). Editing either frozen counter makes
   **both** counters exit 2, not one.
6. **No id collision.** `S ∩ C1cases = ∅`; S has 8 unique ids with no duplicates; B ∪ S is well defined.

### Contradictions and risks (stated, not smoothed)

- **A frozen tool is a moving target if anything lands between freeze and C2's measurement.** The C2 "at
  the freeze revision the tool is still the round-88 tool" reading holds only if the freeze commit leaves
  `tools/mado-mako.py` at `c374d715…`. The counter fails closed (sha pin → rc 2), so this is a
  setup-error risk, not a silent green — but the plan needs the freeze commit to *be* the C2 measurement
  commit.
- **The `c53` exclusion is duplicated.** A case added to `round-88/controls/mako-cases-r88.json` later
  would break C1's carried-set conjunct (count or bytes) while silently widening C2's B. Both verdicts
  would move from an edit outside either claim.
- **The harm re-run has no predicate slot.** PRED-C2-r89-v1 has three conjuncts, none of which is "C2
  also passes at the C1 revision"; the declaration states that re-run as prose ("C2 re-runs at the C1
  revision as a harm check"). A C2 green at freeze and a C2 red at the C1 revision would be a real harm
  finding with nowhere to land in the verdict.
- **Both claims share one file's failure point.** A single bad edit in the C1 candidate that changes any
  B case's verdict makes C1 red and the C2 harm re-run red together; they are not independent evidence
  even though their *measurements* are at different revisions.

### Proposed move (one, bounded — observation only; I did not edit anything)

At the freeze, make the C2 harm re-run an explicit, named artifact: record the C1-revision C2 run in
`receipts/`, state whether it is a predicate conjunct or a note, and cite the mechanical anchor-count
check (8/8 survivor anchors `count=1` in the C1 candidate) as the reason the mutants still apply there.
Affected axes: operability (C2's kill claim gains a second revision) and coverage (C1's harm evidence
stops resting on prose). Harm: none to C1 — the re-run adds a case set the candidate already satisfies.
Risks: it doubles the C2 measurement cost and would surface C1 regressions as C2's, so the receipt must
name which claim it is evidence for.

## 5. Scope discipline

- No fixture, clone, counter run, or scratch directory: `/fast/scratch/hyaku/mado-r89/R89MConnector` does
  not exist (`ls` → No such file or directory). Nothing to delete.
- Read-only git only (`git show`); no jj.
- No host reads beyond the paths the item names: none were needed here (the mako config, man pages and
  `/usr/include/regex.h` were read by other seats, not this one).
- No installs.
- Wrote only this file.

## Commands run (exit codes)

| command | rc | result |
|---|---|---|
| `grep -rlI -e regcomp -e 'POSIX extended' -e REG_EXTENDED -e setlocale <fleet>/*-shokunin/corpus --include=*.md` | 0 | 4 files (§1) |
| `grep -rlI -e regex -e mako -e notification -e 'summary~' -e locale <fleet>/*-shokunin/corpus --include=*.md` | 0 | ~300 files (noise; used only to widen, not as the hit list) |
| `grep -rlI -e regcomp -e REG_EXTENDED -e 'POSIX extended' -e setlocale <fleet>/*/quality` | 0 | 1 file: `mado-shokunin/quality/counters/c1-r89-mako-regex.py` |
| same over `<fleet>/*/tools` | 1 | no matches |
| `grep -rn -i mako /home/vgpnk/Projects/shokuknow/merge/mado` | 0 | 3 lines (S238 + r29 entry) |
| `grep -rn -e regcomp -e REG_EXTENDED -e 'summary~' -e 'body~' -e POSIX /home/vgpnk/Projects/shokuknow/merge/mado` | 1 | no matches |
| `grep -rn setlocale` same tree | 1 | no matches |
| python: C1 case ids / S ids overlap | 0 | 91 cases; S 8 unique; overlap ∅ |
| python: C1 carried block vs r88 cases | 0 | 0 diffs; c53 absent |
| python: survivor + mutant anchor counts in C1 candidate | 0 | all 40 counts = 1 |
| `git -C <lane> show af998dcc:tools/mado-mako.py \| sha256sum` | 0 | `c374d715…92237` |
| `sha256sum .ufo/waves/round-88/controls/{mako-cases,containment-cases}-r88.json` | 0 | `a0e81b19…`, `8b16c0cb…` |
