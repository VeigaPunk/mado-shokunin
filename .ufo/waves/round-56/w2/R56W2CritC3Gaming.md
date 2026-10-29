# R56W2CritC3Gaming — gaming attack on PRED-C3-r56-v2 at 28fc86ac2359ec27406d8a2c63bef82ea6e947ed

Deliverables: `.ufo/waves/round-56/w2/R56W2CritC3Gaming/` (drive.py = variant generator, receipt_check.py, results.txt, run2.out,
base-detail.err, harness-c3.out/err, hout1-5.txt/herr1-5.txt). Scratch removed. Lane: read-only (git cat-file / ls-tree / show /
grep / `git clone --shared --no-checkout` into scratch; no commit, add, stash or checkout against the lane).

## 0. Inputs verified

- Counter `quality/counters/c3-r56-used-by.py` at R: blob `f7c8016935df76c7b2d899a983c1ab7afa939974`; my scratch copy has the same hash.
- Harness `quality/check-r56-controls.py` at R: blob `840e0e49e5ad7a3048e0632854b594222f454346`.
- `c3-name-only.tsv` sha256 `70653e09…948ee` = `c3.allowlist_sha256`; `frozen-tables-v2.json` sha256 `9511151a…5bf795e2` (matches).
- Tool: `/usr/bin/cmark` 0.31.2 (pre-installed system package; I installed nothing; pacman is paused host-wide and I did not touch it).

## 1. Baseline (real counter and real harness, no edit)

```
python3 -I quality/counters/c3-r56-used-by.py --repo <lane> --rev 28fc86ac… --work <scratch>
MADO_USED_BY: rev=28fc86ac… entries=71 rows=328 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none   (rc 0)
python3 -I quality/check-r56-controls.py --claim c3 --repo <lane> --rev 28fc86ac… --work <scratch>
MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK   (rc 0)
```

Harness note (diagnostic only, not scored): its own `metrics()` does not subtract the allowlist, so on the good tree it reports
`missing=24` and prints "counter and harness numbers diverge (not scored)". Cosmetic.

## 2. Method

Each variant is one commit on a fixture clone of the lane (`git clone --shared --no-checkout`; toplevel asserted equal to the fixture
before any commit). Commits are built from `read-tree 28fc86ac` in a temporary index, `update-index`, `write-tree`, `commit-tree -p 28fc86ac`,
so no worktree or lane ref is touched. Each is scored by the real counter:
`python3 -I counter.py --repo <fixture> --rev <commit> --work <scratch> --detail`. Five variants that the counter passes were then
run through the real harness: `python3 -I check-r56-controls.py --claim c3 --repo <fixture> --rev <commit> --work <scratch>`.

A first pass had a construction bug: the probe entries put `source: S001` on a line outside any fence, so every probe failed on
`missing` for that reason alone. I fixed the probes (no source line; the only citation is the one under test) and reran everything.
The table below is the corrected run; the first-pass numbers for those probes are superseded.

## 3. Results (real counter; `--detail` stderr where a leg fails)

