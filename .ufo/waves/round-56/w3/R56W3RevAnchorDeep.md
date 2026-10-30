# R56W3RevAnchorDeep — criterion-107 hand audit, attempt 2

## Findings by severity

No blocking, claim-weakening, or cosmetic anchor defect found in the assigned population at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`. This is a lane-dispatched review, not non-author clearance or claim admission.

Attacked: every E-row re-pointing to S392–S395, plus five other rows across K/E classes, with an independent exhaustive accounting of all 39 registry-citing evidence rows. Axes: row coverage, source-name identity, quoted-line containment, EOF bounds, immutable-revision binding. Frozen predicates were not changed.

## Method and decisive evidence

Read `claims-frozen-v2.md`, `registration-v2.md`, and the scope definition in `registration.md`; read criterion 107 from the scored revision's `corpus/QUALITY.md:592-605`. All scored entry, registry, and pin bytes came from `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:<path>`, not working-tree bytes. No production counter/checker was imported or executed. The deliverable script records arithmetic and exact quoted lines, independently of the committed checker being built by another seat.

Executed command (complete stdout and command saved in the receipt):

```text
TMPDIR=/fast/scratch/hyaku/mado-r56/R56W3RevAnchorDeep python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevAnchorDeep/anchor_handcheck.py /home/vgpnk/Projects/shokunin/mado-shokunin 0f3a54361a9824484d0801679ceb1fd8ac7c32e1
EXIT: 0
CHECK107: rows=39 covered=39 miss=0 verdict=OK
REPOINTED: rows=6 expected=6; host_rows=3 excluded_by_criterion107_source_cell
```

Manual comparisons (all pass; `length` counts newline-separated pieces, including the trailing empty piece):

| row | registry row | entry L | upstream NAME | locator list | pin length | finding |
|---|---|---:|---|---|---:|---|
| E01 | S393 | 66 | MiscFunctions.cpp | 66 | 845 | exact member; replacement call present |
| E03 | S392 | 106 | ConfigWatcher.cpp | 106 | 112 | exact member; `.file = WD->file,` present |
| E04 | S394 | 1190 | HyprCtl.cpp | 1190 | 2347 | exact member; parseKeyword call present |
| E05 | S395 | 630 | ConfigManager.cpp | 630,1838,2134 | 2185 | exact member; resetHLConfig call present |
| E06 | S395 | 1838 | ConfigManager.cpp | 630,1838,2134 | 2185 | exact member; current-path assignment present |
| E07 | S395 | 2134 | ConfigManager.cpp | 630,1838,2134 | 2185 | exact member; return m_configPaths present |
| K01 | S384 | 492 | ConfigValues.cpp | 492 | 735 | exact member; option declaration present |
| K13 | S386 | 128 | EventLoopManager.cpp | 71,128 | 283 | exact member; readable event source present |
| K20 | S387 | 776 | ConfigManager.cpp | 776,1070,1079-1080,1816,1835-1836,1844 | 2185 | exact member; clear call present |
| K29 | S390 | 186 | inotify.7.html | 186,262 | 920 | exact member; write-close description present |
| E08 | S391 | 18 | PropRefresher.hpp | 18,21 | 41 | exact member; watcher bit declaration present |

S392–S395 are unique registry IDs at registry lines 342–345. Their anchor NAME is obtained from the last source URL, not from their prose labels. The anchor occurrences begin their cells: there is no disallowed identifier prefix. Their named pins respectively end in `Hyprland-ConfigWatcher.cpp`, `Hyprland-MiscFunctions.cpp`, `Hyprland-HyprCtl.cpp`, and `Hyprland-legacy-ConfigManager.cpp`; each upstream NAME is preceded by a permitted hyphen in that renamed pin basename. E-row fourth-cell pin basenames equal those named pin basenames. S395's largest locator is 2134, below 2185; S392's is 106 below 112; S393's 66 below 845; S394's 1190 below 2347. None has a hidden extra locator past EOF. The other checked registry anchors likewise remain bounded. Exact pin sizes, SHA256 values, entry/registry line numbers, all locator lists, and all 39 individual verdicts are in the receipt.

## Residual risk and verification gaps

- Zero MISS is specific to the landed anchors at the named revision. It does not prove proposition entailment, runtime reload behavior, or production-checker robustness against mutations.
- H01–H03 cite `host`, not an S-id: they are outside criterion 107, explaining 39 rather than 42 rows. Their host captures were not reverified here.
- LSP unavailable: reading `xd://lsp` returned `No such tool: xd://lsp`; no semantic references/definition/diagnostics calls could run. This audit concerns literal Markdown citations; textual inspection is not semantic proof.
- No runtime/harness, mutation suite, live compositor operation, or other claim counter ran. No tools were installed or updated. No tracked lane files or host configuration were changed. The explicitly created empty scratch directory was removed with `rmdir /fast/scratch/hyaku/mado-r56/R56W3RevAnchorDeep` (exit 0).

## Deliverables

- `.ufo/waves/round-56/w3/R56W3RevAnchorDeep/receipts/anchor-deep-a2.txt`
- `.ufo/waves/round-56/w3/R56W3RevAnchorDeep/anchor_handcheck.py`
- `.ufo/waves/round-56/w3/R56W3RevAnchorDeep.md`

## Self-evaluation

Accuracy 4/5: exact revision and pin lines recorded; semantic entailment intentionally untested. Completeness 5/5: six re-pointed rows, five manual cross-class samples, and every one of 39 S-citing rows accounted for. Clarity 4/5: hand table explicit, but full per-row output lives in the receipt. Actionability 5/5: exact executable replay command and artifacts supplied. Conciseness 4/5: full output retained separately rather than duplicated. Overall 4.4/5. Highest-impact improvement outside this seat: compare this receipt with the committed checker's output, without treating agreement as entailment proof. User-agreement self-check: the scoped 39/39 result meets the requested anchor audit, not broader clearance.
