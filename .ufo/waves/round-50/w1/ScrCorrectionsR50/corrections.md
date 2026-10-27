# ScrCorrectionsR50 — routed D2, D3, D8 (mado round 50, w1)

Append-only corrections for the round-50 lesson. Nothing here edits a round-49 file, a counter, a fixture or a control:
the lane base is `8ae47b95`, claims `13631f24`, and every read was read-only git or worktree (`git log`, `git grep`,
`git show`, `grep`). No tracked file in the lane or the fleet was written; no counter/judge/control was run (D2, D3 and
D8 ask for none); no tool was installed. Snapshot time **2026-10-27T02:57:48 -03:00**, re-checked at **03:00:02** with no change in any of the seven seats.

Routing: `corpus/lessons/round-49-verifier-spotcheck.md` §6 items 2 (D2), 3 (D3), 8 (D8) — `:126`, `:129`, `:145`.

Receipts (all under `receipts/` in this seat): `d2-seat-state.txt`, `d2-postreport.txt`, `d3-figure.txt`,
`d8-counts.txt`, `quote-sources.txt` (locators computed by `grep -nF`), `quote-check.txt` (output of `check-quotes.py`).

---

## D2 — final state of the seven round-49 w1 seats

**The reference point.** The round-49 report commit in the fleet repo is
`b0184c43 2026-10-27 02:36:01 -0300` (`git -C /home/vgpnk/Projects/shokunin log --format='%h %ci' --
.ufo/reports/round-49/mado.md`, `receipts/d2-postreport.txt`). The question the spotcheck routes
(`corpus/lessons/round-49-verifier-spotcheck.md:126`) is each seat's final state plus whether post-report seat bytes are
pending; its own wording of the filing is "filed with 7 w1 seats unsettled" (`:27`).

**Measured state** (commands per row in `receipts/d2-seat-state.txt`:
`git log --format='%h %ci' -- .ufo/waves/round-49/w1/<Seat>.md` and `-- .ufo/waves/round-49/w1/<Seat>`,
`find … -type f | wc -l`, `wc -c`):

| seat | canonical `w1/<Seat>.md` | deliverable actually in the seat dir | commits touching it | **state** |
|---|---|---|---|---|
| ExecControlsC1 | 423 B **interim stub** at HEAD (`dd2e827e`) | final 173-line report + `receipts/{controls,clause-lines,quotes}.txt` + `controls/` (19 tool files + `MANIFEST`, 20 scored rows) + `measure/` (README + 5 weakened copies + fixture symlink), **worktree only** | `dd2e827e`, `602e39e3` (02:35:01), `8ae47b95` (02:45:06) | **partial** — committed state is a stub; the finished report ("status: complete 2026-10-27T02:57-03:00." at `ExecControlsC1.md:3` in the worktree) is uncommitted |
| ExecSessionTriage | absent | `ExecSessionTriage/ExecSessionTriage.md` 19,236 B — "triage every finding of the session-material gate at the base, both scopes" (`:8`); complete: two gate runs, 167-row triage, 9 receipts, `CLAIMS_CHECK passed=36 failed=0` | `dd2e827e` | **landed, non-canonical path** |
| ScoutHyprBinds | 497 B (points at the in-dir report) | `ScoutHyprBinds/report.md` 8,715 B + 4 pinned wiki pages | `dd2e827e` | **landed** |
| CritPremiseC1 | 395 B **"status: RUNNING"** stub | none — `ls -la` shows the directory empty (0 files, invisible to git) | `dd2e827e` (stub line only); **no commit ever touched the dir** | **absent / dead** |
| CritPremiseC2 | 1,028 B, complete verdict | `CritPremiseC2/findings.md` 8,911 B | `dd2e827e` | **landed** — "Detailed counterexample, evidence, impacted axes, source hashes/locators, and smallest safe correction" (`CritPremiseC2.md:5`) |
| CritRoutedItems | 1,133 B, complete | `CritRoutedItems/findings.md` 21,910 B | `dd2e827e` | **landed** |
| SentPrivacy | absent | `SentPrivacy/report.md` 20,573 B (verdict + 24-fixture probe + both gate scans) | `dd2e827e` | **landed, non-canonical path** — "The live instance already exists." (`SentPrivacy/report.md:17`) |

