# RevRegistrationV2 — findings (round 43, w2, seat review of the C2 v1→v2 re-registration)

Scope: the four assigned checks on `PRED-C2-r43` → `PRED-C2-r43-v2` (registration-v2.md, freeze
`496340dd53fabd800be42e8fb19090f35e2c235c`, made before data commit `1959770657f1f8665097c1aed4be6c1cbb07139f`).
All paths relative to the lane root. Every rerun below was executed fresh by this seat at the named revs;
nothing was taken from a receipt on faith without a rerun or a byte-compare.

**Verdict: all four checks PASS. No HIGH, no MEDIUM. Three LOW findings (two prose inaccuracies in
registration-v2.md, one docstring-scope nuance in the v2 counter) and two INFO notes. The re-registration
is sound: the freeze precedes the data, carries no data bytes, the diff is exactly the documented change,
every tightening has a rerun-verified killing control, and control P is admitted under the frozen counter
with true raw URLs.**

---

## Check 1 — commit order and content: PASS

- Order: `496340d` is the **direct parent** of `1959770`
  (`git show -s --format='%P'` on each; `git merge-base --is-ancestor 496340d… 19597706…` → ANCESTRY_OK).
  Author dates 2026-10-26 04:46:54 → 04:46:55 -03:00.
- The v2-freeze commit's stat touches ONLY `.ufo/waves/round-43/ctl/*`, `.ufo/waves/round-43/receipts/*`,
  `.ufo/waves/round-43/registration-v2.md` and `quality/counters/c2-r43-gkeep-entry-v2.py` (70 files,
  +2747) — no `corpus/`, no `tools/` path.
- **No data bytes at the freeze** (canonical paths):
  - `git ls-tree 496340d -- corpus/knowledge/hyprland-gkeep-geometry-r43.md corpus/lessons/round-43.md tools/mado-geometry.py` → empty (all absent).
  - `git show 496340d:corpus/SOURCES.md | grep -cE 'S29[0-9]'` → **0** (no new rows; earlier zero-counts
    in my session used a wrong `^source:` pattern — the registry rows are `| S29x |` table rows — redone
    with the correct pattern).
  - Held rows S155/S158 exist at `496340d` WITHOUT the entry used-by item; the data commit's
    `corpus/SOURCES.md` diff (+12/−2) appends `, corpus/knowledge/hyprland-gkeep-geometry-r43.md` to
    exactly those two rows and adds rows S290–S297.
- Counter blob identity across commits (`git ls-tree`):
  - v1 `quality/counters/c2-r43-gkeep-entry.py` = `a58c340221879e45780239ab25acbe2c722c0759` at
    b2e2efd, 496340d AND 19597706 (v1 untouched by the re-registration).
  - v2 `quality/counters/c2-r43-gkeep-entry-v2.py` = `03f007d3a4e97791a2e8edb68a62a7157576d0a9` at
    496340d and 19597706 (the scored predicate is the frozen one).
- **The freeze's fixtures are not landed-entry derivatives.** Rerunning the committed harness
  (`ctl/v2-forgeries/forge.py`, copied to scratch with only `WORK`/`SEAT` redirected) reproduces the
  committed fixture trees **byte-identically**:
  `diff -r <scratch>/fixtures-out/fixtures .ufo/waves/round-43/ctl/v2-forgeries/fixtures` → identical
  (15 tags). The fixture-P entry shares with the landed entry only the three census lines and
  `verified-at: 2026-10-26` (same host facts by design) — zero prose overlap (comm over sorted unique
  non-empty lines, LC_ALL=C).
- w1 grounding of the "why": `w1/CritClaimSizing.md` finding 2 (17-line entry, three own-work + one
  upstream receipt, `admitted=1/1`, five of eight claimed links optional, fix = require all ten PINS) and
  `w1/CritC2Cheat.md` (16 forged sets admitted; 8 closed by the seven string-local tightenings;
  A1/A2/D1/E2/H1/X1 declared residual) both exist and say exactly what registration-v2.md:5-8 cites.
  File mtimes 04:28–04:46, before the 04:46:54 freeze commit.

