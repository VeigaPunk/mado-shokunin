# round-97 verifier spot-check — mado

author: hyaku closure (non-author integrator, @m_zfl)

- Date: 2026-11-07. Lane repo `mado-shokunin`, branch `master`; round base
  `e6152b589c2c6a28426c28263c4bcc3c46398be4` → round tip `15b6280483fe8fab52acbce689c883c056b34e7d`.
- Report: `.ufo/reports/round-97/mado.md` (fleet repo, commits
  `f5f6fa345f7047035550d23683de169617f12158` and `26a96ca0cd49c24a8903a3819e3762d091d3c585`, both
  `mado-shokunin <mado@shokunin.local>`).
- This file is my only lane write; I did not author, improve or edit any lane artifact, and I did not write
  `[x]` into `SHONEN.md`. The lane's gates were not executed as closure evidence (§Gate standard: the
  integrator verifies committed evidence). The one direct execution below is a read-only capability spot
  check of the delivered tool against `/usr/bin/gio` on two paths — a deliverable, not a gate.

## 1. Step-1 conformance

| item | observed | verdict |
|---|---|---|
| report committed by the lane identity | `git log --format='%an %H' -- .ufo/reports/round-97/mado.md` → `mado-shokunin 26a96ca0` and `mado-shokunin f5f6fa34`; both are on `origin/master` (`git branch -r --contains`) and pushed | pass |
| report lands last | **defect.** `f5f6fa34` (committer 2026-11-07T16:18:23-03:00) cites lane tip `4bfe2e43` (committer 16:17:06). Three lane commits landed after it — `992037c6` (16:19:05), `d7c186bc` (16:19:34), `15b62804` (16:19:47) — and `26a96ca0` (committer 16:20:00) then rewrote the filed bytes (header tip line, an inserted misroot bullet, three table rows) instead of appending an erratum naming the superseded text | defect |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` → 1; four `^- [` lines = the four boxes of `SHONEN.md`, all `[~]` with pointers; no `[x]` | pass |
| cited commits exist and are ancestors of `master` | 12 hashes — `78e9ccdd`, `a1408d47`, `dc0daad9`, `4541d94b`, `65ff5591`, `1b9bad52`, `e957932d`, `d421fd77`, `4bfe2e43`, `992037c6`, `d7c186bc`, `15b62804`: `git cat-file -t` = commit and `git merge-base --is-ancestor <h> refs/heads/master` rc 0 each; `git rev-list --count e6152b58..15b62804` = 12, so the Landed-changes table names every round commit | pass |
| lane repo clean and pushed | `jj-lane.sh state` → `branch=master local=15b62804 remote=15b62804 ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty; `git ls-remote origin refs/heads/master` = `15b62804` | pass |
| prompt carries the template contract | `.ufo/prompts/mado-round-97.md` normalizes to contain the rendered `templates/round-prompt.md` verbatim (`{{LANE}}`=mado, `{{ROUND}}`=97, `{{FLEET_ROOT}}`, axes `coverage + operability (desktop and compositor craft)`, working dir `…/mado-shokunin`); all five child-lane items present (report path §4, `SHONEN` heading §4, commit-hash citation §4, commit-then-report §5, write scope §5 + addendum line 448); §6 hyaku addendum present; prompt committed by the lane identity `cf80f01b` at 13:32:27, before the 13:33:13 launch | pass |
| L2 floor and round shape | `w1-dispatch.json` counts `spawn 14`, `taskCall.tasks` 14, one batched call; `w1b-dispatch.json` `spawn 10`, 10 tasks; attack 5/14 and 5/10 (≥25 %); no `model` key in either spec; `w1/swarm-registry.json` members = 6 executor + 2 mutation-tester + 2 reviewer + 1 critic + 1 scout + 1 connector + 1 scribe = 14. **Defect:** the report and SCORECARD say "3 executors" for w1 | defect |
| marker vs report | real report: named commits, receipts, every required section, checkable hash citations | report, not a marker |

Dispatch/complete digest carried into the closure notes (`.ufo/watchdog.log`, mutable, copied):

```
2026-11-07T13:33:13-03:00 launch mado round=97 pgid=596619 driver=hyaku-inline attempt=1
2026-11-07T16:20:59-03:00 complete mado round=97; hyaku-inline attempt=1
```

Conformance defects (status-neutral; routed in §6): the report was filed before the final three lane commits
and rewritten in place at `26a96ca0`; the w1 role census says 3 executors where the registry holds 6; the
"dead seats … settled with no report" line is contradicted by three committed seat reports; the Notes' claim
that the round-96 spot-check's D1–D13 are closed omits D7 and D9, neither of which is closed; S523's
used-by/recheck cells changed without the old→new lesson log.

## 2. Claim re-checks

Legend: **re-measured** = I ran the count myself over committed bytes; **evidence-verified** = I read the
committed receipt/frozen evidence (self-test tally, frozen-run verdict, revision measured).

### C1 — coverage, new surface (capability): the content type GIO 2.90.1 reports for a path

| check (command) | observed | matches report |
|---|---|---|
| `git cat-file -e e6152b58:tools/mado-filetype.py` | absent (rc 128); `git ls-tree --name-only e6152b58 tools/` lists 33 tools, none answering a path's content type; `git grep -il 'content.type' e6152b58 -- tools/` → `mado-mimeglob.py`, `mado-mimesniff.py`, `mado-mimetext.py`, whose docstrings answer name+bytes, not a path | yes (re-measured) |
| `git show 4541d94b:tools/mado-filetype.py \| sha256sum` | `da6af7a0789265187f6b2c2462bf5104a7c0b780baed3235300f89978a44d2d8` = the freeze pin; tip identical | yes (re-measured) |
| `git show 4541d94b:quality/counters/c1-r97-filetype.py \| sha256sum` | `745a341e8a2aaefc7283d1ad4090ebde01d631d118f788ddd1dcc7b5195ba9e0`; tip identical | yes (re-measured) |
| frozen controls | cases `157` over `15` classes (`dir chr blk fifo sock zero empty sym brok nofollow follow certain uncertain fast readerr`); mutants `101` counted + 11 not-observable + 8 equivalents = 120 probes, `anchor_tool_sha256` = `da6af7a0…8a44d2d8`; host labels 6194 records + 1 summary (`errors: 0`, `paths: 6194`); host list 6194 lines | yes (re-measured) |
| `receipts/c1-measured-r97.txt` | `MADO_FILETYPE_COUNT: TARGET_MET … rev=4541d94b … cases=157 correct=157 classes=15/15 … mutants=101 killed=101 …`; `selftest rc=0 checks=40 failed=0 fail_lines=0`; `host=6194/6194 host_paths=6194 host_mismatches=0 host_errors=0 host_drift=0`; `fresh_seed=4c1d3a48329c2167 fresh=140/140`; `control_nameonly=39/157 control_naive=67/157`; memoriser `fresh=0/140`; forgery `forgery_audit_denials=3 rejected=True`; `audit_denials=0` | yes (evidence-verified) |
| capability spot check (my own, read-only) | `python3 -I tools/mado-filetype.py /etc/passwd` → `MADO_FILETYPE: text/plain attr=full`; `--fast` → `application/octet-stream`; `/usr/bin/gio info -a standard::content-type /etc/passwd` → `text/plain`, `-a standard::fast-content-type` → `application/octet-stream`; `/etc` → `inode/directory` on both | yes (re-measured; deliverable, not a gate) |
| separability and tip stability | `receipts/c1-at-c2-r97.txt` → `TARGET_MET … rev=65ff5591 …`; `git diff --stat 65ff5591 15b62804 -- tools/mado-filetype.py quality/counters/c1-r97-filetype.py quality/counters/c1-r96-magictext.py quality/counters/c2-r96-selftest-kills.py quality/counters/c2-r97-counter-selftest.py` prints nothing | yes (evidence-verified + re-measured) |
| index, entry, SOURCES | README index rows 117 → 118 (`grep -c '^| \`knowledge/'`); SOURCES 460 → 462 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`); S526/S527 `mined`, used-by `corpus/knowledge/gio-content-type-file-r97.md`; the entry frontmatter opens `source:` (S522/S526/S527), `verified-at:`, `recheck:` | yes (re-measured) |

Before → after confirmed: **0 scored paths (no tool; the r94–r96 tools answer inputs, not paths) → 157/157
frozen cases, 15/15 classes, 101/101 counted mutants, 140/140 fresh at a measured seed, 6194/6194 host
labels, `checks=40 failed=0`**. Verdict: **coverage improved** (capability demonstrated:
`tools/mado-filetype.py`, first-working round 97).

### C2 — operability: the two round-96 counters gain the Gate standard's self-invocation mode

| check (command) | observed | matches report |
|---|---|---|
| base has no own `--selftest` | `git show e6152b58:quality/counters/c1-r96-magictext.py \| grep -c -- '--selftest'` → 3 (all references to other tools' modes); the c2 counter → 4 (same); neither parses its own flag | yes (re-measured) |
| tip adds the mode | `grep -c -- '--selftest'` → 5 / 6; each file carries `# Contract-4 self-invocation …` and `if "--selftest" in sys.argv[1:]` | yes (re-measured) |
| production bytes unchanged | strip from the marker line to EOF and append `if __name__ == "__main__":` + `    sys.exit(main())` → `diff -q` against the base file is identical for both counters | yes (re-measured) |
| 10 stable ids each | `_ST_IDS` = `st-fixture-dir`, `st-tool-pin`, `st-gate-target-met`, `st-setup-missing-input`, `st-setup-wrong-pin`, `st-setup-wrong-rev`, `st-target-missed-case`, `st-target-missed-mutant`, `st-result-line-format`, `st-scratch-clean` (10 per counter) | yes (re-measured) |
| registry rows close | `git show e6152b58:SKILL.md \| grep -c 'tools/mado-mimetext.py'` → 1; `…c1-r96-magictext.py` → 0; `…c2-r96-selftest-kills.py` → 0; at `65ff5591` → 2/1/1 (the receipt's table-row-pair count `base=1 rev=2` + `0→1` + `0→1`; `registry=1->3`) | yes (re-measured) |
| `receipts/c2-measured-r97.txt` | `selftest … rc=0 checks=10 failed=0` ×2; `negative_ids=18/18`; `broken_modes=6/6` (3/3 each); `base-control … rc=2 green=False` ×2; `stub_uncredited=18/18`; `always_ok_flagged=0`; `registry=1->3`; `ledger population=191 ledger_rows=191 uncovered=0`; `MADO_COUNTER_SELFTEST_COUNT: TARGET_MET … rev=65ff5591 … counter_pin=ok,ok …` | yes (evidence-verified) |
| instrument pins | `c2-r97-counter-selftest.py` sha `abb17a019141c57635f1c9771ad449a4348dfdc75a0bb57af3776075fe06b879` at `65ff5591` and the tip; the two counters `4f678384…aaa64d` / `54143b8a…002217b` at `65ff5591` | yes (re-measured) |
| separability | `receipts/c2-at-c1-r97.txt` → `SETUP_ERROR … SKILL.md sha256 != --expect-registry-sha256` at `4541d94b` | yes (evidence-verified) |
| panel corrections disclosed | `receipts/panel-correction-r97.txt` records three corrections before/after scoring, keeps run 1 as `c2-run1-r97.txt`, and the frozen panel sha `87ba2f41…` is the one the counter pins | yes (evidence-verified) |

Before → after confirmed: **both counters refuse `--selftest` (argparse rc 2, no result line; receipt
`base-control rc=2`) and the registry holds 1 of 3 instrument rows → `selftest_green=2/2 checks=10,10`,
`negative_ids=18/18`, `broken_modes=6/6`, `stub_uncredited=18/18`, `registry=1->3`, `ledger_members=2/2`**.
Verdict: **operability improved**.

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | **improved** | C1: a surface the coverage map did not hold (the path-level caller) enters core with an admitted entry, index 117 → 118, S526/S527 tier A, and a capability row demonstrated at 157/157 + 6194/6194 + 101/101 |
| operability | **improved** | C2: both round-96 counters gain 10-check self-invocation modes with stable ids, production bytes byte-identical, and the registry closes 1 → 3 instrument rows under a scoring counter |
| depth | unchanged | no separate depth claim; the entry's sections are source-per-line, but the round's declared axes are coverage and operability |
| freshness | unchanged | no entry-level re-verification claimed; the round-96 entry's stale cells are corrected (the quality trend's evidence), not a freshness claim |
| calibration | unchanged | claims and SCORECARD rows match the receipts; the D1–D13 "closed" overstatement and the recurring role census are record defects, not score moves |
| adjacency | unchanged | R97MConnector swept all 20 sibling `PROVINCE.md`s; no sibling claims GIO's `standard::content-type` or `gio info`; `update-mime-database` / `~/.local/share/mime` stay operator-owned |

## 4. Discernment spot-check (LEARNING.md, "checked from outside")

Re-opened live, 2026-11-07, from this session:

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S526 — GLib 2.90.1 `gcontenttype-fdo.c` (new row, admit) | admit | `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gcontenttype-fdo.c` HTTP 200, 32741 B, sha256 `8a5b4f475947a9de2e0ca34e60b0dc31f5c56a2d7e0a9fe8cf84002aca8a2d7c` = the row's pin; line 61 is exactly `size = xdg_mime_get_max_buffer_extents ();`; the quote is 7 words | **agree** | anchor, digest, size and located quote reproduce; the scope (sniff length + Unix mapping) is what the file holds |
| S527 — installed `gio(1)` manual (new row, admit) | admit | `/usr/share/man/man1/gio.1.gz`: container 4961 B, `gzip -dc \| wc -c` → 18793, `wc -l` → 781, sha256 `84b3cdad868feecd69f113b789d7009113e16531b67d750cd0e424ba2bcb8bc5`; line 195 is `\fB\-a\fP, \fB\-\-attributes=<ATTRIBUTES>\fP`; `pacman -Qo` = glib2 2.90.1-1 | **agree** | every cell reproduces; the `file://` locator is shaped like the other installed pages (no HTTP status claimed) |
| `gio/gcontenttype.c` (reject as a separate row) | reject | `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gcontenttype.c` HTTP 200, 10399 B, sha256 `fb9c68782af7c266f22551ef11e328f9d2491c262efd3de7336dbbfc36554664`; lines 291-295 are `g_content_type_from_mime_type` returning `g_content_type_from_mime_type_impl (mime_type)` | **agree** | the file holds the public wrapper only; folding the locator into S526 is the right call |
| contract sentence "a symlink loop is a stat error" (reject as a model fact) | reject | `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/glocalfileinfo.c` HTTP 200, 93614 B, sha256 `b006a93d8a9733ad9245aba396ca7e3ee42019e214f3addd6e873dbd7d334497`; the `errsv != EACCES` guard is at 1941-1942, `symlink_broken = TRUE` at 1994 | **agree** | `EACCES` is tolerated and a broken follow answers `inode/symlink`; the reject and the M97-2 fix are right |
| receipt cell `decompressed=13688` (reject / correct) | reject | `gzip -dc /usr/share/man/man1/gio.1.gz \| wc -c` → 18793, `wc -l` → 781 | **agree** | the measured size is 18793; the digest cell was right and no source claim moved |
| `gio.1` EXIT STATUS as a per-error rule (reject as a model fact) | reject | page line 775: `On success, \fB0\fP is returned, a non\-zero failure code otherwise.`; `grep -c content-type` over the page → 0; `.TH "gio" "" "" ""` | **agree** | the manual promises only 0/non-zero and names no content-type attribute; the CLI's exit 2 is a surface convention, not documented |

Sampled decision agreement: 6/6 (two admits, four rejects). The Gate section's per-row claims were checked
against the sources; the one record defect I found in the same section is the S523 used-by/recheck repair
(§6 item 5), which is a logging defect, not a gate decision.

## 5. Trend verdicts

- **expansion — improved.** A new admitted entry (`corpus/knowledge/gio-content-type-file-r97.md`) on ground
  the coverage map did not hold (the path-level caller), index 117 → 118, citing two new tier-A rows (S526,
  S527) plus the held GLib rows; the capability row entered with the demonstrated run (157/157, 101/101,
  6194/6194). Rows were not padded: SOURCES 460 → 462.
- **quality — improved.** The round-96 entry's stale measurement cells are corrected append-only (`d421fd77`:
  265 → 284 cases, 97 → 84 counted + 13 not-observable + 13 equivalents, the placeholder sentence replaced);
  C1's instrument supersedes "no lane tool answers a path" with a measured answer and four controls behind it
  (name-only 39/157, naive 67/157, memoriser 0/140, forgery rejected); C2 replaces "no self-invocation" with
  10 checks per counter, 18/18 neutralisations flagged with their declared ids and 6/6 broken modes named. The
  harm watch over every prior instrument is `receipts/harm-final-r97.txt`: 25 legs, 24 rc 0 and the declared
  `r90c1_portal_routing` SETUP_ERROR (declared since round 93), including the two round-96 counter replays at
  the tip. No admitted entry fails its re-check.
