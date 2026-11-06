# mado round 91 — claims declaration

L1: MadoR91 (planner seat held by the L1). Base revision `cc0381db585cc44c3dfc13ced807409c32c45bb0` (master, = the
round-90 closure tip). Hyaku run 15, attempt 1. Round shape: ONE v1 wave `w1` (14 seats, build + first falsifiers) + at
most one residual call `r1` (≤2 attack seats) on the frozen and measured bytes; total ≤16. This file is frozen by the
freeze commit; anything after it is an appended erratum.

**Wave state at the freeze.** 13 of 14 w1 seats had written their report file; R91MScoutSources had not (its scratch was
still being written at 21:42). Its output is not scored by either claim: the registry rows S504–S507 that C1's knowledge
entry cites were opened by the L1 (`receipts/sources-open-r91.txt`), and the scout's rows, when they land, are compared
with them in the lesson. R91MScoutBlind's case file was re-written by the seat at 21:49 (88 → 91 cases); the frozen merge
copy below carries those 91 and no later edit.

## Inputs read before declaring

- `corpus/lessons/round-90-verifier-spotcheck.md` (non-author, round 90 admitted): routed defects 1 (gate self-test
  missing on `quality/check-receipt-presence.py`), 2 (seat outputs not retained: R90MScoutSources, R90MScoutCases — lesson
  M90-4), 3 (lesson wording on the UseIn comparator).
- `considerthese/2026-11-06.md` proposal 4: "Widen desktop coverage past bar + mako … Prefer one operator-config gap over
  another harness counter." No lane knowledge or tool on the default-application plane: `grep -n -i -E
  'mime|xdg-open|mimeapps|default app' PROVINCE.md SKILL.md corpus/README.md` → no line at the base.
- GLib tag 2.90.1 (installed `glib2 2.90.1-1`): `gio/gdesktopappinfo.c` (sha256 `8e9ce1a8…5b0d`), `gio/gio-tool-mime.c`,
  `gio/gcontenttype-fdo.c`, `gio/xdgmime/{xdgmime,xdgmimecache,xdgmimealias,xdgmimeparent}.c`, `glib/gkeyfile.c` (S502),
  `glib/gshell.c`, `glib/gutils.c`; freedesktop "Association between MIME types and applications" 1.0.1; host
  `shared-mime-info 2.5.1-2`, `glibc 2.44`.

Stagnation nudge: not claimed (capabilities entered at rounds 88–90). Every owned axis sits at 10, so the lowest-axis
obligation is a tie; C1 works coverage, C2 works operability. Sourced claim: C1 (S504–S507 opened this round; S502 reused).

## C1 — coverage (capability acquisition): default-application resolution as GLib 2.90.1 resolves it

Surface moved: the default-application plane (which `.desktop` application opens a MIME type or URI scheme — the
question `xdg-open`, file managers and OpenURI reduce to `g_app_info_get_default_for_type`), added to PROVINCE by the
round-91 refinement (R91MCritic F7). Edge classes the lane did not govern: `<desktop>-mimeapps.list`, the config/data
search order, Added/Removed/Default groups and their per-directory blocklist, defaults.list, mimeinfo.cache, masking by a
higher-precedence desktop file, the load rules (first group, Type, TryExec, Exec through `g_shell_parse_argv` and
`g_find_program_for_path`, Hidden — accepted for the default, dropped from the lists), MIME aliases (libc `qsort`/`bsearch`
for repeated aliases) and parent fallback from the text files or mime.cache, the GKeyFile rules (bytes, per-key UTF-8,
first-position duplicate keys, `[C]`/`[]` keys, `g_ascii_isspace`). Base: `git cat-file -e cc0381db:tools/mado-mime.py`
fails (0 MIME types resolvable by a lane tool). Deliverable: `tools/mado-mime.py` (= the frozen candidate
`.ufo/waves/round-91/build/mado-mime.c1.py`, sha256 `2532ccb57cf9d67f6590e4aac2e8d0a9f9eb011b25eb42e45118a6ff51871a5e`,
copied unchanged after the freeze), `corpus/knowledge/mime-default-resolution-r91.md`, a capability row.

- Oracle: `/usr/bin/gio` (sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`) with
  `libgio-2.0.so.0.9000.1` (sha256 `b38001cca69b2890a22fd3f6590bea7392bf489009de7ddfb6dbf296a133685e`), invoked only as
  `gio mime <TYPE>` under `env -i` with fixture-only XDG roots, `LC_ALL=C` (`controls/mime-oracle-r91.py`, sha256
  `c3a13e26173a0eca8bf137ced141c53485f7eca588d426ae6b636a52577bf6a8`).
