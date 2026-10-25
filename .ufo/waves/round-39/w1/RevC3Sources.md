# RevC3Sources — SOURCES rows review (round 39, w1)

Audit date: 2026-10-25 (round 39, hyaku run 7). Lane root:
`/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scope: inspect the final SOURCES rows **S218/S219/S220** + **S018 used-by**
in the tree; run the manual census from `CORPUS.md`; write no other file.

## 1. Target rows S218/S219/S220 — ABSENT at inspection time

Claim (frozen registration, `.ufo/waves/round-39/registration.md` § C3 /
Assimilation): S218 (Hyprland configuration/hyprlang option-syntax docs,
opened this round), S219 (`own-work` row for the options tool, opened this
round), S220 (0.56.0 Dispatchers page, reopened this round).

Observed tree state (`corpus/SOURCES.md`, 461 lines, single `## Registry`
table ending at the S277 row before `## Paths`):

- `grep -nE 'S21[89]|S220' corpus/SOURCES.md` → exit 1, **no matches**.
- `grep -nE 'option-syntax|config-option-table' corpus/SOURCES.md` → no matches (content probe).
- Registry has 211 rows; the last rows are S214–S217, S221, S253, S258, S277. No S218/S219/S220 row exists between S217 and S221 or anywhere else in the file.
- `jj status` (read-only): working copy is an empty delta on parent `457d1b12` ("round-39: freeze registration + base receipts + inherited r38 seat reports"); untracked round-39 artifacts are only `tools/mado-options.py`, `quality/counters/c3-r39-options.py`, and the `.ufo/waves/round-39/w1*` wave files. The SOURCES edits have **not landed** (not even uncommitted).

Therefore the per-row checks (11 columns NF=13, unique id, status=mined,
opened=2026-10-25, recheck ISO/NNd/on-*, used-by only admitted entries)
**cannot pass yet** for S218/S219/S220 — the rows do not exist in the tree
at inspection time.

## 2. S018 used-by — NOT extended as declared

Registration (Assimilation): "the held `HyprCtl.cpp` row S018 gets `used-by`
extended" (by the dispatcher-surface-and-request-grammar-r26 amendment).

Observed:

- S018 row (line 30): `used-by` = `corpus/knowledge/window-rule-effects-getprop.md` **only**. Unchanged from base; no dispatcher entry added.
- The held `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`
  exists but cites `source:` S186, S188, S196 — **not S018** (its §3
  request-socket grammar is anchored to S186:19/S186:30, S188:14).

## 3. Census — all commands PASS on the current tree

Manual census from `CORPUS.md` § Census (run from lane root, all exit 0):

| Check | Command | Result |
|---|---|---|
| Row count | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **211** |
| Malformed (NF≠13) | awk NF!=13 counter | **0** |
| Tier histogram | awk $5 | **A=203 B=1 C=7** |
| Status histogram | awk $9 | **mined=192 queued=10 rejected=9** |
| Duplicate ids | awk $2 \| sort \| uniq -d | **none** |
| Enum violations / tier inflation | awk $4/$5/$9 checks | **none** |
| Mined used-by paths exist | awk $12 loop, `[ -e ]` | **no missing paths** |

Fleet script (read-only, from fleet root):
`./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
→ `mado ok …` **exit 0** (only pre-existing W01/W04 warnings: W01 S277
tier-C mined; W04 duplicate-URL S030/S042/S045/S097/S119/S120/S121 — all
baseline, none round-39).
`… census --root … mado` → rows 211, FLEET missing=0, invalid=0, **exit 0**.

## 4. Findings

- **P1 (claim-blocking): rows S218/S219/S220 absent** — C3's quoted rows and
  the assimilation's S220 source are not in the tree; C3 `admitted=1/1`
  predicate artifacts (`corpus/knowledge/config-option-table-r39.md`,
  `quality/counters/c4-r39-options-entry.py`) are also absent.
- **P1 (claim-blocking): S018 used-by not extended** — the frozen assimilation
  declares the extension; the tree still has the base used-by, and the
  amendment entry does not cite S018.
- **P2:** the current registry is structurally clean (census all pass), so the
  missing rows are an incompleteness, not a table corruption.

## 5. Residual risk / verification gaps

- This review is **mid-wave**: the workforce is still writing round-39
  artifacts (C2 tool/counter present as untracked files; C3 files absent).
  Re-run the S218/S219/S220 + S018 checks after the data commit, then verify:
  NF=13 (11 columns), no literal `|` inside cells, unique ids, status=mined,
  opened=2026-10-25, recheck ∈ {ISO, NNd, on-*}, used-by names only admitted
  entries, and the censuses still pass (row count with the new rows,
  malformed 0, dup ids none, enums clean, mined used-by paths exist).
- If the assimilation ships, S018's used-by must gain
  `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`, and the
  append must be logged old→new in the round-39 lesson Gate (rule R2).
