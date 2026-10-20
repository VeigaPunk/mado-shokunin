# ScribeLogCheck — breaks

Tip under check: `01b80946d92b26370d3012a7da655d00dd135154` (`git log -1`: "round-19: tripwire merge …", 2026-10-20T15:01:52-03:00). Read-only attack: LOG.md, the lesson, QUALITY/SCORECARD tails, wave records, and the claim checkers re-run at the tip and at `9c54c56`. Nothing in the lane was written. Scratch copies live only in `/tmp/scribe19/`.

**Headline.** The round-19 LOG entry the assignment names is not at the tip. The three numeric claims (C1 20/28, C2 13/13, C3 6/6) reproduce. Five lesson or log claims do not hold as written: the M5 receipt fix is not wired (the round-19 receipt claims file reads 3/5, exit 2, at the tip); the M9 mitigation ("wave 2 leans on roles whose routes answered") is contradicted by the w2 dispatch (10 reviewer seats on the route that failed in wave 1); the wave-1 record has no outcome data behind the 429 cause; the install record is absent from every round-19 record; and the harm-watch evidence is uncommitted.

## 1. LOG round-19 entry: absent at the tip

- `git show 01b8094:LOG.md | grep -c -i 'round.19'` → `0`. The last entry is `## 2026-10-20 — round 18 …` at `LOG.md:1287`. The worktree `LOG.md` is byte-identical to the tip (`git diff --stat 01b8094 -- LOG.md` empty).
- The only LOG draft is `.ufo/waves/round-19/w1/reports/LogDraft.md` (also `drafts/LogDraft.md`). It is a skeleton with `⟨after⟩` placeholders and an explicit "wave counts and dead seats … install record … verdicts" placeholder list. None of those placeholders was filled into LOG.md.
- Missing from any round-19 record in the lane: C1/C2/C3 after values as a LOG entry; wave counts; dead-seat list; install record; harm-watch result; frozen-baseline digests; verdicts. SCORECARD.md has only the pre-registration (`SCORECARD.md:1059` `## Round 19 — declared claims`); there is no results block.
- Operator directive: installs must be recorded in the report or handoff. The lesson has no Installs line.

## 2. Claim-by-claim (lesson `corpus/lessons/round-19.md` + LogDraft)

