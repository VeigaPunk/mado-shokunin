# WWKD plan — mado round 11 (ufo-round-plan-v1) — the closeout round

Design lane: PREP-M11 (2026-10-14; round-10 wave, width 32; mado round-10
work in flight at the freeze below). Everything below was read at design
time by this lane — freeze 2026-10-14T20:56Z — not taken from a record;
every pin is re-measured at dispatch. Where this draft and the landed
round-10 artifacts disagree, the landed bytes are the authority.
**Final-round frame:** the fleet's round-10 dispatch extends the arc by one
round — the round this plan opens is the eleventh and last, and its charter
is the closeout: verify the handoff the tenth round leaves, settle every
open item, freeze the revision, and commit the arc-end record. The round-10
plan's closing frame ("this is the arc's last plan … no round-11 plan
follows from this lane") is superseded by that decision for the arc's
shape; the round-10 plan remains the authority for round-10 execution.
Round-10 clauses (a10) the synthesis / (b10) the gate's standing-use note /
(c10) the record family are this plan's precondition set, resolved at
dispatch from the round-10 record, never assumed; a clause that did not
land is a finding the closeout carries — the closeout is the arc's last
carrier, and the arc cannot close without its synthesis, its gate contract,
and its record.

Design-time state (measured, read-only; re-measure at dispatch):

