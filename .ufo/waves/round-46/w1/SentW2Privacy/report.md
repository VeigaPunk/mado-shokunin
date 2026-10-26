# SentW2Privacy — round-45 w2: privacy sweep of the round-45 committed evidence

**Attacks** the claim that round-45's committed evidence ships no session material (SKILL.md rule 4), and the
gate `quality/check-session-material.py` that is supposed to find it.
**Supports** round-46's two claims only insofar as it names what round-45 evidence must not carry.
**Target:** `.ufo/waves/round-45/` at `4d22eeb66c2835af8aaa3fac6ad838fa616aa663` (2026-10-26 16:54:18 -0300,
741 files). All reads are from the object database (`git ls-tree -r -z` + `git cat-file --batch`, and
`git archive | tar -x` into scratch); the lane's working tree and index were not touched. No value of any
session string appears in this report or in its receipts: findings name path, line, class and count only.

## Verdict

| class | round-45 tree | gate at 4d22eeb | note |
|---|---|---|---|
| live monitor **serial** | 0 files | 0 (no such rule fires; see G2) | clean |
| live monitor **description** | 0 files | 0 | clean |
| live monitor **make** (vendor) | **6 files** (S2) | 0 | blind: R3 needs a serial in a JSON object |
| live monitor **model** (code) | **2 files** (S2) | 0 | blind: same |
| client **titles** | 0 real (4 files are upstream C++ literals; the other 2 are the gate's own selftest fixtures and a `REDACTED` mutant) | 2 findings, both self-referential | clean |
| **process tables** (`ss -xpa`) | 0 real (1 file = the gate's own selftest rows) | 1 finding, self-fixture | clean |
| **home listings** (whole-line dumps) | 0 | 0 | clean by parity, but see S3 |
| home **paths** (account name) | 151 files, 651 occurrences | 0 | declared limit of R4 (see G3) |
| **tokens/keys** | 0 | (no rule) | clean |
| IPv4 / MAC / `/run/user/<uid>` | 4 files, benign (`/run/user/1000` in an `ss` fixture row, one prose line) | (no rule) | clean |

Round-45 evidence is **clean for serial, description, titles, process tables, listings and tokens.**
It is **not shape-only for hardware identity**: 6 of its files carry the host's real monitor vendor and model
(S2) — strings that round-45 commits introduced, and that the gate cannot see.

Two further results sit outside the assigned tree but are produced by the same evidence and are reported, not
fixed (this seat has no remediation scope): the published corpus still carries the host's real **serial** (S1),
and D1 is now *closed* while round-45's own report still says it is open (V1).

## Method

`w1/SentW2Privacy/sweep.py` (stdlib only) reads every text blob tracked at a revision under a path prefix and
reports, per file:

- `C1_TITLE_OBJECT` / `C2_TITLE_STRING` — a JSON object with `class` + non-empty `title`/`initialTitle`; and any
  line carrying a non-empty title value (the broader net, so a title split out of its object still shows).
- `C3_LIVE_{SERIAL,DESCRIPTION,MAKE,MODEL}` — a substring of the identity strings of one live
  `hyprctl monitors all -j` dump. This is the class the gate does not have: it separates *synthetic* fixture
  identity from *this host's* identity. The live dump stayed in scratch (`/fast/scratch/hyaku/mado-r46/SentW2Privacy/`),
  was never copied into the repo, and no value from it is printed.
- `C4_SYNTH_IDENT` — a JSON object with a non-empty `serial` plus `description`/`make`/`model` that contains **no**
  live identity string (i.e. what R3 would flag without it being a leak).
- `C5_PROC_TABLE` — `users:(("<prog>",pid=<n>`; `C6_HOME_DUMP` — >10 distinct whole-line `/home/...` lines;
  `C7_HOME_PATH` — any `/home/<segment>/`; `C8_TOKEN` — gh/sk/AKIA/Slack/Google key shapes, private-key headers,
  `Authorization:`, `password=`/`secret=`/`api_key=`; `C9_NET_ID` — dotted-quad IPv4, MAC, `/run/user/<uid>`.

Receipts (in this seat dir): `receipt-sweep-r45.txt` (scope `.ufo/waves/round-45`, 741 files),
`receipt-sweep-ufo-selective.txt` (scope `.ufo`, 17,067 files, identity/proc/listing/token classes only),
`receipt-gate-r45.txt` (the gate at the same revision), `receipt-quotes.txt` (quote + locator checks),
`receipt-leakcheck.txt` (this report and every receipt re-scanned for a live identity string).

## S2 — round-45 evidence carries the host's real monitor vendor and model (medium)

Verified by exact substring equality against `hyprctl monitors all -j` on this host (one line per file; locators
computed with `git grep -nF`, not typed):

| file (at 4d22eeb) | line | class |
|---|---|---|
| `.ufo/waves/round-45/w1/CritPremise/receipts.txt` | 5, 17, 20 | live make + live model |
| `.ufo/waves/round-45/w1/ExecLiveHost/verify-quotes.py` | 48 | live make + live model |
| `.ufo/waves/round-45/w1/ExecSeedSweep/name-anchors.txt` | 2, 3, 9 | live make (generated anchor column) |
| `.ufo/waves/round-45/w1/ExecDoNothingC1/control-a-lookup.py` | 206 | live make |
| `.ufo/waves/round-45/w1/ExecDoNothingC1/control-a2-obfuscated.py` | 34 | live make |
| `.ufo/waves/round-45/w1/MutC1Counter/c1-r45-monitors.py` | 255 | live make (copied counter) |

All six were introduced by round-45 commits (`7c0b0035`, and `22a8dedd` for the two counters below), so this is
round-45's own exposure, not an inherited one. Shape, not value: the vendor is 14 characters
(`<2 upper> Electronics`), the model is 12 (`<2 upper> <9 upper>`). The carrier is a fixture vocabulary —
`rng.choice(["Dell Inc.", <the host vendor>, "BOE", "Samsung Electric Company"])` — i.e. the real vendor was
baked into a generator and then into its receipts; `name-anchors.txt:2` shows it in a generated anchor column.

The same two strings also sit in published, frozen files outside `.ufo`:
`quality/counters/c1-r45-monitors.py:255` and `quality/counters/c1-r45-monitors-v2.py:202`. Those are invisible
to the gate, whose scope is `.ufo` only (G1).

Impact: vendor + model identify the operator's display hardware; the description on this host is a
`make model serial` concatenation, so any future paste of the full description into a fixture leaks the serial
too (it already has, upstream — S1). Smallest remediation: draw the vendor from a clearly synthetic vocabulary
in the fixture generators (and in the two frozen counters at their next legal edit), and keep the host vendor
only in a locator-free shape note.

## S1 — the published corpus carries the host's real serial inside a description (high; outside the assigned tree)

`git grep -nF <live serial> 4d22eeb` returns 24 files; 3 of them are **published corpus entries**, not receipts:

| file (at 4d22eeb) | line | class |
|---|---|---|
| `corpus/knowledge/config-health-report-r3.md` | 149 | live serial + live description (a `make model serial` triple in backticks) |
| `corpus/knowledge/hyprctl-verification-layer.md` | 153 | live serial + live description |
| `corpus/knowledge/hyprland-config-plane.md` | 183 | live model |
| `corpus/knowledge/hyprland-config-plane.md` | 184 | live serial |

Added by probation rounds (`f9f58c0e`, `e1e1bb77`, `65a2254d`), i.e. pre-existing. The remaining 21 hits are
`.ufo` snapshot/control copies of the same three files (`round-32` assimilation + controls + mutation fixtures,
`round-37` scribe clone); **round-45 contains none** (`git grep -lF <live serial> 4d22eeb -- .ufo/waves/round-45`
is empty), and the round-45 live receipts (`live-monitors-host-r45.txt`, `w1/ExecIndepA/receipts/live-host-projected.txt`,
`w1/ExecIndepB/receipts/live-host-join.txt`) do not contain it either — the live-run seats kept them shape-only.

Why the gate misses it: G1 (scope) and G2 (R3 needs a JSON object carrying the serial *and* an identifier; a
prose triple is not one). Smallest remediation: replace the serial and the description triple in those three
entries with placeholders (`<serial>`, `make model <serial>`), and widen the gate to the whole tracked tree
with a prose-mode identity rule.

## S3 — home-directory exposure: 151 files carry the account segment (low; R4's declared limit)

- 151 of the 741 round-45 files contain `/home/<segment>/`; 651 occurrences of one 7-character segment
  (`sha256[:8]=4c3a0056`) and 9 of a second (`2a59d59e`, fixture prose).
- Zero whole-line path dumps: both the gate (R4) and `C6_HOME_DUMP` score 0. The largest would-be case,
  `.ufo/waves/round-45/w1/SentTool/raw/r10-scratch-discipline.txt` (31 lines whose first token is the absolute
  path to this checkout, from a `grep -nE` transcript), escapes R4 because every line continues past the path.
- This is not new in kind: the account segment alone sits in 4,639 of the 17,067 `.ufo` files, and the count is
  identical at the round-46 base `b22ea56` and at `4d22eeb` (`git grep -lF -- /home/<account>/ <rev> -- .ufo`,
  4639 both) — so it is noted as a residual, not as a round-45 defect.
- Root cause of the residual is structural: seats run absolute-path commands and paste the transcript. Smallest
  remediation if L1 wants it zeroed: receipts should run from the clone (`cd "$D"` + relative paths) or pipe
  through a redactor; the gate rule would have to count path *occurrences*, not only whole-line dumps.

## Gate parity — the same tree, two tools

`quality/check-session-material.py` at 4d22eeb is byte-identical to the working-tree file
(`sha256 889f8f057bf04fc76ed93dd7ee86e3b0bd9fc1dca3a6bfb712c672da4646e3fb`, and it is the run-45 gate the
ExecPrivacyGate seat wrote), so one run covers "at that revision":

```
python3 -I quality/check-session-material.py --repo <lane> --rev 4d22eeb66c2835af8aaa3fac6ad838fa616aa663
SESSION_MATERIAL_RULES: R1_CLIENT_DUMP=23 R2_PROC_TABLE=26 R3_MONITOR_IDENT=46 R4_HOME_LISTING=2
SESSION_MATERIAL: files=17070 findings=97 rev=4d22eeb66c2835af8aaa3fac6ad838fa616aa663
```

Scoped to `.ufo/waves/round-45/`: **49 finding lines over 47 files** — R1 2, R2 1, R3 46. Independently
classified, **all 49 are false positives for rule 4**:

- R3 46 = 45 `RevengerOmarchy/fixtures/**/mons.json` + the gate's own selftest fixture. All 48 fixture JSONs
  share **one** synthetic identity (`Fake Corp`-shaped vendor, `SN`-prefixed serial); none contains a live value.
  `C4_SYNTH_IDENT` reproduces the same 46 files and no live object (`C4_LIVE_IDENT_OBJECT=0`).
- R1 2 = `w1/ExecPrivacyGate/check-session-material.py:373,381,393` (its own fixture titles — line 373 is the
  literal string `a live window title`) and `w1/ScrMistakes/mutants.sh:42` (an injected mutant whose title value
  is the word `REDACTED`).
- R2 1 = `w1/ExecPrivacyGate/check-session-material.py:406,407` (its own two `ss` fixture rows).

On the same `.ufo` scope the two tools agree rule-for-rule, which is the useful part of the comparison
(`C1_TITLE_OBJECT=23` = R1 23; `C5_PROC_TABLE=26` = R2 26; `C4_SYNTH_IDENT=46` = R3 46; `C6_HOME_DUMP=2` = R4 2).
The deltas are exactly the gate's two blind classes — live-identity comparison (S1, S2) and path occurrence (S3) —
plus its scope, `.ufo` only.

Gate limits this sweep exercised, each located:

- **G1 scope.** `quality/check-session-material.py:4` — "Question answered: does any tracked file under ``.ufo/`` at a revision carry" (quote ends there; next word is `raw`). The three S1 corpus entries and the two S2 counters are tracked and published, and are outside that scope.
- **G2 R3 shape.** `quality/check-session-material.py:28` — "``make`` or ``model``. Redacted/empty serials do not match." A vendor/model mention with no serial, or a serial in prose, is invisible; a synthetic serial is indistinguishable from a real one.
- **G3 R4 shape.** `quality/check-session-material.py:31` — "shape of a ``find ~`` / ``ls`` dump. Paths quoted inside a" (quote ends there; next word is `sentence`). 651 account-name occurrences in 151 files score 0 by this rule, as designed.

## V1 — D1 (round-44's session-material finding) is closed at 4d22eeb; round-45's report still says open

Positive verification, blob-hash level:

| rev | `.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json` | `.ufo/waves/round-43/w2/SentLiveRun/dump-now.json` | `"title"` lines |
|---|---|---|---|
| `ebdba13f7cb16d454763003d424398eec3bb2788` | `ffdb411e1f` | `78abfbc14d` | 4 and 4 |
| `ee6659b90f7bf69aa03283dba804dd90081b7ff5` | `4c7fe8e38b` | `4c7fe8e38b` | 0 and 0 |
| `4d22eeb66c2835af8aaa3fac6ad838fa616aa663` | `4c7fe8e38b` | `4c7fe8e38b` | 0 and 0 |

Both files are now the 7-key projection (`address, at, class, floating, mapped, monitor, size`) — no `title`,
no `initialTitle`; the gate lists neither at 4d22eeb (0 hits for `host-clients-live|dump-now` in
`receipt-gate-r45.txt`), and round-45's own gate receipt `receipts/session-material-data.txt` (generated at
`ee6659b9`) lists neither either. The nested copies inside round-45
(`w1/ExecProjectTitles/proj/.ufo/waves/round-43/...`) are the same projected blob `4c7fe8e3`, so the round-45
duplicate is clean too. The stale statement is in-tree, not a live defect:
`.ufo/waves/round-45/w1/ExecPrivacyGate/report.md:102` — "with the same 50 files: D1 is still unfixed" — true at
its own tip `ebdba13`, false at the revision now under review.

## Declared limits of this sweep

- Titles are detected structurally only. Comparing a committed title against the live ones would need
  `hyprctl clients -j`, which is outside this seat's allowed compositor reads; the class is therefore scored as
  "no dump-shaped object and no non-empty title outside upstream source / gate fixtures", not as a live diff.
- `check-session-material.py` skips binary blobs and limits >16 MiB files to R2/R4. The round-45 tree has no
  binary blob: `file` reports 62 JSON, one empty file, and one plain-text receipt misdetected as HPGL
  (`w1/ExecIdGuard/quote-verify.txt`).
- 21 of the 24 live-serial hits live in `.ufo/waves/round-32`/`round-37` snapshot and control copies of the three
  S1 entries; those trees were not swept further than the identity class (they are outside the assigned round and
  outside this seat's surface).

## Reproduction

```
S=/fast/scratch/hyaku/mado-r46/SentW2Privacy                     # scratch only; never evidence
hyprctl monitors all -j > "$S/live-monitors-all.json"            # allowed read; stays in scratch
python3 -I .ufo/waves/round-46/w1/SentW2Privacy/sweep.py --repo <lane> \
  --rev 4d22eeb66c2835af8aaa3fac6ad838fa616aa663 --scope .ufo/waves/round-45 --live "$S/live-monitors-all.json"
python3 -I quality/check-session-material.py --repo <lane> --rev 4d22eeb66c2835af8aaa3fac6ad838fa616aa663
python3 -I .ufo/waves/round-46/w1/SentW2Privacy/verify-quotes.py --repo <lane> \
  --rev 4d22eeb66c2835af8aaa3fac6ad838fa616aa663 --live "$S/live-monitors-all.json" --report <this file>
```

Tooling: no installs; stock `python3` (3.13), `git` 2.5x from the host. Scratch was deleted after the receipts
were copied here (`rm -rf /fast/scratch/hyaku/mado-r46/SentW2Privacy`).
