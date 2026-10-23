# ReviewRegistration — registration.md vs landed commit 05319e0f

Reviewer: MadoR26.ReviewRegistration (UFO-FSD). Scope: pins, PRED sentences (byte-compare),
kill rule, claimed order, host-safety paragraph vs pilot receipt. No edits made; read-only review.

## Verdict

Registration is faithful to the landed state. Pins all match, PRED bodies are byte-identical
(modulo whitespace and the expected self-referential framing words), the kill rule is encoded in
the counters, order is satisfied (registration landed 146 s before the wave registry), and the
host-safety paragraph tracks the pilot receipt with one arithmetic inconsistency (finding M1) and
one wording slack (finding M3). No finding blocks the wave.

---

## Findings by severity

### Low

**M1 — coredump walk contradicts itself: four failed pilots ≠ 1330→1335 (+5).**
`registration.md:28-30` and `harness/pilot-receipt.txt:3-4` both say the four failed pilot runs
"each aborted and added one record (1330 -> 1335)". Four runs × 1 record = +4; 1330→1335 is +5.
`pilot-receipt.txt:16` independently records `before: hyprland_coredumps=1335` for the final run,
so five records predate it. Either a fifth failed run is unlisted (underreporting; the file claims
"this round's only coredumps … are named here") or one run added two records. The registration
copies the receipt's claim verbatim, so the defect originates in the receipt; it does not affect
the final method's isolation (delta 0) or any counter behavior.

**M2 — `coredumpctl` count includes the live session's own records, so the floor is not a pure
measure of this round.** `harness/oracle.py:70-74` (`coredumps()`) counts every
`/usr/bin/Hyprland` record in the catalog; currently 1335 (sampled during this review). The pilot's
before/after deltas are still meaningful (0 for the final method), and the counters' printed
`HOST_SAFETY` delta (c1:284-285, c2:220-221) is the operative check. Note: the host's own
live session is a Hyprland and would also appear if it ever crashed; the delta is unaffected.

### Info

**M3 — "same sentence in the receipt label" is not literal.** `registration.md:41` and `:60`
say the PRED sentence is "same sentence in … the receipt label". The receipts print the label with
outcome, not the sentence: `PRED-C1-r26 cases_pass=N/41 verdict=…` (c1:287) and
`PRED-C2-r26 cases_pass=N/51 embed_hits=E verdict=…` (c2:223-224). The sentence itself appears
only in registration.md and the docstrings. Wording slack, not a contract breach.

**M4 — `env -i` not literal in harness.** `registration.md:25` says the counter reaches the
instance "with the host's hyprctl under `env -i XDG_RUNTIME_DIR=<private>`"; the code builds a
fresh dict (oracle.py:129-131), which is equivalent but not `env -i`. Cosmetic.

---

## Checks performed (evidence)

### Pins at 05319e0f (registration.md:112-116) — MATCH

`git -C <lane> show 05319e0f:<path> | sha256sum`:

| path | registration.md claim | actual @ 05319e0f |
| --- | --- | --- |
| `.ufo/waves/round-26/c1/count.py` | `f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd` | same |
| `.ufo/waves/round-26/c2/count.py` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` | same |
| `.ufo/waves/round-26/harness/oracle.py` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` | same |

Secondary pins verified against the working tree: V3 generator sha256
`8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375` matches c2:20
(`count-v3.py`); oracle.py pins tinywl `227a74af…40cda` and libwlroots `1f3d7036…7967`
(oracle.py:26-29) — both full sha256s match the pilot receipt's line (pilot-receipt.txt:10).

### PRED sentences — byte-compare

Extracted the PRED-C1-r26 block from `registration.md:41-47` and from the `c1/count.py`
docstring (lines 5-14); same for PRED-C2-r26 (`registration.md:60-68` vs `c2/count.py:5-17`).
After whitespace collapse, the sentence bodies — from "At REV, the committed bytes" through
"cases_pass=41/41." / "embed_hits=0." — are **identical** in both pairs. The only differing tokens
are (a) the Markdown bold markers `**…**` and (b) the self-referential framing ("`c1/count.py`'s
docstring" ↔ "registration.md, this code"), which necessarily differ because each copy points at
the others. No substantive divergence.

Counts cross-check: NODES list has 34 entries (c1:29-34) + internal node = 35, matching the
pilot's `animation_nodes=35` (pilot-receipt.txt:14) and registration's "34 animation nodes +
internal node" (`registration.md:37`). C1 population 41 = 1 BASE + 40 generated (c1:236-245,
286-287); C2 population 51 = 1 BASE + 30 ARITH + 20 V3 (c2:175-188, 222-224).

