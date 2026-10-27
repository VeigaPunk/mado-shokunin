# RevR48 — review of the round-48 closure's routed items (mado round 49, w1 BUILD)

Seat: RevR48 (leaf reviewer; no subagents, no background jobs). 2026-10-27.
Reviewed against base `03e4ae76aff7a4be59cb69970dd553baa319695a` (round-48 closure spot-check commit); lane tip at review time
`5f37c1b8` (round-49 prep — tracked bytes at every cited path are unchanged from base). The round-48 report lives in the FLEET
repo, commit `a72080e7706d5a9ecd4c7bff1c8d2ca3d8f6d7d7`. Method: read-only — `git show`/`ls-tree`/`ls-files`/`grep` at pinned
revs, `sha256sum`, `stat`, and two network fetches whose bytes are receipted in this seat dir. No counter or gate was executed;
no tracked file written; no lane/fleet git or jj mutation. Full evidence: `.ufo/waves/round-49/w1/RevR48/review.md`.

## Verdicts on the routed items

| item | verdict | decisive evidence (all re-run by this seat) |
|---|---|---|
| N1 "52 untracked `*.synthetic`" | **confirmed defect** | fleet report `a72080e7:.ufo/reports/round-48/mado.md:37` says 52; actual = **47** (45 under `.ufo/waves/round-45/w1/RevengerOmarchy/`, 2 under `.ufo/waves/round-46/w1/CritW2Gate/`). "Nothing else untracked" part holds. `ExecSessionMarker/SHA256SUMS`: 77 entries, 48 synthetic, all 48 hash-verify (`sha256sum -c` ALL-MATCH) — the 48th is the seat's own **tracked** demo copy `round-48/w1/ExecSessionMarker/check-session-material.py.synthetic` |
| N2 `host_cache_untouched` = mutant bytes | **confirmed defect, now documented** | `receipts/live-terminal-cache-r48.txt:4` digest `c8b104e6…` = `sha256("r48-w2\n")` exactly; field name says the opposite of what the bytes record. Lesson `corpus/lessons/round-48.md:263` records 7 B mtime 1793064395 → resolver rewrite 190 B mtime 1793069967; round-49 before-digest `receipts/operator-state-before.txt` @`5f37c1b8` matches a live re-read today (`ddd94f6b…`, 190, 1793069967) |
| N3 stale "five gate decisions" | **confirmed defect** | `corpus/lessons/round-48.md:424-425` "the five gate decisions above (three admits, two rejects)"; the Gate section admits **12** rows (S340-S351 block) + `### Rejected after opening` holds **3** REJECTs = 15 decisions |
| N4 text matrix 96 of 98 variants | **confirmed, exactly as stated** | `c2v2-revc2counter-summary.json`: 98 entries incl. `a-entry-at-base` (rc 2, SETUP precondition_failed) and `a-rev-base-direct` (rc 1 MISSED); `c2v2-revc2counter-matrix.txt`: 100 lines = 2 header + **96** variant rows (95 `TARGET_*` + `pos`) + footer; 0 hits for the two missing ids |
| N5 GitLab `-/raw/` anti-bot page | **premise NOT reproduced (transient)** | today 2026-10-27T04:41:50Z plain `curl` fetched the S347 `-/raw/` URL: **HTTP 200, text/plain, 19592 B, sha256 `8cf65550…` = the row's pin** (`x-cache-hits: 0`); the files API returns pin-equal bytes too. Receipts: `fetch-xkb-br-rawurl.bin`, `fetch-xkb-br-api.bin` in this seat dir. The routed "now returns an anti-bot page" note would enshrine a claim that failed to reproduce 4 h later — phrase it as intermittent, keep the API fallback as procedure |
| M48-8 gate red + 16/19 gap + scope | **confirmed + NEW stale locator** | `receipts/a4/session-material-tip.txt:4` `files=21985 findings=159 rev=d8e3d600` (21985 = exactly the tracked `.ufo` subtree at d8e3d600 → default `--scope ufo`); committed gate `--scope` default `"ufo"` at `:1606-1607`, `run(scope="ufo")` → `.ufo`-only at `:787-788`; `gate-on-shapes.txt`: `files=19 findings=3` = 16 missed. **NEW:** lesson M48-8 (`:259`) cites `check-session-material.py:256` — at committed bytes `:256` is inside `_monitor_reason`; `:256` is true only of the pre-rewrite gate at `5ff16742` |
| M48-10 host-write | **confirmed; prerequisite in place** | lesson `:263` + N2 byte proof + before-digest receipt present and matching live state |
| M48-13 1 MiB cap vs clones | **confirmed** | lesson `:269`; `a4r1-results.json:22` "Index lock >1MiB…", `:40` `"RLIMIT_FSIZE=1 MiB rejects numerous committed large files"`; owed clause-r attack + both-ways demo still unrung (`:467-469`) |
| w2/SentScratch (/tmp work dirs) | **confirmed as recorded** | report + 11 receipts committed (`c1-work-gate.txt`, `c2-arg-gate.txt`, `tmp-paths.txt`, …); F1/F2 code claims consistent with the committed counters |
| registration-v2 residuals | **confirmed at :102-110** | all six residuals present verbatim (generator path, uncited meson pin, S346 chain, trust root, owner column, C1 judge) |

