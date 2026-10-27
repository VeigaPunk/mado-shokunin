# CritSidecarsV3 — v3 gate sidecar re-run at the round-50 attack revision

**Verdict: w1/CritSidecars residual RESOLVED. At rev `b4a79843cc2545bbe800db9322e58f6e00436629` the installed v3 gate (`quality/check-session-material.py`, sha256 `ffdc9d62…`, byte-identical to the frozen bytes) honours exactly the 47 fixture sidecar waivers (49 waived findings on 47 files), `--no-waivers` restores exactly that set and nothing else, every waived match's identity is still reserved by its waiver row, and no real-shaped value is suppressed — including under tamper (fail-closed).** The v3 sidecar interaction that w1 marked "unverified" is now verified at the round-50 revision.

## What was run (all under `/fast/scratch/hyaku/mado-r50/CritSidecarsV3`, HOME/XDG_*/TMPDIR sandboxed; receipts in `receipts/`)

- `git clone -q --shared <lane> $SCRATCH/lane`; toplevel asserted == `$SCRATCH/lane`; gate sha256 at rev = `ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61` (frozen v3).
- Run 1: `python3 -I …/check-session-material.py --repo $SCRATCH/lane --rev b4a79843… --scope all` → rc 1, `files=23920 findings=235`, `SESSION_MATERIAL_WAIVED: findings=49 files=47`.
- Run 2: same + `--no-waivers` → rc 1, `files=23920 findings=284`, zero WAIVER lines.
- Selftest at the rev: `passed=94/94` (`receipts/selftest.txt`).

## Exact delta (`receipts/delta.txt`)

284 − 235 = 49; removed set (LC_ALL=C sorted FINDING lines) == the 49 `WAIVER` lines, byte-for-byte as (file,rule) pairs; **added set EMPTY** — sidecars only reduced findings; no rule fired differently on any target. Rule totals: only R3_MONITOR_IDENT 62→15 (47) and R2_PROC_TABLE 44→42 (2) move; R1/R4/R7/R8/R9/R5 unchanged. Composition: 45 `mons.json` × R3 + 2 round-46 markdown × {R2,R3} = 49 pairs on 47 files.

## Per-target shape-only classification (`receipts/w4-shape-probe.txt`)

Independent probe importing the gate's own matchers against the rev's blobs, printing classes/counts only: all 49 pairs `ident_reserved=True w4_ok=True`. Identity reservation per waived file: sidecar first line parses (`kind=fixture`), sidecar sha256 == target blob sha256 == registry sha256, registry rules == sidecar rules, registry kind == sidecar kind, waived rule ∈ listed rules, registry row names the file. Matched values: 186 total — `make` 45, `model` 45, `serial` 45, `description` 47 (key-shape counts 1 or 2 per file), `program` 2 (one synthetic process row per round-46 report, pid inside the reserved ≤1024 band) — **all 186 synthetic, REAL=0**; no newly covered real-shaped value is suppressed.

## Rejections (suppression is never silent; all six keep their findings)

- 2 × `rule-not-listed`: R1_CLIENT_DUMP on the two round-46 files (sidecars list only R2,R3) — findings persist in the with-waivers run.
- 3 × `gate-source-mismatch`: `.ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py` (the round-48 *v2* gate copy) vs the v3 gate source — its R1/R2/R3 findings are now live. This is the honest (anti-suppression) direction: the 48th registry row is void under v3 because the copied fixture no longer byte-equals the installed gate. **Observation for L1:** round-49's "47 sidecars" count referred to fixture waivers; the gate-copy row's waiver held under v2 and is void under v3, adding findings, not removing them.
- No `value-not-synthetic` rejections among committed targets.

## Fail-closed negative fixtures (`receipts/negative-fixtures.txt`, scratch repo, throwaway identity)

- Case A — R7-firing file with a real-shaped home user + valid marker + valid registry row → `WAIVER_REJECTED … reason=value-not-synthetic:home-user-not-synthetic`, finding kept.
- Case B — synthetic value waived pre-tamper; append one non-matching line → `sha-mismatch`, finding returns.

## Limit (declared)

The W4 probe reuses the gate's own `matched_values`/namespace regexes (same code path the selftest's 94 cases and the negative fixtures exercise at this rev); it is a re-derivation, not a byte-independent re-implementation. No evidence contradicts the disposition.

**Axes:** operability/privacy-gate integrity — supported (v3 waiver semantics verified at the round-50 revision, fail-closed confirmed); coverage — w1 gap closed.

Report: .ufo/waves/round-50/w2/CritSidecarsV3.md
