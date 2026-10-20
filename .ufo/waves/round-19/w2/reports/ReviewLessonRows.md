# ReviewLessonRows — breaks

Attacked the assigned tip `01b80946d92b26370d3012a7da655d00dd135154` and the later worktree lesson append (current branch tip observed: `c7693eb29c1a1969087282aa0601e186e0ae488d`). No lane file was changed except this report. Probe commits and synthetic files were confined to `/tmp/ReviewLessonRows-d2`.

## Findings (severity order)

### High — M1/M2's green can pass the same `latest` alias defect it was added to catch

`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-19.md:16-17` records the literal S084/S094 red and green. I independently re-ran the two claimed arms:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/anchor-durability.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
SUMMARY ... mined=80 durable=78 ... flagged=2 ...
FLAGGED S084 S094
ANCHOR_RED_EXIT=1

python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/anchor-durability.py 01b80946d92b26370d3012a7da655d00dd135154
SUMMARY ... mined=81 durable=81 ... flagged=0 ...
ANCHOR_GREEN_EXIT=0
```

The named historical rows do exercise real red/green arms. But in an isolated `/tmp` clone, I added one synthetic 11-column row with source `https://docs.rs/serde/latest/serde/` and anchor `page HTML sha256 000…000; serde 1.0.228`; no web fetch occurred. Re-running the same checker on that clone produced:

```text
python3 -I /tmp/ReviewLessonRows-d2/.ufo/waves/round-19/anchor-durability.py 76a4384789083c89058f421294460e7d90639680 --rows S911
ROW S911 durable — alias segment latest pinned by version 1.0.228; sha256 00000000… is a page digest, not shown to rotate (receipts: 0 records, 0 digests)
SUMMARY ... mined=1 durable=1 ... flagged=0 ...
ANCHOR_PROBE_EXIT=0
```

This is a checker false-green on the M2 defect shape: `latest` remains in the source URL, while the purported version exists only as unrelated prose. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/anchor-durability.py:253-261` rejects an alias only when `pin_token(anchor)` is absent; it does not bind that token to the URL or verify it. The same loophole is documented independently in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/w2/reports/RerunAnchor.md:109-114`. Whether the live docs.rs endpoint serves a different release was not fetched [INFERENCE]; the observed checker result is sufficient to show that the red-green pair only catches S084's exact wording, not this alias class. M1/M2 need a limit or a stronger pin check in the lesson/criterion.

### Medium — M12's `captured-by` cell contradicts its own correction

`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-19.md:87` says the post-wave tripwire scan captured the real hyprctl incident. The same file at `:127-130` says the scan did **not** see that probe and explicitly concludes “M12's captured-by is therefore `none (seat self-report)`, not the tripwire.” The underlying incident description is in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/w2/reports/SentinelGatePath.md:75-79` (real `/usr/bin/hyprctl probe`, rc 0, `unknown request`; the later guarded run was separate). The table cell remains wrong despite the later correction and the current commit message. Update the M12 cell to `none (seat self-report)`.

### Medium — M9's mitigation is incomplete; the retry detail is not supported by the lane record

