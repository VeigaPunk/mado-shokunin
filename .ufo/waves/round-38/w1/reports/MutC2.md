# MutC2 — mutation test of `quality/counters/c2-r38-eventq.py` (mado round 38, wave 1)

Attacked the landed C2 operability counter (`PRED-C2-r38-v3`) with the seven assigned
mutants plus one compound and one variant, scored each against a scratch copy of the
frozen manifest with the lane's discrimination gate, and root-caused every survivor
with direct counter runs on hand-built sandbox cribs.

**Result: 2 killed / 7 survived (of the assigned 7: 1 killed / 6 survived).**
Every surviving mutant is an unexercised clause; one of them (`full_table`) is also
**defective as coded** — demonstrated accepting the exact crib shape the docstring
claims to reject.

## Method

Detector: `quality/check-r38-discrimination.py` (the lane's own gate), run as:

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-r38-discrimination.py \
  --c1 quality/counters/c1-r38-event-ground.py \
  --c2 <counter — lane pristine, or /tmp/mado38-MutC2/mutants/<mutant>.py> \
  --manifest /tmp/mado38-MutC2/controls/manifest.json \
  --rev bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5 \
  --sandbox-root <unique per-run parent> --out /tmp/mado38-MutC2/runs/<run>.txt
```

- `--c1` always the pristine lane C1 counter; `--manifest` a scratch copy of the frozen
  `MANIFEST-r38-v1` (19 controls); `--rev` pinned to the lane HEAD sha `bb1adce4…`
  (pinned, not the moving word `HEAD`, so every control in a run resolves identically
  even if a sibling commits mid-run).
- Gate semantics: exit 0 + `verdict=TARGET_MET` (19/19 agreement) = mutant **SURVIVED**;
  exit 1 + `correct<19` = mutant **KILLED** (the flipped control is the detector).
- Legs: pristine → mutated → restored. Kill criterion per role: a baseline failure is
  inconclusive, not a kill.
- Mutants were built as copies in `/tmp/mado38-MutC2/mutants/` (pristine copy sha-verified
  against the lane file first); the lane was never written. All git writes happened in
  sandbox clones with the sandbox identity; no socket was touched; no subagents.

## Baseline legs

1. **First pristine attempt — inconclusive** (sandboxes on the contended `/tmp` mount;
   two transient clone failures; per role, not a kill and not a pass):
   ```
   control=c1-duprow instrument=c1 expected=TARGET_MISSED observed=ERROR ok=0 note=clone-failed
   control=c1-r28-verbatim instrument=c1 expected=TARGET_MISSED observed=ERROR ok=0 note=clone-failed
   MADO_R38_DISCRIMINATION: controls=19 correct=17/19 verdict=TARGET_MISSED
   ```
2. **Clean pristine reference** (`runs/pristine-new.txt`, current checker):
   `MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET`, exit 0.
3. **Restored leg** (after all mutation work; lane bytes sha-verified unchanged):
   `MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET`, exit 0
   (`runs/restored-final.txt`).

## Kill table

All rows re-run under the current HEAD checker (`581bf2ed…`); the earlier runs under the
pre-`b8400aa` checker (`529569f6…`) agreed in every case. Line numbers are pristine-file
lines of `quality/counters/c2-r38-eventq.py`.

| #  | Mutant (edit) | Clause attacked | Expected detector if exercised | Observed | Verdict |
|----|---------------|-----------------|-------------------------------|----------|---------|
| M1 | drop `proc_ok` from the live conjunction (`:248` → `live = int(sha_ok and replay_ok and full_table)`) | live-v3 `/proc` binding | `c2-proc-mismatch` | `c2-proc-mismatch expected=TARGET_MISSED observed=TARGET_MET ok=0`, `correct=18/19` | **KILLED** |
| M2 | drop the `ss_sha256=` term from `proc_ok` (`:242-243`) | live-v3 proc digest | a proc crib with correct inodes + wrong digest — none in manifest | 19/19, exit 0 | **SURVIVED** |
| M3 | drop `full_table` from the live conjunction (`:248`) | live-v3 snapshot shape | a subset-snapshot control — none in manifest | 19/19, exit 0 | **SURVIVED** |
| M4 | `sha_ok` → presence-only (`:221-222` → `any("tool_sha256=" in l …)`) | live-v3 receipt digest | a wrong-digest-receipt control — none in manifest | 19/19, exit 0 | **SURVIVED** |
| M5 | drop `and "connect(" not in src` from readonly (`:283-285`) | readonly | a `connect(`-in-code reject control — none in manifest | 19/19, exit 0 | **SURVIVED** |
| M6 | drop `blob is not None` from readonly (`:283-284`) | tool-presence | `c2-donothing` | 19/19, exit 0 | **SURVIVED** |
| M7 | delete the four v3-added CASES (`:105-120`: clients-first, client-no-users, comm-spaces, expect-present) → the v2 ten | fixtures | `c2-onepass` / `c2-missall` | 19/19, exit 0 | **SURVIVED** |
| M7b | delete the two SETUP cases (`:127-128` not-listening, `:136-137` unparseable) → 12 cases | fixtures rc=2 path | none exists | 19/19, exit 0 | **SURVIVED** |
| M4+M7 | compound (M4's edit on M7's file) | — | — | `c2-missall expected=TARGET_MISSED observed=TARGET_MET ok=0`, `correct=18/19` | **KILLED** |

## Per-mutant evidence

### M1 — proc-binding drop: KILLED (solely load-bearing clause, single detector)
```
control=c2-proc-mismatch instrument=c2 expected=TARGET_MISSED observed=TARGET_MET ok=0
MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED
```
(reproduced under both checker versions; `runs/m1.txt`, `runs/m1-proc-drop-new.txt`).
The `/proc`-binding clause is the **only** live-v3 subclause with a dedicated manifest
control, and `c2-proc-mismatch` is its single detector — a one-point enforcement.

### M2 — ss_sha256 drop: SURVIVED (term unexercised; demonstrated load-bearing)
- Why it survives: the only proc-artifact control, `c2-proc-mismatch`, forges a proc that
  names **0/3** of the snapshot's server inodes, so the inode-naming half alone rejects it.
  Direct run of the M2 counter on that control's sandbox:
  ```
  PRED-C2-r38-v3 live-detail replay=1 sha=1 full_table=1 proc=0/3 sha_in=0 agree=1
  PRED-C2-r38-v3 fixtures=14/14 readonly=1 live=0 tool=present verdict=TARGET_MISSED
  ```
- The term IS load-bearing against the complement crib — real committed proc with the
  `ss_sha256=` digest zeroed (inodes correct, `OVERALL: AGREE` intact): pristine counter
  `live=0 verdict=TARGET_MISSED` vs M2 counter `live=1 verdict=TARGET_MET`
  (probe s2a2, `live-detail … proc=3/3 sha_in=0 agree=1` in both).
- **Finding:** no manifest control forges a proc with correct inodes + AGREE + wrong
  snapshot digest; the `ss_sha256` consistency term is unpinned.

### M3 — full_table drop: SURVIVED (clause redundant as coded AND unexercised)
- **Redundant as coded:** `extra_rows` counts any data row without the `.socket2.sock`
  substring — and a client/peer row's local is `*`, so peer rows count. For any receipt
  whose client lines carry real holder ids (the committed receipt does), `replay_ok`
  requires the snapshot to replay to those ids, which requires the peer rows to be
  present, which makes `extra_rows >= 1` — i.e. **`replay_ok` ⟹ `full_table`**. The clause
  can never reject a snapshot that the replay clause accepts.
- **Demonstrated:** generated the tool's own `--snapshot-out` output from the real
  committed snapshot (6 lines, 1207 bytes — header + socket2 LISTEN/ESTAB rows + peer
  rows), committed it as `eventq-live-ss.txt` with the proc's `ss_sha256` re-digested to
  the subset, and ran the **pristine** counter:
  ```
  s2d tool --snapshot-out exit=0 ; subset_bytes=1207 subset_lines=6
  PRED-C2-r38-v3 live-detail replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
  PRED-C2-r38-v3 fixtures=14/14 readonly=1 live=1 tool=present verdict=TARGET_MET
  ```
  The docstring claims the snapshot "is not a `--snapshot-out` subset (it must name a
  request-socket or unrelated row too)" — the code does not enforce that; the exact crib
  shape it names is accepted.
- **Unexercised:** no manifest control commits any subset snapshot (the only
  snapshot-writing control, `c2-forged`, commits `CLEAN_SS` — caught by
  `snapshot-is-fixture`, and a full table anyway).

### M4 — accept tool_sha256 mismatch: SURVIVED (term unexercised; demonstrated load-bearing)
- Why it survives: every tool-mutating reject crib is double-caught. Direct run of the M4
  counter on the `c2-lagconst` sandbox:
  ```
  PRED-C2-r38-v3 case=clean want_rc=0 rc=0 ok=0
  PRED-C2-r38-v3 live-detail replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
  PRED-C2-r38-v3 fixtures=13/14 readonly=1 live=1 tool=present verdict=TARGET_MISSED
  ```
  The live clause fully passes under M4 (`sha=1`); the verdict is saved only by the
  `clean` fixture.
- The digest match IS load-bearing against a wrong-digest receipt (everything else real,
  `tool_sha256=` zeroed): pristine `live=0 verdict=TARGET_MISSED` (`sha=0`) vs M4
  `live=1 verdict=TARGET_MET` (probe s2e).
- **Finding:** no manifest control forges a wrong-digest receipt; the sha-digest term is
  unpinned. The compound M4+M7 confirms the flip side: with sha loosened AND the four
  v3 cases dropped, `c2-missall` escapes (`expected=TARGET_MISSED observed=TARGET_MET`).

### M5 — drop the readonly `connect(` check: SURVIVED (half unexercised; demonstrated load-bearing)
- The only control touching `connect(` is the **accept** control `c2-docconn` (mention in
  the tool docstring + receipt digest updated) — it proves the comment/docstring-aware
  scan does not false-miss, but no reject control plants `connect(` in code.
- The half IS load-bearing against a tool that really connects while evading the
  import-socket regex — appended dead branch
  `if __name__ != "__main__": __import__("socket").socket().connect(("localhost", 1))`
  (matches neither `\bimport\s+socket\b` nor `\bfrom\s+socket\b`, contains `connect(` in
  code) + receipt digest updated: pristine `readonly=0 verdict=TARGET_MISSED` vs M5
  `readonly=1 verdict=TARGET_MET` (probe s2f).
- **Finding:** the `connect(` subclause is unpinned; `c2-impsock` exercises only the
  import-socket half.

### M6 — drop tool-presence: SURVIVED (shadowed by the fixtures clause)
Direct run of the M6 counter at the `c2-donothing` rev (tool absent, `b4e47e98`):
```
PRED-C2-r38-v3 fixtures=0/14 readonly=1 live=0 tool=absent verdict=TARGET_MISSED
```
With the term dropped, `readonly` becomes 1 on the empty source, yet the verdict is still
MISSED because `met = passed == len(CASES) and readonly and live` already fails at
`passed=0`. **Finding:** the `blob is not None` term in `readonly` is a redundant belt —
the fixtures clause alone catches tool absence; the manifest cannot pin the term.

### M7 — fixtures reduced to the v2 ten: SURVIVED (v3 cases double-covered)
Dropping clients-first / client-no-users / comm-spaces / expect-present flips nothing:
the tool-mutating cribs (`c2-lagconst`, `c2-missall`, `c2-onepass`, `c2-stub-clean`) do
not update the committed receipt's `tool_sha256`, so the sha clause rejects them before
the new cases can act. The compound M4+M7 (sha loosened + cases dropped) is the probe
that proves the point: `c2-missall` flips to MET (18/19) — the `expect-present` case is
the last line of defense for that crib once sha loosens. `c2-onepass` stays caught even
in the compound (see mechanism note below).

### M7b — SETUP cases dropped: SURVIVED (rc=2 path unexercised)
Dropping `not-listening` and `unparseable` (the two `want_rc=2` SETUP cases) flips
nothing: **no manifest control drives a SETUP rejection** — every c2 reject control is
caught via fixtures-assertion failure, readonly, sha, replay or proc, never via the
rc=2 SETUP path.

### Mechanism note — the `clients-first` case is not `c2-onepass`'s actual detector
- The real committed snapshot **is** client-first:
  `s2h real-snapshot: socket2_server_rows=2 client_peer_rows=2 client_row_precedes_its_server=True`.
- But the manifest's `c2-onepass` py-write (excluding ESTAB client rows from `by_inode`)
  produces **order-independent placeholder clients** — the tool derives each client's
  `(comm,pid,fd)` from `by_inode.get(server_row["peer_inode"])["holders"][0]`, and with
  client rows excluded that lookup is always empty:
  ```
  s2h2 onepass-tool on CLEAN_SS:       exit=0 client_lines=2 comm_dash_placeholders=2 triples_equal_table_expected=False
  s2h2 onepass-tool on real-snapshot:  exit=0 client_lines=2 comm_dash_placeholders=2 triples_equal_table_expected=False
  s2h2 pristine-tool on both tables:   comm_dash_placeholders=0 triples_equal_table_expected=True
  ```
  So the crib is caught by the v2 `clean` fixture (asserts `comm=waybar …`) and by the
  live replay (placeholder triples ≠ receipt triples) regardless of row order — the
  manifest's `clause=clients-first` label for `c2-onepass` overstates what the
  clients-first case contributes.

## Findings (survivors = unexercised clauses)

1. **F1 (M1, killed):** the `/proc`-binding clause is the only live-v3 subclause with a
   dedicated detector, and `c2-proc-mismatch` is its single point of enforcement.
2. **F2 (M2):** `ss_sha256` consistency is unpinned — add a reject control: real proc
   with a wrong digest (correct inodes + AGREE). Demonstrated killable.
3. **F3 (M3, defect-grade):** `full_table` is redundant as coded (`replay_ok` implies it
   for real-holder receipts) and accepts the documented `--snapshot-out` crib shape
   (demonstrated: pristine TARGET_MET on a 6-line subset). Either tighten the predicate
   (count only rows outside the socket2 conversation — e.g. exclude rows whose inode or
   peer-inode belongs to it) or drop the clause as dead weight; today it is unexercised
   by the manifest either way.
4. **F4 (M4):** the receipt `tool_sha256` digest match is unpinned — add a reject
   control: wrong-digest receipt. Demonstrated killable.
5. **F5 (M5):** the `connect(` half of readonly is unpinned — add a reject control:
   `connect(` in code (evading the import-socket regex). Demonstrated killable.
6. **F6 (M6):** tool-presence in `readonly` is shadowed by the fixtures clause
   (`passed == len(CASES)` already fails when the tool is absent) — redundant belt,
   unexercisable as a sole defense.
7. **F7 (M7 + compound):** the four v3-added fixture cases are double-covered; the sha
   clause currently does the fixtures' job for tool-mutating cribs. Under the M4+M7
   compound, `c2-missall` escapes — the manifest's tool-mutating cribs are one sha-weaken
   away from relying on single fixture cases.
8. **F8 (M7b):** the SETUP rc=2 reject path is unexercised — no control drives it.
9. **F9 (mechanism):** `c2-onepass`'s committed crib is order-independent (placeholder
   clients on every table), so the `clients-first` fixture is not its actual detector;
   the manifest's clause label for that control is off.

## Environment record

- **Installs: none.** No tools were installed or updated.
- **Mid-run detector change (not mine):** fleet commit `b8400aa` (2026-10-25T11:23:56-03:00,
  "round-38 seat-fix fold: gate sandbox confinement…") replaced the checker
  (`529569f6…` → `581bf2ed…`). Diff verified: confined file primitives, `--shared` +
  sparse-checkout clones, checker self-cleanup — **scoring semantics unchanged**; my
  baseline/M1/M2–M7b legs ran on the old version, compound/restored on the new, and all
  legs were re-run under the new version with identical verdicts.
- **Disk hygiene:** found the gate's sandbox tempdirs accumulating on the 96%-full `/tmp`
  partition (~15.5G in 13+ dirs mid-baseline; the pre-`b8400aa` checker never cleaned
  them). At my cleanup checkpoint 0 dirs were >10 min idle (all in-flight), so none were
  deleted by me; my own runs used unique `--sandbox-root` parents with immediate
  cleanup. The `b8400aa` fold subsequently added checker self-cleanup and `--shared`
  sparse clones (runs dropped to ~17 s; `/tmp` now 74% used). No lane file was written
  by me at any point.

## Restoration evidence

| File | Before | After |
|---|---|---|
| `quality/counters/c2-r38-eventq.py` | `194a45c68f9e5756752daa8449dda1a7ae190ea016153b8e2e2a09c29f236921` | identical |
| `quality/counters/c1-r38-event-ground.py` | `6872e18d3003b5fcbf94adac4b259a4a3651d313e848dda8999572851fe71866` | identical |
| `.ufo/waves/round-38/controls/manifest.json` | `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8` | identical |
| `quality/check-r38-discrimination.py` | `529569f692e653b532cb4dcb0325efb43b3bcac0421d34754c0e4d0667f00d77` | `581bf2eda726de457d718033215ae5c49450df4703cc5058bccd14a1cde6c454` — changed by fleet commit `b8400aa`, not by me; lane working tree clean |

- Mutants and probe scripts lived only in `/tmp/mado38-MutC2/` and
  `/dev/shm/mado38-MutC2/` (both cleaned; 0 leftover `mado38-dsc-*` dirs).
- Run receipts (per-control lines + summaries for all 14 runs) preserved at
  `.ufo/waves/round-38/w1/scratch/MutC2/runs/`.
- Restored leg: pristine detector after all mutation work →
  `controls=19 correct=19/19 verdict=TARGET_MET`, exit 0.
