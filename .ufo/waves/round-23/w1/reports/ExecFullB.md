# ExecFullB — round-23 C1 candidate (defining-scope provenance)

**Verdict: PASS.** The 12-case repair set goes from 6/12 to **12/12** with
`unparsed_spawns` 0 on every case, and every no-harm guard holds: round-22
primary 57/57, round-22 replay oracle 35/35 + 17/17, round-21 oracle 35/35 +
17/17 (via the same replay), round-22 residual truth 4/4, precision 166/175
with the **identical passing-name set as the base**, eleven legacy selftest
suites 247/247, the 1356-file corpus comparator with **0 added, 0 removed and
0 new error flips**, and both resource populations clean under 384 MiB / 15 s.

Deliverables (lane, `.ufo/waves/round-23/w1/out/ExecFullB/`):
`candidate.patch`, `guards.json`, `design-note.md`.
Report: `.ufo/waves/round-23/w1/reports/ExecFullB.md` (this file).

---

## 1. What I did

Item: C1 operability — an independent complete candidate for
`tools/mado-tripwire.py` that repairs the frozen 12-case repair set with the
mechanism the L1 prescribed: **not** "replace cenv with module env", but

* tag every helper binding with the identity of its **defining scope** (the
  module namespace, or the function frame object that executed the `def`),
* resolve a **followed body's free names through that scope chain** instead of
  through the frame that called it,
* **gate the callback sweep on the same provenance**: sweep only callables
  whose reference escapes into a store, a return, or an unfollowed call.

Implementation (one file, `tools/mado-tripwire.py`, +257 / −21):

* `MODULE_SCOPE`, `frame_scope(fn)`, `sweep_scope(fn)`, `SCOPE_KEY` — the
  scope identity, carried on the AST node (`node.mado_scope`) and in the
  binding dict (`"scope"`), set where the `def` is executed
  (`update_bindings`, `assignment_binding`, `class_method_info`).
* `ctx["scopes"]` — a scope's **own view** (only the names that scope binds)
  plus a `parent` link; `scope_view()` merges the chain innermost-first; the
  **calling frame is not in the chain**, so a caller's local can no longer
  shadow a callee's global.
* `scope_entry()` — records the own view per statement, so a global closed
  over is still read **late** (S121): the `CaptureGlobalLate` oracle case
  rebinds a global after a closure is built and must see the new value.
* `follow_helper` and `sweep_body` both read a body through that view.
* `reference_escapes()` / `parameter_escapes()` — the sweep gate: a callable
  the receiving call only *calls* does not escape it (that call is followed,
  so the callback is already read in its own scope); one that is stored,
  returned or handed on is swept.

Full rationale, per case, and the known limits: `design-note.md`.

## 2. Where the work lives

* Clone: `/fast/scratch/hyaku/mado-r23/ExecFullB` (clone of the lane,
  branch `feature/round-23-c1-scope-provenance`, local commit
  `63dbbab21d8935c43159d6c76a4848209348f210`, base
  `a28e4815aabfa85f55274884000fb2608355f8cf`). Never pushed; the lane's git
  index, working copy and jj state were not touched.
* Candidate bytes: `tools/mado-tripwire.py`,
  sha256 `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`
  (base `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`).
* `candidate.patch` = `git -C <clone> diff a28e4815aabfa85f55274884000fb2608355f8cf -- tools/`.
  Verified: `git apply --check` on a fresh checkout of the base commit, the
  applied tree reproduces the candidate sha256 exactly and compiles.
* The clone keeps an untracked `dbg/base-mado-tripwire.py` (the base bytes
  from `git show a28e4815…:tools/mado-tripwire.py`) so the corpus command in
  §3 is reproducible; it is not part of the patch.

## 3. Exact commands and results (all on the candidate)

Guard commands were run from the lane where the harness allows it, and from
the clone where the harness requires the tool to live inside the repository
(`round-22/replay.py` rejects a `--tool` outside `REPO_ROOT`; the repair,
residual, oracle, selftest and round-21/round-22 resource harnesses accept an
absolute path and were run from the lane).