**Was anything settled at filing time?** Five of the seven already had committed report content at `dd2e827e`
(02:31:37), i.e. before `b0184c43` (02:36:01): ExecSessionTriage, ScoutHyprBinds, CritPremiseC2, CritRoutedItems,
SentPrivacy. Two were not: ExecControlsC1 (interim stub) and CritPremiseC1 (empty dir). Two of the five landed at
in-dir paths, so a reader testing only `w1/<Seat>.md` would count them unsettled.

**Bytes after the report commit.** `git log --since='2026-10-27T02:36:02-03:00' --format='%h %ci' --
.ufo/waves/round-49/w1/` returns exactly one commit, `8ae47b95 2026-10-27 02:45:06` ("late seat output after closure"),
and `git show --stat 8ae47b95` shows one file: `ExecControlsC1/check-quotes.py` (+33). Per-seat counts for the other six
are `post_report_commits=0` (`receipts/d2-postreport.txt`). The committed stub line is
`status: running 2026-10-27T01:56-03:00` (`git show dd2e827e:.ufo/waves/round-49/w1/ExecControlsC1.md | sed -n 3p`).

**Pending (uncommitted) post-report bytes — yes, one seat.** `git status --porcelain` over the seven seats returns only
ExecControlsC1: `M .ufo/waves/round-49/w1/ExecControlsC1.md`, `M …/ExecControlsC1/check-c07-isolation.py`,
`M …/ExecControlsC1/make-controls-receipt.py`, `?? …/ExecControlsC1/receipts/`. Worktree mtimes 02:55:42–02:57:34, and
the seat was still writing while this snapshot was taken (report mtime 02:57:34, snapshot 02:57:48). So the D2 question
"confirm no post-report seat bytes are pending" answers **no**: ExecControlsC1's finished report and its three receipts
are in the worktree only; the L1 must either commit them (errata commit) or declare them dropped.

**Correction line (append-only, for the round-50 lesson).**

> **D2 correction (round 50).** Of the 7 seats the round-49 report filed with unsettled
> (`corpus/lessons/round-49-verifier-spotcheck.md:27`), the final state at 2026-10-27T02:58 -03:00 is: **landed** —
> ExecSessionTriage (`w1/ExecSessionTriage/ExecSessionTriage.md`, in-dir path, `dd2e827e`), ScoutHyprBinds,
> CritPremiseC2, CritRoutedItems, SentPrivacy (`w1/SentPrivacy/report.md`, in-dir path, `dd2e827e`); **absent/dead** —
> CritPremiseC1 (interim stub only, seat dir empty, no commit ever touched it); **partial** — ExecControlsC1 (committed
> state is the interim stub at `dd2e827e`; the finished 173-line report and `receipts/` are uncommitted in the worktree at
> 02:55–02:57; its only committed post-report byte is `8ae47b95` `check-quotes.py`, 02:45:06, after the report commit
> `b0184c43` 02:36:01). Post-report seat bytes are **not** all accounted for: the L1 must commit or drop
> ExecControlsC1's worktree report. Commands: `git log --format='%h %ci' -- .ufo/waves/round-49/w1/<Seat>.md`;
> `git log --since='2026-10-27T02:36:02-03:00' --format='%h %ci' -- .ufo/waves/round-49/w1/`;
> `git status --porcelain -- .ufo/waves/round-49/w1/ExecControlsC1`.

---

## D3 — the 57,865-pair / 400-keymap figure has no receipt; the committed figure is 24,898

**The sentence.** `(w1/ExecRefKeysymB) agrees with the judge on 57,865 random (keymap, keysym) pairs over 400 random
RMLVO keymaps (L1 run).` — `.ufo/waves/round-49/registration.md:22`; repeated in the round-49 report
(`.ufo/reports/round-49/mado.md:16`). Both quotes located by `grep -n` (`receipts/d3-figure.txt`).