- HEAD `de22dfdedc941563cc102781d3936cef9580e74b` ("probation round 9
  (training r8): see LOG", 17:47:30 −03:00 = 20:47:30Z). The arc: mint
  `74d3b7b`; rounds 1–9 `65a2254` / `e1e1bb7` / `f9f58c0` / `3d9ba45` /
  `eead56b` / `c8f6667` / `0c20a76` / `12c8f08` / `de22dfd`; the SHONEN
  closure `c03c249` (boxes 3–4, VER-M3/VER-M4B) sits between rounds 5 and
  6 — an arc event, not a gate row. `git status --porcelain` empty at
  20:50:40Z and 20:53:56Z; at 20:56:53Z two untracked round-10 artifacts
  (below) — round 10 is in flight at this freeze.
- Gate `tools/mado-verify.sh` **committed** revision sha256
  `93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`,
  3,231 L by `wc -l` / 150,103 B, mtime 17:05:32 −03:00;
  `git show HEAD:tools/mado-verify.sh | sha256sum` reads identical — the
  committed blob is the measured file. Runs at that revision (my own, logs
  `/tmp/w10-prep-m11/`): `--selftest` → `MADO_SELFTEST: 268/268 assertions
  passed`, rc 0; `--no-live` → `MADO_VERIFY: CLEAN (29 pass, 4 notes; file
  plane only)`, `counts: pass=29 fail=0 unknown=0 skip=8 note=4`; live →
  `MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes)`, `counts:
  pass=52 fail=0 unknown=0 skip=0 note=8`; boundary `bb2639d9a980…`
  printed in both; `--regression` → `MADO_REGRESSION: PASS
  (case=mado-verify-hardened;
  target=dc7c4141449891cdd83bb603aff7215358328a9ce1b32dba0bb9c0514cb6f8fd)`,
  `REGRESSION_DATE: 2026-10-14T20:52:33Z`, spec `c7ee75b9…1dd8` (recorded
  pin matches), table `match=10/10 … flips=0`, `MUTATE_RESTORE: OK`,
  harness `cf41efaa…242c75` (recorded `b56c6e57…` — provenance, not
  gated); the gate sha was identical before and after every run.
- Census at the committed revision [OBS, my commands]: 189 `row` + 6
  `row_from_rc` call sites; distinct first-arg row ids **56** by
  `awk '/^[[:space:]]*row [a-z-]+ /{print $3}' tools/mado-verify.sh |
  sort -u | wc -l` — the round-9 append records 55 by AUD-M9's counting
  command and 61 as emitted at run time, so every dispatch count names its
  command and never inherits a number; plane ids 8; `theme` rows 27 sites;
  `grep -c walker.sock` → **0**; helper regexes carry eight ids at `:387`,
  `:391`, `:406-410` (seven sites); asserted ids 32 per AUD-M9 (re-count
  at dispatch).
- Gate ladder [OBS, re-derived at this freeze by `git show
  <commit>:tools/mado-verify.sh`]: rounds 1–4 carry **no gate file** (the
  command errors; piped, it reads 0 L / empty-blob `e3b0c442…` — the
  assertion names its command); round 5 `eead56b` `d7edaab4bf108625…` /
  1,098 L; round 6 `c8f6667` `c4c1afb75dd1c8aa…` / 1,186 L; round 7
  `0c20a76` `90d50cdd4d18410b…` / 1,755 L; round 8 `12c8f08`
  `7da4ec5013583c91…` / 2,887 L; round 9 `de22dfd` `93e43f8f…` / 3,231 L.
  Kill ladder: round-5 revision 4/10 (40 %) → `c4c1afb7…` 10/10 →
  `90d50cdd…` 10/10 → `7da4ec50…` 10/10 → `93e43f8f…` 10/10 (target
  `dc7c4141…`, my run above; r5–r8 receipts [OBS-record]: LOG/SKILL).
  Selftest ladder: 28 → 53 → 89 → 217 → 268 (268 is my run; 28–217 are
  [OBS-record]).
- Round-9 landed/unlanded split [OBS, read from the landed gate, the
  notes, and the SKILL append `:1099-1337`]: (a9) the `theme` plane landed
  as the **file-plane arm** — 10 rows, scenarios T1–T9, 27 row sites,
  helper regexes seven → eight ids, pin re-cut `d2bcdb31…` → `dc7c4141…`;
  the two live rows (`theme.wallpaper.live`, `theme.name.display_agree`)
  are **exempted by name**, each with its clause anchor; (b9) the walker
  live-surface rows **did not land** (`grep -c walker.sock` → 0; walker
  stays version + services); the round's walker work is the new note
  `walker-deep-r9.md` (398 L / 24,391 B / `a5acfe0162c9e5cd…`); the routed
  `walker-deep.md` §10/§11 errata is **still owed** (617 L / 38,403 B /
  `0982ba066c72575a…`, unchanged since round 7); (c9) the census closure +
  receipts landed — and the round's own re-cut record states the theme
  clauses' covering mutant is **owed by the sweep lane** (round-6 reading
  rule 2) — the round's largest named remainder. The snapshot-diff receipt
  note `snapshot-diff-receipt-r9.md` (196 L / 12,701 B / `73b1466b…`)
  carries the mode's first real receipt (`MADO_DIFF: CHANGED (rows 31→41;
  appeared=10; detail-changed=0)` — AUD-M9).
- Round-10 activity at freeze [OBS point sample, 20:56:53Z; **content NOT
  consumed** — resolved at dispatch from its record]:
  `corpus/knowledge/arc-synthesis.md` (386 L / 30,761 B, mtime 17:56
  −03:00) and `corpus/knowledge/gate-standing-use.md` (327 L / 21,004 B,
  same mtime) untracked in the worktree — the round-10 (a)/(b) artifacts
  appearing; the plan's predicted `ten-round-synthesis.md` path is
  superseded by the landed `arc-synthesis.md` name (the closeout reads the
  landed path). No round-10 gate edit, commit, or record draft visible at
  the freeze.
- Round-10 plan's stale base [OBS]: every gate number in
  `plans/round-10.plan.md` (295 L / 19,322 B / `eca573b2…`, committed with
  round 9) is a round-8 value (gate `7da4ec50…` / 2,887 L; selftest 217;
  `--no-live` 20 pass; live 43 pass; census 162+6 / 51 ids) — stale against
  the round-9 landing by construction (it froze before the landing). The
  round-10 record must not recite them; this plan resolves round 10 only
  from the landed record and the landed bytes (the same stale-base class
  rounds 7–9 recorded).
- Record family at freeze [OBS]: `LOG.md` 300 L / 22,712 B / `b6b5a4b2…`
  (the round-9 entry at `:300` is a one-liner; rounds 4–9 carry one-line
  summaries — round 7, and only round 7, additionally carries its full
  M7-1 lane entry at `:297`);
  `SCORECARD.md` 21 L / 9,198 B / `17fe5a42…` (rows 4–9 are stubs; rows
  1–3 full; no final row); `SKILL.md` 1,336 L / 99,084 B / `946bf9d5…`
  (round-9 append `:1099-1337`, M9-4); `corpus/README.md` 19 L / 12,709 B
  / `2dd274f5…` — **8 note rows, 19 committed notes, 11 unrowed** (r4×2,
  r5×1, r6×3, r7×2, r8×1, r9×2; no gaps/frontier section);
  `corpus/lessons/` **0 entries** (tenth round of the round-1 promise);
  `plans/round-7-record-draft.md` 568 L / 37,482 B / `045d380a…` — 13
  ⟨PENDING⟩; `plans/round-8-record-draft.md` 657 L / 42,881 B /
  `b46d4c4c…` — 19 ⟨PENDING⟩; `plans/round-9-record-draft.md` 777 L /
  50,905 B / `f0e811c2…` — 19 ⟨PENDING⟩, ends at its own v2 placeholder
  (the landing committed it unfilled); reports `r9-aud-m9.md` 166 L /
  15,580 B / `866272eeda09bc08…`, `r9-ver-m9.md` 139 L / 7,725 B /
  `98ec0c3b57a0d348…`.
- A design-time citation defect [OBS, registered as the closeout
  spot-check's worked example]: `SKILL.md:1314` cites AUD-M9 as
  `reports/r9-aud-m9.md, 166 L / 7ad8eccdd8d213a5…`; the landed blob reads
  `866272eeda09bc08…` (`git show HEAD:reports/r9-aud-m9.md | sha256sum`;
  166 L / 15,580 B) — the line count matches, the sha does not resolve.
  Class: stale citation in landed bytes; if round 10 does not correct it
  append-only, the closeout names it with both values.
- Debt carried into the closeout [OBS]: `corpus/lessons/` 0; README 11
  unrowed notes (round 10's and 11's to come); SCORECARD stubs 4–9; LOG
  one-line summaries 4–9 (round 7's full M7-1 entry excepted); the three
  record drafts' ⟨PENDING⟩ sets 13 + 19 + 19 = 51
  (+ round-10's to come); `walker-deep.md` §10/§11 errata; the theme
  clauses' covering mutant; the five exempted live rows (theme ×2, walker
  ×3); the round-8 assertion-floor residue [OBS-record: the rc-6 arm, the
  two usage arms, `VERSION_STR` at `:68`, the base `--help` omissions, the
  boundary prefix].
- Live pins [OBS point sample 20:54Z; read-only; a session restart
  invalidates them]: walker 1203471 `/usr/bin/walker
  --gapplication-service`, elephant 1203474, swaybg 1203358
  `/usr/bin/swaybg -i …/current/background -m fill`; sockets
  `srwxr-xr-x`, 0 B, mtime 13:11:09 — session unchanged since rounds
  7/8/9 (no restart). The closeout re-samples; a MOVED reading is the
  round's first finding, never an edit of the baseline.
- Operator channel `.ufo/l0-questions.md` (21,539 B, mtime 14:05:52
  −03:00): zero `mado` lines at freeze (`grep -ci`, shape-only) — no
  operator question owed an answer.
- Sibling harness (read-only): `tameshi-shokunin/tools/mutate-and-run.sh`
  `cf41efaa8be5f52d…242c75` — printed by my `--regression` run's
  `REGRESSION_HARNESS` line as provenance, not gated; unchanged since the
  round-8 freeze (round-10 plan's reading).

Candidate decision: post-round-10 candidates — (1) the closeout: verify
the handoff, settle every open item, freeze the revision, commit the
arc-end record (this round's charter; the only candidate that needs the
arc's end to exist); (2) the carried residuals (the theme covering mutant,
the five exempted live rows, the hypr-live stubs J/K/L, the assertion
floor incl. rc-6 and `VERSION_STR`, base-help discoverability) — classified
by name and given their terminal disposition in (b); not the headline; a
closure that lands carries the full discipline and is named; (3) record
debt (README, SCORECARD, LOG, lessons, the ⟨PENDING⟩ sets, walker-deep
errata) — rides the record: the closeout pays what round 10 left and names
the rest in the gaps ledger; (4) a new frontier — declined: the final
round names gaps, it does not open ground.

Axis move: calibration + freshness — ONE move, three ordered stages. The
closeout is a re-verification pass (freshness: every claim re-derived at
the frozen revision, stale citations flagged) whose output is the honest
handoff (calibration: every open item classified, gaps named, confidence
graded, no overreach). Stage (a) verifies the round-10 handoff; (b) settles
every open item; (c) freezes and commits the arc-end record. Every number
in (a)/(b) carries the command that produced it at the frozen revision; a
number that cannot be re-derived is tagged [OBS-record] with its source,
never recited as measured.

Claim:
(a) **The closeout verification of the round-10 handoff.** Resolved at
    dispatch from the round-10 record, never assumed:
    (i) the precondition read — which of (a10) the synthesis / (b10) the
        standing-use note / (c10) the record family landed, at which
        commit and gate revision, with which receipts; each clause quoted
        from the landed bytes; a clause that did not land is stage (b)'s
        carry, reported as such;
    (ii) the ladder re-derived — `git show <commit>:tools/mado-verify.sh |
        sha256sum` (and `| wc -l`) for every arc commit (rounds 1–4 assert
        their empty result with the same command); the design-time values
        above prove the method; the closeout's own round-10/11 rows come
        from the same command;
    (iii) the frozen revision's whole row re-run — `--selftest` (count
        quoted), `--no-live` and live (counts + verdicts + the boundary
        hash), `--regression` (verdict, target sha, spec sha, table,
        `MUTATE_RESTORE`, harness provenance), a snapshot pair →
        `MADO_DIFF` worked example (scratch only) — receipts quoted in the
        closeout note and the arc-end entry;
    (iv) the synthesis's claims re-derived on a named sample — every
        arc-ledger row's gate sha + line count (the whole ladder is cheap
        and is re-derived complete); the kill/pin lineage receipts
        (`c4c1afb7…` → `d2bcdb31…` → `dc7c4141…` → round-10's target, each
        with its source line); the three trends' evidence lines; the
        invariants (the boundary hash `bb2639d9a980…`; the read-only
        substrate record; the scratch-only rule; the single-writer rule) —
        each re-run where the document carries its command, else tagged
        [OBS-record] with its source and reported as not-re-derived;
    (v) the citations spot-check — the shas cited across the record family
        (SKILL appends, notes, LOG, SCORECARD, the synthesis, the
        standing-use note) are checked against the landed blobs (`git show
        HEAD:<path> | sha256sum`); a non-resolving citation is a finding
        with both values; the design-time registered case (SKILL.md:1314's
        `7ad8eccd…` vs the landed `866272ee…`) is the worked example;
    (vi) the standing-use note's mode map — re-quoted against the landed
        `--help` and mode helps at the frozen revision (every mode, its
        contract, the env vars), rc measured; a NOTE stays non-verdict, an
        UNKNOWN stays unknown;
    (vii) the residual ledger re-grepped per item at the frozen revision —
        each item's open/closed state quoted with its command (the theme
        covering mutant; the two theme live rows; the three walker live
        rows; J/K/L; the rc-6 arm; `VERSION_STR`; base-help
        discoverability; any round-9/10 exemption).
    A mismatch is a FINDING delivered as an appended erratum (to the
    synthesis, the standing-use note, or the record family), never an edit;
    the closeout note carries both values.
(b) **The settlement.** Every open item from (a) and from the round-10
    classification (a10)(vi) receives its terminal disposition: **closed**
    (evidence named) / **operator-owned** (named, with why the lane cannot
    own it) / **unknown** (named, with why it stays so) — "carried" does
    not exist in the final round; the disposition ledger counts per class
    and names every item. Where round 10 did not land its charter, this
    round lands it, under the same specs as `plans/round-10.plan.md`
    (a)/(b)/(c) — the synthesis at its landed path or
    `corpus/knowledge/ten-round-synthesis.md` as the fallback; the
    standing-use note at `corpus/knowledge/gate-standing-use.md`; the
    record-family items below — the closeout is the last carrier, and it
    reports the difference. The settlement also carries:
    - the synthesis's terminal epilogue (append, never edit): round 10's
      landed row (measured post-commit from git: commit, artifact shas,
      gate revision, counts) + round 11's closeout row + any (a) correction
      as an appended erratum;
    - the standing-use note's frozen-revision line appended if its own
      revision text is pre-commit;
    - `corpus/lessons/round-11.md` chartered with its `## Gate` section
      (candidates, admits, rejects with reasons) and a non-author
      spot-check (≥1 admit, ≥1 reject; a lane's own subagent does not
      count; `LEARNING.md:38-43`) — or the refusal recorded as the arc's
      named failure with its reason and owner; round 10's own entry (or
      refusal) is read first, never assumed;
    - the record family: README (every committed note rowed, re-measured at
      apply time; the `## Known gaps` closure from the gap ledger; row
      count before → after); SCORECARD (the abbreviated rows replaced from
      the committed drafts' ready text where still owed; rounds 10–11
      rows; the final row naming the frozen gate revision, the synthesis,
      and the standing-use note); LOG (the round-10 entry if round 10 left
      it owed; the arc-end entry); the draft ⟨PENDING⟩ sets closed by
      appended closure blocks (13 + 19 + 19 + round-10's — never edits);
      `walker-deep.md` §10/§11 errata appended if still owed; the
      `AGENTS.md` pointer if round 10 left it owed.
(c) **The arc-end record and freeze.** `corpus/knowledge/arc-closeout.md`
    (self-label M11-1; `source:` / `verified-at:` / `recheck:` per
    CORPUS.md) — the closeout's single durable artifact: (i) the
    verification ledger from (a) (claim → command → re-derived value →
    match/mismatch, every row); (ii) the terminal disposition ledger from
    (b) (counts per class; every item named); (iii) the freeze pins — the
    frozen gate revision (sha, lines, bytes), the final commit, the ladder
    re-derived, the final battery receipts; (iv) the handoff ledger — what
    the operator inherits: the standing-use pointer, the residual list
    with its owners, the promotion materials status (SHONEN 4/4 since
    round 5; promotion is the operator/gate decision, never
    self-declared). The final commit lands last under the lane identity:
    the arc-end LOG entry quoting the closeout's receipts and this round's
    three trend verdicts (expansion: unchanged — no new ground, by design;
    quality: improved only where the settlement closed or repaired with
    evidence, else the harm-side stated; discernment: the verification
    sample's agree/disagree outcome and the spot-check result); the
    closeout note committed; the arc-end statement: the arc is closed, the
    gate is handed over at the frozen revision named by the entry, and no
    further round opens.

Ordering: (a) consumes the round-10 landed revision — (a10)/(b10)/(c10)
resolved at dispatch from the round-10 record (the committed synthesis
path/sha; the standing-use note's SKILL append; the re-cut
`MADO_REGRESSION: PASS` and its target; the receipt lines quoted in its
record; README/lessons/⟨PENDING⟩ movement). If the round-10 commit does
not exist at dispatch, the closeout carries the round-10 charter itself
(the same specs) and the record says so — counted, never silent. (b) rides
(a); (c) rides (a)/(b); the final commit lands last and carries the
arc-end statement. Residual closures are not this round's claim; whatever
stays open ships named in (b)'s disposition ledger and (c)'s handoff; a
closure that lands anyway carries the full discipline (covering mutant,
re-cut, `MADO_REGRESSION: PASS`, selftest count before → after) and is
named in both (a)/(b) and the arc-end entry.

Anti-claim: the closeout verifies, it does not rewrite — a mismatch is an
appended finding with both values, never an edit of the synthesis, the
notes, or any committed record; the archive is append-only throughout; no
new coverage and no new frontier — surfaces never made verdict-bearing
stay named as gaps, never promised; a clause that did not land is reported
as not landed; the standing-use note cannot upgrade the gate (a NOTE stays
non-verdict, an UNKNOWN stays unknown, a stub scenario proves row logic
never live values, and the verdict stays `bash tools/mado-verify.sh`); no
compositor/session mutation (no launcher open, no socket connect, no
`omarchy theme set`, no restart); substrates read-only, secrets
shape-only; the tameshi harness and sibling repos are read-only — a needed
change is a recommendation to that lane; no `git status`/`git fetch` on
the omarchy checkout; snapshots and receipts stay in scratch, never
committed; promotion is never self-declared.

Measure: the closeout note lands (lines / bytes / sha; per-ledger-row
command + re-derived value + match/mismatch; the mismatch count with every
mismatch named); the disposition counts per class with every item named
("carried" → 0); the ladder re-derived per arc commit (`git show
<commit>:tools/mado-verify.sh | sha256sum` — outputs quoted) and the
frozen revision's whole row re-run (selftest; `--no-live`; live; the
regression receipt incl. target + spec + table + restore; a snapshot pair
→ `MADO_DIFF: SAME|CHANGED`; the boundary hash before/after); the
synthesis's epilogue (sha before → after; the appended rows); the
standing-use note's revision append (sha before → after); the mode map vs
the landed `--help`/mode helps (quoted; rc measured); the record family
before → after (README rows 8 → every committed note rowed; SCORECARD
rows; LOG entries; lessons 0 → 1 or the recorded refusal; ⟨PENDING⟩ 51 +
round-10's → closed-by-append or named; `walker-deep.md` sha before →
after); the operator channel (0 `mado` lines at freeze — a mid-round
filing is named, never answered here); the citation spot-check
(non-resolving → the finding text with both values); the three trend
verdicts with their evidence lines.

Open unknowns at draft: whether round 10 lands (a10)/(b10)/(c10) in-window
and under which commit/gate sha — the frozen revision is the ladder's last
row and the closeout's whole precondition set; whether the round-10
synthesis carries round 10's own landed row (its numbers were written
pre-commit — the closeout re-measures from git and appends); whether round
10 pays the README/lessons/⟨PENDING⟩/walker-deep debt or leaves it (the
closeout carries what remains); whether the round-10 gate re-cut leaves
`MADO_REGRESSION: PASS` and what target sha it then carries (the closeout
re-runs it and quotes the landed receipt); whether the theme covering
mutant, the five exempted live rows, J/K/L, and the assertion floor close
in round 10 (their terminal disposition otherwise); whether a non-author
seat exists for the final lessons entry; whether the SKILL.md:1314
citation defect is corrected append-only in round 10 or named by the
closeout; whether each historical gate revision still runs its `--selftest`
faithfully at dispatch (toolchain / fixture drift — if not, its row cites
the record value tagged [OBS-record] with its source); whether the sibling
harness moves mid-round (receipts pin it; provenance, not gated); whether
the operator's L0 files a mado entry mid-round (none at freeze); whether
the gate moves during round 11 (any round-11 edit carries the full
discipline; the frozen revision is the one the final battery runs);
whether the round-11 wave can seat an independent verifier/auditor for the
closeout (the lane's own subagent does not count).

Write scope (execution): one output file per lane as assigned; the gate is
single-writer (no gate edit is this round's claim); this round's artifacts
are the closeout note, the settlement appends, and the record family named
in (b)/(c); scratch `/tmp/w11-<lane>-*`; substrates (`~/.config`,
`~/.local`, the omarchy checkout, the tameshi harness) read-only; secrets
shape-only; snapshots and receipts stay in scratch. This design lane wrote
only this file; scratch `/tmp/w10-prep-m11/`.
