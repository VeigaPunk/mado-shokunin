# ExecCounterC2 — C2 counter `PRED-C2-r51` (round 51 w1, mado)

status: complete. Counter draft + base/fixture receipts + controls are below. Nothing outside my
seat dir and my scratch was written; no tracked file was touched.

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Round base `6ca8c559a4a3d6d361101592116eea2bc7452437`
(lane tip at my start `3ac316426497e8649bffedc88d28241d9bc71c52`).
Counter bytes measured: sha256 `ebe39e1183375e0fb102124057eafecc9a21bdfc330c04ceb03759093d10e6dd`, 666 lines.

## Deliverables

- `.ufo/waves/round-51/w1/ExecCounterC2/c2-r51-dispatch-entry.py`
- `.ufo/waves/round-51/w1/ExecCounterC2/receipt-base.txt`
- `.ufo/waves/round-51/w1/ExecCounterC2/receipt-fixture.txt`
- `.ufo/waves/round-51/w1/ExecCounterC2/receipt-satisfiable.txt`
- `.ufo/waves/round-51/w1/ExecCounterC2/receipt-mutants.txt`
- `.ufo/waves/round-51/w1/ExecCounterC2/receipt-setup-errors.txt`
- `.ufo/waves/round-51/w1/ExecCounterC2/receipt-tip.txt`
- `.ufo/waves/round-51/w1/ExecCounterC2/receipt-draft-fit.txt`
- `.ufo/waves/round-51/w1/ExecCounterC2/receipt-draft-fit-v2.txt`
- `.ufo/waves/round-51/w1/ExecCounterC2/make-fixture.py`
- `.ufo/waves/round-51/w1/ExecCounterC2/mutants.py`

Integration for the L1: copy `c2-r51-dispatch-entry.py` byte-identically to
`quality/counters/c2-r51-dispatch-entry.py`. The code holds no path to its own location; everything
it reads is relative to `--repo` (`ENTRY`, `REGISTRY`, `README`, `FETCH_ROOT`, `WAVES`) or a git
object of `BASE`, so the copy needs no edit.

## What it checks (frozen sentence, clause by clause)

`python3 -I … --repo <lane> --rev <rev> [--work <scratch>]`; stdlib only; TMPDIR-honouring
(`--work`, else `mkdtemp(dir=$TMPDIR)`; a scratch dir inside the scored repo is refused before
anything is created). One diagnostic line per clause, then the frozen final line:

```
C2_R51: clauses=abcd clauses_met=<n> admitted=<0|1>/1 verdict=TARGET_MET|TARGET_MISSED rev=<full sha>
```

- **(a)** `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` exists at `<rev>` and an unfenced
  markdown table row of `corpus/README.md` at `<rev>` names it as `knowledge/<name>`.
- **(b)** rows S364–S379 cited by a `source:` line, each with `status = mined`, `opened = 2026-10-27`
  in the `corpus/SOURCES.md` registry at `<rev>`, and each bound to a pin the entry's pin manifest
  names (`| pin … |` table, first header cell starts with `pin`, annotated pin cells and shortened
  prose names resolve), that pin existing at `.ufo/waves/round-51/fetch/<pin>` at `<rev>`, with a
  quoted span (backticks / `"…"` / smart quotes / `quote=`) of ≤25 words that appears verbatim
  (whitespace-collapsed) in the pin's cited line span. The quote+locator pair may sit on any
  unfenced prose line naming the row (the `source:` line or an `**OBS** S364: `q`(Pin:line)` line);
  a quote written immediately before its locator is tried first. A manifest that declares a row
  column must declare this same row. ≥2 distinct rows required.
- **(c)** entry body (unfenced prose; `source/ground/held/verified-at/recheck/lane/pin` lines and
  table rows removed) as a set of word-8-grams over `[a-z0-9]{2,}`; containment
  `|entry ∩ ref| / |entry|` against **every** `corpus/knowledge/*.md` at the frozen base and
  **every** file under `.ufo/waves/round-*/candidate/` (recursive, read at `<rev>`); ≤30% per file,
  top-3 printed. Body must hold ≥300 distinct shingles, so a short stub cannot pass by percentage.
