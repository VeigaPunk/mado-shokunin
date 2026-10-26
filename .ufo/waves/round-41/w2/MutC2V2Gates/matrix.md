# MutC2V2Gates — mutation matrix for the v2 C2 counter's own gates

mado round 41, wave w2, 2026-10-25. Seat: MutC2V2Gates. Leaf; no subagents.

- Target attacked: every gate of `quality/counters/c2-r41-focus-entry-v2.py`
  (PRED-C2-r41-v2), frozen bytes at v2 freeze 294c6679 (worktree byte-identical;
  sha256 `a2226deb860230111b8835a4a76db69d3186c5f85ad7c67cbec972ea2ef6438c`,
  21832 bytes; pristine copy: `c2-frozen-pristine.py` in this seat dir).
- Harness: the committed `.ufo/waves/round-41/ctl/run-c2-v2-controls.py`
  (sha256 `da8d4850d4e061ce78299a528ac53fab951d7d2225b85394c07e7a4a1b7cc9b5`),
  **imported by path, never edited**; per run its module-global `COUNTER`
  (runner line 26) is repointed at the mutant (`mutrun.py`, `--only` supported).
  Driver: `mutrun.py`; clause probes: `probe.py`; raw results: `results.json`;
  37 mutant sources: `mutants/M*.py`.
- Mutant = ONE exact textual edit, `count(old)==1` asserted, `compile()` checked.
- Verdicts: BASELINE first (pristine counter): `CTL_C2V2: controls=67
  correct=67/67` (11.2 s). A mutant is **NOTICED** if any of the 67 committed
  controls then deviates (`ok=0`); otherwise it **SURVIVED** (coverage finding).
- All line numbers below are the pristine counter unless a `runner:` prefix is
  used. Every quoted fragment was verified by grep against
  `c2-frozen-pristine.py` / the runner (line numbers shown are that output).

**Totals: 37 mutants — 16 NOTICED, 20 SURVIVED as coverage findings, 1 vacuous
(M22, no information). Wall time 95 s, 6 workers.**

## A. NOTICED (16) — these gates are load-bearing for the committed battery

| mutant | gate attacked (line) | single edit | noticed by (observed) | note |
|---|---|---|---|---|
| M01-ghost-refusal-drop | b ghost-id refusal (:308, :316) | drop `and not ghosts` | W02, W03, W06 (64/67) | ghost scan is the sole killer of three W-controls |
| M02-window-refusal-drop | b header-window counter (:301, :316) | drop `and window == 0` | W04 (66/67) | |
| M04-verified-at-any | b `va == OPENED` (:315) | `va is not None` | N11, W05 (65/67) | |
| M06-pin-check-drop | d PINS trust root (:368-370) | `pin_ok = True` always | F1, F3, Z1, W16 (63/67) | F2 held by distinct-interface floor (:431), F5 by clause e + pin basename lookup (:369) |
| M11-staged-drop-both | i STAGED filter (:457) | `lambda p: True` | A06, A07 (65/67) | |
| M12-staged-drop-refuse | i STAGED on REFUSE (:459) | `if True` | A07 (66/67) | |
| M24-window-20-to-200 | b 20-line window (:298) | `if k < 200:` | W01, W04 (65/67) | |
| M25-clause-e-drop | e location uniqueness/kinship (:420) | `int(bool(new_ids))` | F6, N09, W13 (64/67) | F6's sole killer was clause e |
| M26-admit-drop | i ADMIT required (:468) | drop `bool(adm)` | A01, A03, A06, A10 (63/67) | |
| M28-refuse-target-distinct-drop | i REFUSE != ADMIT target (:461) | drop `all(...)` | A08 (66/67) | |
| M29-reason-floor-1 | i >= 4 distinct words (:460) | `>= 1` | A09 (66/67) | A04 held by REFUSE_RE 20-char regex (runner of clause: :120) |
| M30-usedby-drop | c used-by lists entry (:328) | `and True` | N16, X05 (65/67) | W10 held by BASE used-by-preserved subset check (:334-335) |
| M31-held-byte-eq-drop | c held row cells 1-9 byte-equal (:333) | drop `old[0][:9] == cells[:9]` | N08 (66/67) | |
| M32-status-drop | c status mined (:328) | `True` | N13 (66/67) | |
| M33-opened-drop | c new-id opened 2026-10-25 (:339) | drop `cells[8] == OPENED` | X14 (66/67) | |
| M37-opened-const-shift | OPENED constant (:105) | `2026-10-26` | control=P-real AND P-patched (65/67) | over-strict counter breakage is caught via control P |

