# R89MResidC2 — residual attack on C2 (round 89, r1)

Seat: R89MResidC2 · Date: 2026-11-06 · F = `d87361354b4d142287aac05bb973315749ef1fce`, A = `099c662dc55521e365cd4126132cdcda4efc54b6`, base = `af998dcc41d48618ffe7afe0efc9354755a9244e`.
Method: lane clone + `git archive` extracts under `/fast/scratch/hyaku/mado-r89/R89MResidC2/`; all lane files read via `git show` at the named revisions (no lsp device in this seat; pinned-byte inspection only). Tool sha at F `c374d715…2237`, at A `6b4bc409…3a98` — both match the declaration pins; the counter and both pinned machinery files are byte-identical at F and A. No writes outside my scratch and this report; no installs; no mutating git/jj anywhere.

## 1. Exact-command reproduction

Ran the declaration's C2 argv unchanged (except `DIR` = my own scratch roots `…/R89MResidC2/scrF` / `…/scrA`), cwd = scratch clone, `--repo .`, at `--rev F` and `--rev A`:

- rc: **F rc=0, A rc=0** (TARGET_MET both).
- Full-output diff vs the receipts (after stripping the receipt's `$ ` command-echo line and trailing `rc=0` line): **`F_BODY_IDENTICAL`, `A_BODY_IDENTICAL`** — byte-equal bodies; each run prints 95 `case … ok ok` lines and 8 `survivor …` rows.
- Final lines match the receipts exactly:
  - F: `MADO_MAKO_SURVIVORS: TARGET_MET rev=d8736135… cases=95 correct=95 counted=7 killed=7 do_nothing_B_only_killed=0 crash_only=RM6C2-cycle-detected-on-lexical-target tool_sha256=c374d715…`
  - A: same with `rev=099c662d… tool_sha256=6b4bc409…` (harm watch confirmed: C2 is unaffected by the C1 tool change).

Defect of my own first attempt (not a counter defect): rc=2 `SETUP_ERROR scratch root is not a directory` — the counter requires `--scratch-root` to pre-exist and fails closed. Recorded for completeness.

## 2. Pre-freeze controls re-checked (F bytes, in-process)

- **B-only do-nothing control** (`c2-r89-survivor-kills.py` loaded from F bytes via importlib; `evaluate(tool, base_f, base_k, [], [], survivors, S)` with an empty scratch dir): `{'total': 87, 'b_cases': 87, 'correct': 87, 'killed_full': 0, 'killed_base': 0, 'counted': 7, 'verdict': 'TARGET_MISSED'}` — dict-identical to `receipts/c2-controls-prefreeze-r89.txt`; all 8 rows `survived`, `killed_by_B_only=False`, no `differs_on`, no `crashed_on`. **0/7 confirmed.**
- **Tool-selftest control** (each survivor applied to the F tool, `python3 -I <mutant> --selftest --scratch-root …`): rc=1 for exactly **RM7C1-include-accepted-inside-criteria** (`FAIL include inside criteria refused (L45)`), **RM3C2-trailing-slash-refusal-dropped** (`FAIL an include path with a trailing / is refused`), **RM4C2-double-slash-join-dropped** (`FAIL ~//x stays under --home (config.c joins $HOME/ + rest)`), each `MADO_MAKO_SELFTEST: checks=52 failed=1` on stderr; rc=0 for the other five. **3/7 confirmed, exactly the receipt's set.**

## 3. RM6C2 crash-only attack — three new probes, no well-formed separation

Mutant: `if real in self.stack:` → `if target in self.stack:` (tool at F lines 441/458/462/464: `real = os.path.realpath(target)`; stack holds canonical realpaths incl. the config). Probes scored with the frozen K machinery in-process (tool vs RM6C2 mutant):

| probe | shape | tool | mutant |
|---|---|---|---|
| p4-residc2-self-absolute-first | self-include `~/a.ini` placed **before** the symlink-alias edge in the same file | ok, `width=7`, refusals present | **exit=1 crash** (RecursionError) |
| p5-residc2-dangling-alias | alias edge is a **dangling symlink** (non-strict realpath maps it to its own path) | ok, `width=3`, refusals present | ok — identical, **no separation** |
| p6-residc2-blocked-edge-first | mutant-blockable edge (`~/b.ini`) placed first inside the cycle | ok, `width=9`, refusals present | **exit=1 crash** |

Structural argument (grounds the probes): the mutant tests the *expanded lexical* `target` against a stack of *canonical* realpaths. (i) If `target ∈ stack`, `target` equals some canonical path P, so `realpath(target) = P ∈ stack` (realpath idempotent on a stable fs) — every mutant-blocked edge is tool-blocked too, so the mutant can never refuse where the tool reads (p5 shows the only exotic corner — a dangling alias whose realpath string is self-referential — cannot help, because a path that never resolves is never pushed onto the stack). (ii) Conversely, a tool-blocked cycle edge with `target ∉ stack` is followed by the mutant, which deterministically replays the ancestor subtree; the replay pushes only realpaths already on the stack, so the edge's fixed target string never enters the stack, the edge is never blocked on any iteration, and the descent recurses until RecursionError (p4, p6). The only escape is a filesystem mutation between realpath calls — TOCTOU, which is the excluded RM2C2 named limit and non-reproducible by construction. **No terminating input separates RM6C2 with a well-formed result; the crash-only declaration STANDS.**

## 4. Verdict

**C2 VERIFIES.** All three conjuncts of PRED-C2-r89-v1 reproduced at the freeze revision and at the C1 revision: (a) `correct=95` of 95 on B ∪ S; (b) 7 of 7 counted survivors killed, each separated on its named S case (`differs_on` row matches); (c) do-nothing B-only control 0/7. RM6C2 is correctly excluded as crash-only (attack failed as argued). Controls and selftest control reproduce exactly.

## Residual observations (not claim defects)

1. `receipts/c2-measured-F-r89.txt` and `receipts/c2-harm-at-A-r89.txt` exist in the lane working tree but are **not committed at F** (`git show F:<path>` fails). The pre-freeze control receipts are committed and byte-identical at F. Recurrence of the round-88 R4 lesson — L1 should commit the two measured receipts.
2. Lane clone HEAD was already at A; `tools/mado-mako.py` differs F↔A as declared; the C2 counter, machinery, and all input sets are byte-identical at both revisions (verified by sha).
