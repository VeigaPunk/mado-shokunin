# Attack29 — C2 index row and knowledge entry match (seat report)

Seat: `Attack29` (connector), wave `w2`, round 52. Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`,
HEAD = base `85d57a818c3707397e21c840b6498b105ba798aa` (detached `* (no branch)`).
Axes: **coverage** (target), **operability** (untouched). Attack, not a vote; non-author judgment not claimed.

## Attacked clause

`claims-frozen.md` C2: "a distinct new indexed knowledge entry … each material factual proposition maps to a
pinned source quote <=25 words"; `registration.md` C2: "A counter checks proposition count, row/pin/quote
bindings and index". Scoped clause for this seat: **the index row in `corpus/README.md` and the knowledge
entry it names actually match** — and the committed counter can bind the two.

## What verified (worktree, observed)

- `corpus/README.md` (worktree) line 80 adds row `` `knowledge/hyprland-synthetic-dispatch-r52.md` (round 52; source-pinned synthetic shortcut path) ``; the file `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (6535 B, worktree) exists; basename match 1:1, exactly one README mention.
- Row description matches entry content: "argument parsing, key resolution and seat keyboard-call ordering… no dispatcher was run and no client receipt is claimed" ↔ entry title line and P01–P18 (parse P01–P12, delivery P13–P18) and the closing disclaimer.
- Row's `source:` cites S370–S373; `corpus/SOURCES.md` worktree rows S370–S373 (lines 320–323) all carry used-by `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`, status `mined`, opened `2026-10-27`, 40-hex revision and `r52 fetch SHA256` digests; all four digests equal `.ufo/waves/round-52/fetch/SHA256SUMS` entries; all four pin basenames exist under `.ufo/waves/round-52/fetch/`.
- Spot-checked anchors: pins at cited lines contain the cited code (e.g. `sendKeyboardMods(modMask,0,0,0)` at ConfigActions.cpp:1554; repeat guard at DispatcherTranslator.cpp:619-622).
- Base is clean: `git show 85d57a81:corpus/SOURCES.md | grep -c 'S37[0-3]'` → 0; pickaxe `git log --all -S hyprland-synthetic-dispatch-r52` and `-S hyprland-synthetic-key-dispatch-r52` → 0 commits each.

## Falsifier A — the matched pair exists only in the uncommitted worktree

Repro:
```
cd mado-shokunin && git status --porcelain | grep -E 'README|SOURCES|synthetic|c2-r52'
 M corpus/README.md;  M corpus/SOURCES.md;
?? corpus/knowledge/hyprland-synthetic-dispatch-r52.md; ?? quality/counters/c2-r52-proposition-entry.py
git show HEAD:corpus/knowledge/hyprland-synthetic-dispatch-r52.md  → fatal: exists on disk, but not in 'HEAD'
python3 -I quality/counters/c2-r52-proposition-entry.py --repo . --rev HEAD --work <scratch>
  → C2_R52: entry=absent verdict=TARGET_MISSED rev=HEAD   (exit 1)
```
Observed: index row, entry, source rows and the counter itself are all uncommitted. The counter reads
`git show <rev>:<path>` (line 23/26), so at **every** revision the index/entry pair is absent. The frozen
claim requires a committed counter checking a new indexed entry; the index↔entry match is presently true
only between two uncommitted artifacts — no committed revision binds them. Wave warning confirmed:
`w1/C2CounterDraft/receipts/r-green.txt` green ran against a synthetic fixture, not this landing.

## Falsifier B — committed counter default slug ≠ landed slug

Repro: `quality/counters/c2-r52-proposition-entry.py:19` defaults
`--entry corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`; the landed file is
`corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (no `key-`). The W1 draft's own constant carried the
same stale slug with the comment "integration should set this constant to the landed path"
(`w1/C2CounterDraft/c2-r52-proposition-entry.py:99-101`) — integration did not. If the current worktree
were committed as-is, a default run would still print `entry=absent TARGET_MISSED`, and its `indexed`
substring check would search for `knowledge/hyprland-synthetic-key-dispatch-r52.md`, which the README row
never names. The counter's index↔entry binding is structurally wired to a filename that does not exist.

## Falsifier C — committed counter cannot parse the landed table shape

Repro (exact regex from committed counter line 28 run over the landed entry bytes):
```
pat = r'^\|\s*(P\d+)\s*\|\s*(S\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*$'
re.findall(pat, open('corpus/knowledge/hyprland-synthetic-dispatch-r52.md').read(), re.M) → 0 matches
```
Observed: the regex requires the `S###` row id in the table's **second** column; the landed table (like the
W1 draft it replaced — same column order, verified) puts the claim text second and `S###` third.
18 P-rows exist, `props=0` → `props` defect → `TARGET_MISSED` even if the entry were committed and the
`--entry` override given. So the "checks proposition count … and index" predicate cannot ever fire green
on the landed entry as written.

