# ScribeLessonGate — scribe seat, mado round 37 wave 1

Deliverable: draft of `corpus/lessons/round-37.md` at
`.ufo/waves/round-37/w1/scratch/ScribeLessonGate/round-37.md` (289 lines, sha256
`a6c8737b17728bf997ddfdf3ecdeebf62034874ae114568aa9a1d3bb6d747cd7`). Sections: `## Claims`,
`## Gate` (census before + after placeholder, GATE lines, URL/access table, assimilation
admit/refuse, collisions + renumber pointer, S189 quarantine verdict, used-by old→new),
`## Mistakes` (M37-1…4 proposed, `<L1: …>` markers where the L1 decides), `## considerthese`.
No production file was edited. No tool was installed.

## Items and verdicts

| # | item | verdict | evidence |
|---|---|---|---|
| 1 | Claims C1/C2 + Amendment 1 transcribed | PASS | `registration.md:30-67`, `:103-120` |
| 2 | Census before block | PASS | copied byte-for-byte from `receipts/census-before.txt` (8 output lines + `exit=0`); after = placeholder |
| 3 | sha256 of the five receipts, computed by me | PASS | `sha256sum fetch/*` — S189 `eea605df…540d`, S201 `799bf02f…4f9e`, S212 `1e19d926…d7e9`, S213 `1c1b0ce1…ce58`, S214 `d04e3a2f…b868` (full hex in draft) |
| 4 | Quotes confirmed with `grep -F` | PASS | each `grep -cF` = 1; lines S189 :169 and :175, S201 :115, S212 :804, S213 :28, S214 :48; word counts 5, 7, 11, 2, 2, 3 |
| 5 | URL re-open, 2026-10-25T09:16:10-03:00 | PASS | `curl -fsSL` into `/dev/shm/mado37-ScribeLessonGate/`: S189 `http=200 bytes=6479 cmp=identical`, S201 `6550 identical`, S212 `41392 identical`, S214 `1789 identical` |
| 6 | GATE lines parse as the frozen counter parses them | PASS | I ran `GATE_RE` from `c1-r37-event-ground.py:48` and the `## Gate` section rule (`:67-75`) over the draft: 6 lines found under `## Gate`, each `sha256 match=True ≤25=True in-bytes=True` |
| 7 | Assimilation table (1 admit, 2 refuse with reason and flip) | PASS | `registration.md:86-97`; package r28 `:2`, `:24-27`; r29 `:20-26` |
| 8 | Collisions and renumber pointer | PASS | re-counted: `reg-ids` 201 (S001…S211), `staged-ids` 147 (S203…S349), `collisions` 9, guard-proof `collisions` n=1 (`S002`) and `collisions-col0` n=0 |
| 9 | Quarantine verdict, register row S189 | PASS, present | `grep -nF 'auto             eventString = std::format(...)' fetch/S189.bin` → `128` |
| 10 | Used-by old→new | PASS | S189 old `corpus/knowledge/ipc-contract-r25.md`, S201 old `corpus/knowledge/waybar-module-text-route-r25.md` (`corpus/SOURCES.md:201`, `:203`); the new values match `scratch/ScribeRows/rows.md` |
| 11 | Mistakes (4 proposals) | drafted; 2 owed parts marked | see the findings below |
| 12 | considerthese proposal 4 | drafted, with finding F3 | read-only `hyprctl` at 09:17:43-03:00 |

## Findings

**F1 — S189 needs two GATE lines (affects C1 clause g).** Both entries cite S189. The ScribeE2
draft carries `Socket2 fd {} overflowed event queue, removing` but not
`const size_t MAX_QUEUED_EVENTS = 64;` (`grep -cF` → 1 and 0). The controls' only S189 quote
(`controls.py:29`) is the second string. With a single S189 GATE line, E2 would read `g=0`.
The draft therefore carries two S189 lines. The assignment asked for one line per source, so
this is a deliberate deviation. The ScribeE1 draft carries all four of its quotes (S189 ×2,
S201, S212: each `grep -cF` = 1). I messaged both ScribeE1 and ScribeE2 the exact strings.

**F2 — the S201 quote has two spaces before `//`.** The bytes are `buffer;  // Hyprland`.
Any entry must copy it byte-exactly, or clause g/d fails. The E1 draft does.

**F3 — considerthese proposal 4 was already mined in round 34** (`corpus/lessons/round-34.md:96-106`).
That round grounded only whether an oracle exists and chose no surface. The draft treats this
round as making the unmade choice: the event socket's client half (the
`corpus/README.md` Frontier bullet). It leaves `<L1: confirm>` on whether that counts as
"still unimplemented". I re-observed round 34's oracle finding first-hand with `hyprctl` read
verbs: `version v0.56.2 efb50993…`; `windowrules`, `layerrules` and `rules` each printed
`unknown request`; `monitors: count 1`; `workspacerules: count 1`.

