# ScribeReportDraft — round 18 wave 2 (scribe, leaf)

Seat: `MadoR18.ScribeReportDraft`. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Revisions named by hash: receipts `abfbf35b1ed4d4a1eb294d525ef286be30f3886f`, integration `4c103b55b1ea5c3c555884afe3eb69b5189701b7`, baseline `d9a5a18`, pre-registration `d3a0000`.

## Behavior

Drafted `.ufo/waves/round-18/drafts/ScribeReportDraft.md` from `ReportSkeleton.md`. Every filled value was read from committed receipts (cited by path) or from a read-only recomputation over committed bytes (listed below). Values not committed remain `<L1>`: attempt number, admission note, stale-lane, tool installs, jj notes, seat counts, misroot sweep, separability, freshness, frontier, SHONEN boxes, trend verdicts, L0 lines, census end. No value was invented. Verdicts are L1's.

Measured results as drafted: C1 15/23 = 6.5217 → 18/26 = 6.9231; C2 4/6 → 6/6 (instrument 6.6667 → 10.0); C3 `--frozen` match exit 0, tampered exit 2, `d9a5a18` tool exit 2, frozen selftest 17/17; gate selftest 389/389; regression 10/10 KILLED; harm watch PASS; sources 71 → 95; mined 56 → 80.

## Gates

- Draft contains no `TODO`-style placeholder other than `<L1>`. Count of `<L1>` tokens: see final grep in commands below.
- Every filled claim has a `.ufo/waves/round-18/evidence/…`, `…/fetch/<Seat>/receipts.jsonl`, `…/frozen/…`, `…/w1/…`, or `corpus/…` path at a named revision.
- No value copied from a seat report as if it were a receipt. `w1/reports/RevSeparability18.md` is cited only as a seat claim.

## Touched surfaces

- Written: `.ufo/waves/round-18/drafts/ScribeReportDraft.md` (draft, created) and `.ufo/waves/round-18/w2/reports/ScribeReportDraft.md` (this report).
- Scratch only (outside lane, ephemeral): `/tmp/scribe-sources.md`, `/tmp/scribe/*` (SOURCES copy, receipt TSV, check scripts, derived gate copy `derived-c9.sh`).
- Not touched: any lane file, any git or jj write, any gate, tool, corpus or receipt file, `/var/log` (read only), `~/.omp` (not opened).

## Commands run (all read-only)

- `git show <rev>:<path>`, `git show --stat`, `git ls-tree -r --name-only`, `git ls-files`, `git log`, `git rev-parse`, `git diff --stat|--name-only`, `git merge-base --is-ancestor`, `git check-ignore`, `git grep -l`, `git rev-list`, `git diff d9a5a18 4c103b5 -- corpus/SOURCES.md | grep`.
- `git show 4c103b5:tools/mado-verify.sh | sha256sum` → `c9fb0cef…`; `git show d9a5a18:tools/mado-verify.sh | sha256sum` → `fba82a66…`; `f52f43f8…:.ufo/waves/round-17/measure.py | sha256sum` → `a280b3ab…`; `4c103b5:tools/mado-tripwire.py | sha256sum` → `c87a31ef…`; `4c103b5:.ufo/waves/round-17/measure.py | sha256sum` = `d9a5a18` value `de4c422b…`.
- `grep -cE '^[0-9]+\. .*lessons/'` and `grep -cE '^[0-9]+\. '` over `QUALITY.md` at `d9a5a18` (15/23) and `4c103b5` (18/26).
- Python over `git show` output: parsed 301 receipt lines (all `mado-fetch-receipt-v1`, 0 `BAD_JSON`, 0 `BAD_SCHEMA`); 5 non-200 receipts (all 404, none cited by a SOURCES row); row-to-receipt join for S072–S095 (S072–S089, S092–S094 receipted; S090, S091, S095 host rows).
- Python over on-disk bodies of the 301 receipts: `sha256` and `bytes` match for 301/301 (bodies are untracked, see finding F9).
- Route-note section check (python over `git show 4c103b5:corpus/knowledge/{walker,theme}-route-r18.md`): `surface:` at lines 5–6 of each; four sections, each ≥3 non-blank lines; `[UNK]` inside the last section in both.
- Gate derivation: `sed` excision of `MADO-R7-REGRESSION-BLOCK`, `MADO-R7-SELFTEST-BLOCK`, `MADO-R8-BLOCK` on the committed gate (`4c103b5`) → 2460 lines, 121533 bytes, sha256 `20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744` = `PIN_MADO`.
- `sed -n` on `/var/log/pacman.log` at lines 1943, 2416, 2422, 2423, 2429, 2929, 3062, 3095, 3123 (file read only); `grep -nE` for `[PACMAN] Running` lines after 2400.
- `git show abfbf35:…/harm-measure-u.txt | grep` → U-route `count 7`, `score 10.0`.

No package-manager command, no sudo, no systemctl, no journal, no `omarchy*`, no REA or browser tool, no `mado-verify.sh` run (live, default or `--no-live`), no fetch, no install.

