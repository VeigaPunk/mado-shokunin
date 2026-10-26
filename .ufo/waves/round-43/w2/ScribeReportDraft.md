# ScribeReportDraft — Sources & frontier + Trend verdicts (round 43, w2)

Seat `ScribeReportDraft`, role scribe, 2026-10-26. Deliverable: a draft of the round report's **Sources &
frontier** and **Trend verdicts** sections, built only from committed blobs and the round's receipts.

- **Full draft (the deliverable):** `.ufo/waves/round-43/w2/ScribeReportDraft/draft.md`
- **Number re-derivation (this seat's own check):** `.ufo/waves/round-43/w2/ScribeReportDraft/verify.py`
  → output `.../ScribeReportDraft/verify.txt` — `90` checks, `VERIFY: all checks PASS`, `rc=0`.

Nothing in the lane was edited or committed. No tool installed, no scratch tree created, no host/compositor
call made, no git write verb run (only `git show` / `diff` / `ls-tree` / `log` / `ls-files` / `status` /
`rev-parse` / `merge-base`).

## Behavior (what the draft establishes)

**Registry, before → after.** Counting command (`corpus/lessons/round-43.md:28`), run on the two blobs:

```sh
for R in a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f 1959770657f1f8665097c1aed4be6c1cbb07139f; do
  git -C . show $R:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
done      # 226, 234
```

- rows **226 → 234** (+8), distinct ids **226 → 234** (the two counting forms agree, so the 8 rows are 8 ids);
  `corpus/knowledge/` entries **59 → 60**.
- by tier: **code 101→106** (S290-S294), **own-work 24→27** (S295-S297), docs 78, spec 13, community 5,
  paper 3, dataset 1, book 1 all unchanged; tier sum 226 → 234.
- all eight new rows: `status=mined`, `opened 2026-10-26`, `used-by corpus/knowledge/hyprland-gkeep-geometry-r43.md`;
  S290-S294 `recheck on-release`, S295-S297 `2027-01-24`. Ids contiguous, `S298`/`S299` free.
- rows touched old→new: **exactly two, `used-by` cell only** — S155 gains `, corpus/knowledge/hyprland-gkeep-geometry-r43.md`;
  S158 gains the same one item after its five. Evidence: `git diff --numstat a35cfdf 1959770 -- corpus/SOURCES.md`
  → `10 2`, and fields 1-10 of both rows are identical at the two revs.
- census did not move: `census-before.txt` = `census-after-data.txt` on the 8 finding rows (7× `W04` +
  `W01 S277`), `exit=0`.

**Frontier.** `git diff --numstat a35cfdf 1959770 -- corpus/README.md` → `10 0` (no deletion, no edit of an
existing line): one coverage-map index row (`corpus/README.md:71`) and one **new** route
(`:294-303`, `### Round-43 rule-size versus reported-size route`) that parks four open items. **Pre-existing
Frontier bullets advanced: zero** — checked, since the base README carries only two `gkeep` mentions, both
index rows (:37, :69). Instrument: `tools/mado-geometry.py` (+417 lines), byte-identical to
`.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (sha256 `e3c2e471…` both, `cmp` silent).

**Assimilation (theme: gkeep geometry).** 11 candidates → **1 ADMIT** (`gkeep-size-to-real-size-r11.md` →
`corpus/knowledge/hyprland-gkeep-geometry-r43.md`), **4 REFUSE** (r10, r8, r11-observation, r30 — each with a
pinned source that overturns it and a flip condition), **6 not adopted** (r9, r12, r13, r14, r15, r31). Scored
at the data rev: `receipts/c2-after-data.txt:31-33` `clauses=a:1 … i:1 admitted=1`, `admitted=1/1 …
TARGET_MET`, `exit=0`; base `admitted=0/1`.

**ID guard.** 34 collisions (reg 226 / staged 147); guard shown able to fire on a scratch registry
(`S203`); two measured blind spots (4-space indent invisible; ids only, never URLs); 10 staged ids in the
reserved S290-S299 band are under-reported. The round answered the duplicate-pin hazard by citing held rows
S155/S158 instead of opening second rows.

**Trend verdicts (summary table the report can lift verbatim).**

| trend | verdict | one-line evidence |
|---|---|---|
| expansion | **improved** | rows 226 → 234 (+8: code +5, own-work +3), entries 59 → 60, one new Frontier route + one new instrument |
| quality | **improved** | QUALITY +5 criteria (77-81), new `quality/check-locators.py` (405 lines), 10 GATE lines, all 8 mistakes carry a shown-able-to-fail line (6 demonstrated and gated, 1 not yet a gate, 1 not shown); no criterion or held-row cell harmed |
| discernment | **improved** | 11 candidates → 1/4/6; a duplicate-row defect (S045 class) avoided; one stale artifact ships as F1 |
| axes | **unchanged at base / UNVERIFIED at data** | `receipts/axis-base.txt` only (all three axes at max); no axis receipt at `1959770` |

## Gates (what the draft rests on; all read, none run by this seat except the verifier)

| gate | value | pointer |
|---|---|---|
| C1 at data rev | `fixtures=37/37 tool=present verdict=TARGET_MET`, exit 0 | `receipts/c1-after-data.txt:49-50` |
| C2 v2 at data rev | `admitted=1/1 verdict=TARGET_MET`, exit 0 | `receipts/c2-after-data.txt:31-33` |
| C2 v1 at data rev (superseded) | `admitted=1/1` | `receipts/c2-v1-after-data.txt:32` |
| C2 v2 at base | `admitted=0/1` | `receipts/c2-v2-before-base.txt:2` |
| controls (C1) | `controls=46`, `0 of 47`, reference met 1 — **at base rev** | `receipts/ctl-c1.txt:1,50` |
| controls (C2 v1 / v2) | `controls=74 correct=74/74` each | `receipts/ctl-c2.txt:76`, `ctl-c2-v2.txt:76` |
| census after data | same finding set as before, exit 0 | `receipts/census-after-data.txt:10` |
| live host run (reported, not scored) | 4 clients, no gkeep, `NO_MATCHING_CLIENT`, exit 3 | `receipts/live-geometry-host.txt:10-11` |
| lesson Gate | 10 `^GATE S` lines (`:34-43`); counter prints `gates=1 bound=1` for all 10 ids | `corpus/lessons/round-43.md:34-43`; `receipts/c2-after-data.txt:11-20` |

## Touched surfaces

Written by this seat (2 files + 1 receipt, all inside the seat's write scope):

- `.ufo/waves/round-43/w2/ScribeReportDraft/draft.md` — the deliverable draft.
- `.ufo/waves/round-43/w2/ScribeReportDraft/verify.py` — read-only re-derivation script.
- `.ufo/waves/round-43/w2/ScribeReportDraft/verify.txt` — its output (90 checks PASS, rc 0).
- this report.

Read-only elsewhere. Frozen files untouched: `corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md`,
`corpus/lessons/round-43.md`, `quality/counters/*`, `quality/check-locators.py`, `tools/mado-geometry.py`,
`registration.md`, `registration-v2.md`, `.ufo/state/`, the lane index.

## Findings for the L1 (detail + evidence in `draft.md` §5)

- **F1** The id-guard's `assimilation/renumber-map.tsv` is stale by one id for five documents (DefaultFloating,
  Target, WindowTarget, GeometricMovableAnimated, gkeep.conf) — it maps them to S292/S293/S294/S295/S297, the
  landed registry holds S291/S292/S293/S294/S295. The map's own §6 finding 4 warns against exactly this reuse.
  Not edited by this seat.
- **F2** No control or axis receipt exists at the data rev: `ctl-c1.txt:1` and `axis-base.txt:4` both read
  `rev=a35cfdf…`. Controls carry to the tool by byte identity; the report must not describe a control or axis
  run "at the data commit".
- **F3** `quality/check-locators.py` has no receipt at the data commit; its runs on the landed entry are w1's and
  the wave's, so its pass on the landed entry is **UNVERIFIED** here (the counter's clause-g locators are the
  committed proxy: 10 ids, `receipts/c2-after-data.txt:21-30`).
- **F4** The data commit's tree carries no `.ufo/waves/round-43/assimilation/` file and no w1 seat report; those
  land at `a47efeb`/`2a3707c`. Report wording must say "committed at `2a3707c`", not "in the data commit".
- **F5** The round did not observe a live gkeep window: `live-geometry-host.txt` is a null observation on four
  tiled clients, and the 420x500 floating figure comes from the isolated round-27 oracle (not re-run here).

## Out of scope / not done

- Did not re-open the assimilation package under `/home/vgpnk/Projects/shokuknow/merge/mado/` (the four REFUSE
  grounds are reported as the ledger states them); did not run any counter, control, tool, or compositor read.
- Did not edit the round report, the registry, the lesson, the counters, or the renumber map (F1 is a decision
  for the L1).
- No tooling installed (pacman is paused host-wide; nothing needed). No scratch directory was created, so none
  is left behind.

## UNVERIFIED (do not upgrade in the report)

1. `check-locators.py` on the landed entry at `1959770` (F3).
2. Axis / harm / controls at the data rev or the tip (F2).
3. The four REFUSE grounds as re-derived evidence (read as ledger text only).
4. The isolated-oracle 420x500 observation (not re-run; host-safety scope).
