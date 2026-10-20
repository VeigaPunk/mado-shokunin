# CensusRerun — round-17 wave 2 falsification (census / SOURCES rows)

Item: run the fleet census validator against the lane and check every new row S056-S070
against the validator's own rules. Installs: **none**. Host pause honored: no
pacman/yay/paru/sudo/systemctl/hyprctl/live probe of any kind; config and
`/var/log/pacman.log` read as file bytes only. Mutation tests ran on `/tmp` copies only.

Artifact under attack: lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`, lane HEAD
`988b858bd6049bc709807534fd725c05264f7e60`. `corpus/SOURCES.md` at that commit has
sha256 `931a8375b88e7936b84c9f49f72ef40cceb478f93b885d1d40642b2ce7fa0f60` (70 rows).
Working tree changed during this item (§8); the verdict below is pinned to the committed
artifact, reproduced from a `git show` export of all 48 `corpus/` files at that commit.

## 1. Validator output (verbatim, exit 0)

Command as assigned:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
EXIT=0
```

No `E` code, and no `W` code on any of S056-S070. The three `W04`s are rows from rounds
12/13; they are not introduced by round 17 (proof: the same three appear when the
`0175f13` corpus is validated — §2 — so the warning set is byte-stable across the round).

## 2. Census totals and delta

| state | rows | A | B | C | mined | queued | rejected | exit |
|---|---|---|---|---|---|---|---|---|
| `0175f13` (pre-round-17, 48-file export) | 55 | 51 | 1 | 3 | 43 | 8 | 4 | 0 (same 3 W04) |
| `988b858` HEAD (48-file export) | 70 | 63 | 1 | 6 | 55 | 8 | 7 | 0 (same 3 W04) |
| delta | **+15** | +12 | 0 | +3 | +12 | 0 | +3 | — |

Every partition sums to its row total; `FLEET missing 0`. The delta is exactly
S056-S070, and it matches the lesson's own arithmetic (`corpus/lessons/round-17.md:60`,
"55 → 70; tier A 51 → 63, C 3 → 6; mined 43 → 55") with no residual.