### Kill rule (`registration.md:73-84`) — encoded

- Rule 1 (one commit before any control seat): commit 05319e0f contains exactly registration.md,
  harness/ (5 files) and the two counters; parent is 96101be5 (round-25 closure), matching
  `registration.md:5` and rule 5's base.
- Rule 4 (measurement: exit 0 TARGET_MET / exit 1 TARGET_MISSED / exit 2 measured nothing, kept
  and re-run): counters implement `die()` → prints `SETUP_ERROR`, `exit=2`, `sys.exit(2)`
  (c1:50-53, c2:40-43), and the full guard set: oracle.py sha pin (c1:56-63; c2:46-53), binary
  pins + render node via `O.check_build()` (c1:206-208, c2:124-127; oracle.py:48-57),
  `ORACLE_FAIL` (c1:253, c2:161/194), `ORACLE_UNSTABLE` via BASE-twice disagreement
  (c1:254-256, c2:163-165). Print of `HOST_SAFETY hyprland_coredumps_before=… after=… delta=…`
  present (c1:284-285, c2:220-221).
- Rule 5 (base runs): `git show 96101be5:tools/mado-anims.py` fails → `tool=MISSING_TOOL`
  (c1:223-226); round-25 tool exists at base for C2. Correct.

### Claimed order

Registration commit 05319e0f: `1792744851` (2026-10-23 05:40:51 −0300).
Wave registry `swarm-registry.json` `createdAt`: `2026-10-23T08:43:17.229Z` = 05:43:17 −0300.
Registration precedes registry by **146 s**. `controls/` directory exists but contains no files
(yet), consistent with "No control or data seat has run" (`registration.md:119`).

### Host safety vs pilot receipt

Checklist:

| registration.md claim | evidence | status |
| --- | --- | --- |
| coredumps 1335→1335 final (27-28) | receipt lines 12-17, `delta_coredumps=0` | ✓ |
| answered `binds -j` + `animations -j` (27) | receipt line 13 (`binds=192 animation_nodes=35 beziers=6`) | ✓ |
| exited on `dispatch exit` (26) | receipt line 5; oracle.py:203 | ✓ |
| binary pins tinywl/libwlroots (21) | receipt line 10 full hashes | ✓ |
| renderD129 amdgpu, no card node (24) | receipt lines 11, 14 (`card_nodes: []`, `render_mounts: ["/dev/dri/renderD129"]`) | ✓ |
| clearenv, no host WAYLAND_DISPLAY/inheritance (22-23) | receipt line 14 env = only `WAYLAND_DISPLAY=wayland-0` + `XDG_RUNTIME_DIR=/tmp/m26o-…` (sandbox-private); `netns_same: false` | ✓ |
| `LIBSEAT_BACKEND=noop`, `prlimit --core=0 --as=8000000000` (25) | oracle.py:16, 146-147, 157 | ✓ |
| `--tmpfs /run`, private XDG_RUNTIME_DIR under /tmp (23) | oracle.py:152-153; receipt line 14 | ✓ |
| four failed pilots each +1, 1330→1335 (28-29) | receipt lines 3-8 | **✗ arithmetic — M1** |
| "this round's only coredumps … named here" (29-30) | receipt lists 4 failures + no others; but +5 records — M1 | **✗ (same defect)** |

The pilot's isolation evidence is credible: independent host-view probe of the nested process shows
no card node, private env pair, and a fresh netns; leftover run dirs 0, nested processes alive 0
(receipt lines 15-17).

---

## Residual risk / verification gaps

1. Host-side versions are pinned by statement only: oracle.py invokes bare `Hyprland`/`hyprctl`
   (oracle.py:161, 130) with no version check; registration claims v0.56.2 as fact
   (`registration.md:15, 45`). The pilot receipt records `hyprctl` answers but not the binaries'
   versions; a host package change would silently alter authority. (Mirrors CritC2Design's
   finding, which I have not independently verified — I did not run any test tool.)
2. The 1335-record floor (current, sampled) predates wave runs; the receipt claims 1330 in the
   12 h before the round. Neither number is verifiable retroactively; delta-based checks are the
   operative ones.
3. Kill-rule items 2 and 3 (w2 order, data-seat rule) are future tense — cannot be checked yet.
4. The claim "same sentence in the receipt label" (M3) is not literal; a strict mechanical check
   would fail on it, but the label is the predicate ID + target, by design.

## Scope notes

Read-only review; no files modified. No subagents dispatched (leaf bound). No tools installed.