## Counter-coverage gap vs claim text (reported error)

The committed counter drops the W1 draft's binding checks: no fetch bytes are read, no anchor line-span is
opened, no quote-location test is run — it never verifies a quote appears in the pinned source (only word
count ≤25 and non-empty). Its `indexed` check is a whole-file substring search, not an index-row check.
Claim text promises "row/pin/quote bindings"; the landed counter cannot bind a single pin or quote.

## Additional errors observed (adjacent, reported not judged)

- **P17 misattribution**: landed table claims "`sendshortcut`'s repeat branch" at
  `DispatcherTranslator.cpp:619-622`; that code sits inside `sendkeystate` (function opens at :590;
  `sendshortcut` closed at :588). The reviewed draft carried no such misattribution — introduced at integration.
- **P04/P17 duplicate**: both assert "repeat → second `sendshortcut` call iff first succeeded", same row
  (S370), same anchor (619-622), overlapping quotes. Duplicate-claim check (draft counter clause b) would flag.
- **Missing entry id**: every prior index row carries a `MADO-R##-#` id; the r52 row has none.
- **QUALITY17 outstanding**: `corpus/SOURCES.md` search log admits "S370, S371 and S373 reuse canonical
  URLs with new scopes; distinct-scope review remains outstanding"; `census-after.txt` logs the three rows
  as W04 duplicate-URL warnings. QUALITY.md §17 requires explicit human distinct-scope review; per its own
  text "a warning-only shared census is not this review".
- `.ufo/waves/round-52/validate/corpus/` holds byte-identical copies of README/entry/lesson but a SOURCES.md
  whose S370–S373 rows are appended at file end instead of inserted after S369 — identical row content,
  different position.

## Verdict

**Not reproduced.** As a worktree-pair the index row does name and describe the landed entry correctly —
that narrow match survives. But the claim's verifiable form — committed index row ↔ committed entry,
bound by the committed counter — is falsified three independent ways (uncommitted landing; stale default
slug; proposition-table grammar the landed counter cannot parse), plus the counter itself checks neither
pin/quote location nor a real index row. No non-author entailment judgment claimed.

## Limitations

- Did not mutate any git state (per lane rules); post-commit counter outcome shown by running the committed
  counter's own regex/reads against the worktree bytes it would see after commit — the parse result is
  input-identical.
- Counter runs used `--rev HEAD` (base); no later revision exists containing the pair (pickaxe = 0).
- `.ufo/waves/round-52/fetch/` bytes were read for anchors; upstream 0.56.2 truth relies on the pinned
  commit `efb50993` named in rows (not re-fetched by this seat).
- Attack13 (sibling seat) covers the same target from another lane; this report is independently produced.

## Report trailer

```
seat=Attack29 wave=w2 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
claim=C2 coverage index-row/knowledge-entry match
verdict=NOT_REPRODUCED (committed pair absent; counter default slug stale; counter regex cannot parse landed table)
worktree_match=README:80 <-> corpus/knowledge/hyprland-synthetic-dispatch-r52.md <-> SOURCES S370-S373 used-by (consistent, uncommitted)
counter_run=quality/counters/c2-r52-proposition-entry.py --rev HEAD → entry=absent TARGET_MISSED exit=1 (default and --entry override)
regex_check=committed counter line-28 pattern vs landed entry bytes → 0 of 18 proposition rows parse
errors=P17 function misattribution; P04/P17 duplicate proposition; missing MADO-R52 id; QUALITY17 distinct-scope review outstanding
report=.ufo/waves/round-52/w2/Attack29.md
scratch=/fast/scratch/hyaku/mado-r52/Attack29 (removed, --work only)
```