## Findings

Severity: H = would change a verdict or an admission reading; M = receipt or provenance defect that a non-author would hit; L = disclosure.

- **F1 (H, R17-V1 `partial`).** `tripwire-pacmanlog-join.txt` was not re-cut. Line 1 is a `#` comment (`# Round-18 C1 re-derivation …`), not `RECEIPT … tool_sha256= measured_commit=`. The body is an author-assembled join (awk command, then hand-written result lines), not tool output. The five scan receipts (`tripwire-r13..r16`, `tripwire-anchor-r15`) do carry the `RECEIPT` line 1 (`tool_sha256=c87a31ef…`, `measured_commit=4c103b5…`). The round-18 lesson M1 still says the join is hand-authored. Its recorded sha `be361650…` (in `recut-summary.json`) matches the file bytes.
- **F2 (H, host window).** The C1 join's window is `^\[2026-10-(19T2|20T0[0-6])` in local `-0300` time. It excludes 13 `[PACMAN] Running` transactions dated `2026-10-20T07:45:36-0300` through `09:39:21-0300` (`/var/log/pacman.log:2440, 2448, 2454, 2461, 2462, 3064, 3085, 3091, 3092, 3125, 3126, 3132, 3152`), including `pacman -Syu --needed --noconfirm …` at `2462` (`09:15:30`), `pacman -U` of elephant at `3092`, and `-Rns` of btrbk at `3132`. The transcript scan does not cover round-17 or round-18 seats (F4), so attribution to a lane seat is `[UNK]`. The skeleton's "round window" cell cannot be filled as "clean". The draft reports the list and leaves attribution as `<L1>`.
- **F3 (M, R17-V3 `partial`; gate conformance).** S084 (`docs.rs/xdg/latest/…/struct.BaseDirectories.html`, saved HTML, mined tier A) is an unversioned `latest` HTML page. The round-18 gate in `corpus/lessons/round-18.md` (§ Gate, lines ~27–32) names `docs.rs xdg "latest"` among candidates considered and rejects "HTML pages as sole support" and "unversioned docs sites as version-specific support". The walker note cites `XD:356-358`, `XD:302`, `XD:306` for the XDG search order (`corpus/knowledge/walker-route-r18.md:78-79, 204, 292`), and the row is admitted and receipted (`fetch/NoteWalker/receipts.jsonl`). This is a gate-conformance question for L1: either the row is unrowed, or the gate text is amended and the exception is stated. The `RevengeTarballRepro` directory holds two different `docs.rs/xdg` HTML bodies (`latest-a` and `latest-b`, 105537 B each; `pinned` 105205 B; `2.5.0` 92002 B), which shows the per-fetch-token problem the gate names. No receipt covers those artifacts.
- **F4 (M, process).** No committed transcript scan covers round-17 or round-18 seats. The `tripwire-r13..r16` receipts list `MadoR13.*` through `MadoR16.*` transcripts only (second line of each receipt). The skeleton's "C3 over round-18 transcripts" cell has no receipt. The `CONDUCT_RESULT` cell is `<L1>`.
- **F5 (M, R17-V3 `partial`; untracked receipts).** Four receipt lines exist on disk but are untracked and absent from both `abfbf35` and `4c103b5`: `fetch/ReopenS072/receipts.jsonl` (2 lines) and `fetch/MadoR18.ReopenS081/receipts.jsonl` (2 lines), with their bodies (`master-README.md`, `walker-v2.17.2-README.md`, `comm.go.body`, `comm.go.at-commit.body`). `fetch/MadoR18.RevengeTarballRepro/` holds tarballs (`s079-walker-v2.17.2-a.tar.gz`, `-b`, 165438 B each) and docs.rs HTML (`s084-*`) with no receipt file at all. The committed-receipt join does not see these. If S081 or S072 reopen evidence is cited, L1 must commit the receipts.
- **F6 (M, reproducibility).** Fetch bodies are not tracked: `git ls-files .ufo/waves/round-18/fetch` returns the 21 `receipts.jsonl` files only, and `git ls-tree` at `4c103b5` shows the same. `fetch-verify.py` therefore cannot pass from a clean clone of `abfbf35`. My on-disk re-hash is 301/301 `sha256`+`bytes` match. A non-author needs the untracked bodies or a re-fetch.
- **F7 (M, provenance of the regression receipt).** `regression-recut.txt` §1 names the gate as `2bdf5e8a…` (the bytes at the time of the run). The committed gate at `4c103b5` and `abfbf35` is `c9fb0cef…`. The gate changed after §1, and §4 does not name the gate sha. The scribe re-derivation shows the derived target (the file with the three marker blocks excised) is byte-identical in both: `20714096…` in §1, §4 and `PIN_MADO`. So the 10/10 result holds for the committed gate, but the receipt should say so. Gate selftest `389/389` is at `c9fb0cef` (`gate-selftest.txt`, `harm-gate-selftest.txt`).
- **F8 (L, reproducibility).** The red-before receipt `gate-rc-redbefore.txt` ran `/tmp/mado-r18-gaterc.lab.sh` (scratch, not committed) with a synthetic root and PATH stubs. The lab script cannot be re-run from committed bytes. The table is a transcription.
- **F9 (L, census).** `evidence/census-end.txt` is absent at `abfbf35` and `4c103b5`. The only end-state receipt is `harm-census-validate.txt` (`sources-census.sh validate`, exit 0), which is a different command from the declared start count.
- **F10 (L, commit granularity).** All wave-1 changes are one commit (`4c103b5`, 252 files, +36437/−19). The skeleton's per-change commit rows cannot be filled from commits; each row cites the commit message and file set.
- **F11 (L, skeleton).** The skeleton's tier counts omit tier B (1 row, unchanged). The drafted line includes it.
- **F12 (L, measurement).** The instrument score is `count × 10/6` (4/6 → 6.6667; 6/6 → 10.0; 18/26 → 6.9231); the skeleton's target phrasing "6/6" is consistent with it. The `S090`, `S091`, `S095` host rows are credited by the instrument for P3 and P5 without a fetch receipt. The rubric is documentary, not behavioral.

