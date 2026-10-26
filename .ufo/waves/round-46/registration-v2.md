# mado round 46 — registration v2 (frozen BEFORE any round-46 data commit)

Supersedes both predicates of `registration.md` (freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`), as that file allows
("a hole wave `w1` finds before any data commit may re-register as v2 with a new freeze and new controls"). No data
commit exists: above the base `b22ea56b` the lane carries only the freeze `8c5434c6` and the w1 spec/dispatch commit
`e0be61e4`; `tools/mado-devices.py` and `corpus/knowledge/hyprland-input-devices-r46.md` are absent. Wave `w1` (66 seats,
policy v2) had written 63 of 66 reports when this was frozen; the three still running (CritC1Narrow, RevW2Counters,
ConnCalibration) are read after the data and reported, never used to change this registration.

Surfaces, axes, lowest-axis argument, separability (shown both ways by `w1/ExecC1Separability`) and the routed non-claim
work are unchanged from `registration.md`.

## Erratum to registration.md (not a predicate change)

- "The two cross-scope URL repeats" is wrong: five new rows reuse a held URL under another scope — S317 (S162/S303,
  legacy ConfigManager.cpp), S318 (S215, ConfigValues.cpp), S320 (S158/S307, HyprCtl.cpp), S321 (S182, MiscFunctions.cpp),
  S324 (S173, hyprlang config.cpp); the census prints five new W04 lines (`w1/CritRegistration` F1, `w1/CritPremise` A3,
  `w1/RevRows`).
- "per-device resolution was absent at base" holds for the resolution chain; the whole-dump join of `kb_layout` with
  `hyprctl -j devices` is held at `corpus/knowledge/hyprctl-verification-layer.md:159` (`w1/CritPremise` §1).
- The C2 control harness's single-occurrence assertion on S321's URL stopped the first run before any score; the
  runner was corrected to S323 before its receipt (`ctl-c2.txt`, commit `e0be61e4`).

## C1 — `PRED-C1-r46-v2` (replaces `PRED-C1-r46`)

- **Why.** w1 met PRED-C1-r46 with tools that implement nothing: a 12-line delegator that execs a copy of the reference
  found under `/fast/scratch` (`w1/CritClaimSizing` F2, `w1/CritC1Cheat` A/C), and clause r was bypassed by deleting the
  marker, by a bare `hyprctl` during `--selftest` and by `/usr/bin/hyprctl` called by absolute path (`w1/CritC1Cheat` B,
  `w1/SentTool` F1/F2; the live compositor socket was reachable too). The v1 contract was wrong against
  Hyprland/hyprlang on: strtof's single rounding, hex floats, `inf`, out-of-range values that leave the key unset
  (`w1/ExecStofOracle` D1-D7), a last line that still ends in a backslash (`w1/ExecHyprlangOracleB`), the directive
  trigger (`#hyprlangfoo if X`), `source =` inside a block and the VT/FF strip (`w1/CritToolSemantics` F1/F2/F7); three
  docstring sentences were false (kb_file, the virtual-keyboard rationale, FALLBACK as proof of a compile failure;
  `w1/CritToolSemantics` F3-F5, `w1/LabKbFile`, `w1/LabVirtualRules`).
- **Contract:** the docstring of `v2/mado-devices.py` (the v2 reference; selftest 59/59; live host run unchanged:
  9 AGREE, 1 VIRTUAL, OK).
- **Predicate:** the docstring of `quality/counters/c1-r46-devices-v2.py`: clauses a, s, f (110 fixtures of
  `quality/counters/c1-r46-fixtures-v2.json` = the 90 v1 fixtures re-cut to the v2 contract + 20 v2 additions, pinned;
  fewer than 100 is a setup error; three runs each), i (allowlist sandbox: only /usr and /etc of the host, the tool and
  fake-bin dirs read-only, the run dir writable; no /home, /fast, /run, /var, /tmp of the host), r (fake binaries on PATH
  and bound over /usr/bin/<name> write to an inherited pipe the counter reads; the selftest runs in environment A),
  g (150 nonce cases judged by the v2 reference, pinned by sha256).
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r46-devices-v2.py --repo . --rev <rev> --work <scratch outside /home/vgpnk/Projects/shokunin> [--nonce N]`
- **Before** (base): `receipts/c1-v2-before-base.txt` (`fixtures=0/110 ... tool=absent verdict=TARGET_MISSED`, exit 1).
  **Target:** `fixtures=110/110 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0, at
  the data commit and the round tip, under any nonce.
- **Kill rule:** anything else at the data tip is a miss, reported as an honest stop; no narrowing, no re-registration
  after data.
- **Controls** (`ctl/run-c1-controls-v2.py` → `receipts/ctl-c1-v2.txt`): REF (v2 reference) MET; BASE, STUB,
  MONITORS-COPY, V1-REF, DELEGATE-ANY, DELEGATOR-W1, CHEAT-A..D, TRIP-ABSOLUTE-PATH, TRIP-SELFTEST-ONLY and the variants
  V01-V28 (V21-V28 undo one v2 correction each) all MISSED.
- **On "the reference copied meets the target"** (`w1/CritClaimSizing` F1): the reference is the capability drafted
  before the freeze; installing it at `tools/mado-devices.py` IS the claimed landing, as in round 45. What a do-nothing
  control must not reach is the target without that capability, which the controls above test. Declared, not hidden.
- **Residuals (declared):** a tool holding a model of the contract is an implementation of it; a tool can detect the
  sandbox (PID 1 is bwrap) and behave differently on the host - inside it no copy of the reference is reachable; clause
  g's oracle is the reference, so a contract error shared by reference and tool is invisible to it (the w1 oracle seats
  and the non-author reading cover it); clause s is a printed line.

