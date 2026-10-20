# ScoutOpenQueue — 31 open items collected; 11 are owned by wave-1 items, 6 tool-honesty items and all 4 freshness triggers have no wave-1 owner

Read-only. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin` at `e629f73` (branch `master`,
detached HEAD as expected); fleet `/home/vgpnk/Projects/shokunin` at `b332af20`. Observed
2026-10-20T19:46Z. No lane file was written except this report; no git/jj write in the lane;
no pacman/sudo/systemctl/hyprctl/jj command; no web fetch (see **Limits** for the one
`git ls-remote` I did run).

Baselines re-derived at `e629f73` (not copied from prose):

```text
python3 .ufo/waves/round-17/measure.py e629f73   -> c1 {criteria 28, lesson_cited 20, score 7.1429}
python3 -I .ufo/waves/round-19/tw-recall.py e629f73 -> incident 6, detected 6, tool_sha256 367be947…
python3 -I .ufo/waves/round-19/fresh-pins.py e629f73 -> denominator 13, current 13
```

## Open queue

Columns: item → source line → in the closure's R19-V1..V6? → plausible round-20
disposition. "Owner" is folded into the disposition (w1 owner observed from
`.ufo/waves/round-20/gen_w1.py` and `w1/assignments.json`).

| # | Item | Source line | R19-V1..V6 | Disposition |
|---|---|---|---|---|
| T1 | Rule B turns pure data (`BLOCK=frozenset(['pacman','-Q','hyprland'])`) into an ordinary `package_query` row, no lead marker | `corpus/lessons/round-19-verifier-spotcheck.md:66-84`; `SCORECARD.md:1230-1239` | **yes, V3** | **fix** — C1: `tw-precision.py` over the P/S/W/H/L suite; the P cases must also pass at `9c54c56`. Owner: 13 `Case*` seats + `TwRuleB`. |
| T2 | Lead vs observed never encoded in the verdict (E1 `evidence` key); lead rows stay in `findings`, exit 1 | `round-19-verifier-spotcheck.md:151`; `SCORECARD.md:1239-1255` | **yes, V3** | **fix** — schema change; `RevLeadExitSemantics` must decide consumers; check `ScoutRuleBMap`'s consumer list (`--frozen` compare, `--selftest` compare, `harm-watch`, `tw-recall`, `frozen-repin`). |
| T3 | Builtin/pure exemption needs binding+shadowing (E2/E3), cross-cell binding state | `round-19-verifier-spotcheck.md:151`; `corpus/lessons/round-19.md:89` (M14) | **yes, V3** | **fix** — `TwRuleB`; existing `r19-helperfn py-lead-*` expectations change, each edit reasoned (`RevSuitesLeadEdits`). |
| T4 | 78 non-write VCS rows: 74 `jj <sub> --help`, 4 `git --dry-run/-n` (docstring says help excepted, code falls through) | `corpus/lessons/round-19.md:120`; `SCORECARD.md:1208-1210` | **yes, V3** ("help/dry-run nonwrites") | **fix** — E4 in `TwVcsHelp`; `git commit -n` must stay a write (`--no-verify`); empirical backups `ScoutJjHelpEmpirical`/`ScoutGitDryEmpirical`. |
| T5 | Eval-surface VCS writes (the real `.jj` birth/merge/push loop) yield 0 `vcs_write` findings | `corpus/lessons/round-19.md:89` (M14 cell) | **no** (planned item 1 text only: `SCORECARD.md:1208-1210`) | **keep open** — no w1 seat owns the eval-side VCS path; either a W case covers it or the report states the miss as a limit. |
| T6 | `curl … | sh` unclassified | `corpus/lessons/round-19.md:89`; `SCORECARD.md:1210` | **no** | **keep open with reason** — needs a new class/policy; no seat; document as a limit. |
| T7 | pip pre-verb options unclassified (`uv run --with pip`) | `corpus/lessons/round-19.md:121`; `SCORECARD.md:1210` | **no** | **keep open with reason** — installer grammar is unowned this round; round-19 install record is already explicit. |
| T8 | `tw-recall.py` grades a verdict with no `findings` key as 0/6 with exit 0 (should be could-not-evaluate) | `corpus/lessons/round-19.md:153-154`; code `tw-recall.py:72-73,87` | **no** (adjacent V3; V3 does not name it) | **keep open, add a guard** — do not edit the pre-registered counter; `RecallSplit` (or the report's preflight) must exit could-not-evaluate when the key is absent, and C1's "6/6 unchanged" must cite the schema-intact run. |
| T9 | `tw-recall.py` credits any class on an incident line (M7: overfit by construction) | `corpus/lessons/round-19.md:22` | **no** | **keep** — report 6/6 **split** observed/lead beside it (`RecallSplit`); never cite class-correctness from the counter. |
| T10 | Round-17 hardening suite reads 32/33 under the pre-round tool after its one case edit | `corpus/lessons/round-19.md:117-118` | **no** | **report, no fix** — do not advertise "11 suites pass" for the pre-harm tool; state the 32/33. |
| T11 | Frozen baseline comparison keys vs a new `evidence` field | implicit in `SCORECARD.md:1253-1254` (guard: "re-pinned for round 20 if the schema moves") | **no** | **decide** — `ScoutFrozenSchema`; if re-pin, use `frozen-repin.py` and fix H8 first. |
| H1 | `harm-watch.sh` extracts the `### Counting command` block from the **worktree** SCORECARD, executes it with `bash -s`, and stamps `measured_commit=<REV>` even when bytes differ (NOTE only) | `corpus/lessons/round-19.md:112-113`; `w2/reports/SentinelToolSafety.md:32-46`; `w2/reports/ReviewHarmTool.md:17-60` | **yes, V5** ("harm-watch execution/provenance") | **fix** — `HarmWatch20`; but its item text (`gen_w1.py:95`) only asks to "flag every limit you fixed or kept", so L1 must specify fail-closed: skip **and** count a failure when the block's digest ≠ REV's. |
| H2 | `run_pinned` hashes the worktree file, then executes the **worktree path** (mid-run edit invalidates the receipt) | `w2/reports/ReviewHarmTool.md:99` | **no** (V5-adjacent) | **fix cheaply or keep open** — execute the hashed `/tmp` copy, or re-assert bytes after the run. |
| H3 | `measure-mutants.py --out` guard covers only the `--lane` worktree; a lab run against a clone overwrites the real lane receipt | `corpus/lessons/round-19.md:110-112`; `w2/reports/SentinelToolSafety.md:49-58`; `measure-mutants.py:505-524` | **no** | **keep open or 3-line fix** — resolve `out.parent` to its own toplevel and refuse; no w1 seat. |
| H4 | `supersede-sweep.py` says "committed bytes only" but reads its ledger (`supersessions.json`) from the worktree, which decides the verdict | `corpus/lessons/round-19.md:113-114`; `w2/reports/SentinelToolSafety.md:60-69`; `supersede-sweep.py:44` | **yes, V5** ("worktree-ledger") | **fix** — default `git show REV:.ufo/waves/round-19/supersessions.json`, print ledger source+sha; no w1 tool seat (only `RevHarmWatchLimits` reads it). |
| H5 | A non-object receipt line (`[1]`) crashes `anchor-durability.py` with `AttributeError` → exit 1, the code that means "row flagged" | `corpus/lessons/round-19.md:114`; `w2/reports/SentinelToolSafety.md:71-77`; `anchor-durability.py:186-191` | **yes, V5** ("anchor-alias checker limits") | **fix** — could-not-evaluate (exit 2), no traceback; no w1 seat. |
| H6 | A syntactically malformed receipt line is **counted and skipped** (`bad_receipt_lines`), never failing; a malformed second digest silently removes rotation evidence (false green). The lesson's "exits 1 on a malformed receipt line" is only true for the non-object branch | my reading, `anchor-durability.py:176-210,405-428` | **no** (lesson sentence contradicts the code) | **fix + correct the prose** — either fail (exit 2) on `bad > 0` or pin a threshold and say so; criterion 30's kind of count honesty applies to the lesson sentence itself. |
| H7 | `anchor-durability.py` passes a `/latest/` URL when **any** version token appears in the anchor prose ("not durable" instance S911) | `corpus/lessons/round-19.md:151-152`; `w2/reports/RerunAnchor.md:109-112`; `anchor-durability.py:256-264` (`pin_token` returns before the alias arm only if a pin is found) | **yes, V5** ("anchor-alias checker limits") | **keep open with reason** — no round-20 seat; QUALITY 27 must keep this as a checked limit, not a green. A fix needs a path-version rule (version must appear in the URL path or the credited digest must come from a fixed-version URL). |
| H8 | `frozen-repin.py` writes a README `RECEIPT …` line with `tool`, `tool_sha256`, `utc`, `argv` and **no** `measured_commit` | `corpus/lessons/round-19.md:114-115`; `frozen-repin.py:316` | **no** (`SCORECARD.md:1213-1216` planned item 3) | **fix cheaply if a round-20 frozen dir is cut**; else keep open with the round-19 re-cut receipts as the provenance. No seat. |
| H9 | "frozen pin-spelling normpath" | `SCORECARD.md:1215`; `frozen-repin.py:131` | **no** | **keep open, clarify** — no w2 report line names the defect; `ScoutFrozenSchema` should pin the exact shape before anyone edits. |
| H10 | Gate: a stale `.jj` with HEAD detached on a content-identical commit reads HELD (no ancestry check) | `corpus/lessons/round-19.md:137-142` | **no** | **keep open (low)** — no seat; do not claim the F6 rescue is complete. |
| H11 | Gate selftest showed two non-reproducible fixture-loss failures under concurrent seat runs; cause `[UNK]` | `SCORECARD.md:1180-1181` | **no** | **keep open** — HarmWatch20 must run serially, record isolation, and not attribute a loss to the gate. |
| H12 | `fetch-verify.py` CONFLICT check is global (exits 1 on the historical S094 tree URLs; reports digest-only bodies as missing) | `corpus/lessons/round-19.md:102-105` | **no** | **keep open, document** — never cite it as a per-row durability check. |
| F1 | S003's cited PROTOCOL sections moved **+15** lines and the fleet PROTOCOL blob changed since the pin | `corpus/lessons/round-19.md:158-159`; verified below | **no** | **fix cheaply** — append a dated pointer to the fleet tip (`PROTOCOL.md:343-374 + :375-424 @ b332af20`, sha256 `886e459b…`); keep the row revision-pinned to `31baf5c` (`b1d4f4c0…`, verified). No new fetch: host repo bytes. |
| F2 | omarchy is **9 tags past v3.8.4**; 8 rows anchor v3.8.4 (S085-S089, S093, S097) | `corpus/lessons/round-19.md:159`; verified below | **no** | **keep open with reason** — v3.8.4 anchors are durable revision-pinned; supersession needs new tag-pinned receipts (budget); add a dated recheck note naming the 9 tags. |
| F3 | elephant 2.21.0 → 2.22.1, uwsm 0.26.7 → 0.27.1, hyprland pkgrel −2 → −4, hyprtoolkit 0.5.4 → 0.6.0 | `SCORECARD.md:1211-1212`; installed dirs verified below | **no** | **keep open, or minimal fix** — `hyprland-config-plane.md:175`, `hyprctl-verification-layer.md:6,160`, `remaining-planes-census.md:244`, `waybar-walker-semantics.md:24` carry present-tense old pins; S090 covers walker/elephant only, so re-pointing hyprland/hyprtoolkit needs a new host row (S099+). No w1 seat. |
| F4 | Line-level pin rubric: 55 of 73 `2.17.0` lines have no same-line pointer; the counter is file-level | `corpus/lessons/round-19.md:88` (M13); `SCORECARD.md:1170-1172`; `fresh-pins.py:28,70-72` | **no** | **keep open with reason** — planned item 2 intent only; C2 this round is calibration, so no freshness movement may be implied. |
| F5 | Installed walker still 2.17.2 (pin holds) | `SCORECARD.md:1133`; verified below | n/a | **no action**; re-verify by bytes only (host pause). |
| A1 | C1's ≥21/29 miss stays a miss; before reads 20/28 = 7.1429 today | `round-19-verifier-spotcheck.md:149`; `SCORECARD.md:1269-1273` | **yes, V1** | **keep** — C2's 22/30 is registered fresh; no criterion may restate 24/27/28 (`RevCriterion29/30`). |
| A2 | S096 tally: "5/13 name S096" is snapshot-stale; tip = **8/13** any-line, **6/13** first-line; five S090-only files | `round-19-verifier-spotcheck.md:59-61`; `SCORECARD.md:1167-1169`; `corpus/lessons/round-19.md:108-109`; `LOG.md:1324` | **yes, V2** | **fix** — append-only correction (SCORECARD round-20 section + round-20 lesson + LOG entry; `LOG.md:1324` stays as the historical round-19 entry). `TallyCheck` + `RevR19V2Wording` + `ScoutR19Tallies`. |
| A3 | "155 transcripts" vs a **154**-file receipt | `round-19-verifier-spotcheck.md:125`; `corpus/lessons/round-19.md:123-124`; re-derived 154 | **yes, V4** | **fix** — `tally-check.py` registry entry with the derivation I ran (below). Keep "self-report, not detection" wording. |
| A4 | Fail-open isolation harness (setup failure let the payload run) + written-script scan blindness | `round-19-verifier-spotcheck.md:124`; `corpus/lessons/round-19.md:127-130` | **yes, V4** | **fix** — `IsolationHarness` (abort 125 before payload) + QUALITY 29 red on `inns-r19-shape.sh`; no live probe ever. |
| A5 | "ten old OM10 assertions" should be nine labeled occurrences / eight distinct; OM10A six + OM10B eight | `round-19-verifier-spotcheck.md:88`; `SCORECARD.md:1225` | **yes, V5** | **fix** — append-only correction at `SCORECARD.md:1225` + round-20 lesson; the fleet report is read-only. `RevR19V5Wording` + `TallyCheck`. |
| A6 | Worktree-ledger / harm-watch execution-provenance / anchor-alias limits must stay on the queue even where checks are green | `round-19-verifier-spotcheck.md:153` | **yes, V5** | **keep** — H1-H9 above are the concrete items; a green bounded check does not close them. |
| A7 | Misroot lesson, absolute lane paths at every seat boundary, dead seats uncredited, provider recovery ≠ evidence | `round-19-verifier-spotcheck.md:154`; `corpus/lessons/round-19.md:23-24,147-150` | **yes, V6** | **process** — this report was written with absolute paths; `RevR19V6Seats` audits this wave's item texts. |
| A8 | F17 jj colocation | `corpus/lessons/round-19.md:155-157` | **no** (operator) | **keep open** — operator-owned; no lane action. |
| A9 | 10 w1 reviewers still routed to m_zfl | `corpus/lessons/round-19.md:147-150` | **no** (orchestrator) | **keep open** — routing is not L1's; wave-2 item texts already appear on m_zfl (this wave). |
| M1 | C1 is not yet measurable: `precision/` absent and `tw-precision.py` untracked at `e629f73` | `SCORECARD.md:1239-1255` | n/a (C1 machinery) | **dependency** — the suite must land at a commit that lands no tool change (`--suite-rev` pin), then the counter runs; `CorpusDiff` supplies the no-loss proof. |
| M2 | Round-20 fetch hygiene: no `.gitignore` and no `RETENTION.json` under `.ufo/waves/round-20/fetch/`; bodies untracked and **not ignored**; `SrcUnshare` had no `receipts.jsonl` at 19:46Z | `corpus/lessons/round-19.md:21` (M6); lane fetch rule | **no** | **fix before landing** — M6's rule is round-19-scoped; add class patterns (`*.html`, `*.crate`, `*.json` except `RETENTION.json`) + `RETENTION.json`, and require the receipt line per body. Seats are mid-flight (mtimes 16:43-16:45). |
| M3 | Frozen replay re-pin is a C1 guard; schema may gain `evidence` | `SCORECARD.md:1253-1254` | n/a | **decide** — T11. |

