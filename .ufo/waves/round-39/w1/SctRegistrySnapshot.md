# SctRegistrySnapshot — round-39 w1 SOURCES registry census snapshot

Seat: SctRegistrySnapshot · Wave: round-39/w1 · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
Scope: read-only census of `corpus/SOURCES.md` at the data tip, plus the list of
S-ids this round's entries use. No tracked file was edited; the only writes are
the two seat artefacts and this report.

## Artefacts written

- `.ufo/waves/round-39/w1/SctRegistrySnapshot/registry.json` (7,235 B) — machine-readable census
- `.ufo/waves/round-39/w1/SctRegistrySnapshot/census.txt` (7,344 B) — human-readable census with every command and its output
- `.ufo/waves/round-39/w1/SctRegistrySnapshot.md` — this report

## Data tip measured

```
$ git rev-parse HEAD
457d1b125932c1e0d797061a2156b917bcd7edaa
$ git log --oneline -1
457d1b1 round-39: freeze registration + base receipts + inherited r38 seat reports
$ sha256sum corpus/SOURCES.md
9bfd25da6a89a0cf09819803f6075f67c1f8da5694c8e5e30541fbd2f9083e62  corpus/SOURCES.md
$ git status --porcelain corpus/SOURCES.md
(empty — SOURCES.md is byte-identical to the freeze commit)
```

**OBS** No round-39 data commit has landed: `corpus/knowledge/config-option-table-r39.md`
and `corpus/lessons/round-39.md` are absent, and `tools/mado-options.py` exists only as an
untracked worktree file. So "the data tip" at snapshot time **is** the freeze commit
`457d1b1`, and the registry numbers below are the pre-append baseline. Polled the tip
6× over ~110 s while other seats ran; it did not move during the snapshot
(`poll1…poll6 tip=457d1b1 sources=9bfd25da6a89 entry=no`, job output bg_4475).

## Census result (all from the CORPUS.md manual commands, exit 0 on every one)

| metric | value |
|---|---|
| row_count | **211** |
| duplicate ids | **0** (empty — `sort \| uniq -d` printed nothing) |
| unique id count | 211 (max id `S277`) |
| tier histogram | **A=203 B=1 C=7** (invalid=0) |
| status histogram | **mined=192 queued=10 rejected=9** (invalid=0) |
| malformed rows (NF≠13) | **0** |
| enum violations (tier/status/kind/tier-inflation) | **0** |
| mined rows with missing used-by path | **0** |
| sections containing S-rows | `## Registry` only (no E12-class row outside the registry) |

Maintained CLI cross-check agrees exactly — `scripts/sources-census.sh census --root
/home/vgpnk/Projects/shokunin mado` → exit 0, `mado rows 211 / tier.A 203 / tier.B 1 /
tier.C 7 / status.mined 192 / status.queued 10 / status.rejected 9`, and `… validate …
mado` → **exit 0** with only the pre-existing W04×6 + W01×1 warnings, byte-identical to the
round-start baseline `.ufo/waves/round-39/receipts/census-before.txt`.

## S-ids used by this round's entries

- **New rows expected this round: `S218`, `S219`, `S220`** — none are in the registry yet
  (`grep -cE '^\|[[:space:]]*S(218|219|220)[[:space:]]*\|' corpus/SOURCES.md` → 0).
- **`S018` used-by extension** (second citation of the held `HyprCtl.cpp` row).
- All S-ids cited by round-39 drafts: **S018, S158, S187, S196, S218, S219, S220, S253, S258, S277**.
- Per draft: `ScrKnowledgeEntry/config-option-table-r39.md` → S218, S219 ·
  `ScrDispatcherAmendment/dispatcher-amendment-section.md` → S018, S158, S196, S220 ·
  `ScrSourcesRows/rows.md` → S018, S196, S218, S219, S220 ·
  `ScrLesson/round-39.md` → S018, S158, S187, S218, S219, S220, S253, S258, S277.
- **OBS** `ExecAssimIdGuard` confirms S218/S219/S220 are free: `grep -E '^S(218|219|220)$'
  reg-ids` → no match (registry_ids=211, staged_ids=147, collisions=19, none of them in the
  S218–S220 range).