- Cases: `controls/mime-cases-r91.json`, sha256 `15e4b3fc0af091d4c84da43394b711efeaa5d38acb18123b03089fb171020559`,
  **N = 268** (283 asked types): 93 `l1` (`controls/gen-c1-cases-r91.py`, incl. w01–w10 added from w1 findings), 91 `bl`
  (R91MScoutBlind, authored without opening the candidate), 65 `sh` (R91MExecShell), 12 `mc` (R91MMutC1), 4 `rv`
  (R91MReviewC1), 2 `fz` (R91MExecFuzz minimised), 1 `hx` (R91MExecHost); merged by `controls/merge-c1-cases-r91.py`
  (seat labels dropped), every label from one oracle run, re-checked `changed=0`.
- Fresh leg: **F = 120** cases from `controls/fuzz-gen-r91.py` (R91MExecFuzz, sha256
  `0d147b83f85d0a0d25be0282d21624bad8a4743f6964bda9b98b6ef996121418`) with seed = first 8 hex of the measured tool's
  sha256, labelled by gio at measurement time. The counter refuses `--fresh` < 1.
- Mutants: `controls/mime-mutants-r91.json`, sha256 `ed7716546bd7df57bdb78a315ba9d39bfae9a118fb7865b81b29e5524410fb04`,
  **M = 65** (L1 M01–M33 less M09/M10/M32; R91MMutC1 X01–X36 less X08); `equivalent_not_counted` M09, M10, M32, X08 with
  their arguments. A mutant whose only failures are crashes is `crashed-not-killed` (QUALITY 148).
- Sandbox (R91MCritic F2, corrected wording): the host filesystem is visible read-only; `/usr/bin/gio` and every
  `libgio-2.0.so*` under `/usr/lib`, `/usr/lib32` are masked with `/dev/null`; the lane repository (cases, labels, oracle)
  is a tmpfs; the scratch root is a tmpfs with only the per-run work dir (fixtures and tool copies, no labels) bound; no
  network, own pid namespace. Every scored tool (candidate, mutant, base) is the same file name in an opaque directory.
- Counter: `quality/counters/c1-r91-mime-resolution.py`, sha256
  `91ef46d17e0398c315f6b9ef3e5597ce67f105d93cc723b413cc1680576ede26`.