| # | item | variant | counter at the variant | reading |
|---|---|---|---|---|
| a1 | a | non-allowlist base-missing pair (S015 / walker-route-r18.md) left out of used-by, citation kept | `missing=1` | caught |
| a2 | a | same plus ` x` suffix on its citing line | `missing=1` | caught; line-sha is irrelevant for non-allowlist pairs |
| a3 | a | filled non-allowlist pair (S002), suffix only | `TARGET_MET` | correct: suffix is inert when nothing is allowlisted |
| a4 | a | allowlist pair (S005 in output-colour-boundaries-r14.md), ` x` on the citing line | `stale=2` (S005, S040; the stderr names both in that entry) | caught: stale tracks allowlist rows |
| b1 | b | base-missing pair: citation AND used-by deleted | `lost=1` (S015) | caught |
| b2 | b | BASE-FILLED pair (S002 in window-rule-effects-getprop.md): citation AND used-by deleted | `TARGET_MET` | **GAP D1** |
| b3 | b | base-filled pair, citation deleted, used-by kept | `extra=1` | caught |
| c1 | c | new entry naming all 328 ids in prose, registry untouched | `missing=328` | caught |
| c2 | c | same entry, used-by of all 328 rows filled with it | `TARGET_MET` | **D5**: fill passes, records mention-only reliance |
| c3 | c | same mentions inside a ``` block, no used-by | `TARGET_MET` | **D5**: fence hides mentions |
| d1 | d | trailing space on every citing line of the 24 allowlist pairs | `stale=24` | caught (null for evasion) |
| e0 | e | S999 appended to the source line in place | `dangling=1` | caught (control) |
| e1 | e | S999 on the source line, source line moved to line 21 | `TARGET_MET` | **GAP D2** |
| f1 | f | entry with only base-filled pairs renamed, used-by updated | `TARGET_MET` | honest rename passes |
| f2 | f | entry with 3 base-missing pairs (arc-synthesis.md: S090, S091, S096) renamed, used-by updated | `lost=3` | **FALSE POSITIVE D9** (honest rename blocked) |
| f3 | f | same rename, used-by left at the old path | `missing=3 extra=3 lost=3` | caught |
| g1 | g | allowlist rewritten with CRLF line endings | `allow_sha` | caught (null for evasion) |
| h1 | h | HTML comment citing S001 in an entry that does not list it | `missing=1` | caught |
| h2 | h | HTML comment citing an allowlist pair | `stale=1` | caught |
| i1 | i | ``` `` ```a`b `` opener (CommonMark: not a fence) hides a plain new citation | `TARGET_MET` | **GAP D3**; cmark: `<p>```a`b</p><p>Cites S001 here.</p>` |
| i1c | i | control: same citation, no opener | `missing=1` | |
| i2 | i | ``` ` ` ``` line inside an HTML comment opens a counter-fence that hides the citation after `-->` | `TARGET_MET` | **GAP D3**; cmark: `<!-- raw HTML omitted --><p>Cites S001 here.</p>` |
| i3 | i | `S&#48;01` (renders S001) | `TARGET_MET` | **GAP D4**; cmark: `<p>Cites S001 here.</p>` |
| i3c | i | control: literal `S001` | `missing=1` | |
| i4 | i | zero-width space inside the token (`S\u200b001`) | `TARGET_MET` | **GAP D4**; reads S001, not a token |
| i5 | i | ``` ~~~ ``` inside a ``` block around a filled citation, used-by kept | `extra=4` (four pairs of that entry lost their citation; stderr printed S002, S018, S019 of them; the wrapped line's full token list was not printed) | consistent with CommonMark: it is code and the used-by cell now overstates |
| j1 | j | used-by cell reads `NOT used by <entry>` (path string present) | `TARGET_MET` | **D7** |
| k1 | k | body token `S777` naming no registry row | `TARGET_MET` | **D8** (by design; undisclosed) |

Harness on the passing gaming trees (`--claim c3`, all five): b2 `good=ok controls=9/9 verdict=OK`; c3 same; e1 same; i3 same;
j1 same (hout1-5.txt). The harness is green on every counter-level gap above.

## 4. Registry diff (requested verification)

- `git diff 323a69c9014da1cebece67bb111b70a5630f4a60 28fc86ac… -- corpus/SOURCES.md`: 23 changed rows (S015, S041, S046, S057, S059, S060,
  S073, S090, S091, S096, S158, S162, S175, S177, S186, S187, S201, S277, S318, S319, S350, S352, S353), changed part index set **{11}** only,
  0 removed pairs, **41 added pairs**, all 41 are non-allowlist base-missing pairs (41/41), no space-separated paths in cell 11 (`\.md corpus/` absent).
- `receipts/used-by-old-to-new.md` (receipt_check.py): 23 rows; old cell equals PRE cell 11 and new cell equals R cell 11 for all 23;
  added pairs sum to 41; the row set equals the git-diff row set.
- Deviation from the target wording (not a counter leg): the same diff also adds **9 new registry rows S383–S391**, each with used-by
  `corpus/knowledge/hyprland-config-autoreload-r56.md` (PAIRS 381→390). The target sentence says "used-by edits only (cell 11)". Cosmetic: these are
  new registrations, not edits, but the sentence is not literally true.
- Entry text: `git diff --name-status 323a69c9 28fc86ac -- corpus/knowledge` shows only `A corpus/knowledge/hyprland-config-autoreload-r56.md`.
  No existing entry text changed at R. No leg enforces this (see D1).
- Lane state, grep at R over corpus/knowledge: zero entity-coded S ids (`S&#`), zero backtick-info fences, zero HTML comments. The measured state at R hides nothing of the forms in D3/D4.