- **(d)** every line beginning `held` that cites `corpus/knowledge/<file>.md:<line>`: file present at
  base, line in range, and every pinned key token (`keys=a,b`; absent that, the backticked
  identifier spans on the line) present verbatim in that base line. ≥3 distinct `file:line`
  required. `held (cited, not re-registered): S### - …` lines carry no corpus path, are counted as
  `untargeted=` and score nothing.

Exit codes: `0` only on 4/4; `1` on any missed clause; `2` on setup errors (bad `--repo`/`--rev`,
base commit absent, base already holding the entry, unusable scratch). `C2_R51: meta …` and
`C2_R51: work=… probe=written` precede the final line; the scratch dir receives
`c2-r51-probe.json` (per-clause verdicts, top-3 overlaps, held citations).

## Receipts (exact text retained)

**1. Base — MISS, exit 1** (`receipt-base.txt`):

```
C2_R51: a ok=0 entry=absent
C2_R51: b ok=0 skipped=entry-absent
C2_R51: c ok=0 skipped=entry-absent
C2_R51: d ok=0 skipped=entry-absent
C2_R51: clauses=abcd clauses_met=0 admitted=0/1 verdict=TARGET_MISSED rev=6ca8c559a4a3d6d361101592116eea2bc7452437
exit=1
```

**2. Scratch fixture with the round-50 entry bytes at the C2 path — MISS via clause (c), exit 1**
(`receipt-fixture.txt`). Fixture `a506d8a3fd893ab80aad3c653d16a04b8dbbfdbf`: `git clone
--no-hardlinks` of the lane, branch cut at the base, one commit adding the round-50
`hyprland-bind-key-match-r50.md` bytes at the C2 path **plus** a source block (S364/S365 with
verbatim quotes and pin bindings), a pin manifest, three held citations, registry rows S364/S365
(`mined`, `2026-10-27`), the README index row and the two fetch pins — so (a), (b), (d) are met by
construction and only (c) can fail:

```
C2_R51: a ok=1 index_row=`knowledge/hyprland-dispatcher-dispatch-r51.md` (MADO-R51...
C2_R51: b ok=1 rows=2/2 pins=2
C2_R51: c ok=0 body_shingles=3399 files=66+cand3 max=99.1% top=[99.1%:corpus/knowledge/hyprland-bind-key-match-r50.md, 79.6%:.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md, 0.2%:corpus/knowledge/hyprctl-verification-layer.md]
C2_R51: d ok=1 held=3/3 lines=5 untargeted=2 tokens=5
C2_R51: clauses=abcd clauses_met=3 admitted=0/1 verdict=TARGET_MISSED rev=a506d8a3fd893ab80aad3c653d16a04b8dbbfdbf
exit=1
```

The top-3 line reproduces the round-50 falsification inside the counter: the recycled body scores
**99.1%** against its own base knowledge file and **79.6%** against
`.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md` — the candidate-inclusive baseline
round 50 lacked is now what catches it.

**3. Clause discrimination** (`receipt-mutants.txt`, driver `mutants.py`) — six one-change commits cut
from the control fixture, all MISS with the intended clause at `ok=0`: pins removed → `b`
(`pin_file_absent`); S364 status `queued` → `b` (`status:queued`); README index row removed → `a`
(`index_row=absent`); S364 quote removed → `b` (`quote_not_at_pin`); manifest binds the S364 pin to
S352 → `b` (`pin_row_mismatch:…=S352`); held token not on the cited base line → `d`
(`token_missing:keybind-rule-semantics.md:66:…`). Summary `mutants=6 fails=0`, exit 0.

**4. Satisfiability control** (`receipt-satisfiable.txt`, fixture `e0ef410e…`) — same rows/pins/held
with a freshly written control body: `c ok=1 body_shingles=451 max=0.0%`, final line
`clauses_met=4 admitted=1/1 verdict=TARGET_MET`, exit 0. The predicate is reachable; (c) is not a
wall.

