# mado round 45 — registration v2 (frozen BEFORE any round-45 data commit)

Supersedes both predicates of `registration.md` (freeze `22a8dedd02f507689c567777e0f20b5e645c8ce0`), as that file allows ("a hole `w1` finds
before any data commit may re-register as v2 with a new freeze and new controls"). No data commit exists: the lane branch carries only the
freeze `22a8dedd` and the w1 spec `ebdba13f` above the base `0c89478a`; `tools/mado-monitors.py` and
`corpus/knowledge/hyprland-monitor-rule-r45.md` are absent. Wave `w1` ran 41 seats; all 41 wrote reports (`w1/*.md`; `w1-results.json`
records 41 settled, outputs not retained after an orchestrator kernel restart).

Surfaces, axes, lowest-axis argument, separability and the routed non-claim work are unchanged from `registration.md`.

## C1 — `PRED-C1-r45-v2` (replaces `PRED-C1-r45`)

- **Why.** `w1/CritC1Cheat`: 11 of 11 cheat tools reached v1 TARGET_MET (eight narrow one semantic to the fixtures; an environment gate; a
  seed-45 answer table; a scorer oracle reading `/proc/<ppid>/cmdline`); `w1/ExecDoNothingC1`: 5 do-nothing controls met v1 (embedded fixture
  tables, a counter import, a reference loader, a parent-process reader). The v1 contract was wrong against Hyprland on six forms
  (`w1/CritToolSemantics` 2-4, `w1/ExecParseOracle` A/M/T/W, `w1/RevTool` F1, `w1/CritEntryContent` W1): `transform` INTEGER values such as
  `07`/`-0`; std::stoi `addreserved` fields; the 0x0 preferred sentinel; a valid modeline silently not compared; CR-terminated lines; `desc:`
  matching only the long description; a written scale with no clean divisor printed AGREE; NaN/Infinity accepted as numbers.
  `w1/CritToolSemantics` 1 (float32 integrality) is refuted: hyprutils Vector2D holds doubles and divides by a double
  (`fetch/hyprutils-Vector2D.hpp:21-22,39-41`), and `w1/ExecScaleOracle` found 0 divergences in 445,875 cases against a C++ transcription.
- **Contract:** the docstring of `v2/mado-monitors.py` (the v2 reference; selftest 48/48; live host run AGREE / OK).
- **Predicate:** the docstring of `quality/counters/c1-r45-monitors-v2.py`: clauses a, s, f (the 49 v1 fixtures + 32 new = 81, each run as
  seed 45 in environment A, seed 45 in environment B, and a nonce seed in environment A), i (bubblewrap sandbox: pid and net namespaces, the
  repository, the counter's lane and its parent hidden), r, and **g** (150 cases generated from the nonce, judged against the v2 reference
  pinned by sha256 `2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609` and loaded from the counter's own lane, invisible to the tool).
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r45-monitors-v2.py --repo . --rev <rev> --work <scratch outside /home/vgpnk/Projects/shokunin> [--nonce N]`
- **Before** (base): `fixtures=0/81 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED`, exit 1
  (`receipts/c1-v2-before-base.txt`; deterministic: no tool, nothing runs). **Target:** `fixtures=81/81 generated=150/150 selftest=ok
  readonly=ok tool=present verdict=TARGET_MET`, exit 0, at the data commit and at the round tip, under any nonce.
- **Kill rule:** anything else at the data tip is a miss, reported as an honest stop; no narrowing, no re-registration after data.
- **Controls** (`ctl/run-c1-controls-v2.py` → `receipts/ctl-c1-v2.txt`, nonce 4545): REF2 must be MET; the base, `mado-geometry.py` copied, a
  stub, the v1 reference, the v1 variants K03-K15 re-cut on the v2 reference, the v2 variants K16-K25 (each undoes one v2 correction or guard),
  the 11 `w1/CritC1Cheat` cheat tools and the 7 `w1/ExecDoNothingC1` controls must all be MISSED.
- **Residuals (declared):** a tool holding a model of the contract is an implementation of it; a tool may still detect a sandbox by means not
  varied in environment B; clause g's oracle is the reference, so a contract error shared by reference and tool is invisible to it (the
  non-author reading of the contract against the pins covers it); clause s is a printed line.

## C2 — `PRED-C2-r45-v2` (replaces `PRED-C2-r45`)

- **Why.** `w1/CritC2Forgery`: nine forged revisions admitted by v1, three outside its declared residuals (a false table inside a fence, a
  sentence citing the receipt that refutes it, a free README id list), census tokens one space off the regex, a new row claiming a supersession.
  `w1/CritEntryContent`: four entry facts had no pin (comma splitting, the `all` list, the long description, the strict bound), the scale-check
  gate was missing, and one Limits sentence was wrong (the long description is rebuildable from the dump).
- **Predicate:** the docstring of `quality/counters/c2-r45-monitor-entry-v2.py`: v1 plus T1 (spaced census tokens), T2 (no supersession words
  in new rows), T3 (fences only quote pins), T4 (verdict tokens bound to the cited receipt), T5 (README Sources cell = the cited ids), five more
  pins (`fetch/Hyprland-MonitorState.cpp`, `Hyprland-macros.hpp`, `hyprutils-Vector2D.hpp`, `hyprutils-VarList2.hpp`, `aquamarine-DRM.cpp`,
  opened 2026-10-26, sha256 in `receipts/fetch-sha256.txt`) and seven more surfaces (24).
- **Sources:** rows S302-S315 (S311-S315 new in v2). The two cross-scope URL repeats (S303/S162, S307/S158) stay W04 census warnings.
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r45-monitor-entry-v2.py --repo . --rev <rev>`
- **Before** (base): `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-v2-before-base.txt`). **Target:** `admitted=1/1
  verdict=TARGET_MET`, exit 0, at the data commit and the tip. **Kill rule:** as C1.
- **Controls** (`ctl/run-c2-controls-v2.py` → `receipts/ctl-c2-v2.txt`): P (`v2/build-pos.py` on a clone of this freeze) admitted; C2-BASE,
  R14-COPY, SHELL, WIDE-RANGE, HIDDEN-LINE, FORGED-PIN, FALSE-URL, PROSE-CENSUS, ANCHOR-PAST-EOF, PROSE-CENSUS-SPACED, ROW-SUPERSEDES,
  FENCE-TABLE, RECEIPT-CONTRADICT, README-IDS all rejected. P is a control, not the data.
- **Residuals (declared):** claim-to-quote binding, word-form census contradictions and registry prose cells are the non-author reading;
  clause j binds a locator and a keyword per surface, not the truth of the sentence.