## Facts re-derived here (with the commands)

- **154, not 155** — the committed scan receipt's own JSON:

  ```text
  python3 -c "import json;l=[x for x in open('/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt') if x.startswith('{')][0];d=json.loads(l);print(len(d['files']))"
  -> 154   (distinct paths also 154)
  ```

  Its header also says `measured_commit=0fa41252…`, not the final tip — a provenance nuance for the
  round-20 correction, not a new defect. [OBS]

- **S003 moved exactly +15 and the blob changed.** Fleet `31baf5c:PROTOCOL.md` sha256
  `b1d4f4c0940522981a6ace84d8528acb0bad470ebaa69faeeb0dbd017b330c20` (matches S003's anchor
  `b1d4f4c094052298…`), `## Evidence standard` at 328, `## Gate standard` at 360. At fleet
  `b332af20` the same headings are at **343** and **375**; blob sha256
  `886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a`; last commit touching the
  file `7c5b34f` (2026-10-19). The row's `recheck: on-change` trigger has therefore fired: the
  row is still a durable revision-pinned anchor, but its coordinates describe a superseded fleet
  revision. [OBS]

- **The 9 omarchy tags are real** (`git ls-remote --tags https://github.com/basecamp/omarchy`, 73
  tags total): after `v3.8.4` come `v4.0.0`, `v4.0.0-beta3`, `v4.0.1`, `v4.0.2`, `v4.0.3`,
  `v4.0.4`, `v4.0.5`, `v4.0.6`, `v4.5.0-rc1` — nine. [OBS]