| Claim | Stated | Re-run at tip / at 9c54c56 | Verdict |
|---|---|---|---|
| C1 calibration | 18/26 → 20/28; target ≥21/29 missed | `python3 .ufo/waves/round-17/measure.py <rev>`: tip `c1 {criteria 28, lesson_cited 20, score 7.1429}`; 9c54c56 `{26, 18, 6.9231}` | **holds**. Miss reported as a miss (lesson Decisions). Note: `measure.py:93` counts any criterion whose line contains `lessons/`; criteria 27 and 28 both qualify, so the metric moved by criterion count plus citation, not by new evidence. The lesson says "literal"; that is accurate. |
| C2 freshness pins | 2/13 → 13/13, sourced on S096 | `python3 -I .ufo/waves/round-19/fresh-pins.py`: tip `current 13 / denominator 13, score 10.0`; 9c54c56 `2 / 13, 1.5385` | **holds for the rule as defined**. Every pointer line contains `2.17.2`; every cited `S###` token exists in SOURCES.md with status `mined` (none `rejected`). Caveat: pointers cite S073/S090/S091/S072 as well as S096 (e.g. `SKILL.md` lines 573, 1853–1857; `corpus/README.md:44` cites S072/S091). "Sourced on S096" is true for the walker version binding, not for every pointer. |
| C3 tripwire recall | 3/6 → 6/6; the three drafts applied; 20 control lines clean | `python3 -I .ufo/waves/round-19/tw-recall.py <rev>`: tip `incident_lines 6, detected 6, score 10.0`, tool sha `367be947…` = `git show 01b8094:tools/mado-tripwire.py \| sha256sum`; 9c54c56 `3/6, 5.0`, sha `c1ae45a7…` | **holds**, with the M7 caveat below. |
| C3 M7 controls | "zero findings on the 20 control lines" | `/tmp/scribe19/tw.py --scan` on the five frozen inputs (copied from tip): 26 lines total, 6 incident, so 20 non-incident. Findings sit only on incident lines: `r13-global-capture:1` (sudo, pacman:-S, wayland-info, pacman:-Q), `r13-root:4` (pacman:-Q), `r14-review-source-bar:1` (sudo, pacman:-Sw), `r14-source-safety:2` and `:3` (pacman:-Q), `r15-libinput-events:1` (sudo, pacman:-S). Control-line findings: none. | **holds**. The three former misses (`r14-source-safety:2`, `:3`, `r13-root:4`) are `package_query/pacman:-Q` as M7 requires. |
| M1 anchor durability | red `9c54c56` FLAGGED S084 S094 exit 1; green `df84807` flagged=0 | `anchor-durability.py 9c54c56` → `FLAGGED S084 S094`, rc=1; at the tip `mined=81 durable=81 flagged=0`, rc=0 | **holds**. The tool shows `5 distinct 200 digests` for the tree URL. I could find only 4 in the committed `fetch/HtmlAnchorSweep/receipts.jsonl`; the fifth lives in a receipt file I did not identify [UNK]. |
| M1 S097 tag/tree ids | tag v3.8.4 lightweight → `8fcc9d60…`; tree `themes/matte-black` `3fc08f95…` | `/tmp/ReopenS097-omarchy`: `rev-parse v3.8.4` = `8fcc9d6048af…`, `objecttype commit`; `v3.8.4:themes/matte-black` = `3fc08f954e5a…` | **holds**. |
| M1 S097 digest | `colors.toml` sha `dbdd13a6…`, 461 B | `sha256sum fetch/SrcS094/colors.toml` = `dbdd13a6…`; `receipts.jsonl` http 200, bytes 461 | **holds**. |
| M2 S098 | xdg 3.0.0 sha `2fb43323…85b5` = walker v2.17.2 `Cargo.lock:2708` | `sed -n 2705,2708p fetch/SrcS084/walker-v2.17.2-Cargo.lock` → `checksum = "2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5"`; `sha256sum` of the three `xdg-3.0.0.crate` copies = same; receipt http 200, 15,821 B | **holds** |
| M2 walker-route head | head `source:` token re-pointed; correction block appended | `walker-route-r18.md:1` no longer carries S084 as a source token (only the parenthetical "supersedes S084"); `:327` correction block present | **holds** |
| M3 supersession sweep | red `9c54c56` `files=13 pointed=2 stale=11` exit 1; green `stale=0` | `supersede-sweep.py 9c54c56` → `files=13 pointed=2 stale=11`, rc=1; tip → `pointed=13 stale=0`, rc=0 | **holds** |
| M4 gate re-cut receipt | `383 passed, 6 failed` = five OM9 + R10; tool sha `6e6782c3…` | `evidence/gate-swap-receipt.txt`: `MADO_SELFTEST: FAILED — 383 passed, 6 failed`, six listed (R10 + five OM9); header `tool_sha256=6e6782c3…`; `sha256sum evidence/gate-swap-d9a5a18.sh` = `6e6782c3…`. I read the receipt; I did not run the gate. | **holds** (receipt-only). |
| M5 receipt re-cut | recut files `*-before-recut.txt` with `measured_commit=df84807`; bodies identical; claims file read via `receipt-check.py` | bodies: `diff` of lines 2+ of `tw-recall-before*.txt` and `fresh-pins-before*.txt`: IDENTICAL. But `receipt-claims.json` still names the **original** `tw-recall-before.txt`, `fresh-pins-before.txt` (rev 17661e0, expect `ok`), and `git diff --stat 9c54c56 01b8094 -- .ufo/waves/round-18/receipt-check.py` is empty: the three-hunk `tool_rev` change never reached the lane. Tip run: `RECEIPT r19-tw-recall-before ERROR`, `r19-fresh-pins-before ERROR`, `EXPECT_SUMMARY: 3/5`, exit 2. | **breaks**. The bodies are fine; the wiring is not. See §3. |
| M6 privacy | withheld bodies moved out; `fetch/.gitignore` 30 lines; no leak | `WITHHELD.md` present; `git show tip:…/fetch/.gitignore \| wc -l` = 30; tip tree has no `X-Real-Ip` except as prose in `WITHHELD.md`, `SentinelVcsFixtures.md`, and the lesson; the 15 ignored HTML/JSON bodies still in the worktree contain no `X-Real-Ip`, `challenge`, or IPv6-like string | **holds** for what is committed. Undisclosed: the 15 ignored bodies remain in the worktree (`git check-ignore` confirms they are ignored), so the lesson's "bodies moved to /tmp" is true only for the three withheld oldid files. |
| M7 whole-corpus diff | "no lost finding; every added finding outside the new classes listed and judged" | `w1/reports/TwMerge.md` §6 exists; I did not re-run the corpus diff (it reads `~/.omp` session transcripts; out of scope for this seat) | **not re-run** [UNK] |
| M8 misroot | copies deleted from fleet root | `ls /home/vgpnk/Projects/shokunin/.ufo/waves/round-19/` → no such directory; fleet `git status` shows only `?? .ufo/state/mado.report-baseline` (not a round-19 file; owner unknown) | **holds** |
| M9 dead seats | "~30 wave-1 seats routed to m_zfl … ended 429 after 10 retries" | see §4 | **partial**: count is close, cause unverifiable in the lane |
| M9 mitigation | "Wave 2 leans on roles whose routes answered (scout/executor m_flash, critic/sentinel m_opus, mutation-tester m_sol)" | `w2/task-result.json` `details.progress`: `reviewer / m_zfl` × **10** (ReviewFrozen19, ReviewLandedTool, ReviewRepinTool, ReviewHarmTool, ReviewGateF6F9, ReviewLessonRows, ReviewQualityNote, ReviewSourcesRows, ReviewJjFinal, ReviewDeltaCarry); scribe on m_haiku × 3 | **breaks**. The mitigation names a route set that omits the route the wave-2 reviewers use. |
| R18-V2 application | criterion 26 red-before read `MISSING_PROVENANCE`; re-cut `gate-swap-receipt.txt` | `receipt-check.py … receipt-claims.json`: `r19-c26-redbefore-headerless MISSING_PROVENANCE`, `r19-c26-regression-recut-headerless MISSING_PROVENANCE` | **holds** |

