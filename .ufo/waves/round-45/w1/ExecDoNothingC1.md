# ExecDoNothingC1 — cheap controls against PRED-C1-r45, round 45 w1

Seat: cheapest controls against C1 beyond the 16 registered. Full detail and all quotes with locators:
`.ufo/waves/round-45/w1/ExecDoNothingC1/controls.md`.

## What was done

Seven new controls were built and scored against the **frozen** predicate (unchanged, no re-registration) in a
scratch clone of the lane at `0c89478af821a6424c9ac922eafe02e39630cf4f`, each one committed as
`tools/mado-monitors.py` and scored with the predicate's own command. Reference calibration first:
`receipts/ref.txt` → `fixtures=49/49 … verdict=TARGET_MET rev=1131626c…`.

Four controls reach **TARGET_MET without the capability**:

| control | what it is | predicate |
|---|---|---|
| A `control-a-lookup.py` | embeds the predicate's `FIXTURES` (copied), inverts the seeded placeholder substitution by enumerating `names(seed)`, prints the table's expected lines | MET 49/49, also at `--seed 7` and `--seed 1234` |
| A2 `control-a2-obfuscated.py` | same table, zlib+base85-packed so no fixture text is a literal | MET 49/49 |
| B `control-b-counter-import.py` | `exec`s `quality/counters/c1-r45-monitors.py` from its absolute lane path and reuses its table | MET 49/49 |
| B2 `control-b2-reference-loader.py` | 13-line loader that `exec`s `.ufo/waves/round-45/l1-draft/mado-monitors.py`; the scored blob holds no implementation | MET 49/49 |
| E `control-e-proc-parent.py` | no hardcoded path: reads the parent's argv from `/proc/<ppid>/cmdline`, finds `c1-r45-monitors.py`, `exec`s it | MET 49/49 |

Two assigned shapes honestly fail, as the contract should force them to: C (`mado-geometry.py` + **19** added
lines) 1/49, D (exact host config) 4/49 — both MISSED.

**clause that should catch them:** A/A2 → clause `f`, which is not a capability test but a fixed case list;
B/E → clause `r` (`c1-r45-monitors.py:19`), whose scope is PATH only; B2 → clause `a`/`f`, since the blob at
REV is not the capability. **Tightenings, measured, keeping the reference MET:** (T1) three semantics-free
invariance re-runs per fixture — canonical JSON serialisation, one extra comment-only `--config` argument, and
the dump reversed — implemented in `tighten-check.py`; REF stays MET (49/49, 47/47, 48/48, 3/3) while A/A2/B
fall to 2/47, 1/48, 0/3. (T2) a read audit around the fixture call — no open under `/home`, none of
`/proc/<pid>/cmdline|environ` — in `read-audit.py`; REF/A/A2 PASS, B/B2/E FAIL. (T3) the same harness with
`--sandbox bwrap`: only the interpreter tree, tool dir and fixture dir exist; REF and A pass, B/E/B2 fail.

**Declared residual** (unescapable at this predicate): a table over a published finite case set is not
separable from a model by a/s/f; T1 raises the price but any table extended to the variants still passes, and
closing it would need fresh cases from a semantics oracle inside the predicate — which is the implementation
(the registration's own residual at `registration.md:32`). Clause `s` is also self-declared: every control
prints a passing selftest line without running a test.

## Files changed

Written only inside `.ufo/waves/round-45/w1/ExecDoNothingC1/` plus this report:

* `controls.md` — the control matrix, per-control receipts, tightening measurements, residuals.
* `control-a-lookup.py`, `control-a2-obfuscated.py`, `control-b-counter-import.py`,
  `control-b2-reference-loader.py`, `control-e-proc-parent.py`, `control-c-geometry-patch.py`,
  `control-d-host-config.py` — the seven controls.
* `tighten-check.py`, `read-audit.py` — the two tightening harnesses (proposals, not applied).
* `receipts/` — 30 files: predicate scores (REF and per control, plus A at seeds 7/1234), tightening scores,
  strace audits, bwrap runs, and `quote-check.txt` (each quoted source line verified by grep at its locator,
  plus the sha256 of every control file).

No tracked file was edited. The predicate, reference, controls receipt, registration, pins and counters are
untouched. No `pacman`, no compositor call, no git/jj mutation in the lane (only read-only `git -C`; all
fixture/commit work in a scratch clone whose `rev-parse --show-toplevel` was asserted before the first commit).
No tool was installed. Scratch `/fast/scratch/hyaku/mado-r45/ExecDoNothingC1/` deleted after the receipts were
copied here.

## Verification the main agent should run

1. `python3 -I quality/counters/c1-r45-monitors.py --repo <clone> --rev <ctl-rev> --work <scratch>` for any of
   the MET receipts' revs (rev hashes are in each receipt's last line).
2. `python3 -I .ufo/waves/round-45/w1/ExecDoNothingC1/tighten-check.py --repo <clone> --rev 1131626c… --work <scratch>`
   → MET 49/49, 47/47, 48/48, 3/3; and `--rev 57bfe5ec…` → MISSED.
3. `python3 -I …/read-audit.py --repo <clone> --rev <ctl-rev> --work <scratch> [--sandbox bwrap]` for PASS on
   REF/A and FAIL on B/E/B2.

## Risks / blockers

* T1's `reorder` variant covers only 3 of the 49 fixtures; its teeth for a lookup tool come from `serialize`
  and `extra-config`, both of which are cheap to add but not decisive against a table extended to the variants.
* T3 depends on `bwrap` (or an equivalent `unshare`) on the counting host; T2 depends on `strace`. Both are
  present here; neither is assumed by the frozen predicate.
* A2 shows that any textual screen on the blob (fixture literals, expected-line templates) is defeated by
  packing, so clause a cannot be tightened textually.
* No blocker: the frontier walk stops at the residual above.