- **Predicate PRED-C1-r91-v1 (verbatim, = counter docstring):** TARGET_MET iff `<rev>:tools/mado-mime.py`, run on every
  frozen case (fixture tree + XDG_CURRENT_DESKTOP + PATH + the MIME types asked) inside a sandbox that hides
  /usr/bin/gio, libgio and the lane repository, prints for every asked type the same default application as the
  installed gio labelled, and — where gio printed a default — the same registered and recommended lists in the same
  order (correct == cases); does the same on every fresh case the frozen fuzz generator makes from seed = the first 8
  hex digits of the measured tool's sha256, labelled by gio at measurement time (fresh_correct == fresh); every frozen
  mutant of the tool returns a well-formed wrong answer on at least one frozen case (killed == mutants; a mutant that
  only crashes is crashed-not-killed, QUALITY 148); each control scores fewer than the case count (do-nothing, naive
  mimeapps.list reader, mimeinfo.cache-only reader, the base revision's tool — absent = 0); and the installed gio and
  libgio are the pinned binaries and still give every stored label (oracle_agree == cases).
- Pre-freeze controls, executed (`receipts/c1-controls-prefreeze-r91.txt`, DRAFT, rc 3 each): candidate `correct=268/268
  fresh=120/120 killed=65/65 oracle_agree=268/268`; do-nothing 63, naive 62, cache-only 102, base 0; **label-table
  forgery** (memorises all frozen labels, `controls/gen-forgery-table-r91.py`) `correct=265/268 fresh=19/120` →
  MISSED; **gio shell-out / ctypes libgio forgery** (`controls/forgery-gio-shellout-r91.py`) `correct=63/268 fresh=20/120`
  → MISSED (= do-nothing: the sandbox hides the oracle).
- Host evidence (QUALITY 146, not scored): one run of the measured tool against `gio mime` over every type the host's
  lists and mime db name, in the live environment; w1 draft: R91MExecHost 1211 types, 0 semantic differences.
- Measurement argv: `python3 -I quality/counters/c1-r91-mime-resolution.py --repo . --rev <C1 rev> --base-rev
  cc0381db585cc44c3dfc13ced807409c32c45bb0 --cases .ufo/waves/round-91/controls/mime-cases-r91.json --mutants
  .ufo/waves/round-91/controls/mime-mutants-r91.json --oracle .ufo/waves/round-91/controls/mime-oracle-r91.py
  --expect-cases-sha256 15e4b3fc… --expect-mutants-sha256 ed771654… --expect-oracle-sha256 c3a13e26…
  --expect-gio-sha256 d2164260… --expect-libgio-sha256 b38001cc… --fuzz-gen .ufo/waves/round-91/controls/fuzz-gen-r91.py
  --expect-fuzz-sha256 0d147b83… --fresh 120 --scratch-root DIR` (full digests above).
- Before → after: MIME types a lane tool resolves 0 → every type (tool absent at base); frozen set base 0/268 → 268/268.

## C2 — operability: a seat-report retention gate over the lane's wave dispatches

Surface moved: wave evidence retention. No lane check reads a dispatch's `Report:` trailers: at `cc0381db`
`quality/check-receipt-presence.py` and `quality/check-deliverables.py` say nothing about seat reports, and round 90 lost
two (M90-4). Deliverable: `quality/check-seat-reports.py` (= the frozen candidate `.ufo/waves/round-91/build/check-seat-reports.c2.py`,
sha256 `13c4b0a7dc4bbc39c70731dd35ec1f312c09f1a48f3b620e02945184d9cce39a`), modes `--rev`/`--worktree`, scope
`--round N`/`--all`, findings SR01 missing, SR02 empty, SR03 unsafe (absolute, `..` component, or symlink), **SR04
untrailed — a defect, rc 1** (R91MExecGate's independent labels; R91MCritic F4), summary `… unsafe=U untrailed=X
verdict=…`, exit 0/1/2, `--selftest` (16 checks incl. three rev-mode cases on a throwaway repo, R91MReviewC2 F2).

- Set: `controls/seat-reports-set-r91.json`, sha256 `9a05fa8ad4ef771eab9a6e9f4e8f22bfd01155483d92da2134274c705d5cb7dc`,
  **E = 59**: 8 lane rounds at `cc0381db` (42, 71, 83, 90 dirty; 86–89 clean) + `--all` (133 SR01 over 1732 seats), labels
  from R91MExecGate (plain `git ls-tree`/`cat-file`, candidate never opened; 133/133 equal to the candidate's output);
  50 fixtures: F01–F20 (L1), F21–F28 (R91MMutC2 §4 survivors), H01–H04 (git fixtures read `--rev HEAD`), G-fx01…G-fx15
  (R91MExecGate). Built by `controls/gen-c2-set-r91.py`.
- Fresh leg: **60** fixtures generated by the counter from seed = first 8 hex of the measured check's sha256; expected
  findings come from the generator's own choices (R91MCritic F3).
- Mutants: `controls/seat-reports-mutants-r91.json`, sha256 `7cf06df7dc0903e1291d00df4473d23b695f563bc9b24a2663d8c18348ebfcdd`,
  **M = 55** (L1 K01–K18 less K07; R91MMutC2 MC01–MC47 less MC12/MC15/MC19; exact duplicates dropped);
  `equivalent_not_counted` K07, MC12, MC15, MC19 with arguments.
- Counter: `quality/counters/c2-r91-seat-reports.py`, sha256 `c74f5baae915a4669ece5033a35ba16f5db0131a2db9a6e83a702de9e932d486`.
- **Predicate PRED-C2-r91-v1 (verbatim, = counter docstring):** TARGET_MET iff `<rev>:quality/check-seat-reports.py`
  meets every frozen expectation of the set — each lane-round expectation (run `--rev <frozen rev> --round N`: exit code
  and the exact set of SR01/SR02/SR03/SR04 findings as (id, wave, seat, path); seats/trailered counts), the `--all`
  expectation (exit code, SR01 count, seats), and each fixture (worktree, or a throwaway git repository read with `--rev
  HEAD`: exit code, the finding ids as a multiset, and the summary fields the fixture names) — meets every fresh fixture
  the counter generates from seed = the first 8 hex digits of the measured check's sha256 (expected findings taken from
  the generator's own choices; fresh == fresh_met); its `--selftest` exits 0 and prints `SEAT_REPORTS_SELFTEST: checks=N
  failed=0`; every frozen mutant of the check fails at least one frozen expectation or changes the selftest result line
  (killed == mutants); and each control meets fewer expectations than the set holds (the base revision's check — absent
  = 0 —, always-OK, always-MISSING, and quality/check-receipt-presence.py run with the same arguments).
- Pre-freeze controls (`receipts/c2-controls-prefreeze-r91.txt`, DRAFT rc 3): candidate `met=59/59 fresh=60/60 selftest
  checks=16 failed=0 killed=55/55`; base 0, always-OK 5, always-MISSING 0, receipt-presence stand-in 11.
- Measurement argv: `python3 -I quality/counters/c2-r91-seat-reports.py --repo . --rev <C2 rev> --base-rev
  cc0381db585cc44c3dfc13ced807409c32c45bb0 --set .ufo/waves/round-91/controls/seat-reports-set-r91.json --mutants
  .ufo/waves/round-91/controls/seat-reports-mutants-r91.json --expect-set-sha256 9a05fa8a… --expect-mutants-sha256
  7cf06df7… --fresh 60 --scratch-root DIR`.
- Before → after: lane checks that detect a missing seat report 0 → 1; frozen set base 0/59 → 59/59.
- This round's records commit carries a `--worktree --round 91` run of the gate (it names R91MScoutSources if that seat
  never writes its report).

## Separability

C1 lands first (`tools/mado-mime.py` + its ledger, registry, PROVINCE, index and knowledge rows); C2 second
(`quality/check-seat-reports.py` + its rows). C1 is measured at its own revision; the C2 counter at the C1 revision must
print `SETUP_ERROR … absent`; the C1 counter is re-run at the C2 revision.

## Routed work (not claims)

- D1: `quality/check-receipt-presence.py --selftest` (round-90 spot-check routed defect 1; R91MExecD1 copy: 87 added
  lines, 0 removed, `RECEIPT_PRESENCE_SELFTEST: checks=6 failed=0`); registry row updated.
- D2: this round's wave context named a report path for every seat, scouts included (routed defect 2); C2 checks it.
- D3: append-only note in `corpus/lessons/round-91.md` on the round-90 lesson wording (routed defect 3).
- Routed to round 92 (not landed): `tools/mado-portals.py` carries the GKeyFile divergences found here (`\v` as
  whitespace, whole-file UTF-8 voiding, duplicate-key reordering, `[]` keys dropped).
