# CriticHonestyW2 — partial

Seat `MadoR19.CriticHonestyW2` (critic, wave 2). Target: tip `01b80946d92b26370d3012a7da655d00dd135154`, read-only. Lane worktree = tip except for untracked `.ufo/waves/round-19/w2/` and `.ufo/waves/round-19/fetch/RevRubricVRisk/`. All runs were in a `/tmp/chw2` clone checked out at the tip. I edited no lane file; this report is my only write.

**Verdict.** Every number the round states reproduces independently: C1 20/28, C2 13/13, C3 6/6, anchor-durability red→green, supersede-sweep 11→0, gate-swap 383/6, gate selftest 443/443, tripwire suites 247/247, the S096 host bytes, and the S097/S098 upstream bytes. The prose is the problem. Eleven sentences say more than their evidence shows; they fall under fetch-verify scope, receipt headers, recall versus suite preservation, privacy coverage, and stale or unobserved "live" facts. None of them moves a scored counter, so the counters stand. Two of them (A2, A5) are criterion-24 failures inside the round that says it applied criterion 24.

## What holds (re-run, not trusted)

| claim | command (in /tmp/chw2) | output |
|---|---|---|
| C1 18/26 → 20/28 | `python3 .ufo/waves/round-17/measure.py {9c54c56,df84807,01b8094}` | c1 `26/18 6.9231`, `26/18 6.9231`, `28/20 7.1429`; measure.py sha `de4c422b…` at tip |
| C2 2/13 → 13/13 | `python3 -I .ufo/waves/round-19/fresh-pins.py REV` | 9c54c56 `current 2`, df84807 `13`, 01b8094 `13` |
| C3 3/6 → 6/6 | `python3 -I .ufo/waves/round-19/tw-recall.py REV` | 9c54c56 `3` (tool `c1ae45a7…`), 01b8094 `6` (tool `367be947…`) |
| QUALITY 27 red/green | `anchor-durability.py` | 9c54c56 `FLAGGED S084 S094` rc=1; 17661e0 same rc=1; df84807 and tip `flagged=0` rc=0 |
| QUALITY 28 red/green | `supersede-sweep.py` | 9c54c56 and 17661e0 `files=13 pointed=2 stale=11` rc=1; df84807 and tip `pointed=13 stale=0` rc=0 |
| R18-V2 swap 383/6 incl. R10 | `bash .ufo/waves/round-19/gate-swap.sh df84807…` (fixture `--selftest` only) | `383 passed, 6 failed` (R10 + 5×OM9); body equals the committed receipt apart from the /tmp dir name |
| re-cut receipts | receipt-check over a /tmp claims file | `tw-recall-before-recut` ok, `fresh-pins-before-recut` ok, `gate-swap-receipt` ok (tool = fixture); bodies equal the originals; tool bytes are identical at 17661e0, df84807 and 01b8094 |
| suites | `tools/mado-tripwire.py --selftest DIR` ×11 | 9+16+33+30+31+1+45+34+18+17+13 = 247/247 |
| gate | `bash tools/mado-verify.sh --selftest` | `443/443 assertions passed` |
| frozen | `--frozen round-19/frozen` / `round-18/frozen` | `frozen_match` rc0 / `frozen_verdict_mismatch` rc1 |
| M7 classes and controls | base vs tip tool `--scan` on the 5 frozen inputs | the 3 new findings are exactly `package_query/pacman:-Q` (`r13-root:4`, `r14-source-safety:2,3`); 0 findings on the other 20 lines (26 lines total, trailing newline in every file). TwMerge.md:151 and CriticC3.md:19 say "21 control lines": the lesson's 20 is right and those reports are wrong |
| S096 host bytes | `sha256sum`, python `find`/`count` on `/usr/bin/walker`; `sed` on pacman.log; `desc` | `25240650…`, 7,039,912 B, find 856302, count 1, `2.17.0` → -1; `pacman.log:2929` upgraded walker 2.17.0-1→2.17.2-1; `desc` sha `5c0d9d89…`, `%VERSION% 2.17.2-1`; elephant `:3095`, uwsm `:2926`, hyprland `:2733` confirm SKILL's "same-morning moves" |
| S097 | curl, `git ls-remote`, blob-less /tmp clone | url `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml` status 200, 461 B, sha256 `dbdd13a6…1786`, fetched_at 2026-10-20T18:06:33Z (= committed body); tag → `8fcc9d6048af…`; tree `themes/matte-black` = `3fc08f954e5a…`; `git hash-object` of the committed body = tag blob `5e1a8cca…`; 19 theme dirs on both sides; `~/.config/omarchy/themes` empty; `theme.name` 12 B (size only) |
| S098 | curl + tar | url `https://static.crates.io/crates/xdg/xdg-3.0.0.crate` status 200, 15,821 B, sha256 `2fb433233f2d…85b5`, fetched_at 2026-10-20T18:06:33Z = `walker-v2.17.2-Cargo.lock:2708` checksum; `base_directories.rs:447-448` quote present |
| rows 95→98 | parse SOURCES at both revs | A 88→91, mined 80→81, rejected 7→9 |
| M6 leak absent at tip | `git grep -i x-real-ip 01b8094`; IPv6-shape grep | prose hits only (WITHHELD.md, SentinelVcsFixtures.md, gen_w2.py, lesson); no IPv6 literal |
| M8 / M9 | fleet `ls`; w1 `spec.json` vs reports | fleet `.ufo/waves/round-19` absent; 86 seats, 29 without a report (reviewer 18, connector 7, revenger 3, simplifier 1), which matches "~30" |