## B. SURVIVED (20) + 1 vacuous — coverage findings, not permission to change the contract

| mutant | gate attacked (line) | single edit | predicted kill | actual: why no committed control noticed | class |
|---|---|---|---|---|---|
| M03-min-ids-4-to-1 | b >= 4 sources (:315) | `>= 1` | none | no control varies the source count with otherwise-valid paperwork | gap |
| M05-header-recheck-shape | b header recheck validated (:315) | `rc is not None` | none | no control puts a malformed header `recheck:` (W07/W08 mutate ROW cells, killed at :329) | gap |
| M07-pin-path-drop | d `path == FETCH + basename` (:370) | `and True` | F5 | F5 held by PINS basename lookup (:369, `None != digest`) + clause e; the relocated-receipt-inside-fetch/ sub-path is unexercised | gap |
| M08-mode-accept-120000 | d receipt mode 100644 (:373) | accept 120000 | none | W14 held by pin digest mismatch; symlink-mode gate unexercised | gap |
| M09-provenance-floor-8 | d receipt >= 512 bytes (:106, :372) | `MIN_RECEIPT = 8` | none | no control commits a short receipt | gap |
| M10-new-ids-3-to-1 | c >= 3 new ids (:343) | `>= 1` | N07 | N07 held by per-id exactly-one-row requirement (:322); the >= 3 floor itself unexercised | gap |
| M13-quote-exclusivity-drop | d quote in no OTHER receipt (:392-396) | `for j in []:` | none | W15 held by `nq not in seen_quote` (:377); exclusivity loop unexercised | gap |
| M14-quote-binding-drop | d quote occurs in own receipt (:378) | `and True` | N04 W16 W17 | all three held by the PIN-SHADOW (finding 1): their receipts carry pinned basenames, probe `pinEqualsFixture=False`; clause-d content binding has NO sole kill | gap |
| M15-sha-binding-drop | d sha256(blob)==digest (:374) | `and True` | N03 | N03 held by pin (patched PINS keep real sha; gate says `0*64`) | gap |
| M16-quote-word-window | d quote 3-25 words (:375) | 1..999 | N05 | N05 held by pin-shadow | gap |
| M17-sessions-floor-1 | h >= 2 sessions (:431) | `>= 1` | J02 | J02 held by pin-shadow (d:0 -> S289 unbound -> h skipped, probe) + boot floor (:432) + adverts floor (tail = 37 adverts < 40; probe `J02-TAIL boot-lines=0 lines=38`) | gap |
| M18-adverts-floor-8 | h >= 40 adverts (:431) | `>= 8` | none | no control lands in 8..39 adverts | gap |
| M19-distinct-floor-2 | h >= 20 distinct interfaces (:431) | `>= 2` | none | only F2 has < 20 distinct (fake journal: interfaces=1) and it is a designed pin kill (kind=real); no sole kill | gap |
| M20-ascending-drop | h session firsts distinct+ascending (:432) | drop `jc[5]` | J17 | J17 held by pin-shadow (d:0) | gap |
| M21-loglevel-loosen | h ADVERT `[LOG]` grammar (:116) | allow `[ERR]` | J11 | J11 held by pin-shadow | gap |
| M23-cited-case-drop | b ghost scan covers lowercase (:307) | uppercase-only | W02 | W02 held by body ghost: the OBS line keeps uppercase S288 (probe `b:0`); a lowercase-ONLY ghost is unexercised | gap |
| M27-badloc-drop | i BAD_LOC localized-channel scan (:467) | `bad |= False` | A05 F4 | both held by clause-e location/receipt kinship (probe `e:0`); BAD_LOC has no sole kill | gap |
| M34-index-ge-1 | f exactly one index row (:454) | `>= 1` | none | X07 leaves ZERO unfenced rows; the duplicate-row case is unexercised | gap |
| M35-dup-rows-allowed | c one registry row per id (:322) | `len(rows) < 1` | none | no control duplicates a registry row | gap |
| M36-base-precond-drop | main precondition entry absent at BASE (:486-487) | drop raise | none | no control commits the entry at BASE (defense-in-depth unexercised) | gap |
| M22-census-anchor-drop | h census line anchor (:113) | drop `^` | X03 | **VACUOUS**: `re.Pattern.match` anchors at position 0 with or without `^`; probe `match(prose)=None`, `match(bare)=match`. No information; not a coverage claim | vacuous |