## 3. The round-19 receipt claims are red at the tip

- `receipt-claims.json` header and `tool_rev_semantics` say the three-hunk checker change "makes them ok". The change is demonstrated only in a `/tmp/r19demo2` clone (`w1/reports/ReceiptClaims19.md:89`, `:95`, `:114`). Its own unpatched result is `3/5 exit 2` (`ReceiptClaims19.md:123`); the patched result is `5/5`.
- The lesson's M5 remedy (a re-cut) is only half landed: the recut files exist and match, but no claim in `receipt-claims.json` references them and the checker is unchanged.
- Consequence: the committed round-19 claims file fails its own expectations. The R18-V2 note in QUALITY is unaffected (it cites the two red claims, which do return `MISSING_PROVENANCE`).

## 4. Waves, dead seats, routes

- **Wave 1** (`w1/record.json`, `w1/dispatch.json`): 86 members, `counts.spawn 86`, `resume 0`. Roles: reviewer 18, executor 15, scribe 15, scout 14, connector 8, critic 5, revenger 4, mutation-tester 3, simplifier 2, sentinel 2. Routes (`w1/task-result.json` progress): `m_zfl` = connector 8, revenger 4, reviewer 18, simplifier 2 (**32**); all others on m_flash/m_opus/m_sol/m_haiku.
- Reports on disk: `w1/reports/*.md` = 59 files. 58 match a member; `TwMerge.md` is the seat `MadoR19.TwMerge-2` (its header says so) and is **not in w1 record or dispatch**. That is a bookkeeping gap, not a data loss.
- Members with **no report**: 28. Breakdown: reviewer 17 of 18, connector 7 of 8, revenger 3 of 4, simplifier 1 of 2. All 28 are on `m_zfl`. So 28 of 32 `m_zfl` seats have no report; the lesson's "~30" is approximately right.
- The 429 cause is **not** in the lane: no `429` or "rate limit" text in any w1 report or `task-result.json` (grep hits are hashes). `task-result.json` shows every progress entry `pending`, so there is no outcome record. The record file has no status field. The 429 claim is [UNK] from the lane.
- "No dead seat respawned": consistent (`resume 0`, `resumeSends []`).
- **Wave 2** (`w2/dispatch.json`, `w2/task-result.json`): 67 members (scout 22, executor 20, reviewer 10, critic 5, mutation-tester 4, sentinel 3, scribe 3). Status at my check: all `pending` in the spawn record; `w2/reports/` held only `swarm-registry.json` plus in-flight reports from this wave. No dead-seat accounting exists yet for w2. The reviewer route contradicts M9 (§2).
- `w2/spec.json` and `w1/dispatch.json` carry the same `/skill:godspeed` prompt body; not an error.