**5. Setup errors** (`receipt-setup-errors.txt`) — unresolved rev, non-git `--repo`, and `--work`
inside the scored repo each print `C2_R51: setup error: …` and exit 2; the frozen TMPDIR-only form
(no `--work`) creates its scratch under `$TMPDIR` and MISSes at base, exit 1.

**6. Lane tip** (`receipt-tip.txt`) — `--rev 3ac31642` (entry still absent) MISSes, exit 1.

**7. Fit probe on the live draft** (`receipt-draft-fit.txt` v1, `receipt-draft-fit-v2.txt` v2) — each
built independently here in a scratch clone (branch cut at the base, draft at the C2 path, rows
S364–S369 from `w1/ScrRowsDispatch/rows.md` §1, the `w1/ExecFetchDispatch/fetch` pins under
`.ufo/waves/round-51/fetch/`, one README index row):

v1 (28964 B, 07:04) — `a=1 b=1 rows=3/2 c=1 max=0.1% d=0 held=0/3`, MISS.
v2 (27683 B, 07:10, fixture `969e3fcc…`) — all four clauses, exit 0:

```
C2_R51: a ok=1 index_row=`knowledge/hyprland-dispatcher-dispatch-r51.md` (MADO-R51...
C2_R51: b ok=1 rows=6/2 pins=6
C2_R51: c ok=1 body_shingles=2835 files=66+cand3 max=0.1% top=[0.1%:corpus/knowledge/bind-table-r25.md, 0.1%:corpus/knowledge/hyprland-bind-key-match-r50.md, 0.1%:.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md]
C2_R51: d ok=1 held=7/3 lines=8 untargeted=1 tokens=14
C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=969e3fccf6994523c39f94a0fcbafc6ad09ba3e4
exit=0
```

The same clone at the base still MISSes (`clauses_met=0 admitted=0/1`, exit 1). So the live draft is
novel (max 0.1% against 66 base entries and the round-49 candidate), binds six rows to six pins, and
carries seven held citations across six base knowledge lines — the predicate is satisfiable by the
lane's own entry, not just by my control. (The author's own run reported `held=6/3 tokens=12` on an
earlier revision of the same file; my count is 7 targeted `held:` lines plus one untargeted registry
line, all seven verifying.)

## Risks and notes for the freeze

- **(b) and (d) are shape-sensitive** and the frozen sentence is what w2 attacks. I sent
  `ScrDispatchEntry` the shapes twice (first the strict form, then the measured relaxations after
  reading its draft). Two relaxations were forced by the real draft and are documented in the
  module docstring: quote+locator accepted on any row-naming prose line, and annotated/shortened
  pin names resolved. A tighter reading would fail the lane's own draft on a form the sentence does
  not literally demand.
- **The counter certifies shape and binding, not truth.** A quote that verifies at a cited pin line
  can still be cherry-picked, and (c) measures reuse of *wording*, not of *facts* (the round-50
  held-fact omission class). w2 should attack both; `d` is the only clause that scores facts at all.
- (c) reads base knowledge and candidate files at `<rev>`; a candidate committed later in the round
  is in scope once committed.
- `MIN_BODY_SHINGLES=300` is the only threshold not named in the sentence; the round-50 body is
  3,399 shingles, the live draft 2,985.
- The setup guard `base already holds the entry` exits 2 rather than silently scoring against a
  wrong baseline; `--rev` may be any rev of the lane, as received at base and tip.
- Non-author adversaries for this clause are `CritC2Stub` and `CritHeldFacts`; I did not message
  them.

## Scratch and host discipline

All clones, fixtures and probe dirs lived under `/fast/scratch/hyaku/mado-r51/ExecCounterC2/`
(mkdir'd, deleted at finish; receipts copied into the seat dir first). Disk guard checked before
the first heavy pass: `/fast/scratch/hyaku` 63% used, 300.8G free; `/tmp` 3% used, 124.3G free. No
pacman transaction, no service restart, no tool install. No mutating git in the lane; the only git
mutations were inside scratch clones, each preceded by `git rev-parse --show-toplevel` asserting
the fixture root. Config planes untouched; no compositor socket used.

Report: .ufo/waves/round-51/w1/ExecCounterC2.md
