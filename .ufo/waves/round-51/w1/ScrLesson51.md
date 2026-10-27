# ScrLesson51 — round 51 / w1 (BUILD): lesson skeleton

Status: complete. Deliverable is the `corpus/lessons/round-51.md` skeleton, drafted inside this seat dir. No product
code, counter, fetch or commit was made, and no tracked file was written by this seat.

## Deliverables

- `ScrLesson51/round-51.md`

Report: .ufo/waves/round-51/w1/ScrLesson51.md

## 1. What the skeleton holds

Section inventory, in file order (house shape `corpus/lessons/round-50.md`: header, `## Gate` with
`### Rejected after opening` and `### Assimilation (...)`, `## Mistakes`):

| section | state left to the L1 |
|---|---|
| header | base, claims commit and the 43-seat w1 roster are real values; `TODO-L1`: freeze revision, w2 seat set, round total, WAVE-DONE verdict. Names the two claims' artifacts and the round-50 routed items carried here (D1 → M51-1, D4/M50-9 receipt-only cleanup, the candidate-inclusive novelty carry, the 13-row quarantine hand-check) |
| `## Gate` intro | `TODO-L1`: fetch/verify seats, pin count, pin manifest, `SHA256SUMS`, pin-binding receipt, clause (c) per-file overlap numbers, census-after. Census-before is cited as committed (`receipts/census-before.txt`, 22 lines: 19 `W04`, 1 `W01`, `mado ok`, `EXIT=0`) |
| admit block | one non-counting template (`- **S<id> admit**, tier <A\|B\|C>, …` with URL, `opened 2026-10-27`, `pin …:<line>`, `»quote« (<n> words)`, and a criterion-100 slot for *why the line sets the symbol*); row-cell constraints (status `mined`, tier `A`, day, used-by the entry) and the `S364`–`S379` band from claim clause (b) |
| `### Rejected after opening` | one non-counting template plus the four classes the round must test — unanchored archive page, moving wiki URL, page stating no 0.56.2 dispatcher behaviour, re-registering a URL already held (`HyprCtl.cpp` `S307`/`S320`, legacy `ConfigManager.cpp` `S303`/`S317`, `IKeyboard.cpp` `S319`) |
| status/recheck/used-by | old→new table with the base cells measured (worked row `S319`: `A \| mined \| 2026-10-26 \| 90d \| corpus/knowledge/hyprland-input-devices-r46.md`), the candidate held rows `S303`/`S307`/`S317`/`S318`/`S320`/`S321`, the renumber-map rule, and the base top `S363` over 300 rows |
| `### Assimilation` | admit/reject/`none — <reason>` line shapes, the id-collision guard (indented-row fixture, never arithmetic) with lane ids measured at 300, and the quarantine verdict summary block (13 rows: 6 payload-absent `S189`/`S195`/`S201`/`S205`/`S224`/`S228`, 7 unchecked-prose `S199`/`S200`/`S209`/`S222`/`S223`/`S225`/`S235`; `adopted=0`; `unverifiable` is not a presence claim) |
| `## Mistakes` | M51-1 complete except the arm the L1 must capture (`· fix shown able to fail: TODO-L1`, red/green shape named) |

Counts: 131 lines, 16 `TODO-L1` markers, 5 headings, `sha256 b1762a844de19022…` (measured after the last edit; full value
in §3).

Decision-count pipeline, written into the skeleton so no count is typed (the M50-2 fix):

```
A=$(sed -n '/^## Gate/,/^## Mistakes/p' corpus/lessons/round-51.md | grep -cE '^- \*\*S[0-9]+ admit\*\*')
R=$(sed -n '/^## Gate/,/^## Mistakes/p' corpus/lessons/round-51.md | grep -cE '^- \*\*REJECT ')
```

On this skeleton it reads `A=0 R=0`; on `corpus/lessons/round-50.md` — the control — it reads `A=12 R=5`, the round-50
gate's own admit and reject counts. The templates are written `S<id>` / `**REJECT**` precisely so they cannot score.

## 2. Measured inputs (read-only git, 2026-10-27)