Contract's own census block (`SOURCES-CONTRACT-v1.md` § Census), run at HEAD:

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
70
$ awk -F'|' '... NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
```

Independent re-derivation: a separate Python parser (not the shell/gawk path) over the
whole 70-row registry reproduces exactly three findings — W04 S030, W04 S042, W04 S045 —
and nothing touching S056-S070.

## 3. Row-by-row S056-S070

All 15 rows are `NF=13` (11 content columns, no `|` inside a cell), no duplicate ids
(S001-S070 strictly increasing, 70 unique).

| id | kind | tier | status | opened | recheck | used-by (path exists?) | codes |
|---|---|---|---|---|---|---|---|
| S056 | docs | A | mined | 2026-10-20 | on-release | terminal-route-r17.md ✓ | none |
| S057 | code | A | mined | 2026-10-20 | on-release | terminal-route-r17.md ✓ | none |
| S058 | docs | A | mined | 2026-10-20 | on-release | terminal-route-r17.md ✓ | none |
| S059 | code | A | mined | 2026-10-20 | on-change | terminal-route-r17.md ✓ | none |
| S060 | code | A | mined | 2026-10-20 | on-change | terminal-route-r17.md ✓ | none |
| S061 | docs | C | rejected | 2026-10-20 | 180d | — | none |
| S062 | community | C | rejected | 2026-10-20 | 180d | — | none |
| S063 | docs | A | mined | 2026-10-20 | 90d | idle-lock-route-r17.md ✓ | none |
| S064 | docs | A | mined | 2026-10-20 | 90d | idle-lock-route-r17.md ✓ | none |
| S065 | docs | A | mined | 2026-10-20 | on-change | idle-lock-route-r17.md ✓ | none |
| S066 | code | A | mined | 2026-10-20 | on-change | idle-lock-route-r17.md ✓ | none |
| S067 | code | A | mined | 2026-10-20 | on-change | idle-lock-route-r17.md ✓ | none |
| S068 | code | A | mined | 2026-10-20 | on-change | idle-lock-route-r17.md ✓ | none |
| S069 | docs | A | mined | 2026-10-20 | on-change | idle-lock-route-r17.md ✓ | none |
| S070 | community | C | rejected | 2026-10-20 | 180d | — | none |

Rule-by-rule: kind ∈ {docs, code, community} ⊂ the 10-value enum (no E05); tier ∈ {A, C}
(no E06); status ∈ {mined, rejected} (no E07); `opened` = today, not future (no E08);
`recheck` ∈ {on-release, on-change, 90d, 180d} (no E09; `on-release`/`on-change` are
established in S016/S040/S044); no community row at tier A (S062/S070 are C, no E10);
no tier-C mined row (all three C rows rejected, no W01); rejected `teaches` cells are
long, not thin (no W02); every mined row names a used-by path (no W03); both used-by
files exist on disk (no E11) **and actually cite the rows they own** —
terminal-route-r17.md cites S056-S060 in its `source:` header (`:1`) and S061-S062 at
`:131`; idle-lock-route-r17.md cites S063-S069 at `:1` and `:3`; no URL collision with
another row (no E04/W04).

One strictness note, lane-wide and pre-existing: the contract defines `used-by` as the paths
that cite the row, yet rejected S061/S062 carry `—` although `terminal-route-r17.md:131`
and the lesson Gate cite them; S030/S045 behave identically. This is the lane's
rejected-row convention, not a round-17 defect, and it is invisible to E11/W01/W03 because
all three inspect `status=mined` only.

Tier/kind assignments are precedent-consistent: tag-pinned upstream raw = A (cf. S053/S054);
host file bytes = A (cf. S020, S043); current hypr wiki "Latest git" = A (cf. S016/S017/S029);
third-party/Arch-wiki restatement = C community/docs (cf. S010-S012).

## 4. Non-vacuity — mutation matrix on a `/tmp` copy of exactly these 15 rows

Baseline copy (15 rows + the two used-by stubs): `ok`, exit 0. One injected violation at a
time, each fired the expected code with the expected id, so the `ok` verdict is informative
rather than vacuous:

| mutation | observed | exit |
|---|---|---|
| S066 `kind=blog` | `E05 S066 kind=blog` | 1 |
| S066 `tier=D` | `E06 S066 tier=D` | 1 |
| S066 `status=watch` | `E07 S066 status=watch` | 1 |
| S066 `opened=2026-12-01` | `E08 S066 opened=2026-12-01` | 1 |
| S062 `community` at tier A | `E10 S062 community-at-A` | 1 |
| S059 used-by → missing file | `E11 S059 missing used-by …nope-r17.md` | 1 |
| S060 anchor cell dropped | `E01 S060 fields=10` | 1 |
| S056 row duplicated | `E03 S056 duplicate id` (+E04) | 1 |
| S999 copy of S056 url+scope | `E04 S999 duplicate url … within scope …` | 1 |
| S998 same url, reworded scope | `W04 S998 … across scopes` | 0 |
| S062 tier C → mined (used-by `—`) | `W03 S062 mined but unused` | 0 |
| S062 tier C + mined + real used-by | `W01 S062 tierC mined used-by=…` | 0 |
| S070 rejected with 1-word teaches | `W02 S070 thin reject reason` | 0 |
| rows moved under `## Paths` | `E12 S066/S067/S068 row outside Registry section` | 1 |

## 5. Where the checker is weaker than the prose rule (properties, not row violations)

Demonstrated on the same copy; none is triggered by S056-S070, but each bounds what
"used-by existence" and "cadence" mean here:

1. **E11 only inspects `status=mined`.** A `queued` row with
   `used-by=corpus/knowledge/ghost.md` and a `rejected` row with the same pass with **no
   code** (`usedby_findings()` skips non-mined rows). New rows are not exposed (their
   non-mined rows use `—`).
2. **E09 accepts any alphabetic token as a symbolic cadence** (`symbolic()` =
   `^[A-Za-z][A-Za-z0-9 _-]*$`): `recheck=banana` and `recheck=soon-ish` both validate
   clean. The new rows use only existing vocabulary.
3. **E04 requires byte-identical `scope` prose.** A duplicate URL with reworded scope
   downgrades to the `W04` warning (exit 0), so "duplicate url within scope" is evadable
   by rewording. The new rows have no URL collisions at all.

## 6. Concrete counterexample that survived: rule 5 (Search log) is unmet for round 17

The registry is row-valid, but the contract duty attached to adding rows is not satisfied.

All line numbers in this and the next section are **HEAD (`988b858`) numbering**; the live
tree is +1 after `:82` because of the uncommitted S071 (§8).

