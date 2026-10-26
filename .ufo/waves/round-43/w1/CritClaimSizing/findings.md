# CritClaimSizing — claim sizing and re-registration attack (mado round 43, w1, before any data)

Seat: `CritClaimSizing`. Base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`, freeze `b2e2efd6e268920d31f3c32cf52dc097dd6e1d22`.
No tracked file was edited; no mutating git ran. Scratch: `/fast/scratch/hyaku/mado-r43/CritClaimSizing/` (deleted at
seat close). Receipts cited below live in this seat directory, relative to the lane root:

| receipt | what it holds |
|---|---|
| `c1-copy-verbatim.txt` | the frozen C1 counter scoring a byte copy of the round-42 reference |
| `c1-copy-noselftest.txt` | the same copy with its selftest neutralised (registered cheat shape, re-confirmed) |
| `c1-copy-shas.txt` | sha256 of the reference and of the copy (identical) |
| `copy-verbatim-tool.py.txt` | the exact 417-line file that was scored |
| `c2-4new-receipt.txt` | the fixture, the command and the output of the 4-new-id C2 control, plus the whole admitted entry |
| `c2-4new-entry.md` | the 17-line entry that reaches `admitted=1/1` |
| `c2-3id-entry.md` | a weaker 18-line variant (3 own-work pins + one held id), also admitted |
| `c2-diff-classification.txt` | every changed line of the C2 r42→r43 diff, classified |
| `c2.diff` | the raw unified diff |
| `checks.txt` | history, freeze provenance, control tallies, axis receipt, separability greps, PINS vs fetch bytes |

## Verdicts

| # | finding | severity | fix before data? |
|---|---|---|---|
| F1 | C1's target is met by `cp` of the frozen round-42 reference | **HIGH** | yes |
| F2 | C2's target is met by a 17-line entry that cites **no** compositor source | **HIGH** | yes |
| F3 | C2's "end to end" is a universal clause the counter does not enumerate | MEDIUM (same root as F2) | yes, with F2 |
| F4 | "Every published axis ties at its maximum at base" is not enumerated by its receipt | LOW | prose only |
| F5 | separability sentence is an unenumerated universal negative (it does hold) | LOW | prose only |
| F6 | frozen seat count (37 w1 / 69) vs committed spec (38 / 70) | LOW | report note |
| — | re-registration is **not** a rule changed after data | cleared | — |
| — | C2 r43 **is** constants-only (42 changed lines, all classified) | cleared | — |
| — | control tallies and PINS are consistent | cleared | — |

## F1 — HIGH — the C1 target is reachable by copying the frozen reference

**Sentence attacked** (`registration.md:28`): "**Target:** `fixtures=37/37 tool=present verdict=TARGET_MET`, exit 0, at the data
commit and at the tip." with the claim at `:19-21` ("a new tool `tools/mado-geometry.py` … capability acquisition").

**Command** (scratch paths):

    cp .ufo/waves/round-42/c1/ctl-ref-tool.py.txt /fast/scratch/hyaku/mado-r43/CritClaimSizing/tools/copy-verbatim.py
    C1R42_TMP=/fast/scratch/hyaku/mado-r43/CritClaimSizing \
      python3 -I quality/counters/c1-r42-geometry.py --repo . \
        --rev a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f --nonce c1c1c1c1c1c1c1c1 \
        --tool /fast/scratch/hyaku/mado-r43/CritClaimSizing/tools/copy-verbatim.py

**Output** (`c1-copy-verbatim.txt`, exit 0):

    PRED-C1-r42 clauses=a:1 b:1 b2:1 b3:1 g:1
    PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET rev=a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f nonce=c1c1c1c1c1c1c1c1

`sha256sum` of the reference and of the copy are both `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`
(`c1-copy-shas.txt`). The scored file is the reference, byte for byte, 417 lines, unchanged — I wrote nothing, only copied it.
(With `--tool` the counter takes clause a from the file's presence; a real landing needs the copy committed at REV, which is one
`cp` + the round's data commit.)

**Why this is a sizing defect, not a counter bug.** Prompt §6 item 9 binds the lane to build "the cheapest control that skips
the claimed work … if it meets the target, the counter or target is wrong — fix it before data." The cheapest such control is one
`cp`, and it meets the target. The same artifact scored `met=1` in round 42 as the REF anchor (`receipts/ctl-c1.txt:2`:
`ok  REF … met=1 clauses=[a:1 b:1 b2:1 b3:1 g:1]`). So round 43's after-state cannot distinguish "acquired this round" from
"promoted round 42's control artifact": the capability the claim names was already demonstrated in round 42 by the reference.
The counter's declared residual ("a tool that CONTAINS a model of this contract is an implementation") admits a model-bearing
tool; it does not declare that the model-bearing tool is already committed in the lane and that installing it is the target.

**Impacted axis:** operability (the claim's own axis) — the round would score an axis move for a file copy.

**Smallest safe correction (before data).** Either
(a) declare the after-state honestly: C1-r43 is "`tools/mado-geometry.py` installed with the round-42 reference's behaviour",
    and say in the registration that the round-43 work is the installation plus the live host run — the live `hyprctl clients -j`
    join the counter explicitly does not score; or
(b) add one enumerable clause to the counter: `sha256(tool at REV) != e3c2e471…` (the reference).
(b) kills the literal `cp`, but a one-comment-different copy still passes and still carries the reference's model, so if the lane
wants a genuine acquisition target it has to name work the reference does not already do — (a) is the honest form.

## F2 — HIGH — the C2 target is met by an entry that cites no compositor source

**Sentence attacked** (`registration.md:30-34`): "**C2 … what determines the size of the host's gkeep window, end to end (host
rule text, `RE2::FullMatch`, the `size`/`float` effects, the floating algorithm, the target and window that store the box, the
animated variable behind `hyprctl clients -j` `size`, the client's own `set_default_size(420, 500)`, and today's host census)."

**Counter's minimum, as written** (`quality/counters/c2-r43-gkeep-entry.py`, clauses b, c, h): clause b requires ">= 4 distinct
`source: S###` lines"; clause c requires "ids absent from the BASE registry (at least 3)"; clause h requires "exactly three new
cited rows have kind own-work and their receipts are host-gkeep.conf, host-clients-r43.json and gkeep-ui-excerpt.py". Nothing
requires any of the seven Hyprland pins.