## Overclaims — sentence, counterexample, replacement

### A1 — "fetch-verify still exits 1" (fetch-verify scope; lesson M1)
`corpus/lessons/round-19.md:16`: "`fetch-verify.py` still exits 1 on the historical round-18 receipts (append-only; not claimed fixed)."
- A bare run exits **0**. At both 9c54c56 and the tip, `python3 -I .ufo/waves/round-18/fetch-verify.py` prints `SUMMARY receipts=424 ok=329 bad=0 digest_only=95 … conflicts=0` with rc=0. Conflicts are computed only with `--sources` (`fetch-verify.py:384` `build_conflicts(receipts) if args.sources else {}`).
- With `--sources`, every row request exits 1, whatever the row: `--rows S097` gives `ROW S097 receipted` and rc=1; `--rows S072` also gives rc=1. The four `CONFLICT` lines are global (`fetch-verify.py:461`). So S097 can never be shown green by this tool. Any "Fix: S097" next to "fetch-verify exits 1" (draft `drafts/LogDraft.md:8`) reads as if S097 makes it green, and it cannot.
- The tool's default `--fetch-root` is `round-18/fetch` (`:272-273`), so no round-19 receipt is checked. `--fetch-root .ufo/waves/round-19/fetch --sources … --rows S096,S097,S098` gives `bad=32` (`MISSING` for every gitignored body, because round 19 has no `RETENTION.json`), `ROW S098 UNRECEIPTED body-unverified`, rc=1.
- Replacement: "`fetch-verify.py --sources corpus/SOURCES.md --rows <any>` exits 1 at the tip on 4 global `CONFLICT` lines from the round-18 GitHub tree-URL receipts; a bare run exits 0 (no conflict check without `--sources`). The default root is round-18 only. Over `round-19/fetch` it reports 32 `MISSING` digest-only bodies (no `RETENTION.json`) and S098 `body-unverified`. S097/S098 are not fetch-verify-green; their support is the tag clone and the lockfile checksum. Not claimed fixed."

