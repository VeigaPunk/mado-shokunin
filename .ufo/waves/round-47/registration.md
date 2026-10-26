# mado round 47 — registration v1 (frozen BEFORE any round-47 data commit)

Base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750` (lane tip at round start). Claims declared at `c24adef2` (`claims.md`),
before wave `w1` (41 seats, policy v1, build). This file, the two counters, the C1 fixtures, the pins and the L1
reference land in one freeze commit; no seat has scored either counter before it. A hole that wave `w2` (falsify) finds
before any data commit may re-register as v2 with a new freeze and new controls; after the data commit nothing here
changes (kill rule).

## Lowest-axis rule

The published axis table sits tied at its maximum (round-46 tip `receipts/axis-tip.txt`, `checked=3 mismatched=0`), so no
axis is lowest; both claims sit on the lane's declared axes, coverage + operability.

## Premise corrections from w1 (before freeze)

- `w1/CritPremise` F1/F2: print modes never observe a launch, and the round-17 cache line (`terminal-route-r17.md:123-127`)
  already recorded the user-local selection as cache bytes. So C2 answers only the **selection half** of the round-17
  `[UNK]` at `:144-145`, by a cold-cache capture of the resolver itself (not by the cache, not by our tool); the
  launch half ("at launch") stays `[UNK]` and the entry must say so.
- `w1/CritPremise` F3: list order, validation keys and execarg defaults are partly held at `terminal-route-r17.md:24-59`
  as documentary statements. C2's new ground is the executed selection semantics (the functions the census terms name;
  clause i of C2) - the carried-over keys between candidates, the read-loop exit status, `command -v` over aliases,
  functions and builtins, the find-based desktop-file IDs, the tokenizer and field stripping, the print composition and
  exit map - each tied to the script lines and to the C1 fixtures that exercise it.
- C2 separability (L1): the w1 draft of the C2 counter re-ran `tools/mado-terminal.py`, which made C2 depend on C1;
  clause f now binds the entry's sentence to a committed capture of the resolver (digest named) and never runs our tool.

## C1 — operability (capability acquisition): `tools/mado-terminal.py` — `PRED-C1-r47`

- **Contract:** the docstring of `.ufo/waves/round-47/l1-draft/mado-terminal.py` (the reference; selftest 43/43; 3000
  random cases and the 140 w1 seat fixtures agree with the real script on stdout and exit status before the freeze).
- **Predicate:** the docstring of `quality/counters/c1-r47-terminal.py`: clauses a (tool present), s (selftest N/N, N >= 30),
  f (190 pinned fixtures of `quality/counters/c1-r47-fixtures.json` x 2 variants, tool stdout+rc == the pinned real
  script's stdout+rc on a separate tree; oracle == recorded expect, else setup error), x (`explain` names what the
  oracle prints; `--observed` AGREE and DIFFER both ways), g (150 nonce cases judged by the real script at count
  time), i (bwrap allowlist root without /usr/bin, /usr/share, /etc, /home, /fast), r (strace around bwrap: no process
  and no socket after the sandboxed python3's execve). Fixtures are built by `ctl/build-fixtures.py` (w1 ExecFixtures
  snapshot `ctl/seat-fixtures.json` + the reference's selftest cases; every `expect` from three pin runs).
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r47-terminal.py --repo . --rev <rev> --work <scratch outside the lane> [--nonce N]`
- **Before** (base): `receipts/c1-before-base.txt`: `fixtures=0/190 explained=0/190 generated=0/150 selftest=fail
  readonly=fail tool=absent verdict=TARGET_MISSED`, exit 1.
- **Target:** `fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present
  verdict=TARGET_MET`, exit 0, at the data commit and at the round tip, under any nonce.
- **Kill rule:** anything else at the data commit is a miss, reported as an honest stop; no narrowing, no re-registration
  after data.
