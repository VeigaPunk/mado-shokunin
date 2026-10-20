# MutAnchorSweep — partial

Seven independent, behavior-bearing mutants were run against both requested committed data revisions, on pristine, mutated, and exactly restored script bytes. **The real revision pair kills four mutants when complete output is checked; three survive with byte-identical stdout/stderr and unchanged exits.** With classifications/counts only, three are killed and four survive. With exit codes alone, only two are killed.

This is a mutation-sensitivity finding, not a lane admission judgment or a change to either checker's contract. No production defect was installed. The pristine integrated scripts reproduce the claimed red/green measurements.

## Axes and scope

- **Calibration / anchor correctness:** rotation threshold, alias membership, revision-pin versus access-date detection, mined-only evaluation.
- **Freshness / supersession coverage:** component-wise scope globs, permitted row matching, citation-span expansion.
- **Detector sensitivity and restoration integrity:** distinguish classification failures from diagnostic-only differences; preserve exact source bytes and reproduce pristine outputs after restoration.

Data revisions:

- R = `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`.
- G = `01b80946d92b26370d3012a7da655d00dd135154`.

**Script and ledger bytes were held at G while the data revision varied.** The two scripts are new round-19 artifacts; this does not compare nonexistent round-19 script bytes at R.

Targets:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/anchor-durability.py`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/supersede-sweep.py`.
- Unmutated ledger: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/supersessions.json:8-10` (`2.17.0` → `2.17.2`, permitted rows S090/S096, five scope globs).

All seven copies lived under `/tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/`. Each retained its normal four-parent root derivation and the adjacent, committed ledger. A no-checkout shared clone in `/tmp` provided committed data; `MADO_LANE` was explicitly removed from the subprocess environment. No corpus or receipt data was mutated.

## Commands and bounded detector

Preparation actually executed:

```sh
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane
git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive 01b80946d92b26370d3012a7da655d00dd135154 .ufo/waves/round-19/anchor-durability.py .ufo/waves/round-19/supersede-sweep.py .ufo/waves/round-19/supersessions.json | tar -xf - -C /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane
```

The individual copies were created from `git show G:<target>` bytes with the file-write tool; each mutant was then applied and reversed with surgical edits. There was no source rewrite to redirect the checker to a different lane.

The same bounded detector was used in all three valid phases:

```sh
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/detector.py pristine
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/detector.py mutated
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/detector.py restored
```

Each phase executes the following 14 commands, four subprocesses concurrently at most, each with a 60-second timeout and working directory `/tmp`:

```sh
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/anchor-A1-rotation.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/anchor-A1-rotation.py 01b80946d92b26370d3012a7da655d00dd135154
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/anchor-A2-alias.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/anchor-A2-alias.py 01b80946d92b26370d3012a7da655d00dd135154
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/anchor-A3-pin.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/anchor-A3-pin.py 01b80946d92b26370d3012a7da655d00dd135154
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/anchor-A4-mined.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/anchor-A4-mined.py 01b80946d92b26370d3012a7da655d00dd135154
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/sweep-S1-glob.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/sweep-S1-glob.py 01b80946d92b26370d3012a7da655d00dd135154
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/sweep-S2-token.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/sweep-S2-token.py 01b80946d92b26370d3012a7da655d00dd135154
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/sweep-S3-span.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
python3 -I /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane/.ufo/waves/round-19/sweep-S3-span.py 01b80946d92b26370d3012a7da655d00dd135154
```

Detector levels, fixed before applying any mutant:

1. **Exit-only:** require R exit 1 and G exit 0.
2. **Classifications/counts:** also require the pristine counters below and exactly the same per-row/per-file classifications. This catches lost flags, scope changes, and denominator changes without treating prose as a classification failure.
3. **Complete output:** require the exact `(exit, stdout, stderr)` tuple for the same script/revision. This additionally checks the emitted reason text, which carries the access-date versus revision distinction.

The collector exits 0 after collecting mutants even when a mutant violates an oracle; the per-command exit codes and comparisons determine the verdict, not the collector's own exit.

### Initial baseline precondition failure, excluded from verdicts

The first, unmutated preflight incorrectly expected **49 receipt files at G**, copied from the wave-1 red measurement. Actual G output was 57; all classification/count claims under attack already matched. That initial detector run exited 1 and is **inconclusive**, not a killed mutant. No mutant had yet been applied.

Independent `git -C /tmp/mado-r19-MutAnchorSweep-TbXRvx/lane ls-tree -r --name-only REV`, filtered by the checker's receipt-path regex, counted R=49 and G=57. The eight additions were round-19 receipt files for CriticC1, DeltaWalkerCli, DeltaWalkerConfig, FrontierRows, HtmlAnchorSweep, MadoR19.UnpinnedUrlSweep, SrcS084, and SrcS094. Only the scratch harness's G receipt-file expectation was corrected to 57. The full pristine phase was then rerun and **all 14 baseline commands passed before any mutation**. The 42 valid pristine/mutated/restored executions below exclude the 14 initial preflight executions.

## Pristine outputs

Every anchor copy produced these actual stdout summaries; anchor stderr was empty:

```text
SUMMARY rev=9c54c56a6a7528675027b7f628f97a1b8d1b8e8d mined=80 durable=78 per_fetch_digest=1 unpinned_alias=1 flagged=2 receipt_files=49 bad_receipt_lines=0
FLAGGED S084 S094
# command exit: 1

