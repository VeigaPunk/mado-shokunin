# MutC1FrozenCounter — w2 FALSIFY report (round 50, attempt 2)

Seat: MutC1FrozenCounter. Target: frozen PRED-C1-r50 counter
`quality/counters/c1-r50-bind-entry.py`, sha256
`e162d6717915f5585c40853afa8223d0398e50f0de37da4fd02004d2b08a84c0`.
Detector command (all runs): `TMPDIR=<scratch>/tmp python3 -I <counter.py> --repo <clone> --rev <rev>`
on a `git clone -q --shared` of the lane under my scratch; lane counter never modified
(post-run sha256 equals the freeze pin, see `SHA256SUMS.txt`).

Verdict legend: SURVIVED = mutant verdict equals the pristine verdict at the scored rev
(the mutation is unobservable there — honest equivalence, a coverage finding only).
KILLED = the verdict changes; the mutated check is load-bearing on that input.
A surviving mutant is not permission to change the contract.

## Pristine control (baseline)

`--rev 906178b607f2071af7c2efec5aad976a8bfa5757` (data), clone of the lane:

```
PRED-C1-r50: clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1 verdict=TARGET_MET rev=906178b607f2071af7c2efec5aad976a8bfa5757
```

exit 0 — matches the freeze receipt `.ufo/waves/round-50/receipts/c1-at-data.txt`
byte-for-byte in the verdict line. Baseline is green; mutant comparisons below are against it.

## Per-mutant results at the data rev 906178b6…

### (a) Drop clause c entirely (registry rows never checked) — SURVIVED

Diff: in `score()`, the `clause_c(...)` call is replaced by `c_ok, head_pins = True, {}`
and `cl["c"] = 1` (mutant sha256 `e462a4eb…`). Row URL pinning, pin sha256/mode and
anchor-range checks never run; `head_pins` is emptied so downstream citation sets rely
on `bound_pins()` alone.

Data-rev output: `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1
verdict=TARGET_MET` exit 0. Honest equivalence: the data rows genuinely satisfy every
dropped check (`bound_extra=21` vs 10 pristine — `bound_pins` alone covers the row pins
that `head_pins` used to carry), so dropping c is unobservable on well-formed data.

Behavior-bearing proof (fixture F1, my scratch clone, commit
`84a2f83a48388317fcdefc6fd4198208a321e82a`): S352 row URL ref changed to the branch
`main`. Pristine: `clause=c id=S352 url_branch_ref:https://…/main/src/managers/KeybindManager.cpp`,
`c:0 … verdict=TARGET_MISSED` exit 1 (`run-F1-pristine.txt`). Mutant (a): all clauses 1,
`verdict=TARGET_MET` exit 0 (`run-F1-m_a-drop-c.txt`). The check bites; at data it is
honestly equivalent.

### (b) Weaken clause d to presence-only — SURVIVED

Diff: `clause_d` rewritten (mutant sha256 `f441c403…`) — a quote passes if it occurs
anywhere in the resolved pin; locator-out-of-pin, pin-not-cited-by-row, quote-length and
the `[a,b]` occurrence-range check are all dropped.

Data-rev output: `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1
verdict=TARGET_MET` exit 0. Honest equivalence: all 85 data quotes occur inside their
stated ranges, so presence-only is unobservable on well-formed data.

Behavior-bearing proof (fixture F2, commit `c2e9b16988fd7a1ab3dfc6a9a178849e3196ea6e`):
OBS-line quote locator shifted off its occurrence (`…ConfigManager.cpp:1616` → `:1617`).
Pristine: `clause=d quote_out_of_range line=77 pin=Hyprland-legacy-ConfigManager.cpp
q='if ((!KEY.empty()) || multiKey) {' at=[1616] range=1617-1617`, `d:0 … TARGET_MISSED`
exit 1 (`run-F2-pristine.txt`). Mutant (b): `d:1 … TARGET_MET` exit 0
(`run-F2-m_b-d-presence.txt`). The range check is load-bearing; clause e's independent
step-range check still passed on F2 (e:1 both runs), so d is not redundant with e.

### (c) Remove the RECEIPT_NAME filter in clauses f/r (any receipt counts) — SURVIVED

Diff (mutant sha256 `9ff6fca4…`): clause f `named = list(cand)` instead of the
`RECEIPT_NAME.match(...)` filter; clause r's filter line removed likewise.

Data-rev output: `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1
verdict=TARGET_MET` exit 0. Honest equivalence: the data entry cites exactly
`binds-live-r50.txt`, which passes the name filter anyway, so the filter is unobservable
on this data.

Behavior-bearing proof (fixture F3, commit `73a4fc8e7746543ac501ed5ef9a4729e89aafa2c`):
a byte copy of the pinned receipt committed as `binds-live-fake.txt` and cited from the
entry instead. Pristine: `clause=f receipt_name=['binds-live-fake.txt'] want=^binds-live-r50\.txt$`,
`clause=r no_receipt_found`, `f:0 r:0 … TARGET_MISSED` exit 1 (`run-F3-pristine.txt`).
Mutant (c): `clause=f receipt=….ufo/waves/round-50/receipts/binds-live-fake.txt binds=192
forms=named:142,code:42,mouse:6,switch:2 sha=9a47199e2297 resolve=0`, `clause=r replay=ok`,
`verdict=TARGET_MET` exit 0 (`run-F3-m_c-receipt-any.txt`). The F2 repair pin is
load-bearing against receipt-name laundering.