`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-19.md:24` says wave 2 leans on answered routes, but its fix names only some roles. The appended correction at `:80-81` says 10 reviewer seats still went to `m_zfl`; `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/w2/reports/ScribeLogCheck.md:34,45-50` confirms those reviewers were on the route that failed in wave 1. The fleet report records 25 wave-1 deaths, all on `m_zfl`, notifies the route failure, and lists the seats (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-19/mado.md:151`); 25 is a reasonable approximation for “~30”. The no-respawn clause is consistent with `resume 0` (`ScribeLogCheck.md:45,49`). I found no `10 retries` evidence in the w1 reports, dispatch, task-result, or fleet report [UNK]. The correction explains that routing is orchestrator-owned but does not make the table's mitigation complete; report it as a residual, not a fix by L1.

### Medium — a malformed tripwire verdict is graded as a valid 0/6 instead of “could not evaluate”

This w1 counter defect is not among M1-M14. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/w1/reports/SimplifyCounters.md:37` describes the loose parser; `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tw-recall.py:68-73` accepts a JSON object without `findings` via `.get("findings", [])`.

I independently reproduced it in `/tmp/ReviewLessonRows-d2` using a synthetic committed `tools/mado-tripwire.py` that prints a scan label and JSON with no `findings` key:

```text
python3 -I /tmp/ReviewLessonRows-d2/.ufo/waves/round-19/tw-recall.py bd42c1c38fb03a2a2091577c4e36cd4e9dfbb654
"incident_lines": 6,
"detected": 0,
"score": 0.0,
TW_RECALL_PROBE_EXIT=0
```

This is not a false high score, but an invalid scan is silently presented as a valid measurement. It should be recorded alongside M7's counter-vacuity limitation or in a separate lesson row; changing the pre-registered counter was not necessary to disclose it.

### Medium — carried F17 has no lesson disposition

The lesson preamble carries `F17` (`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-19.md:8`), and M14 mentions the `.jj` birth/merge/push loop as undetected by `vcs_write` (`:89`), but there is no F17 disposition or the enforceable invariants in the lesson. W1 `RevSpotcheckRouting.md:30,83-100` explicitly marks F17 as unowned and recommends routing it into the lesson. W1 `JjIncidentScan.md:243-259` supplies the disposition: keep colocation, forbid non-helper `jj`, restrict direct git writes, and treat helper `commit`/`state` according to their semantics. M14 records the classifier survivor, not that process disposition.

### Low — w1's triggered freshness findings are omitted

W1 `RecheckSweep.md:28,37,105-107` reports 8 fired triggers. In particular S003's cited PROTOCOL ranges shifted by 15 lines (`:37`, `:105`), leaving its numeric anchor stale, and seven omarchy v3.8.4 rows triggered recheck against the v4/quattro changes (`:28`, `:106`). The lesson only says “Recheck cells unchanged” at `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-19.md:49`; it records no re-anchor, supersession, or explicit deferment. The version-pinned facts may remain valid, but the trigger outcome should be recorded as deferred or disposed.

## Row checks and reruns

- **M1/M2:** the exact S084/S094 baseline red and assigned-tip green reproduce as shown above. The S911 probe falsifies broader alias coverage. RerunAnchor also reports the red/green at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/w2/reports/RerunAnchor.md:20-30`.
- **M3/M11:** with the committed pre-wave ledger, `supersede-sweep.py 9c54c56` returned `files=13 pointed=2 stale=11`, exit 1; `supersede-sweep.py df84807 --ledger /tmp/ledger-tip.json` returned `files=13 pointed=13 stale=0`, exit 0. With the current three-entry ledger, the baseline is red and current `c7693eb` is green: `walker-2.17.2 stale=0`, `S094-to-S097 stale=0`, `S084-to-S098 stale=0`, exit 0. Current final receipt agrees (`evidence/final/supersede-sweep-green.txt:1-4`).
- **M4:** re-ran the gate copy only with the explicitly permitted `--selftest`: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh --selftest` returned `MADO_SELFTEST: FAILED — 383 passed, 6 failed`, exit 2. The six failures are listed at `evidence/gate-swap-receipt.txt:3-9`; the current receipt-claims check expects and accepts that red.
- **M5:** `diff` of each original `*-before.txt` against its `*-before-recut.txt` shows only line 1 differs; bodies are identical. Producer files are absent at `9c54c56` and present at `17661e0`. The pre-recut claims at assigned tip still fail: `receipt-check.py /tmp/claims-tip.json` → `EXPECT_SUMMARY: 3/5`, exit 2 (tw-recall and fresh-pins `ERROR`). The later worktree claims now name the recuts and final receipts: re-run at current HEAD → `EXPECT_SUMMARY: 17/17`, exit 0. The appended correction at lesson `:73-75` is accurate: the “tool not yet committed” note predated the commit by 23 seconds; the actual defect was the wrong `measured_commit`.
- **M6:** the assigned-tip `.gitignore` has 30 lines but no class patterns; the w2 correction at lesson `:76-79` accurately records that an added `.crate` was not ignored. Current HEAD has 36 lines; `git check-ignore -v .../RevRubricVRisk/xdg-3.0.0.crate` matches `fetch/.gitignore:33:*.crate`. One literal-scan detail in M6 is not exact: `git grep -l X-Real-Ip 01b8094 -- .ufo/waves/round-19` also returns `gen_w2.py` (line 131), where the token appears in the sentinel task prompt, not as an IP. No IPv6 value is reproduced here.
- **M7:** independently re-ran `tw-recall.py`: baseline `9c54c56` gives 3/6, score 5.0; assigned tip `01b8094` gives 6/6, score 10.0; both exit 0. The class/control/whole-corpus companions are documented in w1 `TwMerge.md:178-224` and w2 `CriticC3W2.md:65-85`; the 6/6 remains an overfit-set reading, not general recall.
- **M8:** fleet `git status --porcelain -- .ufo/waves/round-19` and `git log --all -- .ufo/waves/round-19` are empty, the fleet directory is absent, and the lane tree contains both `drafts/QualityDraft.md` and `w1/reports/QualityDraft.md`. The claimed old `cmp` cannot be independently repeated after the fleet source copies were deleted [UNK].
- **M9:** the 25-seat count and route are in the fleet report; no independent w1 status record supports “10 retries”. The wave-2 reviewer route is demonstrably still `m_zfl`, so the mitigation is partial.
- **M10-M14:** M10's current fresh-pins run reproduces 2/13 at the baseline and 13/13 at current HEAD; M11's final ledger red/green reproduces. M12 needs the `captured-by` correction above. M13/M14's findings are already explicit in the append; the separate parser defect above is not.

## Limits

- S911 is an intentionally synthetic source/anchor row in a `/tmp` clone, not a fetched docs.rs page; its checker output is observed, while actual upstream page movement is [INFERENCE].
- I did not re-open the withheld ArchWiki bodies or reproduce the original `cmp` against deleted fleet files. Privacy and source removal are the point of those fixes.
- I did not run the live gate, any compositor/host command, or any package manager. The only gate copy run was `--selftest` as required by the host pause.
- No packages or tools were installed or updated.

## Installs

none.

Report: .ufo/waves/round-19/w2/reports/ReviewLessonRows.md