## Checked and agreed (no defect)

- C1 15/23 and 18/26 reproduced from `4c103b5:corpus/QUALITY.md` by the declared `grep -cE` pair. `measure-after.json.txt` agrees.
- C2 6/6: `measure-after.json.txt` P3 and P5 entries cite the two route notes with `surface:` lines at lines 5–6 and the expected S-rows. `measure.py` sha `de4c422b…` is unchanged between `d9a5a18` and `4c103b5` (instrument unchanged in round).
- C3: frozen receipts' tool sha `c87a31ef…` matches `4c103b5:tools/mado-tripwire.py`. `frozen/provenance.json` names `962919ce…` as the round-17 tool receipt sha. Frozen input shas in `tripwire-frozen-match.txt` match the file hashes in the committed frozen inputs.
- Tripwire anchor: `tripwire-anchor-r15.txt` contains the finding tuple `line 54`, `call_38165`, `sudo` and `pacman:-S` (two entries). Its `RECEIPT` line 1 carries `measured_commit=4c103b5…`.
- Join claims: `/var/log/pacman.log` lines 2416 (`man-pages`, unmatched), 2422, 2423, 2429 (`libinput libinput-tools`, `04:25:16-0300`) match the join file's rows.
- S090 log lines: `pacman.log:1943` walker `2.16.2-1 -> 2.17.0-1` (`2026-10-11`); `:2929` walker `2.17.0-1 -> 2.17.2-1` (`09:16:46-0300`); `:3062` and `:3123` `walker-restart.hook`; `:3095` elephant `2.21.0-1 -> 2.22.1-1` (`09:31:03-0300`). All match the row text.
- SOURCES: no existing row changed; 24 rows added (S072–S095). Status counts 56/8/7 → 80/8/7 (mined/queued/rejected). Tier A 64 → 88.
- Route sections: four required sections present in both notes; `[UNK]` inside the last section in both.
- Mutant receipt: `measure-mutants.json` `summary` 6 mutants, 6 bites, `no_bite []`, `expectations_met 6`, `baselines_agree true`; harness sha `075815bd…` (`.ufo/waves/round-18/measure-mutants.py` at `4c103b5`).
- R17-V2: `corpus/lessons/round-17.md:198-199` (`4c103b5`) names `7a98720e…` (the `f71ccbe` tool) and `962919ce…` (landed) with labels.
- Harm watch: `harm-watch-summary.txt` 10 commands, all `OK exit=0`; `HARM_WATCH: PASS`; `rev=4c103b55…`.

## Out of scope (not done by this seat)

- Verdicts, admission, SHONEN boxes, trend verdicts, separability, freshness, frontier, L0 questions, stale-lane, tool installs, jj notes, seat counts, misroot sweep: all `<L1>`.
- No re-run of `fetch-verify.py` (a lane tool; the item asked for value-filling). No re-run of `measure.py`, tripwire, gate, or harm watch.

## Artifact paths

- Draft: `.ufo/waves/round-18/drafts/ScribeReportDraft.md`
- Report: `.ufo/waves/round-18/w2/reports/ScribeReportDraft.md`
- Committed inputs used: `.ufo/waves/round-18/evidence/{measure-before.json.txt, measure-after.json.txt, tripwire-frozen-*.txt, tripwire-r13..r16.txt, tripwire-anchor-r15.txt, tripwire-pacmanlog-join.txt, recut-summary.json, measure-mutants.json, regression-recut.txt, gate-rc-redbefore.txt, gate-selftest.txt, harm-*.txt, census-start.txt}`, `.ufo/waves/round-18/fetch/*/receipts.jsonl`, `.ufo/waves/round-18/frozen/provenance.json`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/knowledge/{walker,theme}-route-r18.md`, `corpus/lessons/round-18.md`, `corpus/lessons/round-17.md`, `SKILL.md` (all at `4c103b5`, ancestor of `abfbf35`).

## Install record

None. No tool was installed or updated by this seat.