### A2 — the baseline receipts are not all header-bound (SCORECARD pre-registration)
`SCORECARD.md:1069-1070`: "Baseline receipts: `.ufo/waves/round-19/evidence/*-before.txt` (first line `RECEIPT … tool_sha256=… measured_commit=9c54c56…`)."
- The glob matches `census-before.txt`, whose first line is `utc=2026-10-20T16:59:29Z cmd=…/sources-census.sh validate …`. It has no RECEIPT header. receipt-check on it (/tmp claims) gives `MISSING_PROVENANCE`.
- The other two matches read `ERROR` under the committed checker (lesson M5). `python3 -I .ufo/waves/round-18/receipt-check.py .ufo/waves/round-19/receipt-claims.json` at the tip prints `EXPECT_SUMMARY: 3/5`, rc=2. The claims file still expects `ok` for them and relies on an unlanded "three-hunk change" (`receipt-claims.json:15`). The ok re-cuts are not in any committed claims file.
- Replacement (append): "Correction: of the three `*-before.txt`, `census-before.txt` has no RECEIPT header (provenance only, `MISSING_PROVENANCE`), and `fresh-pins-before.txt`/`tw-recall-before.txt` read `ERROR` (tool absent at `9c54c56`). The header-bound baselines are `evidence/*-before-recut.txt` (`measured_commit=df84807`, data rev 9c54c56; checker `ok`). The committed `receipt-claims.json` reads 3/5, exit 2, until its two `ok` claims point at the re-cuts."

### A3 — "header-bound re-cut" names one receipt for two (QUALITY note after 28)
`corpus/QUALITY.md:194-198`: "criterion 26's red-before `gate-rc-redbefore.txt` and `regression-recut.txt` read `MISSING_PROVENANCE` … The header-bound re-cut is `evidence/gate-swap-receipt.txt`".
- `gate-swap-receipt.txt` re-cuts the W3 transplant experiment: the d9a5a18 block in the 17661e0 gate, `--selftest`, 383/6. Its blocks line is `base=17661e0…:3467-3489 … old=d9a5a18…:3402-3415`.
- It does not re-cut `gate-rc-redbefore.txt` §1 (old gate on a stub root → `FAIL … local edit`). It does not re-cut `regression-recut.txt` (PIN_MADO via the external harness). Both stay headerless.
- Replacement: "The header-bound receipt of the swapped-block run (R18-V2's requested form) is `evidence/gate-swap-receipt.txt` …; `gate-rc-redbefore.txt` §1 and `regression-recut.txt` stay headerless, provenance only."

### A4 — "round 18 left out R10" (QUALITY:200-201; lesson M4 `:19`)
- The round-18 SCORECARD summary (`SCORECARD.md:1043`, "383/389, five OM9 failures") left it out. The W3 report that sentence cites lists it: `.ufo/waves/round-18/w3/reports/W3CriticC1Final.md:188` "R10 (pin drift, expected)".
- Replacement: "round 18's SCORECARD summary named only the five OM9; its cited W3 report (`W3CriticC1Final.md:188`) listed R10 as expected pin drift."

### A5 — the round's own new replay receipt fails criterion 24 (SKILL round-19 notes; lesson M4/M5 "Applied", "Rule kept")
- `.ufo/waves/round-19/frozen/README.md:1` has `RECEIPT tool=/home/…/tools/mado-tripwire.py tool_sha256=367be947… utc=2026-10-20T18:01:27Z argv=…` and **no `measured_commit`**. That is a worktree measurement taken 25 s before commit `01b8094` (18:01:52Z), never bound at the commit (criterion 7). receipt-check gives `MISSING_PROVENANCE`.
- `SKILL.md:1879-1883` ("The frozen replay baseline for the current classifier is `.ufo/waves/round-19/frozen` … the three round-18 known misses are expected `package_query/pacman:-Q` findings") rests on that receipt.
- The bytes are right: I replayed it, `frozen_match` rc0. The provenance header is what is missing. The generator `frozen-repin.py` emits this header shape, so every future re-pin repeats the defect.
- Replacement for lesson M5's "Rule kept: …": add "— not yet applied to round 19's own `frozen/README.md` RECEIPT (no `measured_commit`; `MISSING_PROVENANCE`); re-cut with `measured_commit=01b8094` and a lane-relative tool path." The smallest fix is a header-bound `--frozen` replay receipt at `01b8094` and a `frozen-repin.py` header that includes `measured_commit`.