## 5. Defects (input, output, severity)

**D1 — `lost` covers only the 65 base-missing pairs; deleting both sides of a base-filled pair passes (weakens the claim).**
Input b2: `S002` replaced by `S---` in `window-rule-effects-getprop.md` and removed from its used-by. Output `TARGET_MET missed=none`.
The frozen text names "deleting citations (lost)" as a do-nothing control; the counter catches it only for base-missing pairs (E12 discloses
the scope, but the claim sentence does not). The variant also changes entry text, which the target forbids; no leg reads entry text against the base.
The harness does not catch it: `r56_ctl_c3.py mut_delete_citation` selects only `p not in bused[s]` (base-missing), so control 8 can never exercise a base-filled
pair (H1, 9/9).

**D2 — `dangling` reads `source:` only in the first 15 lines (weakens).**
Input e1: `S999` on the source line of `config-drift-r12.md`, line moved to 21. Output `dangling=0 TARGET_MET`. The control e0 (in place) gives `dangling=1`.
A grep for `[:15]` across `quality/` at R finds only the C1 counter/harness, the C3 harness and the options-entry counter, so I found no gate that enforces the
window for the other 70 entries (crude grep, not a full audit).

**D3 — counter fence rule differs from CommonMark; a citation can be hidden as prose (weakens; reproducible).**
Inputs i1 (`` ```a`b ``) and i2 (a ``` line inside an HTML comment). The counter opens a fence on both and hides every following citation. cmark 0.31.2
renders both as prose, so the citation is a live reference in the rendered view. Output `TARGET_MET` for a new unrecorded citation (control i1c: `missing=1`).
Fix direction: follow the CommonMark info-string rule and HTML-block rule, or cross-check the fenced set against cmark.

**D4 — entity-coded and zero-width tokens are invisible (weakens).**
Inputs i3 (`S&#48;01`, renders `S001`) and i4 (`S\u200b001`). The counter's regex needs literal `S` and three digits. Output `TARGET_MET`. The declared limits in
registration-v2 name ranges (`S175–S177`) but not entities or zero-width characters.

**D5 — `missing` is cleared by recording reliance the text denies, or by fencing the text (weakens; the claim's honesty rests on reviewers).**
Inputs c2 and c3: a new entry that names all 328 rows in prose. Unfilled: `missing=328`. Filled with all 328 used-by cells: `TARGET_MET`. Fenced with no used-by: `TARGET_MET`.
The frozen allowlist (24 pairs, hash-locked by allow_sha) is the only mention exemption, so any new mention-only citation can be cleared only by recording reliance
the text does not have, by rewriting the text, or by fencing it. The counter cannot tell these apart. The registration itself warns about this for the 41 existing
fills (R56CritCiteDef, "~21 of 65 refuted"); the same mechanism applies to every new entry and is not disclosed as such.

**D7 — `used-by` matching is substring-based, so negated mentions count (weakens).**
Input j1: cell 11 reads `NOT used by corpus/knowledge/walker-route-r18.md`. Output `TARGET_MET`. `USED_BY = corpus/knowledge/[A-Za-z0-9_.-]+\.md` is a `findall`
on the whole cell with no boundary or negation check.

**D8 — body tokens that name no registry row are ignored (weakens; design choice, not in the declared limits).**
Input k1: `Cites S777 which has no row.` Output `TARGET_MET`. The selftest treats `S243` (a draft id) as intentionally ignored. Only `source:` lines
are checked by `dangling`. registration-v2 "What v2 does not repair" does not list this.

**D9 — an honest rename of an entry with base-missing pairs is blocked by `lost` (weakens; false positive).**
Input f2: `arc-synthesis.md` renamed to `probe-renamed-f2-r56.md` with used-by updated to the new path. Output `lost=3 TARGET_MISSED missed=lost`
(S090, S091, S096). `lost` is keyed on the path, so no citation was removed. f1 (filled-only entry) passes, so this is specifically the base-missing case.

**D10 — harness green does not mean the claim holds (weakens the harness as an independent check).**
All five gaming trees give `good=ok controls=9/9`. The harness tests discrimination of its own nine mutations, not truth; combined with D1 (control 8 is base-missing only), it cannot see the gaps above.

## 6. Null results (commands that found nothing)

- (a) stale only for allowlist rows: a2 vs a4. A suffix on a non-allowlist citing line cannot evade `missing` (a2 `missing=1`) and a suffix on an allowlist
  citing line is caught by `stale` (a4). Null for evasion.
- (d) trailing space on all 24 allowlist citing lines: `stale=24`. Null for evasion.
- (g) CRLF allowlist: `allow_sha`. Null for evasion (the line-sha is over the citing lines and the file hash is over the whole blob).
- (h) HTML comments on a non-filled pair: `missing=1`; on an allowlist pair: `stale=1`. Null for evasion.
- (f) rename with used-by not updated: `missing=3 extra=3 lost=3`. Null for evasion.
- (b) deleting a base-missing pair's citation and used-by: `lost=1`. Null for evasion (D1 is the base-filled case, not this).
- Lane state, grep over corpus/knowledge at R for entity-coded S ids, backtick-info fences and HTML comments: all zero. No hidden citation in the measured state.
- Receipt vs registry (receipt_check.py): no mismatch on any of 23 rows.

## 7. Verdict on the claim

- The measured state at 28fc86ac is consistent with the claim as frozen (missing=0; the 41 fills match the receipt and touch only cell 11; no hidden citation forms in the lane). Nothing I found makes the lane's actual PASS false.
- The PASS is not a proof of registry consistency in general. Five gap families (D1, D2, D3, D4, D5/D7/D8) reach TARGET_MET with a registry that does not record the reliance the text carries, or that hides it. Of these, D1 and D2 break a stated frozen sentence; D3, D4 break the counter's reading of "citation"; D5 is the honesty problem of mention-only citations. None is blocking for the measured state; all weaken the claim as worded.
- The harness (9/9 on all five gaming trees) does not guard against any of them.

## 8. Not verified / limits

- Rendering: cmark 0.31.2 is the CommonMark reference; GitHub renders with cmark-gfm. I did not run cmark-gfm; the fence and HTML-block results should be checked there before a claim about GitHub.
- Entailment of the 41 fills (whether the entries actually rely on the rows): out of scope for this seat.
- Fence edge cases not run: closer-length (a ```` opener closed by ```) and closers with info strings. The direction I reasoned about is over-counting (safe), so I did not run them.
- The lane-wide `source:` window enforcement check was a crude grep, not an audit.
- The "used-by edits only" wording vs the nine new rows is read, not scored by any leg.
- Did not run C1 or C2 harnesses; not in scope.
- Wall time: counter run ~2 s each, harness ~30 s each; all runs finished.