### (d) Clause i accepts ground terms present at base — SURVIVED (honest equivalence)

Diff (mutant sha256 `5b57b080…`): the `ground_present_at_base` finding no longer sets
`ok = False` (it still prints a `…_ACCEPTED=` trace).

Data-rev output: `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1
verdict=TARGET_MET` exit 0. Honest equivalence, verified not assumed: every round-50
GROUND term (`xkb_state_key_get_layout`, `m_modifiersState`, `keysym_to_name`,
`xkb_keysym_get_name`) is absent from `corpus/` at base `8ae47b95…` — `git grep -F -q`
returns rc=1 for all four, so the dropped check has no input it could fire on at any rev
while the r50 tuple stands.

Behavior-bearing proof: combined mutant (d)+(e) (r49 GROUND tuple restored AND
base-presence accepted; sha `9a86ca9d…`-family combination, run output
`run-m_de-combined.txt`) at the data rev prints
`clause=i ground_present_at_base_ACCEPTED=xkb_state_key_get_one_sym rc=0` and
`…_ACCEPTED=m_xkbSymState rc=0` and reads `verdict=TARGET_MET` exit 0 — it re-admits
exactly what (e) alone rejects. So (d)'s dropped check is the one that would let the
stale round-49 ground back in; with the r50 tuple it is unobservable, with the r49 tuple
it is decisive.

### (e) Restore the round-49 GROUND tuple — KILLED (the load-bearing check)

Diff (mutant sha256 `9a86ca9d…`): `GROUND` restored to the round-49 tuple
`("xkb_state_key_get_one_sym", "m_xkbSymState", "keysym_to_name", "xkb_keysym_get_name")`
(read from `c2-r49-bind-entry.py` at base `8ae47b95…`, line 172-173).

Data-rev output:

```
PRED-C1-r50 hyprland-bind-key-match-r50.md clause=i ground_present_at_base=xkb_state_key_get_one_sym rc=0
PRED-C1-r50 hyprland-bind-key-match-r50.md clause=i ground_present_at_base=m_xkbSymState rc=0
PRED-C1-r50: clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:0 j:1 r:1 admitted=0/1 verdict=TARGET_MISSED rev=906178b607f2071af7c2efec5aad976a8bfa5757
```

exit 1. As the registration predicts, the round-49 closure text quotes both r49 terms
under `corpus/` at base and at data (`git grep rc=0` for both, verified on the clone),
so the frozen counter with the stale tuple rejects the data commit. The clause-i GROUND
re-base recorded in the freeze (registration.md, C1 repairs) is load-bearing; this is
the only assigned mutation that changes the verdict at the data rev.

## Summary table

| mutant | data-rev verdict | vs pristine | behavior-bearing probe |
|---|---|---|---|
| pristine | TARGET_MET (exit 0) | — | F1–F3 all TARGET_MISSED (exit 1) |
| (a) drop clause c | TARGET_MET | SURVIVED (honest equivalence) | F1: pristine MISSED / mutant MET |
| (b) clause d presence-only | TARGET_MET | SURVIVED (honest equivalence) | F2: pristine MISSED / mutant MET |
| (c) f/r any receipt | TARGET_MET | SURVIVED (honest equivalence) | F3: pristine MISSED / mutant MET |
| (d) ground-at-base accepted | TARGET_MET | SURVIVED (honest equivalence) | (d)+(e) at data: MET while (e) alone MISSED |
| (e) r49 GROUND restored | TARGET_MISSED (exit 1) | KILLED — load-bearing | fires at data itself |

## Restoration and hygiene

- Lane counter untouched: post-run sha256 of `quality/counters/c1-r50-bind-entry.py` =
  `e162d6717915f5585c40853afa8223d0398e50f0de37da4fd02004d2b08a84c0` (freeze pin).
- All clones/fixtures lived under `/fast/scratch/hyaku/mado-r50/MutC1FrozenCounter`
  (toplevel asserted for every fixture commit); scratch dir deleted after evidence copy.
- No host state written: HOME/XDG dirs for the replay were created by the counter inside
  TMPDIR under my scratch; hyprctl used read-only (`binds -j`, `getoption … -j`) by the
  frozen bytes themselves. No pacman, no lane/fleet writes; seat dir + this report only.
- Evidence: this file's sibling dir `.ufo/waves/round-50/w2/MutC1FrozenCounter/`
  (`run-*.txt` per run above, `SHA256SUMS.txt` with detector/lane hashes).

## Read for the L1

The freeze's counter is sound against all five assigned mutation classes: four are
honestly equivalent at the data rev (coverage findings — the data is well-formed, so
the dropped checks have nothing to bite; each was proven behavior-bearing on a dedicated
adversarial fixture), and (e) confirms the clause-i GROUND re-base is the load-bearing
repair. No counter change is supported by these probes; surviving mutants are coverage
notes, not contract edits.
