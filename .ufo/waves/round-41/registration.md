# mado round 41 — registration (frozen before any round-41 data)

Lane `mado-shokunin`, base `ab2bfaab661c846d1de9d58c01651cd156a13949` (the round-40 tip; `jj-lane.sh state` at round
start: `local=remote=ab2bfaa… ahead=0 behind=0`). Host `2026-10-25`, Hyprland 0.56.2 (`efb50993780079460b0cbed1363e2166a2de1d9f`).
Shape: one v2 wave `w1` of 64 seats (policy v2, band 64–128), no residual call, round total 64. The §3 planner seat is held by the L1.

**Lowest-axis rule.** Every published axis ties at its maximum at base (`receipts/axis-base.txt`: navigation 58/58, calibration 55/55,
operability 12/12, `MADO_AXIS checked=3 mismatched=0`), so each axis is a lowest axis; the stagnation nudge is not needed. Lane axes this
round: **operability** and **coverage**.

## Claims

- **C1 — operability (capability acquisition): `tools/mado-globals.py`**, a read-only census of the Wayland globals the compositor
  advertised to its desktop portal, read from the user journal (`journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`):
  sessions, per-global version and count, a fixed class decision table (focus-grab, input-synthesis, input-capture, session-lock, idle,
  clipboard, capture, toplevel-control, output-control, sandbox, other), `--diff` drift between the last two sessions, `--expect NAME`,
  `--live` (one allowlisted program, exact argv, bounded output). Before: the lane has no tool that reads the compositor's advertised
  protocol set (`ls tools/` holds ten files, none for globals; `tools/mado-globals.py` absent at base).
  - **Predicate `PRED-C1-r41-v1`:** the docstring of `quality/counters/c1-r41-globals.py` (the code is the same sentence): 24 fixtures
    (8 generated on a nonce lattice, 16 fixed) scored byte-exactly against the judge's model inside a bubblewrap sandbox, plus clauses a
    (tool at REV, absent at BASE), b (selftest k==n, n>=25), b2 (selftest teeth: 6 nonce-chosen comparison flips, >=4 killed), g
    (stdlib imports, no exec/eval/compile/`__import__`/os.system/popen/exec*, no `shell=True`, no judge strings).
  - **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r41-globals.py --repo . --rev <rev>`
    (a fresh nonce per run; printed on the final line and replayable with `--nonce`).
  - **Before** (base): `fixtures=0/24 tool=absent verdict=TARGET_MISSED`, exit 1 (`receipts/c1-before-base.txt`).
  - **Target:** `fixtures=24/24 tool=present verdict=TARGET_MET`, exit 0, at the data commit and at the tip.
  - **Kill rule:** anything else at the data tip is a miss, reported as an honest stop; no narrowing.
- **C2 — coverage (sourced): `corpus/knowledge/hyprland-focus-grab-r41.md`** — focus as a protocol surface: the Hyprland focus-grab
  protocol (interfaces, requests, the `cleared` event), its advertisement on this host (own-work journal census), a real client's grab
  lifecycle, and the rule-level counterpart; the lane holds none of it (`grep -rli 'focus_grab\|focus-grab\|focus grab' corpus PROVINCE.md
  SKILL.md tools` is empty at base). It is the successor of two staged package entries, re-grounded this round, and rests on `SOURCES.md`
  rows opened this round (the §2b sourced claim).
  - **Predicate `PRED-C2-r41-v1`:** the docstring of `quality/counters/c2-r41-focus-entry.py` (clauses a–i).
  - **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r41-focus-entry.py --repo . --rev <rev>`
  - **Before:** `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-before-base.txt`).
  - **Target:** `admitted=1/1 verdict=TARGET_MET`, exit 0. **Kill rule:** as C1.

**Separability.** C1 touches `tools/mado-globals.py` only (plus the C1 receipts). C2 touches the entry, registry rows, the lesson `## Gate`
and the README index; its own-work row is a *saved journal*, parsed by C2's own parser, so C2 does not read C1's tool and C1 does not read
any C2 file. Each is verifiable without the other having landed (`git show <rev>:` of the other's paths is not read by either counter).

## Controls (committed receipts at the freeze)

- **C1:** `receipts/ctl-c1.txt` — `CTL_C1`: the reference (`c1/ctl-ref-tool.py.txt`) reaches TARGET_MET; three do-nothing controls (empty tool, an
  echo of the NO_SESSIONS report with a constant selftest, a hardcoded plausible report) and 43 single-defect mutants / single-edit cheats
  of the reference each score below MET. Do-nothing floor: the base (tool absent) scores `0/24`.
- **C2:** `receipts/ctl-c2.txt` — `CTL_C2`: control P (a fabricated self-consistent set) is admitted (`1/1`: the declared residual); 40
  mutants each score `0/1`.
- `receipts/freeze-counter-check.txt` — criterion 64: every counter/checker path this file names exists at the freeze commit.

## Frontier step (§2b) — declared, not a claim

- Census before: `receipts/census-before.txt` (`mado ok`, W04 ×7 + W01 S277, exit 0); after: `receipts/census-after.txt`, exit 0 required.
- Assimilation (operator directive 2026-10-24/25): ONE theme from `merge/mado/` — **focus control surfaces** (the staged
  `focus-control-surfaces-r28`, `focus-grab-protocol-live-on-host-r14`, `privileged-client-surface-r29`, the focus-grab r8–r15 series,
  `compositor-focus-manipulation-literature-r26`, `wayland-input-security-literature-r8`). Admit target: one successor entry
  (C2), re-grounded in-round with this lane's own access dates and quotes; refuse target: `privileged-client-surface-r29` (generic
  Wayland analysis, truncated quote, no measurement) and the Japanese-channel section of `focus-control-surfaces-r28` (PROVINCE.md
  excludes localized-documentation material). The id-collision guard runs in scratch first and is proved on an indented row; the quarantine
  slice (`absent-defect-register.md`, lane `mado`) is re-derived and hand-checked for the rows the entry cites.
- considerthese: at most one still-unimplemented proposal of `considerthese/2026-10-25.md` is mined (chosen by a seat, recorded in the lesson).
- Mistake mining: `corpus/lessons/round-41.md` `## Mistakes` — M41-n from this round and the round-40 spot-check's routed defects.

## Residuals (declared)

- C1: a tool that **contains** the reference parser and class table is an implementation; the stub's canned journal is in the stub and a
  tool that decodes it without running it passes; clause g is a heuristic, the sandbox is the boundary; a hang (`--live` timeout) is not
  exercised by a fixture. The host receipt (`--live` against the running desktop) is reported, not scored.
- C2: see the counter docstring (fabricated self-consistent set passes).
- The wave may falsify these predicates; if so the L1 re-registers as `registration-v2.md` before any data commit and discloses the order,
  as round 40 did.
