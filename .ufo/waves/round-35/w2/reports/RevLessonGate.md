# RevLessonGate — round-35 lesson gate

Seat: `L1Mado35.RevLessonGate` (leaf reviewer, no dispatch). Date: 2026-10-25.
Target: `corpus/lessons/round-35.md`.

## Artifact identity (read before the verdicts)

The lesson was **absent** when this seat started (`test -e` failed; nothing in
`corpus/lessons/` named round 35) and appeared twice during the review:

| observed | size | mtime |
|---|---|---|
| absent | — | before 03:30 |
| v1 | 14 737 B | 03:31 |
| v2 (adds M35-4, `RevCollision` paragraph) | 17 287 B | 03:34:13 |
| **v3 (adds `## Wave-2 falsifications applied as errata`)** | **18 925 B** | **03:36:21.471498679 -0300** |

Verdicts below apply to **v3**, the state at the end of this review:

```
$ stat -c '%s %y' corpus/lessons/round-35.md
18925 2026-10-25 03:36:21.471498679 -0300
```

The file is newer than the wave-2 dispatch and was edited while seats were
running, so a later mtime invalidates this report. No lane corpus file was
edited by this seat.

Independent state (read-only; counters run with `python3 -B -I` so no bytecode
was written):

```
$ python3 -B -I .ufo/waves/round-35/c1/count.py --root /home/vgpnk/Projects/shokunin/mado-shokunin \
    --frozen /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET      rc=0

$ python3 -B -I .ufo/waves/round-35/c2/count.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --frozen /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/c2/frozen.json
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET   rc=0
```

So these are gate defects, not data-absence defects. C1 was re-run after the
three entries were amended at 03:35:08/03:35:30 and still reads `TARGET_MET`
rc=0, which corroborates the lesson's errata paragraph ("`PRED-C1-r35-v1` is
unchanged … after every errata append").

## Element verdicts