### A6 — the M7 side-evidence is narrated, not receipted (lesson M7 `:22`)
"Reported beside recall, not instead of it: class of each former miss …, zero findings on the 20 control lines, and a whole-corpus base-vs-merged diff (no lost finding; every added finding outside the new classes listed and judged)."
- No committed receipt carries any of the three. The only source is `w1/reports/TwMerge.md` §4/§6 (prose, no RECEIPT header). The lesson does not cite it. Criterion 24 says "a claimed re-cut is a committed receipt…, never a narrated rerun".
- I confirmed the first two independently (table above). TwMerge §6 does not say which sha its corpus scan used: §2(g) says a docstring edit after the battery gave a "new sha". It also excludes 122 live-drifting files.
- Replacement: "Reported beside recall in `w1/reports/TwMerge.md` §4 (classes; 0 findings on the 20 control lines) and §6 (4,632 byte-stable files, added 4,838, lost 0; 13 non-new-class additions read by hand). These are narrated seat results, not header-bound receipts."

### A7 — "every existing suite still all-pass" versus a rewritten case (SCORECARD:1108; commit `01b8094` "247/247 suites")
- `01b8094` edits `.ufo/waves/round-17/tripwire/hardening/expected.json`. Case `multiline-quoted-commit-clean` (want rc0, no findings) becomes `multiline-quoted-commit-vcs` (want rc1, `vcs_write/git:commit`). The fixture keeps its `-clean` name.
- The 9c54c56 tool on the tip suite gives `SELFTEST_SUMMARY: 32/33 failed=['multiline-quoted-commit-vcs']`. 247/247 therefore means 246 unchanged cases plus one rewritten expectation. TwVcsClass.md:85 disclosed this as a "taxonomy supersession"; no landed text (lesson, SKILL, commit message) does. The case's original guard (no `host_mutation` from a quoted `sudo pacman -S` inside a commit message) still holds.
- Replacement for the results text: "all suites pass, 247/247, with one round-17 expectation rewritten (hardening case 5 `-clean` → `-vcs`: a `git commit` is now a `vcs_write` finding; still no `host_mutation`)."

### A8 — fetch `.gitignore` covers only named files (lesson M6 `:21`; `fetch/.gitignore:1`)
Lesson: "`fetch/.gitignore` keeps all HTML/crate/API bodies digest-only (30 lines)". Header: "bodies stay local, never committed."
- The file is 29 exact paths plus one comment. It contains no pattern rule.
- Counterexample in the worktree: `.ufo/waves/round-19/fetch/RevRubricVRisk/xdg-3.0.0.crate` (15,821 B, sha `2fb43323…`). `git check-ignore -v` → rc=1 (not ignored); `git status -uall` → `?? …/RevRubricVRisk/xdg-3.0.0.crate`. A directory add would commit a crate body, which is the M6 landing route.
- Replacement: "`fetch/.gitignore` lists the 29 wave-1 bodies by exact path; a new seat's body is not covered (w2 `RevRubricVRisk/xdg-3.0.0.crate` shows as untracked). Bodies stay out of commits only if each new path is listed or a pattern rule (`*.html`, `*.crate`, `*.json` except `receipts.jsonl`) lands."

### A9 — stale statements about S096 (C2 pointers; QUALITY 28 limit)
- `corpus/knowledge/remaining-planes-census.md:338`: "the binary-bytes row S096 is reserved and not yet recorded". `corpus/knowledge/walker-live-surface.md:305`: "the host binary bytes are reserved as S096 (row pending, not re-read this round)". Both are false at the tip: S096 is a committed `mined` row from `df84807`, and the bytes were read this round.
- Six of the 13 pointers cite only round-18 rows (S090 or S072–S091): `corpus/README.md:44`, `arc-synthesis.md:392`, `closeout-r11.md:299`, `config-health-report-r3.md:1009`, `waybar-walker-plane.md:479`, `waybar-walker-semantics.md:467`. The pre-registered C2 text (`SCORECARD.md:1099-1102`) requires a pointer "citing a SOURCES row opened this round for the host walker bytes". Five files meet that and name S096 as recorded: SKILL, `walker-deep-r9`, `walker-deep`, `walker-route-r18`, `tools/mado-verify.sh`. Two name it as pending. The counter's 13/13 holds; the declared semantics give 5/13. This overlaps CriticC2W2.
- Replacement (append-only, per file): "Correction (round 19): S096 is recorded (`df84807`); `/usr/bin/walker` bytes were read 2026-10-20 (sha `25240650…`, literal `2.17.2` at 856,302)." Also, when results land: "C2 13/13 by `fresh-pins.py` (any `S###` token); 5/13 pointers name the round-19 host row S096 as recorded."