### INFO-1 (not a defect): one-second commit gap
`496340d` 04:46:54 → `1959770` 04:46:55. The DAG (parent link) is the ordering proof — a parent must
exist before its child is committed; timestamps are consistent with two consecutive scripted commits.
Git dates are client-controlled, so "frozen before data" is proven at **commit** granularity; that the
v2 counter's *source* was drafted before the entry's source is not provable from git and is not claimed
anywhere it would matter (the entry was written to satisfy the frozen predicate, which is the design).

## Check 2 — diff ↔ docstring correspondence: PASS (2 LOW)

`diff` of the two committed blobs (v1 `a58c3402…`, v2 `03f007d3…`) is **byte-identical** to the frozen
receipt `receipts/c2-v1-to-v2.diff` (`cmp` → IDENTICAL): 10 hunks, 97 changed content lines, 6 `---`
separators (one per change hunk — normal-diff format, not strays). This matches registration-v2.md:19's
"97 changed lines".

Every code change is stated in the v2 docstring (`quality/counters/c2-r43-gkeep-entry-v2.py`):

| code (v2 line) | docstring statement |
|---|---|
| 2 (title), 117 (`PRED = "PRED-C2-r43-v2"`) | docstring line 1, line 19 (final-line format), line 20 ("where it says PRED-C2-r43 read PRED-C2-r43-v2") |
| 294-349 `occurrences` / `strip_comments` / `quote_in_code` / `all_body_lines_bound` | lines 9-14 (d+: "EXACTLY ONCE, word-bounded, in its receipt's normalized text"; "with comments removed (C/C++ `//` and `/* */`; `#` in .py and .conf)"; g+: "EVERY unfenced entry line … carries that id's Gate quote and, for a non-HTML receipt, its computed locator") |
| 501-503 `len(occurrences(blob, nq)) == 1` + `quote_in_code(...)` in the clause-d good test | d+ (line 9-10) |
| 535-537 `rb.startswith('hyprland-') and not cells_[1].split()[-1].startswith('https://raw…efb5099…/')` | e+ (lines 11-12) |
| 576 `cl["g"] = int(g_ok and all_body_lines_bound(...))` | g+ (lines 13-14) |
| 582-583 `staged_ok` exact package path | i+ (line 15) |
| 587-589 flip-word regex in REFUSE reasons | i+ (line 16) |
| 596-597 `used = …; bad \|= not set(PINS) <= used` | i+ (lines 17-18, "all ten pinned receipts are cited") |
| 598 `bad \|= any(b_ in l.lower() for l in lines for b_ in BAD_LOC)` | i+ (line 16, "no BAD_LOC marker occurs in any unfenced entry line") |

Nothing in the docstring lacks code: all four v2 conditions (d+/e+/g+/i+) have code. The v1 clause
bodies are unchanged (line 20 is accurate on that point).

### LOW-1 — docstring cross-reference "(each also stated in its clause below)" is not literally true
`quality/counters/c2-r43-gkeep-entry-v2.py:8`. The clause bodies below (d, e, g, i) are unchanged v1
text and do NOT state the additions: v1 clause d has word-boundaries and normalized-text occurrence but
neither "exactly once" nor comment removal; clause e has no raw-URL prefix rule; clause g says "one
entry line", not "EVERY line"; clause i has neither the exact package path, nor the flip word, nor the
all-PINS rule, and scopes BAD_LOC to cited registry rows, not entry lines. The four conditions are
stated only in the header note (lines 9-18). Reproduction: `diff` the two counters — no hunk touches any
clause body; read v1 clause bodies in `quality/counters/c2-r43-gkeep-entry.py`. Behavioral effect: none
(the code enforces the header conditions). Fix: reword to "(each extending its clause below)" or fold
the conditions into the clause bodies at the next re-registration.