## Two findings the integrator must act on

**1. S220 duplicates the S196 URL — W04 risk, not E04.** `S196` already holds
`https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/` with the *same* page bytes
(`sha256 f9b51362f2440e02…`, 297,863 B, revision "Last updated on July 15, 2026") and the
same used-by entry (`corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`).
Drafting S220 as a fresh row over the same URL with a different scope produces the
maintained validator's `W04 duplicate url … across scopes` — a warning, exit status stays 0,
so `scripts/sources-census.sh validate … mado` still exits 0 at round end. `ScrSourcesRows`
flagged this verbatim and left it to the judge. [INFERENCE] If S220 lands as drafted, expect
one additional W04 line against the current 6.

**2. S219's receipt hash in the lesson draft is already stale.** `ScrLesson/round-39.md`
binds S219 to `sha256=9787b53b298216aee93ec1193814e2972d9fef9125656ce9ed0bd03ed7fbcf59`
(`tools/mado-options.py` at draft time). The tool file has since been edited: the current
worktree bytes hash to
`cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e`
(37,358 B, mtime 2026-10-25 16:10:55 -0300; stable across a 20 s re-hash). The lesson's
"re-hash at data tip" instruction is therefore load-bearing — the row's sha256 must be taken
from `git show <data-tip>:tools/mado-options.py | sha256sum`, not from the draft-time
worktree hash. Quote check is still good: `tools/mado-options.py:2` reads
`"""mado-options.py - static resolver of the config-tree option table.`

## Projected state after the append [INFERENCE]

If S218/S219/S220 land as drafted (all tier A, status mined) and nothing else changes:
row_count **214**, tier A=206 / B=1 / C=7, status mined=195 / queued=10 / rejected=9,
malformed still 0 (the three drafted rows measure NF=13 in `ScrSourcesRows/rows.md`), and
the S018 change-line table in that draft is NF=7 — it is a 4-column old→new change table, not
an 11-column registry row, and must not be appended verbatim into `## Registry`.

## Commands run (all read-only, all exit 0)

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md                                  # 211
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' …           # 0
awk -F'|' … $5 tier histogram …                                                                         # A=203 B=1 C=7
awk -F'|' … $9 status histogram …                                                                       # mined=192 queued=10 rejected=9
awk -F'|' … $2 id … | sort | uniq -d                                                                    # (empty)
awk -F'|' … enum check (tier/status/kind/tier-inflation) …                                              # (empty)
awk -F'|' … mined used-by paths … | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done         # (empty)
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census   --root /home/vgpnk/Projects/shokunin mado  # exit 0
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado  # exit 0
```

## Tooling

No installs. `awk`/`grep`/`git`/`sha256sum` were already present; `scripts/sources-census.sh`
is the fleet's maintained CLI and was run read-only against the lane (it writes only stdout).
No pacman transaction, no mutating git/jj, no host config tree or socket touched.

## Final answer (≤6 lines)

1. Census at data tip `457d1b1`: rows=**211**, duplicate ids=**0**, tier A=203/B=1/C=7, status mined=192/queued=10/rejected=9, malformed(NF≠13)=**0**; maintained `validate … mado` exit **0**, same 7 pre-existing warnings as `census-before.txt`.
2. This round's S-ids: new rows **S218/S219/S220** (none in the registry yet — no data commit has landed) plus the **S018** used-by extension; drafts cite S018, S158, S187, S196, S218, S219, S220, S253, S258, S277.
3. `ExecAssimIdGuard` confirms S218/S219/S220 are collision-free (registry_ids=211, collisions=19, none in range).
4. **S220 duplicates S196's URL** (same page bytes, same used-by) → one added W04 warning at round end; exit status stays 0.
5. **S219's lesson-draft hash `9787b53b…` is stale** — current `tools/mado-options.py` bytes hash `cee78d99…`; re-hash from `git show <data-tip>:tools/mado-options.py`.
6. Artefacts: `.ufo/waves/round-39/w1/SctRegistrySnapshot/registry.json` + `census.txt`; no tracked file edited, no tools installed.