- **Installed versions, read as directory names under `/var/lib/pacman/local/` (no pacman
  invocation):** `elephant-2.22.1-1` (+12 elephant plugins at 2.22.1-1), `uwsm-0.27.1-1`,
  `hyprland-0.56.2-4`, `hyprtoolkit-0.6.0-1`, `walker-2.17.2-1`. The SCORECARD's "same-morning
  moves" already match disk; the debt is in lane prose, not host state. [OBS]

- **`anchor-durability.py` receipt-line behavior is two-branched, not one.** JSON syntax errors are
  counted in `bad_receipt_lines` and skipped (`:186-188`), execution continues, exit is decided
  only by `flagged` (`:427-431`); a JSON value that parses but is not an object raises
  `AttributeError` at `rec.get(...)` and the interpreter exits 1 with a traceback — the code the
  lesson attributes to "row flagged" (`SentinelToolSafety.md:71-77`). The lesson sentence
  (`round-19.md:114`) is therefore right only for the non-object branch, and the silent-skip
  branch is the more dangerous one (it can erase a second digest that would have flagged
  rotation). [OBS] + [INFERENCE] on the false-green direction (no receipt pair was constructed).

- **`tw-recall.py` malformed verdict path confirmed in source:** `verdict.get("findings", [])`
  (`tw-recall.py:73`) yields an empty hit set, `det=0`, `score=0.0`, `return 0` (`:87`). Its
  could-not-evaluate paths only cover `git show` failure, digest mismatch, scan rc ∉ {0,1}, and
  fewer than two stdout lines (`:38-48,58-72`). [OBS]

