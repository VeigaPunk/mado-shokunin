# ScribeScorecardCheck — partial

Scope: tip `01b80946d92b26370d3012a7da655d00dd135154` (committed bytes; worktree clean except untracked round-19 dirs). Attack on the SCORECARD round-19 numbers against their receipts under `.ufo/waves/round-19/evidence/` and `…/evidence/harm/`, plus re-runs of C1/C2/C3 counters at tip and baseline. No lane file edited; scratch in `/tmp/r19*`.

## 1. SCORECARD round-19 results section

`git show 01b8094:SCORECARD.md | grep -c "Round 19 — results\|Round 19 — committed"` → **0**. The file ends at `## Round 19 — declared claims (2026-10-20)`. The results section is absent, so there is no stated number to mismatch. The section must carry the numbers below; each row is what I re-derived or what a receipt states.

| Claim | Before (9c54c56) | Tip (01b8094) | Target / status | Receipt (re-derived by me unless noted) |
|---|---|---|---|---|
| C1 calibration (QUALITY lesson-cited criteria) | 18/26 = 6.9231 | 20/28 = 7.1429 | ≥21/29 **not met** (declared L1 miss) | `evidence/measure-before.json.txt`; `harm/harm-measure-r17.txt`; my `measure.py` runs: 9c54c56 → 18/26, tip → 20/28 |
| C2 freshness pin currency | 2/13 = 1.5385 | 13/13 = 10.0 | 13/13 met | `evidence/fresh-pins-before*.txt`; `harm/harm-fresh-pins.txt`; my runs: 2/13 and 13/13 |
| C3 tripwire recall on 6 incident lines | 3/6 = 5.0 | 6/6 = 10.0 | 6/6 met (narrow; see §3) | `evidence/tw-recall-before*.txt`; `harm/harm-tw-recall.txt`; my runs: 3/6 (tool `c1ae45a7…`), 6/6 (tool `367be947…`) |
| Frozen r18 replay | — | `frozen_verdict_mismatch`, exit 1 | expected by C3 | `harm/harm-tripwire-frozen-round-18.txt`; my `--frozen` replay: extra_findings = the three r18 known misses |
| Frozen r19 re-pin replay | — | `frozen_match`, exit 0 | — | `harm/harm-tripwire-frozen-round-19.txt`; my replay matches. Self-generated pin (README says `expected_findings` is the tool's own output), so not independent recall evidence |
| Tripwire selftests (11 dirs) | — | 16, 9, 33, 30, 45, 34, 18, 17, 13, 1, 31 = **247 cases**, all pass | "every existing suite all-pass" | `harm/harm-tripwire-*.txt`; my reruns reproduce every count. Commit msg says "247/247 suites": these are cases across 11 dirs |
| Gate selftest | 389/389 (baseline archive, my run) | 443/443 (harm receipt and my reruns) | "selftest 443/443" | `harm/harm-gate-selftest.txt` (tool sha `1036d100…`, matches `git show 01b8094:tools/mado-verify.sh`); see §4 for instability |
| Action-plan selftest ("classifier") | — | 52/52 | — | `harm/harm-action-plan-selftest.txt` |
| Harm-watch aggregate | — | 22 runs, ok 21, baseline 1 (r18 frozen mismatch, by design), fail 0, `HARM_WATCH: PASS` | — | `harm/harm-watch-summary.txt`, `harm/harm-watch-pins.txt` |
| Navigation index | — | indexed 34/34, missing 0, dangling 0, duplicates 0, coverage 10/10 | "navigation complete" | `harm/harm-nav-fleet-round-1.txt` |
| Census | — | exit 0; W04 warnings 3 → **4** (adds S097 dup of the omarchy theme URL) | "census exit 0" | `evidence/census-before.txt`; `harm/harm-census-validate.txt` |
| U-route rubric | — | 7/7 seen, score 10.0 | U 7/7 | `harm/harm-measure-u.txt` (receipt is round-16 measure) |
| Rubric V | — | **[UNK]**: no receipt in the harm set that I read | V 6/6 | not verified |

Non-claim numbers in the wave-1 commit message and the lane text: "selftest 443/443", "247/247 suites", "frozen r18 suite 31/31" (my `--selftest` on `round-18/tripwire/frozen`: 31/31). All reproduce.

## 2. C2 freshness: attack on the metric and the sourcing

Reproduced: 2/13 at 9c54c56, 13/13 at tip. Commands: `python3 -I .ufo/waves/round-19/fresh-pins.py <REV>`.

- **Metric is line-loose.** `fresh-pins.py:POINTER` matches any line containing `2.17.2` and any `S###` token. Two of the baseline's "current" files are not supersession pointers at all:
  - `corpus/README.md:44` is the upstream-contract index row for walker 2.17.2 with range `S072–S091`.
  - `corpus/knowledge/walker-route-r18.md:1` is the source header.
  Both were already counted at 9c54c56. Under the stated definition ("in-file, source-cited forward pointer or re-pinned value") they pass through the "re-pinned value" branch. So the 2/13 baseline was not a count of stale-only files.
- **Self-match.** `SKILL.md:573` is a probe-table row describing this very checker. It counts as a pointer. No score effect, because `SKILL.md` also passes at `:1853–1857` (the erratum).
- **Spot-checked the 11 newly counted files.** The pointer lines are genuine dated supersession notes: `arc-synthesis.md:392`, `closeout-r11.md:299`, `config-health-report-r3.md:1009`, `remaining-planes-census.md:338,340`, `walker-deep-r9.md:403`, `walker-deep.md:622,623`, `walker-live-surface.md:305`, `waybar-walker-plane.md:479`, `waybar-walker-semantics.md:467`, `tools/mado-verify.sh:56,101,1258,1920,3285`. So 13/13 holds in substance; the score is looser than its wording.
- **Residual 2.17.0 mentions.** Present-tense `walker 2.17.0` remains at `SKILL.md:23` and `:114` and is handled only by the erratum. The lesson and criterion 28 allow this, so it is not a violation.
- **S096 host bytes verified (file bytes only, no execution):**
  - `/usr/bin/walker`: 7,039,912 B, sha256 `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096` (matches S096).
  - Exactly one `2.17.2` occurrence, at offset 856,302 (`0xd10ee`), inside `.rodata` (addr `0xb6900`, size `0x74654`). Matches S096.
  - `/var/lib/pacman/local/walker-2.17.2-1/desc`: sha256 `5c0d9d89d3e8…0928` (matches S096).
  - `/var/log/pacman.log:2929`: `[ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`, matches S090.
  - [INFERENCE] `/usr/bin/walker` mtime is `2026-10-08 11:14:32 -0300`, 12 days before the 2026-10-20 ALPM line. S096 states the mtime without comment. Package mtimes can predate install, so this is not a contradiction.

## 3. C3 tripwire recall: attack on generalization

Reproduced: 3/6 at baseline (tool `c1ae45a7…`), 6/6 at tip (tool `367be947…`, byte-equal to `git show 01b8094:tools/mado-tripwire.py`).

- **Class check on the six lines.** The three new detections are the right classes: `r13-root.jsonl:4`, `r14-source-safety.jsonl:2,3` are `package_query pacman:-Q`. Numerator counts any finding, but these are the expected class.
- **Variant probes** (synthetic JSONL in `/tmp/r19probe/inputs`, tip tool):
  - Detected: py-variable rename (a), helper rename with argv list (b), bash heredoc (i), eval triple-quoted snippet via `bash -c` (j), concat variable (k), `shell=True` (l), direct `bash -c "pacman -Q"` (e), direct `pacman -Q` (d).
  - Missed: shell-variable indirection in the bash tool: `cmd="pacman -Q zlib"; $cmd` (f), `c=pacman; $c -Q zlib` (g), `cmd='pacman -Qe'; bash -c "$cmd"` (h).
  - The tool docstring already states "variable indirection (`$UV tool install ...`) is invisible here", so this is a documented limit, not a hidden one. Still, "recall 6/6" is only true on the six pinned lines. The claim should say so.
- **Draft suite flip (precision).** `round-18/drafts/tripwire/r18-helperfn`: baseline 13/24, tip 22/24. Failing cases are `sh-fn-positional-n` (`q() { pacman "$1" wayland; }; q -Qi`) and `sh-fn-single-quoted` (`f() { sh -c 'pacman $1'; }; f -Q`). The draft wanted `package_query` only. Tip emits an extra `host_mutation` on rule `pacman`, a read-only query. The round-19 suite (`round-19/tripwire/r19-helperfn`, 34/34) re-declares it as expected `host_mutation`. This looks like the conservative unknown-verb default, and it is codified, but the SCORECARD should name it. The "every existing suite all-pass" wording covers only the superseding suites.
- **Frozen r19 pin is self-referential** (see §1). Recall evidence rests on the six hand-labelled pairs in round-18.

## 4. Gate selftest stability (not declared in the claim)

- Receipts: `harm/harm-gate-selftest.txt` = 443/443 at tip. My reruns at tip: 3 sequential + 3 concurrent + 1 traced (`bash -x`) = 443/443 each. Baseline archive 389/389 (2 runs).
- **Two of nine non-trace tip runs failed:**
  - First run in the lane: `MADO_SELFTEST: FAILED — 323 passed, 120 failed`.
  - First run in an archive extract (`/tmp/r19tip`): `FAILED — 388 passed, 55 failed`.
  - Both show `cp: cannot stat '…/clean/.'` and missing `clean/` and `omarchy/` fixture subtrees, while later scenario dirs exist (`census/`, `theme/`).
  - The gate has no `trap`, and no `rm` in the selftest block (grep). I could not reproduce after that: not in six more runs, including concurrent runs.
  - [UNK] root cause. The scorecard's "443/443" should carry the run count or name this intermittency.
- The gate-swap receipt (`evidence/gate-swap-receipt.txt`, `383 passed, 6 failed`, exit 2) is a fixture copy of `d9a5a18` with the R10 self-pin. The QUALITY note already labels it this way. It is not the 443 number, but both sit in the evidence folder and should not be conflated.

## 5. Path:line evidence cited

- `SCORECARD.md`: no `Round 19 — results` heading at tip (grep count 0).
- `.ufo/waves/round-19/fresh-pins.py:POINTER` (line-level regex).
- `.ufo/waves/round-19/tw-recall.py` (six pinned pairs, `expected_findings ∪ known_misses`).
- `tools/mado-tripwire.py` docstring, "variable indirection (`$UV tool install ...`) is invisible here".
- `.ufo/waves/round-19/tripwire/r19-helperfn/expected.json`: `sh-fn-positional-n`, `sh-fn-single-quoted` expect `host_mutation`.
- `corpus/QUALITY.md` round-19 note: criterion 26 re-cut; `383 passed, 6 failed` labelled as the fixture re-cut.

## Limits

- Read only: `git show`, `git archive` to `/tmp`, `grep`, and file-byte reads of host files (`/usr/bin/walker`, pacman `desc`, `pacman.log` line via Python `open()`). Did not run `walker --version`, pacman, hyprctl, systemctl, or any service.
- Ran `tools/mado-verify.sh --selftest` only (in the lane, `/tmp/r19tip`, `/tmp/r19b`), never `--regression`.
- Ran tripwire `--selftest`, `--frozen`, and `--scan` only on `/tmp` copies, not the lane.
- Counters `measure.py`, `fresh-pins.py`, `tw-recall.py` re-run at tip and baseline. Their receipts were checked by sha256: tool shas match `de4c422b…`, `a094be01…`, `22090298…`.
- Did not verify rubric V 6/6 (no receipt read). Did not check the S094 row status beyond the scorecard text. Did not run the anchor-durability or supersede-sweep checkers (outside this item).
- No fetches: no curl, so no fetch receipts. [UNK] the gate flake cause.

## Installs

None. No tools installed or upgraded.

Scratch used (not in lane): `/tmp/r19s`, `/tmp/r19st`, `/tmp/r19fz`, `/tmp/r19probe`, `/tmp/r19base`, `/tmp/r19tip`, `/tmp/r19b`, `/tmp/r19-*.txt`.