### A10 — unobserved live runs stated as fact (gate comment)
`tools/mado-verify.sh:101-102`: "the old pin failed every live run from that transaction onward."
- No live gate run is evidenced after 2026-10-20T09:16:46-0300 (host pause). The only `live.walker.version FAIL` at the tip is a stub-PATH matrix (`w1/reports/GateFreshJj.md:146-148`), and earlier text says "would FAIL" (`round-18/w1/reports/ConnUnknownsJoin.md:481`, `PacmanLogMoves.md:7`).
- Replacement: "the old pin would FAIL any live run after that transaction (inferred; no live gate run since — host pause)."

### A11 — forward references stated as present (lesson header; LOG)
- `corpus/lessons/round-19.md:9-10`: "report `.ufo/reports/round-19/mado.md` (fleet)". At this time `/home/vgpnk/Projects/shokunin/.ufo/reports/round-19/` holds only `kagi.md kake.md kotoba.md kotodama.md`, and no `mado.md`. Replacement: "report (pending): …" or land it before admission.
- LOG tail: `LOG.md` ends at the round-18 entry (`:1287-1310`). There is no round-19 entry at the tip, and SCORECARD has only "Round 19 — declared claims", no results. The candidate text, `drafts/LogDraft.md`, is a placeholder skeleton. Its `:8` pairs "`fetch-verify` exits 1" with "Fix: superseding row S097" (see A1), and its `:28` correctly leaves pre-round gate/suite values `⟨UNK⟩`. When finalized, it must not credit S097 with a fetch-verify fix, and it must state A2, A7 and A9.

## Minor or disclosed (no change required)

- `QUALITY.md` 27's checker accepts `ROW S005 durable — alias segment main pinned by date 2026-01-16`. The anchor is an 8-hex short commit (`3dac056d`) plus a date, with no byte sha. Today it reproduces: `-/raw/main/README.md` and `-/raw/3dac056d/README.md` are both 200, 12,721 B, sha `e81ad629e8d7beba23cf4d99d0c58e4af662a7df9564d2423fff19a1eed65548`, fetched_at 18:09:23Z / 18:09:25Z. So it is not a defect now; the "dated version" arm is just looser than criterion 27's wording ("tag- or commit-pinned bytes with their sha256").
- SKILL registry rows at `SKILL.md:571-573` still say "contract control, unobserved until landed" although the controls now pass (17661e0 `FLAGGED S084 S094`; 11 STALE). This understates; it does not overclaim.
- M5's "the commit carrying the producer" names df84807. The first carrier is 17661e0, and the bytes are identical at both, so checker `ok` holds either way.

## Impacted axes

Calibration (QUALITY note and lesson wording: A1, A3, A4, A5, A6), freshness (A9: declared versus counted semantics, plus two false lines), operability (A7: preservation claim), harm and privacy (A8: open landing path). No score changes: the counters are pre-registered and reproduce.

## Smallest safe correction

Make append-only text corrections A1–A4 and A6–A11 as written above. Then add header-bound receipts at `01b8094` for the frozen re-pin replay and for `census` (A5, A2). Add the two re-cut claims to `receipt-claims.json`. Add one pattern rule to `fetch/.gitignore` (A8). No tool or criterion change is required.

## Limits

- I did not probe the running walker process. Its status stays [UNK], which the docs also say.
- I did not re-run the whole-corpus base-vs-merged diff. The live transcript corpus is owned by RerunPrecision; A6 is about provenance, not the numbers.
- M9's "429" cause is [UNK]. I counted only missing reports (29/86); `task-result.json` has empty `results`.
- The S097 tree and blob ids were checked with `git ls-remote` and a blob-less `--depth 1` clone in `/tmp` (read-only git), not curl. Those are verification reads, not fetch receipts.
- Fetch bodies are in `/tmp/chw2-fetch/` only.
- Read-only git and `/tmp` writes only. I ran no jj, pacman, systemctl, or live gate; the gate and its swap fixture ran only with `--selftest`.

## Installs

none