## Wave-1 ownership gaps

`gen_w1.py` has **no item** for: freshness (S003, omarchy tags, elephant/uwsm/hyprland/
hyprtoolkit — the only hits are context text and the case fixtures' `hyprland` argv), supersede-sweep
ledger, anchor-durability exit-code/receipt handling, `measure-mutants --out`, frozen-repin's
receipt field, or round-20 fetch hygiene. Those are H3-H9, F1-F3, M2 above. Conversely,
`RevHarmWatchLimits` and `RevSkillTripwireText` review but do not fix; `HarmWatch20` may keep the
SCORECARD block unless L1 says otherwise (its text asks only to *flag* limits).

## Limits

- I did not run the gate, any selftest/regression, the harm watch, or the classifier; I did not
  scan this round's transcripts. Only the three registered counters above, `git show`/`ls-tree`/
  `ls-remote`, `grep`, and Python-over-committed-bytes counts ran.
- One network read: `git ls-remote --tags https://github.com/basecamp/omarchy` (read-only, no body
  fetched). I wrote no fetch receipt because no body was saved; if L1 wants this count cited as a
  source, it needs a receipted `curl` of a tag-pinned URL instead.
- `[UNK]` H9 ("pin-spelling normpath"): no w2 report line names the defect; `frozen-repin.py:131`
  is the only `normpath` in the file, but the failure shape is unproven.
- `[UNK]` H11 fixture-loss cause; `[UNK]` whether `HarmWatch20` will gate the SCORECARD block
  (item text is silent).
- F3's stale-line list is a grep sample, not exhaustive (grader: present-tense pin without a
  same-line `S###` pointer). Only `corpus/` Markdown was searched; `.ufo/waves/**` prose was not
  treated as claim text.
- I did not verify the round-20 case suite (dirs `CaseLeadsInvisible`, `CasePureCrossCell` only at
  19:46Z); family coverage and red counts are the counter's job once `precision/` lands.
- Fetch dirs were mid-flight when observed; M2 is a state observation at 19:46Z, not a verdict on
  any seat.

## Installs

none — no tool installed, upgraded, or queried (host pause respected; no pacman/uv/npx).