**Command** (`c2-4new-receipt.txt` reproduces it in full; it reuses the committed round-43 control harness's own `admitted()`
fixture with `REAL` reduced to four ids, drops the fixture's synthetic held id `S050` and its receipt, then calls the harness's
`score(..., "real")`, which runs the **frozen** counter):

**Output** (`c2-4new-receipt.txt`, exit 0):

    control=Q-4new-noheld-real expected=admitted=1/1 observed=admitted=1/1 verdict=TARGET_MET clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 rc=0
    entry-lines=17 cited=['S293', 'S297', 'S298', 'S299']

The whole admitted entry (`c2-4new-entry.md`) is: a title line, four `source:` lines, `verified-at`, `recheck:`, one `**OBS**`
line per id, and the three census lines. Its four ids are **NEW** and every one of their receipts is a real **PINS** file
(`Hyprland-Target.cpp`, `host-gkeep.conf`, `host-clients-r43.json`, `gkeep-ui-excerpt.py`) — no held id, no synthetic receipt, no
declared residual is needed for it. `S293` was my free choice among the seven upstream pins; the other six are optional.

Consequence, against the claim's own enumeration: the forced set is **3 own-work receipts + any 1 of 7 upstream receipts**. Five
of the eight named links are unforced — `RE2::FullMatch` (S290), the `size`/`float` effect chain (S291), the floating algorithm
(S292), the window-side storage (S294), and the animated variable behind `hyprctl clients -j` `size` (S295/S296). An entry that
answers none of them is admitted. The counter's own positive control P does cite all ten (`receipts/ctl-c2.txt:1-2`), so the
counter is capable of the ten-id shape; it merely does not require it.

**Impacted axis:** coverage — the entry that earns the coverage credit need not cover the chain the claim names.

**Smallest safe correction (before data; `registration.md:78-79` already allows a v2 re-registration for a w1 hole found before
the data commit).** Raise clause b's minimum to the ten PINS ids (seven upstream + three own-work), keeping clauses c/e per id as
they are; or keep `>= 4` and add a per-pin anchor requirement — each cited upstream id's Gate quote must contain its chain token
(`FullMatch`, `static_.size`, `windowGeometry`, `setBox`, `GEOMETRIC_GOAL`, `"size"`, `set_default_size`). Either change must be
followed by re-deriving `receipts/ctl-c2.txt` (74 controls), which the frozen predicate change costs.

