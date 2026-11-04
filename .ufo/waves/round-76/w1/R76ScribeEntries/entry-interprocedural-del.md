---
source: own-work — committed round-76 declaration, controls and C2 measurement (locators below); predecessor corpus/knowledge/guard-carrier-copy-del-r75.md
verified-at: 755b339f1f6ec18f45b494d40515aecdbe9ceb73 (recorded measurement revision; not a new execution)
---

# Interprocedural and dynamic-key guard deletion (round 76, C2)

## Evidence locators

All paths are relative to the lane root; aliases preserve exact committed path:line citations.

| Alias | Committed path |
|---|---|
| D | `.ufo/waves/round-76/claims-declaration-r76.md` |
| F | `.ufo/waves/round-76/controls/c2-cases-r76.json` |
| M | `.ufo/waves/round-76/measurement-c2-r76.txt` |
| B | `.ufo/waves/round-76/control-baseline-r76.txt` |
| P | `corpus/knowledge/guard-carrier-copy-del-r75.md` |

## Two bounded deltas

The predecessor cancellation rule covers a literal-key delete in the same scope only; it explicitly excludes interprocedural and dynamic-key flow (P:25-30,64-67). Round 76 adds the following syntactic cancellations (D:133-143).

| Rule | Cancellation condition | Boundary |
|---|---|---|
| D3 | A live `del m[KEY]` in local `f(m)` removes the guard on the mapping passed to `f(env)` | Call line strictly between guard line and first launch use; simple positional first argument; callee key literal or module constant |
| D4 | `del env[k]` removes the guard when `k` resolves to its key | Same-scope name bound exactly once before deletion to a literal or module constant |

Rule provenance: D:133-143. The tested guard key is `GIT_NO_REPLACE_OBJECTS` (F:290,296,308,356).

## The twelve appended cases

The frozen set contains 59 cases, including 47 byte-identically carried predecessor controls; its sha256 is `df9e89841ed560613d7a05ad50f345b2d6bbf0d8e40a98f51e8b8134492b3948` (D:108-112; M:1-2). Every appended case is labelled reader=yes; the table gives guard labels and measured classifications (D:114-127; M:70-81,130-141).

| Case | Expected reader / guard | Candidate guard / held guard | Shape or negative boundary | Source; candidate receipt |
|---|---|---|---|---|
| `callee-del-literal` | yes / no | no / yes | Callee deletes from guarded literal mapping | F:289-292; M:70 |
| `callee-del-store` | yes / no | no / yes | Callee deletes after explicit store | F:295-298; M:71 |
| `callee-del-param-rebound-live` | yes / yes | yes / yes | Parameter copied with `m = dict(m)` before delete | F:301-304; M:72 |
| `dynamic-key-del` | yes / no | no / yes | Local `k` is guard-key literal | F:307-310; M:73 |
| `callee-del-other-key` | yes / yes | yes / yes | Callee deletes `PATH`, not guard key | F:313-316; M:74 |
| `callee-del-dead-branch` | yes / yes | yes / yes | Delete under `if False` | F:319-322; M:75 |
| `callee-never-called` | yes / yes | yes / yes | Deleting helper is never called | F:325-328; M:76 |
| `callee-called-after-launch` | yes / yes | yes / yes | Call follows launch | F:331-334; M:77 |
| `callee-del-param-rebound` | yes / yes | yes / yes | Parameter replaced by keyless mapping | F:337-340; M:78 |
| `dynamic-key-other` | yes / yes | yes / yes | Local key constant is `PATH` | F:343-346; M:79 |
| `dynamic-key-rebound` | yes / yes | yes / yes | Key name rebound from guard key to `PATH` | F:349-352; M:80 |
| `dynamic-key-module-const` | yes / no | no / yes | Module constant names guard key | F:355-358; M:81 |

Held classifications: M:130-141. The two parameter-rebinding negatives are distinct: the live copy retains the key before deletion, while the keyless replacement does not (F:302,338). [INF] The keyless replacement example would raise `KeyError` if executed through its delete; its guard label therefore pins syntactic carrier identity, not successful runtime completion. The predecessor likewise distinguishes syntactic ordering labels from reachable execution (P:64-67).

## Recorded gain and limits

The pre-freeze held leg records 55/59 and names exactly the four missed cancellations (B:2). The measurement reports `population=20 readers=13 guarded=13 unguarded=0 controls=59/59 base_controls=55/59 verdict=TARGET_MET`, revision `755b339f1f6ec18f45b494d40515aecdbe9ceb73` (M:143). Thus 20 is the check-script population, 13 the reader subset; it is not a claim of 20 readers (M:3-22,143).

- Line order is not execution order; this remains a syntactic approximation that does not interpret values (D:139-143).
- D3 matches a simple call with positional first argument, not function aliases or call chains (D:139-141).
- A callee's delete key must be a literal or module constant, not a dynamic key (D:141-142).
- D3 is modelled in env-named/subscript carrier flows, not attribute flows (D:142-143).
- [INF] Passing these frozen cases is not proof for arbitrary Python control flow; the claim remains bounded by those declared approximations.

Provenance conflicts retained: F:3 says “thirteen appended” and mentions “name bound after the delete”, but the declaration enumerates twelve and the recorded corpus totals 59 = 47 + 12 (D:108-127; M:1-2). M:142 calls the held leg “round-74”; M:82 identifies the actual held counter as `quality/counters/c2-r75-shapes.py`. No label or instrument is rewritten by this entry.
