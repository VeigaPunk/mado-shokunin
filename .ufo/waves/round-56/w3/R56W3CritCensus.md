# R56W3CritCensus

Attacked item: **the census still discriminates after the attempt-1 used-by fills at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`** — the census as a *detector*, not as a scoreboard. Frozen claims `claims-frozen-v2.md` / `registration-v2.md` were read first and never edited.

**Verdict: the census DOES still discriminate.** All six named mutants are flagged by the maintained `sources-census.sh validate --file`, each with a distinct, correct E-class. The tip registry itself is clean (0 E-classes, exit 0) and the null results are non-vacuous (411 mined used-by paths are actually checked; 357 base + 41 fill-added + 13 new rows reconciles to 411 exactly). Six further probes beyond the named six found **four** discrimination gaps, none of which is reachable by the attempt-1 fills as landed. Severity of the gaps is **weakens the claim** (a general census limitation), never **blocking this round's claim**, because the frozen predicates C1/C2/C3 are not census-shape claims and the fills as landed are not affected.

Deliverable: `.ufo/waves/round-56/w3/R56W3CritCensus/receipts/census-a2.txt` (both halves verbatim).

---

## Half 1 — every frozen manual census command over `corpus/SOURCES.md` at the tip

Extraction was read-only git; the lane's working tree was never touched.

```
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 | tar -x -C <scratch>/tree
```

`corpus/SOURCES.md` at the tip is byte-identical to the lane's working-tree copy (both sha256 `a9cd682198fba4d6cf52bfee3be667d942a740f65ab8dfa98f7f6b0780e75631`), so the tip tree and the lane root agree.

Verbatim output of all seven frozen commands (CORPUS.md `Census` section, column-zero forms):

```
### CMD1 rows (spacing-tolerant)
332
### CMD2 malformed rows — 11 columns means NF=13; must print 0
0
### CMD3 tier histogram
A=320 B=5 C=7
### CMD4 status histogram
mined=311 queued=10 rejected=11
### CMD5 duplicate ids — must print nothing
### CMD6 enum violations and tier inflation — must print nothing
### CMD7 mined rows whose used-by paths do not exist — must print nothing
```

CMD5, CMD6 and CMD7 print **nothing** — the null results the seat asks about. The command that found nothing, and the proof they are not vacuous:

- **CMD7** is the decisive one for this seat (it is the check that a fill could break). It checks every `used-by` path of every row with `status=mined` and `NF==13`. At the tip it checks **411 paths** (base `13f0acbe`: 357). 357 + 41 fill-added + 13 new rows S383–S395 = **411**, reconciling exactly. All 411 exist on disk, both from the extracted tree and re-run from the lane root itself (`cd /home/vgpnk/Projects/shokunin/mado-shokunin && <frozen CMD7>` → no output).
- CMD5's input is the same 332 ids; CMD6's input is the same 332 rows. Both are non-empty inputs producing empty output.
- Sanity: 311 mined rows, **0** mined rows carry `—`, **0** mined rows carry a blank cell, **0** used-by paths are a directory rather than a file. 332 rows all sit inside `## Registry` (lines ≤ 346; the `## Paths` section begins at 347).

Maintained census on the same registry (for comparison; `census` mode):

```
file	rows	332
file	tier.A	320  file	tier.B	5  file	tier.C	7
file	status.mined	311  file	status.queued	10  file	status.rejected	11
FLEET	rows	332 ... FLEET	missing	0
exit=0
```