## F3 — MEDIUM — "end to end" (`registration.md:31`) is a universal clause the counting command does not enumerate

Item 9: "Use no universal clauses ('all', 'complete', 'every', 'no harm anywhere') unless the counting command enumerates the
full set." The C2 counting command prints `PRED-C2-r43: admitted=N/1 verdict=…`; its clauses a–i (counter docstring) read: entry
presence, header lines, registry rows, Gate lines, location uniqueness, README index, per-id observation lines, the three census
lines and the assimilation pair. No clause reads the entry for the eight named links. F2's counterexample is the measurement of
that gap: `admitted=1/1` with five of the eight links absent.

`grep -c gkeep PROVINCE.md` → `0`; `corpus/README.md:37` and `:69` already index two gkeep entries (drift r12, bar-producer census
r40), so the coverage ground C2 opens is the geometry chain, not the application — the claim should name that ground, and the
word "end to end" should either go or be enumerated (F2's fix enumerates it).

**Smallest safe correction:** fold into F2 — replace "what determines the size … end to end (eight links)" with "an entry citing
all ten pinned receipts with a located quote each, plus the three census lines", which is exactly what the corrected predicate
would score.

## F4 — LOW — the lowest-axis sentence is not enumerated by its receipt

**Sentence** (`registration.md:13-14`): "**Lowest-axis rule.** Every published axis ties at its maximum at base
(`receipts/axis-base.txt`: navigation 59/59, calibration 63/63, operability 12/12, `MADO_AXIS checked=3 mismatched=0
rev=a35cfdf…`), so each is a lowest axis."

**Evidence** (`checks.txt`): `receipts/axis-base.txt` has exactly three `MADO_AXIS_ROW` lines and `MADO_AXIS: checked=3`;
`quality/check-axis-scores.py:32` — `AXES = ("navigation", "calibration", "operability")`. **Coverage — the axis C2 is declared
on — is in neither.** Coverage's saturation is recorded elsewhere in `SCORECARD.md` (`:1012` rubric V 6/6; `:1089` U-route 7/7,
both "harm watch"), but the registration does not name it, so "every published axis" is a universal whose set the receipt does
not enumerate.

**Impacted axis:** calibration (self-assessment). The conclusion survives on the SCORECARD lines; the sentence as written does not
carry it.

**Smallest safe correction:** "the three axes `check-axis-scores.py` re-derives tie at their maximum at base
(`receipts/axis-base.txt`); coverage's rubric V (6/6) and U-route (7/7) are saturated (`SCORECARD.md:1012`, `:1089`), so each of
the lane's two axes is a lowest axis." No counter change.

## F5 — LOW — the separability sentence is a universal negative with no named command (it does hold)

**Sentence** (`registration.md:42-43`): "… so C2 never runs C1's tool and C1 reads no C2 file."

Re-measured (`checks.txt`): `grep -c 'mado-geometry\|tools/' quality/counters/c2-r43-gkeep-entry.py` → `0`;
`grep -c 'corpus/' quality/counters/c1-r42-geometry.py` → `0`. The only `gkeep` strings in the C1 counter are fixture class pools
(`c1-r42-geometry.py:345,348`), not a read of C2's entry. The sentence is true; it is not backed by a named command.