| # | Required element | Verdict |
|---|---|---|
| 1 | `## Gate`: path + `2026-10-24` + located quote ≤25 words, contiguous substring of its receipt, for **every** row S203–S210 | **PASS** (8/8) |
| 2 | `## Mistakes`: class, evidence pointer, captured-by, fix **shown able to fail** | **FAIL** (M35-3, M35-4 fail the fix leg; M35-1's demonstration is wrong) |
| 3 | census before/after outputs **pasted** with exit codes | **FAIL** (after output not pasted; before pasted) |
| 4 | ≥1 admit and ≥1 reject from the assimilation set, each with reason + flip | **PASS** |

### 1 — Gate rows: PASS (8/8)

`## Gate` → `### Admit — eight rows, corpus/SOURCES.md:205-212` has a row for
each of S203–S210, each with a path, `opened 2026-10-24`, and a located quote
with a word count. Re-derived independently
(`.ufo/waves/round-35/scratch/RevLessonGate/quote-check.txt`):

| id | words | ≤25 | contiguous in its receipt |
|---|---|---|---|
| S203 | 14 | yes | yes |
| S204 | 13 | yes | yes |
| S205 | 17 | yes | yes |
| S206 | 13 | yes | yes |
| S207 | 15 | yes | yes |
| S208 | 14 | yes | yes |
| S209 | 13 | yes | yes |
| S210 | 15 | yes | yes |

Counts match the lesson's own parentheses exactly. The test used the quoted
string **including** the `located:` prefix, exactly as printed, against
`.ufo/waves/round-35/fetch/S2NN.receipt.txt` bytes (`q in bytes` → True ×8).
Paths match the registry rows for S203 (`~/.local/share/omarchy/bin/omarchy-first-run`),
S206 (`~/.config/waybar/config.jsonc`), S207 (`.../indicators/idle.sh`), S208
(`~/.local/share/omarchy/bin/omarchy-menu`); S204/S205/S209/S210 cite their own
registry path, which is the measured receipt. Quote authority is the entries'
`gate-quote:` lines and those still stand after the 03:35 errata (C1 `TARGET_MET`).

### 2 — Mistakes: FAIL

**M35-1 (id-space) — fix leg defect.** `class`, `evidence pointer`,
`captured-by`, `fix` are all present. The demonstrated command does not produce
the stated result. The lesson says:

> → 7 differing lines. The check passes only on a derived list; it fails on the
> copied one.

Run as written, the diff has **23 changed lines** (17 `>`, 6 `<`), because
`merge/mado/knowledge/corpus/knowledge/idle-lock-*.md` matches **8** package
entries and derives **19** unique ids — `S223 S225 S228 S282 S283 S289 S290
S291 S300 S301 S309 S315 S316 S327 S335 S336 S337 S340 S342` — not the eight
adopted documents. Narrowing the glob to the three admitted entries still gives
**14** changed lines (7 deletions, 7 insertions), not 7. The *conclusion* —
"seven of eight are wrong, only S336 matches" — is true for the narrow set; the
quoted command does not show it. Evidence: `scratch/RevLessonGate/diff-broad.txt`
(`changed_lines=23`, `broad_glob_files=8`, `rc=1`).

Note: the earlier dangling pointer to `.ufo/waves/round-35/w2/reports/RevIdRemap.md`
is **resolved** in v3 — that report now exists and opens "the registration's
list is **wrong**". No defect here.

**M35-2 (instrument) — pass.** All four fields; `corpus/QUALITY.md:361` is
criterion 55 and `:362` is criterion 56 (`sed -n '360,364p'` → 54/55/56 at
360/361/362); the demonstration reproduces:

```
$ python3 -B -I .ufo/waves/round-35/c1/count.py --root .ufo/waves/round-35/scratch/CritVacuous \
    --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   rc=0
```

That is the criterion failing the artifact — a demonstrated failing case for the
fix, as claimed. The repair itself is a stated round-36 claim.

**M35-3 (hygiene) — fix leg fail.** `Fix. none needed; the sweep stays in the
round report.` No failing case is shown, so "a fix that has been shown able to
fail" is unmet. The row also says it is "a **clean** sweep, not a defect", and
its evidence pointer is a `git status` command plus prose, not a committed
receipt.

**M35-4 (instrument) — fix leg fail.** The row claims:

> Demonstrated able to fail: the mutant receipts above are `TARGET_MET` on the
> current counter and `TARGET_MISSED` on the proposed one (the seat's M3a run is
> the receipt).

No "proposed" counter exists (the same row calls it a round-36 claim), and the
cited M3a run is the opposite of the claim —
`.ufo/waves/round-35/w2/reports/MutC2Real.md:100-101`:

```
pristine exit=0 … ledger_tip_ok=1 verdict=TARGET_MET
mutant   exit=0 … ledger_tip_ok=1 verdict=TARGET_MET      <-- survived
```

The only `TARGET_MISSED` near it is M3b (all six tip labels altered), on the
**current** counter. The fix therefore has no demonstrated failing case.

### 3 — Census before/after: FAIL (after output not pasted)

`### Census before → after` names the command correctly and pastes the **before**
run in a fenced block with `exit 0` — seven `W04` lines plus `mado ok`. The
**after** run is not pasted; it is described:

> **After** (registry 200 data rows), exit **0**: the same seven `W04` warnings
> on old ids (S030…S121), none on S203–S210, and the same `mado ok` line.

The element requires both outputs pasted. The description is substantively
correct — reproduced by this seat
(`scratch/RevLessonGate/census-after.txt`; `11` lines incl. command and exit):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	W04	S030 … S042 … S045 … S097 … S119 … S120 … S121 (7 lines)
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
exit=0
```

No finding names S203–S210. So the missing paste would have passed; the defect
is formal, not substantive. Row count 192 → 200 verified: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`
→ `200`; the 192-row pre-state is corroborated by `assimilation/reg-ids-pre`
(192 lines). The lesson carries no timestamp for the before run, so execution
"at round start" is asserted, not evidenced.

### 4 — Admit / reject with reason + flip: PASS

Admit: the eight rows above plus three entries with cite lists.
Reject: two named items, each with `refused:` reason and `Flip:` —

- `corpus/knowledge/chinese-article-revision-r30.md` (localization; outside
  `PROVINCE.md`) — exists in the package
  (`merge/mado/knowledge/corpus/knowledge/chinese-article-revision-r30.md`).
- staged row `S203` (Hyprland IPC page) — `merge/mado/SOURCES.append.md:7` is
  the Hyprland wiki IPC page as stated, and the S203 collision is correctly
  named.

Arithmetic checked against the package: 147 staged rows − 8 adopted = 139
refused; 65 knowledge files + 4 amendments = 69 items − 3 admitted entries = 66
refused. Both figures match the lesson.

## Defect list (exact)

- **D1** — `## Gate` / census: the **after** census output is described, not
  pasted (`corpus/lessons/round-35.md:47-51`). Only the before block appears.
  Requirement: both outputs pasted with exit codes.
- **D2** — `M35-1`: the demonstrated failing command does not reproduce "7
  differing lines". As written it yields 23 changed lines; the glob matches 8
  package entries / 19 ids instead of the 8 adopted documents. Under the
  intended three-entry glob it is 14 changed lines. The conclusion is right; the
  quoted result is wrong.
- **D3** — `M35-3`: fix is "none needed"; no failing case shown for the fix leg.
- **D4** — `M35-4`: the fix's claimed failing case ("`TARGET_MISSED` on the
  proposed one", citing M3a) is not in the cited receipt — M3a is `TARGET_MET`,
  and no proposed counter exists.
- **D5** — `## Gate` / Id-collision paragraph (line 146): the seat is quoted as
  saying "the `^ {0,3}` prefix **carries** the indent into the comparison key";
  `RevCollision.md:139-140` says "**embeds** the indent into the comparison key".
  Quotation is not verbatim.

## Verified and NOT defective (guard against over-reporting)

- C1 `TARGET_MET` rc=0 and C2 `TARGET_MET` rc=0 at v3; golden control
  `TARGET_MET` rc=0.
- `corpus/QUALITY.md:361` = criterion 55, `:362` = criterion 56.
- Freeze commit `19e4ab3171c1540c40d6b12097745af98053b07d` resolves in the lane
  repo (`git cat-file -e …^{commit}` rc=0).
- Collision evidence matches the lesson: `assimilation/reg-ids-pre` 192,
  `collisions-pre` 0 lines, `staged-ids` 147, `reg-ids` 200, `collisions` 8 lines
  = S203–S210, `guard/collisions` = `S203`.
- The collision-pipeline paragraph is mechanically right. On the committed guard
  fixture (`guard/reg.md` = `  | S203 | x |` + `| S204 | y |`,
  `guard/staged.md` = `| S203 | z |`), the specified pipeline
  (`grep -oE '^ {0,3}\|[^|]*' … | grep -oE 'S[0-9]+'`, per `w1-spec.json:49`)
  intersects at `S203`, count 1; dropping the second `grep` yields 0
  (`scratch/RevLessonGate/collision-check.txt`).
- All eight gate quotes are contiguous in their receipts (element 1 table).

## Out of scope

Not checked here: the truth of each row's substantive claim beyond quote
contiguity; the append procedure itself; the counters' internal logic (other
seats own that); the new errata section's per-entry findings beyond the one
counter re-run. No lane corpus file, counter, control, `SOURCES.md`, jj state,
Git index or sibling lane was written. `/home/vgpnk/Projects/shokuknow` was read
only (`ls`, `grep`, `diff`, `stat`) — nothing executed that writes there.

## Tooling

No installs, no upgrades, no package-manager invocation (pacman paused host-wide).
`python3 -B -I` for every counter run so no bytecode was written outside scratch.

## Artifacts

- `scratch/RevLessonGate/quote-check.txt` — 8/8 quote word counts and contiguity.
- `scratch/RevLessonGate/census-after.txt` — census after-run output + `exit=0`.
- `scratch/RevLessonGate/diff-broad.txt` — M35-1 command as written, `rc=1`,
  `changed_lines=23`, `broad_glob_files=8`.
- `scratch/RevLessonGate/collision-check.txt` — both collision pipelines on the
  committed guard fixture (count 1 / count 0).
- This report: `.ufo/waves/round-35/w2/reports/RevLessonGate.md`.