- `corpus/SOURCES.md:115` `## Search log` holds per-round notes for round 12 (`:117`),
  round 13 (`:148`), round 14 (`:181`, plus two correction notes), round 15 (`:209`), and
  round 16 (`:224`), each carrying question, where, date, identified/screened/included/
  excluded counts (or an explicit statement that the count unit is the registry delta —
  rounds 14/15/16 name S047/S048, S051/S052, S053-S055 respectively) and a stop rationale.
- The section ends at round 16 and is followed by `## Leads (unopened)` at `:236`.
  **There is no Round-17 note** (`grep` for round-17 prose in `:115-235` = 0).
- Contract v1 (`SOURCES-CONTRACT-v1.md` § Shape, rule 5) defines `## Search log` as "one
  prose note per bounded search" with "identified / screened / included / excluded counts,
  exclusion reasons, stop rationale". Round 17 opened 15 sources and ran bounded searches
  for them; the lesson's `## Gate` (`corpus/lessons/round-17.md:22-60`) lists candidate
  classes but gives no identified/screened/included/excluded counts and does not live in
  the mandated section.
- The census validator exits 0 regardless: it only parses `## Registry` table rows and
  never reads the `## Search log` prose.

So the C2 statement "SOURCES S056-S070" is true as *row validity* and false as *round
completeness*: the sources were opened and recorded, but the round's search accounting was
not appended to the section the contract names.

## 7. Weaker departure: `## Paths` not updated for round 17

`corpus/SOURCES.md:84-114` carries path bullets through round 16 (U7 Waybar, S053-S055);
zero mention of round 17, S056-S060, S063-S069, or the terminal / idle-lock routes. This
is **not** a numbered contract rule (Shape merely defines Paths as "ordered study
sequences"), but rounds 13, 14, 15 and 16 each appended one, and the two new knowledge
files are exactly such sequences. Report as convention drift, not an E/W violation.

## 8. Live working-tree mutation observed during this item (integration hazard)

The working tree is not at HEAD. At the time of writing:

```
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/knowledge/terminal-route-r17.md
 M corpus/lessons/round-17.md
?? .ufo/waves/round-17/w2/   (and other wave artifacts)
```

- `corpus/SOURCES.md` gained one uncommitted row, **S071** (host user-local
  `Alacritty.desktop`, code/A/mined/on-change, used-by `corpus/knowledge/terminal-route-r17.md`),
  mtime `2026-10-20 11:56:37 -0300` (14:56:37Z) — it appeared *after* my first census run,
  which saw 70 rows. Diff is exactly `+1` line at `:83`.
- Re-running the validator on the live tree: **exit 0**, same three W04, `ok`; census
  rows 71, A 64, B 1, C 6, mined 56, queued 8, rejected 7. S071 is itself census-valid:
  NF=13, valid enums, used-by file exists and cites S071 at `terminal-route-r17.md:1` and
  `:75`. README's row was updated to `S056–S060, S071` in the same edit.
- **But S071 has no `## Gate` entry**: `grep -c S071 corpus/lessons/round-17.md` = 0, and
  the Gate still says `55 → 70` (`:60`). If S071 is intended to land as a round-17 row,
  contract rule 1 ("the round lesson's `## Gate` records, for every new row, the URL, the
  access date, and a ≤25-word quote") is unmet for it and the Gate count is stale by one.
  If it is not intended to land, it is an uncommitted edit on the registry that the round
  does not claim.

I did not touch the lane tree. The main agent decides whether S071 is in scope and whether
the lesson Gate must gain its row before the registry is committed.

## 9. Attack result

- **Falsifying "S056-S070 are census-valid / the C2 SOURCES landing is real": failed.**
  All 15 rows pass every E/W rule, independently recomputed; totals and delta reconcile
  exactly with the lesson; the validator's clean exit 0 is non-vacuous (14 mutants fired
  the right code on these very rows).
- **Falsifying "the round-17 registry is contract-complete": succeeded, narrowly.**
  Rule 5's round-17 search note is absent from `## Search log` (§6) — a real, anchored
  deviation the validator cannot see. Two weaker items: no round-17 `## Paths` bullet
  (§7) and, in the live tree only, an S071 row without a Gate record (§8).
- The three `W04` warnings and `ok` are pre-existing and unchanged by the round; nothing
  in S056-S070 introduces an E code or a new W code.