**Search for a receipt** (`receipts/d3-figure.txt`, commands and raw output):

```
$ git grep -n -e "57,865"
.ufo/waves/round-49/registration.md:22  … 57,865 random (keymap, keysym) pairs over 400 random RMLVO keymaps (L1 run).
.ufo/waves/round-50/claims.md:38        … D3 (the 57,865-pair figure: receipt or correction)
corpus/lessons/round-49-verifier-spotcheck.md:54,84,129   (the spotcheck's own D3 text)
$ git grep -nP "(?<![0-9a-f])57865(?![0-9a-f])"          → rc=1 (no hit)
$ git grep -n -e "57,865" -- "*.txt" "*.json" "*.jsonl" "*.py"   → rc=1 (no receipt/script carries it)
$ grep -rl -e "57,865" -e 57865 .ufo/waves/round-49/receipts/ .ufo/waves/round-49/w1/ExecRefKeysymB/receipts/ .ufo/waves/round-49/w1/ExecCounterC1/   → rc=1 (none)
```

So: no receipt, no counting command, no fixture — the figure exists only as prose (the earlier `-e 57865` hits in the
lane are hex substrings in `round-21/…/manifest.json` and JSONL receipts, not this number).

**The committed figure.** `24898 comparisons, 0 mismatched.` — `w1/ExecRefKeysymB.md:51`; the committed summary table
ends `| total | 24898 | 0 |` at `w1/ExecRefKeysymB/receipts/diff.txt:34`, and its seven rows (`diff.txt:27-33`) are
9000 + 6000 + 400 + 7916 + 1520 + 59 + 3 = 24898 (checked by `python3 -c`, `receipts/d3-figure.txt`). Those rows name
60+40+8+3+9+5 = **125 keymaps**; no committed row names 400 keymaps.

**Correction line (append-only, for the round-50 lesson).**

> **D3 correction (round 50).** `registration.md:22` and report `:16` cite "57,865 random pairs over 400 random RMLVO
> keymaps (L1 run)". No receipt or counting command for that figure exists in the lane: `git grep -nP
> '(?<![0-9a-f])57865(?![0-9a-f])'` → no hit, `git grep -n '57,865' -- '*.txt' '*.json' '*.jsonl' '*.py'` → no hit;
> the only occurrences are the prose at `registration.md:22`, `claims.md:38` and the spotcheck. The committed
> reference-B figure is "24898 comparisons, 0 mismatched" (`w1/ExecRefKeysymB.md:51`), whose committed summary
> (`w1/ExecRefKeysymB/receipts/diff.txt:25-34`) sums to 24898 over the seven rows it lists and names 125 keymaps
> (60+40+8+3+9+5). The claim should read: reference B agreed with the judge on **24,898 comparisons, 0 mismatched**, and
> the 57,865/400-keymap sentence is withdrawn as unreceipted.

---

## D8 — "2 drafted admits and 4 rejects": the gate holds 12 admits and 5 rejects

**The sentence.** `Spot-check shape: the non-author closure samples from the 2 drafted admits and 4 rejects above` —
`corpus/lessons/round-49.md:26` (locator by `grep -n '2 drafted admits'`, `receipts/d8-counts.txt`).

**Counts in the round-49 Gate section** (`corpus/lessons/round-49.md` lines 6–27):

```
$ sed -n '/Located examples/,/^### Rejected/p' corpus/lessons/round-49.md | grep -c 'drafted admit'
2                      # S352 (line 14) and S355 (line 16) — the located examples
$ sed -n '/^### Rejected after opening/,/^Spot-check/p' corpus/lessons/round-49.md | grep -c '^- '
3                      # three bullets, lines 20-22
$ … | grep -oE 'https://[^`]+|ArchWiki|IKeyboard\.cpp|ConfigValues\.cpp' | wc -l
5                      # wiki 0.56.0, wiki latest, ArchWiki, IKeyboard.cpp, ConfigValues.cpp
```

**Counts in the gate file** (`w1/ScrRows/gate.md`, the source the lesson points at, `round-49.md:11-12`):

```
$ grep -cE '^- \*\*S3[0-9][0-9] admit\*\*' .ufo/waves/round-49/w1/ScrRows/gate.md
12                     # lines 8-19 = S352..S363, under '## 1. Admit — gate lines' (:6)
$ grep -cE '^- \*\*REJECT' .ufo/waves/round-49/w1/ScrRows/gate.md
5                      # lines 23-27, under '## 2. Reject lines' (:21); first is
                       #   - **REJECT `https://wiki.hypr.land/0.56.0/Configuring/Basics/Binds/`**, docs. …  (gate.md:23)