| fact | command | output |
|---|---|---|
| round base / claims | `git log --oneline -1 6ca8c559` / `… -1 d2740281` | spot-check commit / `round-51: claims freeze … + census-before receipt; remove .ufo/wakes leftover` |
| registry rows / top at base | `git show 6ca8c559:corpus/SOURCES.md \| grep -cE '^\| *S[0-9]{3,} *\|'`; `… \| grep -oE '^\| *S[0-9]{3,}' \| tail -1` | `300` / `\| S363` |
| criteria ids at base | `git show 6ca8c559:corpus/QUALITY.md \| grep -oE '^(\*\*)?[0-9]+\.' \| tr -d '*.' \| sort -n -u \| wc -l` | `102`, top `102` (103 is the in-flight `w1/RevQuality103` draft) |
| knowledge / lessons at base | `git ls-tree --name-only 6ca8c559 corpus/{knowledge,lessons}/ \| wc -l` | `66` / `76` |
| `corpus/lessons/round-51.md` | `git cat-file -e 6ca8c559:corpus/lessons/round-51.md`; `test -e corpus/lessons/round-51.md` | ABSENT / ABSENT |
| w1 seats | `python3 -I -c "…len(json.load(open('.ufo/waves/round-51/w1-spec.json'))['items'])"` | `43` |
| base-absent C1/C2 targets | `git cat-file -e 6ca8c559:<path>` ×5 | `quality/tool-ledger.md`, `quality/check-tool-ledger.py`, `quality/counters/c1-r51-ledger.py`, `quality/counters/c2-r51-dispatch-entry.py`, `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` — all ABSENT |
| census before | `receipts/census-before.txt` (claims commit) | 22 lines: 19 `W04`, 1 `W01`, `mado ok`, `EXIT=0` |
| held row cells (`S303`/`S307`/`S317`-`S321`) | `python3 -I` row parse of `corpus/SOURCES.md` | 11 cells each; used-by `hyprland-monitor-rule-r45.md` (`S303`,`S307`) and `hyprland-input-devices-r46.md` (`S317`-`S321`); all `mined`, `2026-10-26`, `90d` |
| round-50 closure receipt | `cat .ufo/waves/round-50/receipts/wave-done-r50.txt`; `git log -1 -- <path>` | `--rev 8dbbf61a…` → `waves=1 settled=1 verdict=OK`, `exit=0`, landed `b4a79843` |
| round-50 LOG assertion | `git show 74782d39:LOG.md \| grep -n 'waves=2 settled=2'` | `2560:- \`quality/check-wave-done.py --repo . --rev <tip> --round 50\` → waves=2 settled=2 verdict=OK; index 66/66, exit 0.` |
| fleet report assertion | `grep -n 'waves=2' /home/vgpnk/Projects/shokunin/.ufo/reports/round-50/mado.md` | `:3` — same verdict with the full `--rev 74782d39e7…` hex |
| `waves=2` strings under round-50 | `grep -rl 'waves=2' .ufo/waves/round-50/` | only `w1/ExecWaveDone/{check-wave-done.py,receipts/history-base.txt,receipts/selftest.txt}` — rounds 41/43/44/47 probes and a round-49 fixture, no round-50 closure receipt |
| w2 results landed | `git show --stat c12b588e` | `round-50: integrate w2 falsification and honest-stop findings`, `w2-results.json +200` |
| register path | `test -f /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` | present (READ-ONLY; nothing read into the draft beyond the path and the round-50 row classes) |

## 3. Self-checks actually run on the draft

| check | how | result |
|---|---|---|
| declared path exists | `test -f .ufo/waves/round-51/w1/ScrLesson51/round-51.md` | present |
| heading inventory | `grep -n '^#\|^###'` | `#` header, `## Gate`, `### Rejected after opening`, `### Assimilation (…)`, `## Mistakes` — no stray top-level section |
| decision-count pipeline | the two commands of §1, run on the draft and on `corpus/lessons/round-50.md` | draft `0`/`0`; control `12`/`5` (= round-50's gate) |
| mistake evidence re-derived | `grep -rl 'waves=2' .ufo/waves/round-50/`, `cat receipts/wave-done-r50.txt`, `git show 74782d39:LOG.md \| grep -n`, `git log -1 -- receipts/wave-done-r50.txt` | as tabulated in §2; every number in M51-1 is a command output |
| nearest instrument is live | `python3 -I .ufo/waves/round-41/w1/ScrQualityCriteria/check69.py --repo . --rev 74782d39e7697608917b5e909f0e8580aaa3e15c --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-50/mado.md --receipts .ufo/waves/round-50/receipts --text` | `MISSING 74782d39… : no committed receipt under .ufo/waves/round-50/receipts names it` / `FAIL 1/1 cited revisions lack a committed receipt`, exit 1 — read-only; this is M51-1's `captured-by` evidence |
| seat names in `TODO-L1` slots | each name checked against `w1-spec.json`'s 43 `name` values (`ScoutDispatchMap`, `ExecFetchDispatch`, `ScrRowsDispatch`, `ScrDispatchEntry`, `RevNovelty`, `CritHeldFacts`, `RevRowsTruth`, `ScoutAssim`, `ScoutConsiderthese`, `ScoutQuarantine`) | all present; no invented seat |
| draft digest | `sha256sum` / `wc -l` | `b1762a844de19022a5d0f8e45e5e7ed211a97e54a2fe8a95c1a3e28d306319b0` / `131` lines |
| never edited a tracked file | `GIT_OPTIONAL_LOCKS=0 git status --porcelain -- .ufo/waves/round-51/w1/ScrLesson51 .ufo/waves/round-51/w1/ScrLesson51.md` | exactly `?? …/ScrLesson51.md` and `?? …/ScrLesson51/` — the seat's two paths, nothing else at those paths (round-51 overall carries 80 untracked entries from the other seats, untouched) |

In-flight peer drafts were read, not asserted: `w1/RevQuality103/criterion-103.md` (criterion 103's text — cited as a draft
"landed at integration", never as an existing criterion) and `w1/ScoutQuarantine/quarantine-verdicts.md` (per-row verdicts —
the skeleton leaves the counts `TODO-L1` rather than importing its current all-unverifiable state, which may change before
freeze).

## 4. Limits / what this seat did not do

- No admit line, reject line, overlap number, pin count, census-after block, assimilation verdict or quarantine count is
  drafted: each is the L1's data, and the skeleton's placeholders are written so the count pipeline cannot score them.
- M51-1's `fix shown able to fail` arm is left `TODO-L1` as instructed; the arm shape (red = round 50's w1-only receipt
  offered as the two-wave verdict; green = the fresh integration-tip receipt) is named in the skeleton, its numbers are not
  captured here.
- No counter, gate or checker was written; `check69.py` was only executed read-only against committed/fleet bytes.
- No commit, push, git mutation, pacman call, service restart, compositor socket or config-plane write. No tool installed.
  Scratch `/fast/scratch/hyaku/mado-r51/ScrLesson51` was created and removed; nothing was written to `/tmp`.
- Unverified by design: the round's own outcome (C1/C2 verdicts, honest-stop wording), the freeze revision, and every
  `TODO-L1` slot in the skeleton.