**F4 — the probe string in S213 is aquamarine ERR.** `grep -F 'drm: getCurrentCRTC: No CRTC 0'`
on the session log gave `7 ERR from aquamarine ]` (counts only). The draft says exactly that.
The core-logger ERR markers themselves are not shown to reach the journal.

**F5 — the `## Gate` heading must stay exact.** The counter reads only lines under a heading
equal to `## Gate` (`c1-r37-event-ground.py:70-71`). Round 36 used extra `## Gate — …`
headings, and GATE lines placed under a heading like that are not counted. The draft keeps
every GATE line under `## Gate` → `### Sources cited this round`.

**Mistake proposals (class · evidence · captured-by · fix):**
- **M37-1**, instrument: the v1 golden met with `admitted=2/2` (`receipts/controls.txt`). Captured-by: criterion 36 covers reject controls only. Fix: clause g. Able to fail: `c1-token-stub` reads `g=0 TARGET_MISSED` and `c1-golden-v2` reads `TARGET_MET` (`controls-v2.txt`, 13/13).
- **M37-2**, instrument: in `check-evidence-pointers.py`, the git calls at :76, :172 and :204 pass no `env=`. In ExecPointerEnv's `red-green.txt`, `GIT_DIR` gives `error=revision-not-readable` and `GIT_WORK_TREE=/dev/shm` gives `inherited_dirty=8 TARGET_MISSED`, against plain `TARGET_MET`. Captured-by: none. The fixed copy agrees in all three runs and still misses at `4243d03`. The sweep of other files is owed by ExecPointerEnv.
- **M37-3**, hygiene: fleet r36 report :379 says "working tree clean". `DistillerFindings.md` (19,033 B) was untracked until `80b83c8`. Captured-by: none for the round's own paths (`check-evidence-pointers.py:23`, `:171` check only the round-35 paths). Fix: a committed porcelain witness. Able to fail, run in my sandbox clone: at `a5aaa09` with the file present, porcelain gives `?? .ufo/waves/round-36/w1/reports/DistillerFindings.md`; at `80b83c8` it gives 0 lines.
- **M37-4**, inference (null channel): package r28 :27 and r29 :26 infer "never overflowed". Captured-by: none. The same class is in the round-35 erratum (`round-35.md:183-184`, `idle-lock-never-asked-r12.md` E1) but never became a criterion. Proposed criterion: a zero count is a negative only beside the writer's gate state and a same-writer positive probe. The red half is shown on r28/r29. The accept half is owed (marked for the L1).

**Cross-seat confirmation (12:21 UTC).** Both entry scribes replied.
- **ScribeE1:** each of the four quotes appears exactly once in its draft (S189 ×2, S201 with two spaces, S212), and there are `**OBS**` lines for each id (S189 12, S201 8, S212 5).
- **ScribeE2** (draft sha256 `f88f2ec1…49cf`): its `source:` lines name S213, S214 and S189. The quotes sit at body lines 28 (S213), 26 (S214) and 19 (S189 overflow marker), with `**OBS**` lines for every id. Its body does not carry the `MAX_QUEUED_EVENTS` quote, which confirms F1.
- ScribeE2 asked whether the inner double quotes in the S213 quote would break parsing. The counter-regex check in item 6 already covers that line, so I kept the quote.

## Commands run (all read-only on LANE)

`sha256sum`/`wc -c` on `fetch/*`; `grep -nF`/`grep -cF` on the receipts and on the ScribeE1/E2
drafts; `curl -fsSL` × 4 into `/dev/shm/mado37-ScribeLessonGate/` + `cmp`; `git log`,
`git ls-tree`, `git show 8f0a9e3:…`, `git cat-file -s` in LANE (read verbs only);
`hyprctl version|windowrules|layerrules|rules|monitors|workspacerules -j` (read verbs, counts
only); in the sandbox clone `/dev/shm/mado37-ScribeLessonGate/sb` (since deleted): `git checkout`,
`git status --porcelain`, `git ls-files --error-unmatch`; a Python re-implementation of the
counter's GATE parse over my draft.

## Out of scope / not done

I did not run the census after the round: that is the L1's job at round end. I did not run
the C1 counter, because no target entry is committed yet. I did not edit any production file.
I did not run `git status` in LANE, because it can refresh the index.

Artifacts: `.ufo/waves/round-37/w1/scratch/ScribeLessonGate/round-37.md`; this report.