- **Controls** (`ctl/run-c1-controls.py` → `receipts/ctl-c1.txt`): REF (the reference) MET; BASE, STUB, EXIT1, CONST,
  DELEGATE-SH, SUBPROC-EMBED, EMBED-EXECV, CTYPES-EXECVE, SOCKET-AND-REF, EXPLAIN-CANNED, EXPLAIN-ALWAYS-AGREE and 17
  one-rule-undone variants of the reference (V-*) all MISSED. Two pre-freeze variants were equivalent mutants and are
  not controls: the execarg-default re-read (the first `read` already leaves no single trailing ':'; the code was
  removed from the reference) and strip-fields-always (the failure path returns its input unchanged; replaced by
  V-STRIP-FAIL-EMPTIES). Pre-freeze runs `l1` scratch: 5 of 27 met before the fixture additions, 0 of 26 after.
- **Residuals (declared):** a tool carrying a model of the resolver (an emulator, or a Python interpreter for an embedded
  copy of the script) is an implementation of it; the judge is this host's bash, find, awk and tr at count time (a
  different host may drift; the drift check stops the count); the warm-cache path, `-h/--help`, an empty argv element
  (the script loops forever), XDG dirs holding glob characters or quotes, and non-ASCII `\u` delimiters are outside the
  contract; the explain trace text is not judged, only its MADO_TERM line; clause s is a printed line.

## C2 — coverage (sourced): `corpus/knowledge/xdg-terminal-selection-r47.md` — `PRED-C2-r47`

- **Predicate:** the docstring of `quality/counters/c2-r47-terminal-entry.py` (w1 ExecCounterC2 draft, clause f changed
  by the L1 as above): a entry new at REV; b provenance head with >= 2 `source: S###` >= S326, rows mined/opened
  2026-10-26/used-by the entry; c every cited row pin-bound (fetch copy under `.ufo/waves/round-47/fetch/`, digest equal,
  xdg-terminal-exec files equal to the real v0.14.3 bytes) and ref-pinned (tag or commit, no branch); d every quote
  verbatim inside its pin at its stated range; e >= 6 numbered chain steps, each with a script locator; f the
  selection half of the round-17 `[UNK]` answered by a committed resolver capture (receipt with `resolver_sha256=`,
  >= 3 XDG_* lines, `observed=`), the entry line stating its id and path; g one README index row covering the head ids;
  h rows S056-S060 byte-equal to base; i the census terms `read_config_paths`, `check_entry_key`, `find_entry_paths`,
  `print-delimiter` absent under corpus/ at base (`receipts/c2-ground-base.txt`, git grep exit 1) and >= 2 present at REV.
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r47-terminal-entry.py --repo . --rev <rev>`
- **Before** (base): `receipts/c2-before-base.txt`: `admitted=0/1 verdict=TARGET_MISSED`, exit 1. **Target:**
  `admitted=1/1 verdict=TARGET_MET`, exit 0, at the data commit and the tip. **Kill rule:** as C1.
- **Controls** (`ctl/c2/build-control.py` + `ctl/c2/run-controls.py` → `receipts/ctl-c2/`): POS (a minimal entry-only
  tree, no tool) admitted; BASE, QUOTE (quote in no pin), BRANCH (branch URL), HELD (S056 moved), RECEIPT (absent),
  NOSTEPS (citation index), OBS (capture contradicts the entry), NOSHA (receipt without the resolver digest), RANGE
  (true quote, false range), PIN (pin bytes changed) rejected, each on its intended clause.
- **Residuals (declared):** a capture can be typed rather than produced by the resolver (the counter checks its form
  and digest line; the non-author closure re-runs the print command); a true quote can stand beside a claim it does not
  support; clause e counts steps and locators, not the truth of each step; clause i is a term census, not a novelty proof.

## Separability

C1 reads only `tools/mado-terminal.py`; C2 reads only the entry, rows, README row, pins and receipts. The C2 positive
control is an entry-only tree (no tool) and is admitted; a tool-only tree has no entry (C2 clause a). Shown both ways
again on the landed bytes by a w2 seat.

## Routed non-claim work (round-46 closure R1-R4)

R1 erratum on `hyprland-input-devices-r46.md:57`; R2 digest of the untracked round-46 seat file, then its removal;
R3 the session-material synthetic marker, shown able to fail both ways (receipt, not a claim); R4 the S290-S297
supersession and the round-45 / round-44 errata, each verified before landing.