| # | Command (cwd) | Result |
|---|---|---|
| 1 | `python3 -I .ufo/waves/round-23/repair/measure.py --tool TOOL` (lane) | **12/12**, `unparsed_spawns` 0 on all 12 |
| 2 | `python3 -I .ufo/waves/round-22/residual-truth/measure.py --tool TOOL` (lane) | **4/4** |
| 3 | `python3 -I .ufo/waves/round-22/oracle/measure.py --tool TOOL` (lane) | **57/57** |
| 4 | `python3 -I .ufo/waves/round-22/replay.py --tool tools/mado-tripwire.py --mode oracle` (clone) | **35/35 + 17/17** |
| 5 | `prlimit --as=402653184 --cpu=15 python3 -I TOOL --selftest .ufo/waves/<suite>` (lane), 11 suites | **247/247** (9+16+33+30+1+31+45+34+17+13+18) |
| 6 | `python3 -I .ufo/waves/round-22/replay.py --tool tools/mado-tripwire.py --mode corpus --before-tool dbg/base-mado-tripwire.py` (clone) | 1356 files, 1217 retained, **0 removed, 0 added**, 107 errors — every error string identical before and after → **0 new error flips** |
| 7a | `python3 -I .ufo/waves/round-22/resource-closure-measure.py --tool TOOL --mode module-main` / `--mode cli` (clone) | 3/3 fixtures each: exit 0, `clean`, 0 unparsed, 0.09–0.28 s, 20–43 MiB RSS |
| 7b | `python3 -I .ufo/waves/round-21/resource/measure.py --tool TOOL --mode module-main` / `--mode cli` (clone) | 3/3 fixtures each: exit 0, ≤0.11 s, 19–39 MiB RSS (base measured the same: 19–37 MiB) |
| 8 | `python3 -I .ufo/waves/round-20/tw-precision.py 63dbbab21d8935c43159d6c76a4848209348f210` (clone) | **166/175** (P66/66 S17/17 W21/22 H47/52 L15/18); the passing **name set is identical** to the base commit's (checked by diffing the two case lists) |

Machine-readable receipts: `guards.json` (every command, its exit status and
its numbers). The corpus comparator's 107 errors are pre-existing: the base
classifier raises the same error string on the same 107 files (20
`RecursionError` deep-expression fixtures, malformed/agent.db/refused-name
fixtures, unknown-record-shape receipts); `before == after` for all 107, so
there is no error flip. `compare.py` exits 1 on any error, hence the
non-zero exit of command 6 — the base run produces the same exit.

## 4. The routes the L1 relayed (same mechanism, no special-casing)

Run from **copies** of the neighbours' directories (their runners write
`cases.json` next to themselves, which would have overwritten the lane's
files), with the round-21 oracle scan helper and the round-23 repair judge:

* `CritFrameNeighbour` — helper called from a method, from a lambda, through
  a decorator wrapper: **3/3 `base-correct`** (was 3 × `base-false-observed`).
* `CritScheduledNeighbour` — Thread target / Timer function started from a
  shadowing frame, `Thread.run` from a forwarder: **3/3 pass** (was 3 ×
  `base-false-observed`); thread args/kwargs stay evaluated in the starter
  frame.
* `CritEscapeNeighbour` — `EscapeSecondForwarder` (the frame leak one hop
  deeper): **pass**, `observed` the global, no foreign row.
  `EscapeListAppendThenCalled`: **pass** on the `present` rule (`lead` the
  global, no foreign row, 0 unparsed; at the base it was a silent miss with
  `unparsed_spawns` 1).
  `EscapeTupleNestedClosureLater`: **still a pre-existing recall gap** — it
  needs tuple values, tuple unpacking and a closure captured through
  unpacking, which is a separate feature. As the L1 said, I fixed it only if
  safe; a half-built tuple resolver would put the corpus and precision
  guards at risk, so I left it untouched and report it as not passing.

## 5. Risks and limits (stated, not hidden)

* **Scope-entry fallback.** When a scope has no chain entry (a factory result
  that is never followed, a decorator-built wrapper), the lookup falls back to
  the call-site view — the pre-change behaviour. The factory closure overlay
  still supplies the captured values in those cases, and every frozen case
  and neighbour route is covered by the chain proper.
* **Escape analysis is name-based.** A callback stored through a subscript
  (`d["k"] = cb`) is not detected as escaping and is not swept. The analysis
  errs toward sweeping (no finding is lost), which is the safe direction for
  a `lead`; the corpus comparator confirms no finding changed anywhere.
* **The sweep now resolves free globals.** A swept body is read in its
  defining scope, so a swept global can produce a `lead` where the base left
  an `unparsed_spawns` count. Across the 1356-file corpus this produced **no
  added and no removed finding**; the repair set's two recall cases
  (`CallbackStoredInDict`, `CallbackStoredOnAttribute`) keep their `lead`.
* The diff is confined to `tools/mado-tripwire.py`; nothing else in the repo
  was touched, and the lane's `tools/`, `corpus/`, `PROVINCE.md` and the
  frozen repair set were not written to.

## 6. Host and tooling

Read-only host probes only; no package, service, display or `~/.config`
change; no `pacman` transaction of any kind (all pacman transactions are
paused host-wide). **No tool was installed or updated** for this item, so
there is no install receipt to record — the work used the system `python3`
(3.14.8) and the repository's own harnesses. Nothing was spawned except the
harness children the guarded commands create (one `python3 -I` child per
fixture, 384 MiB / 15 s caps, sequential).

## 7. Handoff

The candidate is a single-file patch on top of the lane tip; the L1 owns
integration and judgement. Suggested landing order: apply `candidate.patch`,
then re-run guard 1 (repair set) and guard 6 (corpus comparator) at the
landed tip, since those are the two that decide C1's claim.
