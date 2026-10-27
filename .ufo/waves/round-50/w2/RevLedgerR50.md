# RevLedgerR50 — live-state tool ledger classification gap (w2 falsify, round 50 attempt 2)

## Verdict

The w1/ConnLedger finding **holds at the attack revision and is now a live defect**: the only
live-state tool ledger in the lane (round-49 seat artifact) fails its own completeness rule at
`b4a79843` on exactly the two unpartitioned tools, and **no lane-level tracked ledger/checker
exists** — the ledger is a wave-seat artifact, not standing infrastructure. Both drafted
exclusions (keysym, hostguard) are delivered to this seat dir with cited class reasons; the lane
was not edited.

## The attacked artifact

- Ledger: `.ufo/waves/round-49/w1/ScrToolLedger/ledger.md` (12 rows + 3 ARTIFACT exclusions,
  generated from base `03e4ae76`).
- Checker: `.ufo/waves/round-49/w1/ScrToolLedger/check-ledger.py`; all-tools rule at docstring
  `:10-11` ("every blob under `tools/` at the revision is a row or a listed exclusion; a tool
  that is neither is a failure"), enforced in `derive()` at `:311-318`; base pinned at `:49`.
- w1/ConnLedger (`.ufo/waves/round-50/w1/ConnLedger.md`) verified the ledger at its own base and
  flagged the keysym gap; its "one bounded proposal" (partition all `tools/` blobs into live rows
  or cited exclusions) was never executed — no round-50 ledger exists.

## Finding 1 — checker fires at the attack revision (supports w1/ConnLedger; attacks any
"ledger is current" claim)

Command (scratch clone, never the lane tree):
`TMPDIR=<scratch> python3 -I .ufo/waves/round-49/w1/ScrToolLedger/check-ledger.py --repo <clone> --rev b4a79843cc2545bbe800db9322e58f6e00436629 --ledger <r49 ledger.md>`
Output (`receipts/check-at-attack.txt`, exit 1):

```
PROBLEM tool not covered: tools/mado-hostguard.py
PROBLEM tool not covered: tools/mado-keysym.py
LEDGER rows=12 excluded=3 problems=2
```

Boundary (`receipts/check-boundary.txt`): at the pinned r49 base `03e4ae76` the ledger
re-derives clean (`LEDGER-MATCH`, reproduces w1/ConnLedger's receipt); at round-50 base
`8ae47b95` only keysym is uncovered (1 problem); at data `906178b6` both are uncovered (2
problems, same as the attack rev). So the keysym gap dates to round-50 base and the hostguard
gap opened between base and the data commit.

## Finding 2 — no tracked lane-level ledger/checker exists (the claim that one does is a defect)

Search evidence at attack rev `b4a79843` (`receipts/tracked-ledger-search.txt`):
- `git ls-tree -r --name-only b4a79843 | grep -i ledger` outside `.ufo/`: only
  `quality/counters/c2-ledger.py` (the round-36 *evidence-ledger* counter — verified unrelated,
  its docstring names `PRED-C2-r36-v1`).
- The only tracked files outside `.ufo/` mentioning `check-ledger` / "tool ledger" /
  `ledger.md`: `corpus/lessons/round-47.md` (historical lesson prose).
- The only tracked ledger+checker copies: `.ufo/waves/round-47/w1/ScrToolLedger/{ledger.md,
  check-ledger.py}` and `.ufo/waves/round-49/w1/ScrToolLedger/{ledger.md,check-ledger.py}` —
  both wave-seat artifacts. Nothing in `quality/`, `tools/`, `corpus/`, the lane root, or the
  round-50 freeze (`registration.md` names no ledger among frozen artifacts).

Consequence: nothing in the lane gates on the ledger; the freeze claims C1/C2 do not depend on
it. But any prose (here or downstream) asserting "the lane carries a current live-state tool
ledger" is falsified by Finding 1 — the committed copies are stale by one and two tools
respectively, and the checker's own rule says so.

## Deliverable — the two drafted rows/exclusions (lane untouched)

Full draft with checker-dict and ledger-table forms, per tool: `RevLedgerR50/draft-ledger-additions.md`.
Summary (both drafted as exclusions, class `ARTIFACT`, per w1/ConnLedger's partition proposal):

1. **`tools/mado-keysym.py`** (present since round-50 base; sha256 `dcc13cce…` at attack rev) —
   exclusion: "Read-only. Starts no process, opens no socket, writes no file"
   (`tools/mado-keysym.py:4-5`); input is a caller-supplied keymap FILE and keysym
   (`:14-21`). Matches the three existing ARTIFACT exclusions (`check-ledger.py:136-146`).
2. **`tools/mado-hostguard.py`** (added base→data; sha256 `fdaa5c2e…` = the registration's frozen
   hash) — exclusion with an honest reason that does *not* claim "no host state": it pins "a
   declared list of operator-owned paths" (`tools/mado-hostguard.py:6-8`), "never creates,
   truncates or touches a declared path" (`:14`), and its one host-facing subcommand is
   read-only "lstat + sha256" (`:60-61`, `:182`). It dispatches no probe and joins no capture;
   the wrapped child is the caller's instrument, not this tool's.

With both added: 12 rows + 5 exclusions = 17 blobs = `git ls-tree --name-only b4a79843 -- tools/`
count — the partition closes. A retargeted checker must also move `BASE` off `03e4ae76`
(`check-ledger.py:49`) to the round-50 base and re-derive receipts there (w1/ConnLedger's core
complaint; still open).

## Residual risk / verification gaps

- The r49 checker's receipt sweep is expensive (~30 s/rev); the boundary receipt used a
  `--shared` clone and read-only git only.
- I did not run the two tools: classification rests on their committed docstrings and code
  literals cited above, consistent with w1/ConnLedger's keysym reading.
- Whether the L1 adopts a refreshed ledger is out of scope; the drafts are advisory and the lane
  is unedited.

## Artifacts

- `RevLedgerR50/draft-ledger-additions.md` — the two drafted exclusions, both forms.
- `RevLedgerR50/receipts/check-at-attack.txt` — checker at `b4a79843` (2 problems, exit 1).
- `RevLedgerR50/receipts/check-boundary.txt` — checker at `03e4ae76` / `8ae47b95` / `906178b6`.
- `RevLedgerR50/receipts/tracked-ledger-search.txt` — ls-tree/grep evidence no lane-level
  ledger exists; tools/ inventory + hashes at attack rev.