## C2 — `PRED-C2-r46-v2` (replaces `PRED-C2-r46`)

- **Why.** `w1/CritC2Forgery`: six forged revisions admitted outside the declared residuals (F4 README redirect, F5d a
  falsified uncited row on a pinned URL, F6 an anchor cell naming unread lines, F7 a receipt authored by the scored
  revision, F8 indented code in no pin, F10 the chain replaced by a citation index); `w1/RevC2Counter`: `OK` missing from
  the T4 tokens. Entry prose defects found by `w1/ExecC2Census` D1-D5 and `w1/CritEntryContent` H1-H8 are fixed in the
  v2 draft `v2/entry.md` (data side, not predicate).
- **Predicate:** the docstring of `quality/counters/c2-r46-input-device-entry-v2.py`: v1 clauses a-j plus clause k (A-G:
  quote inside its row's anchor ranges; README row without redirect words or another knowledge path; cited receipts
  byte-equal at `8c5434c6`; indented code verbatim in a pin; uncited rows on pinned URLs unchanged; no orphan row on a
  pinned URL or naming the entry; >= 5 numbered steps carrying every surface) and `OK` among the T4 tokens.
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r46-input-device-entry-v2.py --repo . --rev <rev>`
- **Before** (base): `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-v2-before-base.txt`). **Target:**
  `admitted=1/1 verdict=TARGET_MET`, exit 0, at the data commit and the tip. **Kill rule:** as C1.
- **Controls** (`ctl/run-c2-controls-v2.py` → `receipts/ctl-c2-v2.txt`): P (`v2/build-pos.py` on a clone of this freeze)
  admitted; the 14 v1 controls plus F4-README-REDIRECT, F5D-ORPHAN-FALSIFIED, F6-ANCHOR-WRONG-LINES, F7-SELF-RECEIPT,
  F8-INDENTED-CODE, F10-INDEX-NOT-CHAIN and OK-TOKEN rejected.
- **Residuals (declared):** as v1 (claim-to-quote binding, word-form census contradictions, registry prose cells, the
  sentence around a locator) - `w1/CritC2Forgery` F1, F2, F3, F9 stay residuals for the non-author reading.