Maintained `validate` over the tip registry: **exit 0**, `file ok`, with the W-class set `W01 × 1` (S277 tier-C mined) and `W04 × 36` (duplicate URL across scopes, from the 13 new rows repeating held URLs). Base-vs-tip code delta: `1×W01, 28×W04` → `1×W01, 36×W04`; **no E-class appears at either revision**. The L1 receipt `.ufo/waves/round-56/receipts/census-before-a2.txt` shows the identical W01+W04 set, so the L1's own baseline and my re-run agree.

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh selftest` → `selftest ok` (exit 0). The fleet script is at its committed state (`git status --porcelain scripts/sources-census.sh` empty; fleet commit `f47ad6ba`).

## Half 2 — six mutant registries through the maintained census

Each mutant is built over a **full lane-tip layout** (top-level entries symlinked to the tip tree; `corpus/knowledge`, `corpus/lessons`, `corpus/README.md`, `corpus/QUALITY.md` symlinked; only `corpus/SOURCES.md` replaced), so the *only* difference from the clean registry is the mutation. Command: `sources-census.sh validate --file <mut>/corpus/SOURCES.md`.

| # | mutant | maintained `validate` | exit | frozen manual census |
|---|---|---|---|---|
| 1 | malformed 11-col row (S001 scope cell deleted) | `file E01 S001 fields=10` | 1 | CMD2 → `1` |
| 2 | duplicate id (second S001 row, distinct url+scope) | `file E03 S001 duplicate id` | 1 | CMD5 → `S001` |
| 3 | bad status enum (S002 `mined`→`watch`) | `file E07 S002 status=watch` | 1 | CMD6 → `status S002 watch` |
| 4 | tier-A community (S003 kind→`community`, tier stays A) | `file E10 S003 community-at-A` | 1 | CMD6 → `tier-inflation S003` |
| 5 | mined row whose used-by path does not exist (S004) | `file E11 S004 missing used-by corpus/lessons/no-such-round-99.md` | 1 | CMD7 → `missing: corpus/lessons/no-such-round-99.md` |
| 6 | escaped `\|` in a cell (S005 teaches cell) | `file E01 S005 fields=12` | 1 | CMD2 → `1` |

**All six are flagged, each with a distinct and semantically correct E-class. The census has not lost discrimination.** The W-class noise (`W01`/`W04`) is identical to the clean registry's in every case, so each flag is attributable to the mutation alone.

Mutant 5 is the fill-shaped one and it is the decisive discrimination test: mutating one path that the attempt-1 fill actually added also fires:

```
--- PROBE: fill-corrupted-path   (S090's fill-added corpus/knowledge/walker-deep.md -> walker-deep.mdX)
    file E11 S090 missing used-by corpus/knowledge/walker-deep.mdX
    frozen CMD7: missing: corpus/knowledge/walker-deep.mdX
```

## Independent re-verification of the attempt-1 fills (my own reader, not the counter)

I re-derived the fill set from the base blob (`13f0acbe`) and the tip blob without using the counter: 23 existing rows changed, **41 (row, entry) pairs added**, 13 new rows S383–S395. Every one of the 41 added pairs names an entry that exists and whose text (outside fenced blocks) contains the row's id token: **0 defective**. The old→new log at `.ufo/waves/round-56/receipts/used-by-old-to-new.md` matches the base and tip cells exactly for all 23 rows (0 mismatches), and `corpus/lessons/round-56.md` logs the change set (rows 319→332, 41 paths, comma separators, M56-6).

C3 counter re-run at the tip, read-only, `--work` in scratch:

```
MADO_USED_BY: rev=0f3a54361a9824484d0801679ceb1fd8ac7c32e1 entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none
exit=0
```

---

## Defects found

### D1 — the census's `used-by` existence check (E11 / CMD7) is **status-blind below `mined`**, and a `queued`/`rejected` row with a dangling used-by path is invisible to it. **Severity: weakens the claim (general census limitation). Not reachable by the fills as landed.**

Input: `S006` (status `queued`) with `used-by` = `corpus/lessons/no-such-round-96.md` (does not exist on disk).

```
$ sources-census.sh validate --file <mutant>/corpus/SOURCES.md
file	ok	<mutant>/corpus/SOURCES.md
exit=0
```

Both the maintained `usedby_findings()` (`[ "$status" = mined ] || continue`) and the frozen CMD7 (`if (s=="mined")`) skip non-mined rows. The contract (`CORPUS.md` SOURCES.md `used-by`) defines `used-by` as "repo-relative paths of the knowledge entries or lessons citing the row" without restricting it to mined rows, so a non-mined row carrying a stale path is a real registry defect that neither census reports. At the tip this is **not** live: 0 queued/rejected rows carry a non-`—` used-by, and all 311 mined rows' paths exist. Smallest safe correction: make E11 (and CMD7) evaluate `used-by` for every row whose cell is not `—`, not only `mined`.

### D2 — a `used-by` cell that is **blank** (whitespace only) on a `mined` row is invisible to the census, and to the C3 counter too. **Severity: weakens the claim. Not reachable by the fills as landed.**

Input: `S001` (status `mined`) with the used-by cell set to a single space.

```
$ sources-census.sh validate --file <mutant>/corpus/SOURCES.md
file	ok	<mutant>/corpus/SOURCES.md
exit=0
```

The cell is neither `—` nor a path, so `W03` (mined-but-unused) does not fire, `E11` does not fire, and CMD7 splits it to an empty path that is skipped. The C3 counter is blind here too for a knowledge-path row's neighbours: emptying `S001` gives `missing=0`, because `S001` has no knowledge-entry cite pair (its only used-by was a lesson path, outside C3's `USED_BY` regex). Emptying `S090`'s cell — which *does* hold knowledge paths — is caught (`missing=10`, exit 1), so the hole is specific to rows whose used-by held only non-knowledge paths. Smallest safe correction: treat a whitespace-only used-by cell on a `mined` row as `—` for W03's purposes (or as E11 against the empty path).

### D3 — the frozen manual census and the maintained script **disagree on which used-by paths exist** when a cell uses `;` as a separator. **Severity: cosmetic-to-weakens. Not reachable by the fills as landed (the fills use commas).**

Input: `S001` used-by = `corpus/lessons/round-12.md; corpus/lessons/no-such-round-97.md`.

```
frozen CMD7  -> missing: corpus/lessons/no-such-round-97.md      (splits on [,;])
maintained   -> file E11 S001 missing used-by corpus/lessons/round-12.md; corpus/lessons/no-such-round-97.md
```

The maintained `usedby_findings()` splits on `,` only (`IFS=',' read -r -a paths`), so it treats the whole cell as one path and reports the *joined* string, which never exists. Both flag the row, so discrimination is intact, but the maintained message names a path that does not exist and the two tools disagree on the offending path. Smallest safe correction: split the maintained cell on `[,;]` like the frozen CMD7, or state the comma-only rule in `CORPUS.md`'s maintained-parser note.

### D4 — a `used-by` cell naming a **directory** (`corpus/knowledge`) is accepted by both censuses. **Severity: cosmetic. Not reachable by the fills as landed.**

Input: `S001` used-by = `corpus/knowledge` (a real directory).

```
$ sources-census.sh validate --file <mutant>/corpus/SOURCES.md
file	ok	<mutant>/corpus/SOURCES.md
exit=0
```

Both E11 and CMD7 use `[ -e "$path" ]`, which is true for directories. At the tip, 0 of the 411 used-by paths is a directory. Smallest safe correction: test `-f` rather than `-e`.

### D5 (observation, not a defect) — the strongest compensating mutation I could build is **still caught**: an escaped `\|` inside the `kind` cell plus a dropped `teaches` cell keeps `NF=13` and every enum-checked field legal-looking, and the census still fires (`E05 S006 kind=docs \`); the same trick on the `opened` cell fires `E08`. A variant that puts the escaped pipe in the `anchor` cell and drops the `teaches` cell **does pass the census** (`exit=0`, all frozen commands silent) — but it also produces a row whose `scope`/`teaches` content is silently shifted, so it is a content defect rather than a census-discrimination loss, and no such row exists at the tip (`grep -c '\\|' corpus/SOURCES.md` → 0). Recorded because it is the closest thing to a census evasion I found.

### D6 (observation, pre-existing, outside this round's fills) — **15 of the 41 non-`corpus/knowledge/` used-by paths name a file that does not contain the row's id** (S173/S174 → `tools/mado-binds.py`; S178–S182 → `tools/mado-wsrules.py`; S332–S339 → `.ufo/waves/round-47/w1/ExecSupresede/rows.md`). These 15 are **identical at the base revision** (0 new, 0 gone between base and tip), so the attempt-1 fill neither created nor worsened them. They matter because they are invisible to **both** censuses and to the C3 counter: C3's `USED_BY` regex is `corpus/knowledge/[A-Za-z0-9_.-]+\.md`, so a lesson/tool/wave path in `used-by` is not read at all, and E11/CMD7 only check existence. I confirmed this with a targeted fixture: a fill naming `corpus/lessons/round-13.md` on `S001` (a file that does not cite S001) yields `extra=0 … verdict=TARGET_MET` from the C3 counter and `exit=0` from the census. **Severity: weakens the C3 claim's coverage, but it is a pre-existing condition at the base revision and explicitly outside the frozen change set** — a ROUTED finding for round 57, not a change here. Note also that C3's `extra` leg *does* fire on a knowledge-path fill naming a real-but-wrong entry (`extra=1 … TARGET_MISSED`), so the discrimination that matters for the fills-as-landed is present.

---

## What I could not verify

- **Non-author closure of the 24 allowlist pairs.** The lesson states four allowlist pairs are disputed between the two wave-1 readers; the census cannot adjudicate that and neither can I.
- **Whether the 41 fill-added pairs are *semantically* reliance** rather than token-level coincidence. My reader checks token presence outside fences (the C3 `CITE` rule), which is what the frozen counter measures. Several of the 41 cite the row only inside a "Freshness pointer" / "superseded by" sentence (e.g. `walker-deep.md` L623 cites S090 in the negative context "superseded for the host by S090 line 2929"; `walker-deep-r9.md` L404 likewise), which is the same *shape* the 24-pair allowlist was built for — but the allowlist is frozen at 24 and these 41 were judged as reliance by both wave-1 readers. Whether the distinction holds is a closure question, not a census question, and the frozen predicate is unaffected either way. **This is the one finding I would route to round 57**: the attempt-1 fills were drawn from the *complement* of a frozen allowlist whose membership was decided on a different (pre-fill) reading, so a reader who now judges e.g. `S090 ← walker-deep.md` as name-only would want that pair moved to the allowlist. That changes a frozen predicate, so it is ROUTED, not changed.
- I did not run the C1/C2 counters or the control harness; this seat's scope is the census.
- I did not verify the corpus's `## Gate` non-author spot-check or the C1 entry's 30/30 and 33/33 legs (other seats' scope).

## Tooling

No tool was installed, upgraded or removed. Everything used was already present: GNU Awk 5.4.1 (`/usr/bin/gawk`), bash, coreutils, git 2.x (read-only), python3 (`-I`). No pacman transaction was attempted. Nothing under `~/.local/bin` or any PATH directory was created or modified. No credential material appears in any file I wrote.

## Scratch

All scratch lived under `/fast/scratch/hyaku/mado-r56/R56W3CritCensus/` (extracted tip tree, base tree, 21 mutant registries, one `git init` fixture clone at `fixture-repo/`, work dirs). The fixture's `git -C "$D" rev-parse --show-toplevel` was asserted equal to `$D` before its first commit, and its commits used `-c user.name=ctl -c user.email=ctl@ctl`. The lane's tracked files were never edited; no git/jj mutation of any kind was performed against the lane or the fleet repo (`git archive`, `git show`, `git rev-parse`, `git log`, `git status` only). The scratch tree is removed before this report is finalised.