- **discernment — improved.** Six mistakes are mined with a criterion each (M97-1…M97-6, QUALITY 168–169);
  the wave reversed four of the L1's own sentences before the freeze (the sniff extent, the `EACCES`/loop
  refusal boundary, the registry base count, the memoriser control); the panel's setup error was caught by the
  counter's own SETUP check and disclosed (three corrections, run 1 kept). My outside sample agrees 6/6.

## 6. Routed defects (status-neutral; the lane fixes them next round)

1. **Report ordering and in-place rewrite.** `f5f6fa34` (committer 16:18:23) filed the report before
   `992037c6` (16:19:05), `d7c186bc` (16:19:34) and `15b62804` (16:19:47); `26a96ca0` (16:20:00) then
   rewrote the filed header line, inserted a misroot bullet and added three table rows without an erratum
   naming the superseded text. Append an erratum naming both versions (PROTOCOL "filed report is a record"),
   and land the report after the lane tip next round.
2. **w1 role census drift.** The report and SCORECARD say "3 executors"; `w1/swarm-registry.json` and
   `w1-results.json` hold 6 executor seats (14 = 6 executor + 2 mutation-tester + 2 reviewer + 1 critic +
   1 scout + 1 connector + 1 scribe). Report the census from the registry (this is the round-96 spot-check's
   D9 class, recurring).