## Closure numbers re-derived (all pass)

SCORECARD +31/0, LOG +10/0 (pure append); whole-round deletions 67 = SKILL.md 1 + gate 31 + tool 35 (exactly three files);
knowledge 64→65; SOURCES rows 276→288; fixtures 228 = 204 + 24 new, 10 `v2-hu-*`, 10 READDIR; a4 receipt's `files=21985` =
`.ufo` subtree at d8e3d600.

## Defects the closure missed

1. **R1 (Medium, affects the freeze):** N5's premise is transient — see verdict row. Re-word the fallback note before the L1 appends it; the freshness procedure should record both URLs, not declare `-/raw/` dead.
2. **R2 (Low, stale locator in committed lesson):** M48-8's `check-session-material.py:256` — actual scope lines in the committed v2 gate are `:787-788` (run) and `:1606-1607` (argparse); `:256` is the pre-rewrite number (true only at `5ff16742`). Same number appears in `w1/SentPrivacy.md`, where it was correct at scan time. The lesson is the committed artifact and must carry a computed locator; recompute it in the M48-8 fix-up.
3. **R3 (Low, second row-dropping receipt):** `w2/RevC1Fixtures/boundary.log` = 17 rows vs `boundary.json` = 18 entries; the `primed-cache (terminator line 11)` variant exists only in the JSON. Same class as N4, seat-level (JSON is complete, nothing lost). Sibling pairs (`order`, `readdir`, `rootsubst`) line up; no other drops found.
4. **R4 (informational, sidecar ledger):** the lane tracks 100 `*.synthetic` demo files (ExecSessionMarker demo trees mirror rounds 45-48 sidecars inside seat dirs). Removing the 47 untracked sidecars does not touch the tracked mirrors; `SHA256SUMS` covers both classes (48 entries), keyed to paths that will stop existing for the 47.

## Residual gaps

- No counter or gate was executed (closure standard kept): M48-8's 16/19 tally rests on committed receipts + lesson, not a re-run; the 16 MiB truncation (D-C) and R5 serial rules were not re-derived.
- N5: one clean fetch at 04:41Z proves the standing claim failed to reproduce; it does not prove anti-bot never triggers (time/IP-dependent).
- The round-48 report is a fleet-repo artifact; N1's fix lands in the next fleet report with the counting command cited.

Scratch `/fast/scratch/hyaku/mado-r49/RevR48` was created unused and removed. No tools installed (no package or tool transaction).