### LOW-2 — e+ as coded covers NEW ids only; the docstring sentence reads as all ids
`quality/counters/c2-r43-gkeep-entry-v2.py:525` (`for i in new_ids:`) vs docstring line 11 ("an id whose
receipt name starts with `Hyprland-` …"). A held id (present at BASE) cited with a pinned
`Hyprland-*` receipt is never e+-checked. Reachable shape [INFERENCE from code, not executed]: cite
held S287 (row frozen at BASE with location `https://github.com/hyprwm/Hyprland/issues/565`,
`corpus/SOURCES.md` at a35cfdf) with `GATE S287 receipt=.ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp
sha256=798b7c6c…` — clause d applies to held ids without the pin check, clause c keeps the row
byte-equal, so the admitted state would contain a `Hyprland-` receipt cited for an id whose location is
not a raw URL. In the landed round this is moot: S155/S158's rows already carry true raw URLs, and the
gap is adjacent to the DECLARED residual (claim-to-quote binding, A1 family). Fix: run the e+ check for
all cited ids (held rows at this BASE all satisfy it).

### LOW-3 — registration-v2.md says "three helper functions from the probe"; the diff carries four
registration-v2.md:19. `c2-v1-to-v2.diff` hunk `275a294,349` adds FOUR function definitions
(`occurrences` :296, `strip_comments` :314, `quote_in_code` :324, `all_body_lines_bound` :329), and all
four exist in the cited probe `w1/CritC2Cheat/probes.py` (lines 37, 55, 65, 70). Provenance claim is
right, the count is not. Behavioral effect: none.

Provenance verified beyond the count: `occurrences` is byte-identical between probe and v2 counter; the
other three differ only by string-escaping artifacts (probes.py embeds the counter source inside a
Python string, so `\*`, `\n`, `\s`, `\b` appear doubled there) — semantically identical. The probe's
PROBES dict (probes.py:94-113) maps 1:1 onto the v2 patch sites (`unique-occurrence` → :501-502,
`quote-not-in-comment` → :503, `every-naming-line-bound` → :576, `package-path-exact` → :582-583,
`url-exact-NEGATIVE` → :535-537), and the three more.py probes cover the remaining i+ sub-conditions.

Harness re-pointing verified: `diff w1/CritC2Cheat/forge.py .ufo/waves/round-43/ctl/v2-forgeries/forge.py`
→ only the docstring's scratch-path sentence + `WORK`/`SEAT`/`COUNTER`/`CTL`;
`diff …/more.py …/more.py` → only `WORK`/`COUNTER`/`CTL`. Matches registration-v2.md:26-27 ("only
`COUNTER`, `CTL`, `WORK` and the output dir changed").

## Check 3 — every v2 tightening has a killing control: PASS (rerun-verified)

The frozen logs are honest — rerun fresh (harness copied to scratch, only `WORK`/`SEAT` redirected;
`TMPDIR` under `/fast/scratch/hyaku/mado-r43/RevRegistrationV2/`):

- `forge-v2.log` ↔ rerun: identical (16 content lines; the frozen file adds one trailing `exit=0`
  capture line). Counter sha printed by the harness = sha256 of the committed v2 blob
  (`9a83407062d165661d211a714ce06b381391c7c4574c91c71eb54689dde1d028`) — verified by hashing
  `git cat-file blob 03f007d3…`.
- `more-v2.log` ↔ rerun: identical (10 content lines, same caveat).
- Result set: P, A1, A2, D1, E2, H1, X1 admitted (7); B1, B2, C1, C2, E1, F1, F2, G1, G2, X2, X3
  rejected (11) — exactly registration-v2.md:24-29's list ("still admitted: A1, A2, D1, E2, H1, X1").

Tightening → killing control (clause flags from the rerun):

| tightening | killed by | observed |
|---|---|---|
| d+ exactly-once, word-bounded | B1 (quote at 4 lines of WindowRuleApplicator, locator names another), B2 (locator names a non-first occurrence) | both `d:0 g:0 i:0` rejected |
| d+ comments removed | C1 (`// TODO: not very OOP, is it?` in DefaultFloatingAlgorithm.cpp:105), C2 (`// Reserved area…` in WindowTarget.cpp) | both `d:0 g:0 i:0` rejected |
| e+ true raw-URL prefix | G1 (`https://example.invalid/nope/Hyprland-Target.cpp`), G2 (`nowhere/DefaultFloatingAlgorithm.cpp`) | both `e:0` rejected |
| g+ every naming line bound | E1 (`**NOTE** S291 is unrelated…` names S291 without its Gate quote) | `g:0` rejected |
| i+ exact package path | F1 (`merge/mado/not-a-real-dir/…`) | `i:0` rejected |
| i+ flip word | F2 (`reason=this refusal says nothing else`) | `i:0` rejected |
| i+ no BAD_LOC in entry lines | X2 (Chinese-channel sentence in entry prose; isolated by the `bad-loc-in-entry` probe: P admitted, X2 rejected) | `i:0` rejected |
| i+ all ten PINS cited | X3 (own-work-only entry; isolated by the `all-pins-cited` probe: P admitted, X3 rejected) | `i:0` rejected |

Each i+ sub-condition is additionally isolated by a more.py probe that shows the sub-check alone kills
its forgery while P stays admitted (`probe=refuse-flip-marker`, `probe=bad-loc-in-entry`,
`probe=all-pins-cited` — P `1/1`, target `0/1` in the rerun). The still-admitted six are the declared
claim-binding residual (A1/A2/D1/E2/H1/X1) — consistent with w1/CritC2Cheat.md's classification.

## Check 4 — control P with true raw URLs matches the counter's e+ prefix: PASS

- `ctl/run-c2-controls-v2.py` differs from `ctl/run-c2-controls.py` ONLY in: the docstring title,
  `COUNTER` → the v2 counter, and the fixture rows' URLs — `CODE_ROWS` S290-S296
  `https://example.org/…` → `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/…`
  and `HELD_ROW` likewise (diff shown above, lines 38-49, 94). This is exactly registration-v2.md:30-31's
  "the v1 runner with the v2 counter and the true raw URLs in control P's code rows" (the HELD_ROW URL
  is part of P's fixture rows).
- Fresh rerun of the runner (`TMPDIR` in scratch; fixtures in `tempfile.mkdtemp` repos, toplevel
  asserted): `control=P-real … observed=admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1
  g:1 h:1 i:1 ok=1` and `control=P-patched … ok=1`; `CTL_C2: controls=74 correct=74/74`, rc 0, 74
  `ok=1` / 0 `ok=0`. Output matches the frozen `receipts/ctl-c2-v2.txt` line-for-line (modulo its
  trailing `exit=0` capture line). P-real runs the FROZEN counter over the REAL pinned receipt bytes
  (`blob(fn)` reads `.ufo/waves/round-43/fetch/`), so e+ passes against the true prefix with genuine
  receipts.
- The landed rows satisfy the same shape: at the data commit, S290-S294's location cells end with the
  true raw URL (last whitespace token = the URL, the counter's "location"), S295-S297 are own-work
  (e+ not applicable), S155/S158 held rows carry true raw URLs.
- End-to-end: `python3 -I quality/counters/c2-r43-gkeep-entry-v2.py --repo . --rev 19597706…` →
  `admitted=1/1 verdict=TARGET_MET`, rc 0, output matches `receipts/c2-after-data.txt` line-for-line
  (modulo `exit=0`). At base a35cfdf: `admitted=0/1 verdict=TARGET_MISSED`, rc 1 — matches
  `receipts/c2-v2-before-base.txt`. The v1 counter at the data commit also prints `admitted=1/1
  verdict=TARGET_MET` (the goal's "v1 also 1/1").

## Residual risk and verification gaps

- The w1-grounding reports (CritClaimSizing, CritC2Cheat, RevC2Counter F1, ExecC2ExtraMutants F1/F3)
  were read and their headline numbers matched the registration's citations; their internal fixtures
  were NOT re-executed by this seat (out of scope — w1 seats' own receipts cover them).
- LOW-2's forged held-id shape is argued from the code (e+ loop over `new_ids` only, clause d's
  no-pin-check for held ids, clause c's byte-equal rows) and the S287 row at BASE; the full forged
  fixture was not built.
- Commit-order proof is at commit granularity (DAG + absence of data bytes at the freeze); authoring
  order of the two sources is not provable from git (INFO-1).
- No host compositor read, no pacman, no mutating git, no writes outside the seat dir; scratch
  `/fast/scratch/hyaku/mado-r43/RevRegistrationV2/` removed at close. Tools used: python3 3.14.8, git
  2.56.0 (preinstalled) — nothing installed.