3. **"Dead seats … settled with no report" is false.** `w1/R97MScoutSources.md` (283 L),
   `w1/R97MExecC2.md` (204 L) and `w1/R97MMutC2.md` (199 L) all exist and are substantive. Correct the
   dead-seat line (their items were superseded, but the reports exist).
4. **The Notes' "the r96 spot-check's D1–D13 are closed" overstates.** Its own parenthetical omits D7 and D9,
   and neither is closed: D7's rationale text at `.ufo/waves/round-96/claims-declaration-r96.md:114-115` is
   unchanged, and D9's class recurs in this round's w1 census. Correct the closure claim and close D7/D9
   append-only.
5. **S523's used-by/recheck cells changed without the old→new log.** `a1408d47` moved
   `corpus/knowledge/mime-textdb-magic-r96.md` from the recheck cell into the used-by cell; the lesson's
   "Rows touched" lists ten rows (the r97 entry's appends) and the report's "ten used-by cells" omits this
   repair. Log it old→new in the next lesson and add a registry read-back that catches a path landing in the
   recheck cell (the census's `NF` test is blind to it).
6. **Fleet-root leftovers predating the round.** Untracked `f.txt` (2 B, mtime 2026-11-07 04:40) and
   `trail-ids.txt` (1 B, 2026-11-06 20:36) sit at the fleet root; their mtimes fall inside mado rounds 94/90.
   Identify and sweep them (the round-97 misroot sweep removed its own two files).
7. **Carried:** round-95 routed defects 1, 2, 4 and 5 remain open (re-flagged by the report).

## 7. Operator notes (not lane defects)

- **SHONEN.** All four boxes look checkable by a non-author from committed evidence: box 1 by the `SKILL.md`
  registry rows (`mado-filetype`, `mado-r97-filetype`, `mado-r96-magictext`, `mado-r96-selftest-kills`,
  `mado-r97-counter-selftest`) and the entry's tables; box 2 by the C1 measured run and its receipt; box 3
  by the entry's §5/§11 commands and the counter CLI; box 4 by R97MConnector's 20-lane `PROVINCE.md` sweep
  (a dispatched seat, so still the lane's own work). Promotion is operator-owned; the lane filed `[~]` only
  and wrote no `[x]`.
- The round's two claims reproduce at the tip as well as at their landing revisions (the five instrument
  bytes are unchanged `65ff5591..15b62804`); the capability and the guard both hold. The defects above are
  record/registry defects, not claim failures.