## 5. Installs

- Every w1 report that carries an `## Installs` section says `none` (I grepped the section headers; no install command was found in any sampled body). `w1/reports/CriticHonesty.md:43` records an empty `find ~/.local/bin ~/.local/share/uv/tools ~/.cargo/bin -newermt 2026-10-20 13:53:34`.
- The lesson, LogDraft and SCORECARD carry no install record line. The LogDraft lists "install record" as a placeholder that was never filled.
- Host pause respected in this check: no pacman, sudo, service or gate command. `/usr/bin/walker` and `/var/log/pacman.log:2929` were read as bytes (`sha256sum`, `python open()`, `sed -n`).

## 6. Other mismatches

- **LogDraft S096 literal** (`w1/reports/LogDraft.md`, GATE row in lesson): "byte 856,302: `version2.17.2`". At `/usr/bin/walker`, `find(b'version2.17.2')` = 856,295 (0-based); `find(b'2.17.2')` = 856,302. The S096 row and the lesson correction block say "`2.17.2\n` literal at file offset 856,302", which is correct; the LogDraft quote is wrong.
- **Control-line count**: `w1/reports/TwMerge.md:151` and `CriticC3.md:19`, `:70` say 21; `TwHelperFn.md:86` says 20; arithmetic (26 − 6) gives 20. The lesson's 20 is right.
- **Stale annotation** in the before receipts: `evidence/fresh-pins-before.txt` and `tw-recall-before.txt` still say "tool not yet committed"; the tools are in `17661e0`. Known to LogDraft item 1; still uncorrected in the originals (the recut files carry the correct header).
- **Harm watch**: `evidence/harm/` (22 runs, `HARM_WATCH: PASS`, `failures=0`, `harm-watch-summary.txt`) exists in the worktree but is **untracked**. So does `fetch/RETENTION.json` and `fetch/RevRubricVRisk/`. The lesson does not cite the harm watch; a LOG entry that did would cite uncommitted bytes.
- **Worktree ≠ tip**: `git status --porcelain --untracked-files=all` → 46 untracked entries (harm evidence 22, RETENTION.json, RevRubricVRisk/, `w1/reports/RevDraftInstallers.md`, `w2/` in progress). The assignment's "worktree equals the tip" premise does not hold for these.

## Limits

- Not run: the gate, any gate copy, `measure-mutants.py --out`, the corpus-wide base-vs-merged diff (M7), any live host command. Re-ran read-only checkers: `measure.py`, `fresh-pins.py`, `tw-recall.py`, `anchor-durability.py`, `supersede-sweep.py`, `receipt-check.py`; a `/tmp` copy of `tools/mado-tripwire.py --scan`.
- The 429 cause and the 5th S094 tree digest are [UNK] from the lane.
- The S097 tag check used the existing `/tmp/ReopenS097-omarchy` clone; I did not fetch from the network.
- C1 and C2 are checked against their literal rules, not against their intent; the rules are documented as literal.

## Installs

none. No package, binary, or tool was installed or updated by this seat. Read-only tools already present: `git`, `python3`, `sha256sum`, `sed`, `grep`, `curl` (not used). No git write; no `jj` command.