**Smallest safe correction:** add the two greps to the separability paragraph (or point at this seat's `checks.txt`).

## F6 — LOW — the frozen seat count does not match the committed wave spec

**Sentence** (`registration.md:5-6`): "`w1` (build + first falsifiers, 37 seats) and `w2` … 32 seats; planned round total 69".

**Evidence** (`checks.txt`): `git log -1 --format='%h %s' -- .ufo/waves/round-43/w1-spec.json` →
`5add5b4 round-43: w1 spec, dispatch and validator registry (38 seats)`; `len(items)` = `38`. The spec was committed **after** the
freeze (`git ls-tree --name-only b2e2efd .ufo/waves/round-43/` → `ctl`, `fetch`, `receipts`, `registration.md` only), and
`w1.ready` / `w1.ready.dispatched` sit untracked in the worktree — the round-40 closure's routed defect (a) recurring.

**Smallest safe correction:** the round report states 38 w1 seats (70 planned), or the v2 freeze F1/F2 require carries the corrected
count. No claim is affected — the 1–3 claim cap is untouched.

## Cleared 1 — re-registering round 42's predicates is not a rule changed after data

- No seat scored either predicate in round 42: `.ufo/waves/round-42/w1/swarm-registry.json` has 36 members and **0** with an
  `agentId`; there is no `.ufo/waves/round-42/w2`; `find .ufo/waves/round-42 -name 'Report*' -o -name 'report*'` → 0 files;
  `git log --format='%h %s' 809dc2c..a35cfdf` → the round-42 spec commit, the honest-stop commit and the closure commit, no data
  commit (`checks.txt`).
- The frozen bytes are the bytes at the round-43 base:
  `git diff --stat 809dc2c a35cfdf -- quality/counters/c1-r42-geometry.py quality/counters/c2-r42-gkeep-entry.py` → empty.
- Provenance wrinkle (informational, no action): the orchestrator snapshot `8af0263` rewrote `c1-r42-geometry.py`
  (`+6/−17`: added `"#" not in body`, removed the timeout cap — `git diff --stat 809dc2c 8af0263 -- quality/counters/`), and a
  later round-42 commit restored the freeze bytes. Nothing scored in that window, so the rule was never changed after data, and
  the restore is what makes "frozen at 809dc2c" true of the file the counter runs today.
- The C1 sentence names two bases (BASE `62dd798` in `:26`, the round-43 base in `:27`); harmless —
  `git diff --stat 62dd798 a35cfdf -- tools/` is empty and tools/ holds 11 files with no geometry tool at either revision.

## Cleared 2 — PRED-C2-r43 is constants-only, exactly as declared

`diff -u quality/counters/c2-r42-gkeep-entry.py quality/counters/c2-r43-gkeep-entry.py` → 24 insertions / 18 deletions = 42
changed lines (one is a blank line). Every changed line classified (`c2-diff-classification.txt`):

    6   the inserted docstring note (the registration's "6-line docstring note")
    18  docstring label/path/date/receipt-name lines (title, entry path, verified-at, opened, lesson, fetch dir, host-clients name, final-line label)
    12  module constants: PRED, BASE_DEFAULT 62dd798→a35cfdf, ENTRIES, LESSON, FETCH, OPENED
    4   PINS: gkeep-ui-excerpt.py sha, host-clients-r42.json → host-clients-r43.json name+sha
    4   code lines that only rename the receipt inside clause h's own-work set and its json.loads

No clause text, regex or numeric threshold changed — "every clause is unchanged" (`c2-r43-gkeep-entry.py:1-7`) holds. The two
changed PINS are inputs to clause h rather than constants in the strict sense; the docstring note and `registration.md:37`
declare them, so the claim is accurate.

## Cleared 3 — control tallies and pins are consistent

- `receipts/ctl-c1.txt`: `controls=46`, 48 `ok` lines (REF + BASE-absent + 46), M=38 D=3 K=5,
  `CTL_C1 VERDICT: PASS (controls scoring TARGET_MET: 0 of 47; reference met: 1)`, exit 0 — matches `registration.md:59-61`'s
  definition (controls excludes the two anchors; the verdict denominator is controls + BASE-absent) and closes the round-42
  routed item 3.
- `receipts/ctl-c2.txt`: 74 `control=` lines, 74 `ok=1`, exit 0, matching `:57`.
- All ten C2 PINS match the committed `fetch/` bytes (`checks.txt`), so the constants-only counter pins the receipts the freeze
  committed.

## What I did not do

I did not judge the claims, edit any tracked file, run the round's gates, or touch the host session; no compositor verb beyond the
read verbs was needed and none was issued. No tool was installed or updated (nothing was needed). My two C1 runs and five C2
fixture scorings ran in the scratch directory, whose artifacts are copied into this seat directory; the scratch tree is removed at
seat close. `git status --porcelain` at seat close shows one tracked modification, `M LOG.md`, which no command of mine wrote (my
only writes are the two untracked seat paths); it is a concurrent lane write, not this seat's.