SUMMARY rev=01b80946d92b26370d3012a7da655d00dd135154 mined=81 durable=81 per_fetch_digest=0 unpinned_alias=0 flagged=0 receipt_files=57 bad_receipt_lines=0
# command exit: 0
```

Every sweep copy produced these actual stderr summaries:

```text
supersede-sweep: walker-2.17.2 rev=9c54c56a6a7528675027b7f628f97a1b8d1b8e8d files=13 pointed=2 stale=11
# command exit: 1
supersede-sweep: walker-2.17.2 rev=01b80946d92b26370d3012a7da655d00dd135154 files=13 pointed=13 stale=0
# command exit: 0
```

At R the two POINTED files were `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/README.md` and `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/walker-route-r18.md`; G had 13 POINTED files. Full per-command stdout and stderr are retained in the JSON artifacts named below.

## Mutation matrix: actual results and expected detector

`A` below means anchor counters `(mined, durable, per_fetch_digest, unpinned_alias, flagged)`; `S` means sweep counters `(files, pointed, stale)`. Receipt-file counts remained R=49/G=57 and bad receipt lines remained 0 for every anchor mutant.

| Mutant | Smallest defect applied | R actual | G actual | Complete-output verdict | Classifications/counts verdict | Exit-only verdict |
|---|---|---|---|---|---|---|
| A1 rotation | Raise both rotation comparisons from `>= 2` to `>= 3` | A=(80,78,1,1,2), exit 1; complete output identical | A=(81,81,0,0,0), exit 0; complete output identical | **survived** | survived | survived |
| A2 alias list | Drop only `latest` from `ALIAS_SEGMENTS` | A=(80,79,1,0,1), exit 1; S084 becomes durable; only S094 flagged | A=(81,81,0,0,0), exit 0; complete output identical | **killed at R** | killed at R | survived |
| A3 pin detection | Change the access-date guard's `continue` to `pass`, allowing the date to be returned as a pin | A=(80,78,1,1,2), exit 1; unchanged classifications but changed reason text | A=(81,81,0,0,0), exit 0; unchanged classifications but changed reason text | **killed at R and G, diagnostic only** | survived | survived |
| A4 mined-only | Change default `status == "mined"` to `status != "queued"`, accidentally including rejected rows | A=(87,85,1,1,2), exit 1 | A=(90,88,1,1,2), exit 1; rejected S084/S094 fire again | **killed at R and G** | killed at R and G | killed at G |
| S1 scope globs | Replace component-wise matching with `fnmatch.fnmatchcase(path, pattern)` | S=(13,2,11), exit 1; complete output identical | S=(13,13,0), exit 0; complete output identical | **survived** | survived | survived |
| S2 row-token matching | Replace the permitted-row intersection with `if here:`, accepting any covered row | S=(13,2,11), exit 1; complete output identical | S=(13,13,0), exit 0; complete output identical | **survived** | survived | survived |
| S3 span expansion | Replace `rows.update(range(lo, hi + 1))` with `rows.update((lo, hi))`, retaining endpoints only | S=(13,1,12), exit 1; README becomes STALE | S=(13,12,1), exit 1; README becomes STALE | **killed at R and G** | killed at R and G | killed at G |

Totals: **complete output 4 killed / 3 survived; classifications/counts 3 killed / 4 survived; exit-only 2 killed / 5 survived.** No mutant is classified from a failed baseline.

### A1 — rotation threshold survives genuine rotating-page data

Behavior sites: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/anchor-durability.py:228,232`.

The real R rotating row already has **five** distinct successful digests:

```text
ROW S094 PER_FETCH_DIGEST — 5 distinct 200 digests for https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black (3b18a612… ≠ 50c1ac25…; matched by credited digest 50c1ac25…)
```

R and G `(exit, stdout, stderr)` are byte-identical under the threshold-3 defect. The real pair therefore does not constrain the threshold to 2. [INFERENCE] An exactly-two-digest credited case is the missing discriminating input for this mutant; five observed digests cannot distinguish the two thresholds. No such synthetic input was added in this probe.

### A2 — real S084 kills removal of latest

Behavior site: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/anchor-durability.py:70`; real input: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:96` at both revisions, mined at R and rejected at G.

The source path contains `/latest/`. R loses its UNPINNED_ALIAS classification, and actual mutant output includes:

```text
SUMMARY rev=9c54c56a6a7528675027b7f628f97a1b8d1b8e8d mined=80 durable=79 per_fetch_digest=1 unpinned_alias=0 flagged=1 receipt_files=49 bad_receipt_lines=0
FLAGGED S094
```

S094 independently keeps R red, so merely checking exit 1/0 would miss this defect.

### A3 — pin defect changes truth-bearing diagnostics, not flags

Behavior site: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/anchor-durability.py:123-125`; real access-date anchors: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:44-47` (S032–S035).

At both R and G, each of S032–S035 changes from the correct form:

```text
ROW S032 durable — no assigned class fired; anchor dates the access, not a revision
```

to the mutant form:

```text
ROW S032 durable — no page digest; anchor pins date 2026-10-19
```

The same change is observed for S033, S034, and S035. The complete-output detector kills the mutant on both revisions. **The real flag/summary measurements do not kill it:** all row classifications and all counters remain identical. Thus a claim that the red/green counts alone cover access-date rejection would overclaim this experiment.

### A4 — including rejected rows kills the green state

Behavior site: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/anchor-durability.py:365-368`; G rejection evidence: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:96,106`.

The mutant adds rejected S011/S012/S030/S045/S061/S062/S070 at R, increasing the purported mined count 80→87. At G it adds those seven plus S084/S094, increasing 81→90 and re-flagging the superseded rows:

```text
SUMMARY rev=01b80946d92b26370d3012a7da655d00dd135154 mined=90 durable=88 per_fetch_digest=1 unpinned_alias=1 flagged=2 receipt_files=57 bad_receipt_lines=0
FLAGGED S084 S094
```

G exits 1 instead of 0. This defect is killed even by the exit-only detector.

### S1 — scope component boundary survives

Behavior site: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/supersede-sweep.py:60-63`; ledger scope: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/supersessions.json:10`.

Whole-path `fnmatch` replaces component-wise matching, removing the source's explicit equal-component-count guard. Despite that defect, all 13 classified paths, all classifications, both summaries, and both exits are byte-identical. The current real pair does not test the component boundary. [INFERENCE] There is no classification-relevant nested old-version mention in this pair to discriminate these implementations; this is not evidence that the two glob rules are equivalent.

### S2 — permitted-row constraint survives removal

Behavior site: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/supersede-sweep.py:118-124`; permitted row list: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/supersessions.json:9`.

The mutant still requires `2.17.2` and some covered S-row on the same line, but no longer requires S090/S096. Both real revisions have byte-identical complete output. Therefore the real pair does not discriminate allowed-row matching from any-row matching. The wave-1 negative wrong-row fixture is a separate test and was not substituted for real revision data here.

### S3 — span interior is genuinely load-bearing at both revisions

Behavior site: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/supersede-sweep.py:106-114`; real citation: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/README.md:44` carries Walker v2.17.2 and `S072–S091`.

Permitted S090 lies inside that span, not at either endpoint. Keeping endpoints only changes exactly this file's classification on each revision:

```text
STALE corpus/README.md
supersede-sweep: walker-2.17.2 rev=9c54c56a6a7528675027b7f628f97a1b8d1b8e8d files=13 pointed=1 stale=12
# exit 1

STALE corpus/README.md
supersede-sweep: walker-2.17.2 rev=01b80946d92b26370d3012a7da655d00dd135154 files=13 pointed=12 stale=1
# exit 1
```

Unlike the S2 whitelist defect, this defect is detected by both real data revisions; the integrated green state also exits nonzero. The README's newer prose does not remove this dependency: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/README.md:137-139` splits S096, the new version, and the pointer-row enumeration over separate lines, while the checker requires same-line co-occurrence.

## Hashes and exact restoration

Original hashes, obtained from committed G bytes before mutation:

- **A** = `9e66dce8c6af26df13769ce47fdaa3ff1464296d3929ea80bf13ee6aa77bc9e4` (16,276 B).
- **S** = `fd7c31df15e43309e7c425f811bdfb3fcd16cadf9698277e2e6ac665bd7a7dc4` (7,326 B).
- Unchanged ledger = `87644b585eb486c0056c3b9800966a0d5a3d6e582f77141a8716adde0cd38d58` (311 B).

Every mutant's before and after-restoration hashes equal its named original exactly:

| Mutant | Before | Mutated SHA-256 | After restoration |
|---|---|---|---|
| A1-rotation | A | `d5ce69f307f6c86f3489890e6e964efd1a0382c53055fc089bd8ec81e3239d6d` | A |
| A2-alias | A | `a5a8ca62c1eec40bc0815d2f3684adf8f1379b8ac101bc9e17ab2ee40bc01317` | A |
| A3-pin | A | `557e694de869d46e1da33d8f14775e5f71bfc7daf7c0514835c45ea939a3e45c` | A |
| A4-mined | A | `1a178196a6bd8862b9c77f804d7af5d50ba8d80d9287f869afc24f26b2cd463e` | A |
| S1-glob | S | `0ef49c6a1d9c142e2bbb6ab2d3f3eb7b15cb75d9466f037ab5677b7844bb33e8` | S |
| S2-token | S | `0df28edc699de3dc02cf0070f6ba393bb93f3080ec5d6cc3676b6dba88c2293d` | S |
| S3-span | S | `1493c1b18c52fd8b74adaeb8dbfee307edaf5bd00a38905f581bbaafb68facdc` | S |

The restored phase actually reran all 14 commands and returned:

```text
runs = 14
all_semantic_pass = true
all_full_output_equal = true
all_exact_bytes_restored = true
```

Thus restoration is evidenced by both exact source hashes and byte-identical `(exit, stdout, stderr)`, not by reversing an edit alone. Final `sha256sum` of the lane's two original target paths and ledger also matched A, S, and the ledger hash above. They were never modified by this seat.

### Retained complete evidence

| Absolute artifact path | SHA-256 |
|---|---|
| `/tmp/mado-r19-MutAnchorSweep-TbXRvx/detector.py` | `2f6fcfff1cff8921e494b3620c8d1fd38293fa5d28a8aeb0f1261665bab759b3` |
| `/tmp/mado-r19-MutAnchorSweep-TbXRvx/results-pristine.json` | `090678ed25360eeea4bc9ec1dafb626caaa9573774f7fcd5f1e9f1ce862ae67d` |
| `/tmp/mado-r19-MutAnchorSweep-TbXRvx/results-mutated.json` | `3a626ad3fa27dc090e1860dfdba1a9e0eae7c90e50184a2abf674bb9370679ea` |
| `/tmp/mado-r19-MutAnchorSweep-TbXRvx/results-restored.json` | `b189fb5a373c7ffff5d7c8b7fb5269ee6fbf546214915bc43522d5a6424cf788` |

Each results file records the 14 full command argument vectors, exit codes, complete stdout/stderr, source and output hashes, counters, and per-row/per-file classifications. Mutated/restored results also record comparisons against the valid pristine baseline. All seven on-disk scratch mutation copies are restored, not left mutant.

## Limits

- This probes seven concrete defects, not every possible defect within the seven named areas. In particular, the row-token mutation removes the permitted-row constraint; it does not separately mutate token-boundary regexes.
- The three full-output survivors are a coverage finding for this real R/G pair, not permission to weaken rotation, component-wise globs, or permitted-row matching.
- A3 is intentionally distinguished: complete emitted reasons detect access-date acceptance, but classification/summary/exit measurements do not. Do not count that mutant as killed by flags alone.
- Initial preflight failed only an outdated scratch expectation for the G receipt-file count; that run is explicitly excluded and no mutation verdict rests on it.
- The baseline classification maps anchor the differential detector; it establishes mutation sensitivity, not an independent proof that every pristine classification is semantically correct. The two declared summaries were independently reproduced as shown.
- No synthetic registry, receipt, nested-path, or wrong-row fixtures were run; no external source, host-state, source-registry quality, gate, or tripwire judgment is implied.
- No gate or copy of the gate was executed, including no selftest/regression. No forbidden host operations, package-manager calls, `jj` commands, service/compositor operations, network fetches, delegated agents, or additional mission runtimes were invoked.
- Lane writes are limited to this report. All other writes, including clone metadata, mutant copies, collector, and output evidence, are under `/tmp`.

## Installs

None.