## Finding 1 (open defect on the control harness): the "patched" scorer cannot neutralize the pin for pinned basenames

`patched_counter` (runner:158-165) inserts the fixture's own receipt hashes
right after `PINS = {` — i.e. BEFORE the 9 original entries — and a Python dict
literal keeps the LAST duplicate key, so for any basename already pinned
(`protocols-README.md`, `xdph-journal.txt`, `issue-565.html`, ...) the ORIGINAL
pin wins. The runner's docstring promises a fixture mutant is "killed by ITS
clause, not by the pin" (runner:12-13) — for 11+ controls that is not true:
N03, N04, N05, J02, J03, J11, J16, J17, W14, W16, W17 all carry a pinned
basename in the receipt they mutate and are (also) pin-killed.

Reproduction (probe.py + results.json; also run standalone):
- M06 (pin dropped entirely) flips W16 -> W16's real killer is the pin.
- M14/M15/M16 (their nominal clause dropped) do NOT flip N04/N03/N05.
- Direct check, N04 fixture, patched copy of the counter:
  `PINS["protocols-README.md"] = 3c7007636e138898...` (original) while the
  fixture's bytes hash `513f00f4b89b2eb6...` -> `pinEqualsFixture=False`;
  same for J17's `xdph-journal.txt` (`bf8fa91a...` vs `2cc1d12a...`).
- Sub-finding: control `W16-quote-across-html-blocks` never tests
  quote-across-HTML: its quote binds fine through the HTML normalizer (it only
  flips when the pin is removed, M06). Its kill is the pin-shadow artifact.

Consequence for this battery: the clause-d content gates (:374 :375 :378) and
the journal gates (:431 :432, :116) have no sole kill in the committed battery
— every control that could exercise them is pin-confounded. Reported open; the
counter and controls stay frozen; no third registration from this seat.

## Probe evidence (probe.py, verbatim)

```
J02-TAIL boot-lines=0 lines=38
M22-JOURNAL_RE match(prose)=None match(bare)=<re.Match object; span=(0, 56), ...>
M14 x N04  rc=1 admitted=0/1  clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1
M16 x N05  rc=1 admitted=0/1  clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1
M17 x J02  rc=1 admitted=0/1  clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:0 i:1
M20 x J17  rc=1 admitted=0/1  clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:0 i:1
M21 x J11  rc=1 admitted=0/1  clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:0 i:1
M23 x W02  rc=1 admitted=0/1  clauses=a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:1 i:1
M22 x X03  rc=1 admitted=0/1  clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1
M07 x F5   rc=1 admitted=0/1  clauses=a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:1 i:1
M10 x N07  rc=1 admitted=0/1  clauses=a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 i:1
M27 x A05  rc=1 admitted=0/1  clauses=a:1 b:1 c:1 d:1 e:0 f:1 g:1 h:1 i:1
M27 x F4   rc=1 admitted=0/1  clauses=a:1 b:1 c:1 d:1 e:0 f:1 g:1 h:1 i:1
```

## Reproduction

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 .ufo/waves/round-41/w2/MutC2V2Gates/mutrun.py            # full battery
python3 .ufo/waves/round-41/w2/MutC2V2Gates/mutrun.py --only M09-provenance-floor-8
python3 .ufo/waves/round-41/w2/MutC2V2Gates/probe.py             # clause attribution
```

No tracked byte is written: the harness is imported and its `COUNTER` global
repointed; mutants and the pristine extract live only in this seat dir; git
fixtures are throwaway `mktemp -d` repos created by the committed runner itself.

## Restoration evidence

- Counter sha256 before == after: `a2226deb860230111b8835a4a76db69d3186c5f85ad7c67cbec972ea2ef6438c` (mutrun.py PRISTINE/POST lines).
- Runner sha256 before == after: `da8d4850d4e061ce78299a528ac53fab951d7d2225b85394c07e7a4a1b7cc9b5`.
- `git status --porcelain` on the counter path: empty (worktree equals freeze 294c6679).
- Seat scratch `/tmp/mutc2v2gates-tmp` removed by driver and probe on every clean exit. `/tmp` still holds ~360 `c2p-*`/`mado-c2v2ctl-*` dirs from OTHER concurrently running seats (the unmodified runner leaks `c2p-` by design); left untouched on purpose.