```

So the sentence's two numbers are both wrong as counts of the section: the located examples are 2 of the **12 admitted
rows**, and the rejects are **5** (in 3 bullets), not 4. This is the same class as round-48 N3 (`round-49.md:55`),
which the spotcheck also routes (`round-49-verifier-spotcheck.md:145`).

**Correction line (append-only, for the round-50 lesson).**

> **D8 correction (round 50).** `corpus/lessons/round-49.md:26` says "the 2 drafted admits and 4 rejects above".
> Measured: `w1/ScrRows/gate.md` §1 (`:6`) holds **12 admits** (S352–S363, lines 8–19) and §2 (`:21`) holds **5
> rejects** (lines 23–27: wiki 0.56.0, wiki latest, ArchWiki, IKeyboard.cpp, ConfigValues.cpp); the lesson's Gate
> section itself shows **2 located admits** (lines 14, 16) and **5 rejected sources in 3 bullets** (lines 20–22). The
> admit number "2" is the lesson's examples, not the gate; the reject number is 5, not 4. Commands:
> `grep -cE '^- \*\*S3[0-9][0-9] admit\*\*' .ufo/waves/round-49/w1/ScrRows/gate.md` → 12;
> `grep -cE '^- \*\*REJECT' .ufo/waves/round-49/w1/ScrRows/gate.md` → 5;
> `sed -n '/Located examples/,/^### Rejected/p' corpus/lessons/round-49.md | grep -c 'drafted admit'` → 2;
> `sed -n '/^### Rejected after opening/,/^Spot-check/p' corpus/lessons/round-49.md | grep -oE
> 'https://[^`]+|ArchWiki|IKeyboard\.cpp|ConfigValues\.cpp' | wc -l` → 5.

---

## Limits of this correction set

- D2's ExecControlsC1 row is a **snapshot during a live write** (report mtime 02:57:34, this snapshot 02:57:48); if the
  seat finished or the L1 committed after that, the row upgrades from "partial, uncommitted" to "landed at `<hash>`". The
  worktree state is reproducible with the three commands in the correction line.
- "Landed" here is judged by the presence and commit of report **content**, not by a WAVE-DONE record: no WAVE-DONE
  exists for round-49 w1, which is D1's defect, not D2's.
- Two of the five landed seats (ExecSessionTriage, SentPrivacy) used an in-dir report path instead of the canonical
  `w1/<Seat>.md`. I record the state; I do not propose moving bytes, since that would edit a closed round's files.
- D3: I did not attempt to reproduce reference B's 24,898 comparisons (that would be executing round-49 evidence); I
  verified only that the number is the committed one and that the table sums to it. The arithmetic check
  (`9000+6000+400+7916+1520+59+3 = 24898`) is in `receipts/d3-figure.txt`.
- D8: counts are of gate/lesson **lines**, computed with the commands quoted in each correction line; the quote locators
  in this file are the output of `grep -nF`, re-checked by `check-quotes.py` (`receipts/quote-check.txt`).
- Not run, deliberately: no counter, judge, control, gate, build, lint or test; no host service, compositor, pacman or
  `~` write; no tool installed (so no tooling row). Scratch: a single `mkdir -p
  /fast/scratch/hyaku/mado-r50/ScrCorrectionsR50` was created and removed; no file was ever written there.
