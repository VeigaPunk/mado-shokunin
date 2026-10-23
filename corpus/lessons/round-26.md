author: mado

# Round 26 — a nested Hyprland that never touches the desktop; the animation table; hyprlang arithmetic in binds

Base: lane tip `96101be523b2f6e897eee743d5b396b0225bf9ed` (round-25 closure: admitted). One attempt (`MadoR26`). Unless a
full path is given, `harness/`, `c1/`, `c2/`, `controls/`, `quality/`, `evidence/`, `w1/`, `w2/`, `res/` and `drafts/`
resolve under `.ufo/waves/round-26/`.

Order (UTC): pilots 08:22–08:36 → harness + registration + counters c1 v1 / c2 `05319e0f` 08:41 → wave w1 (40 seats;
registry `createdAt` 08:43:17, dispatched 08:49 after the slot gate) → C1 counter v2 frozen before data (w1
`CritC1Design`) → control receipts (C1 v1 and v2, C2) + w1 reports `1b0b91e9` 09:16:22 → wave w2 (34 seats; registry
`createdAt` 09:16:39, dispatched 09:24 after the slot gate; first data seats ExecAnimTool*/ExecArithTool*) →
C1 tool lands `2b3487f7` (ExecAnimToolA, first C1 file returned, unmodified) → single C1 measurement 09:3xZ
(`evidence/c1-after-v2-2b3487f7.txt`: 41/41 TARGET_MET) → note, sources, PROVINCE, README, QUALITY 37 `ca135237` →
C2 tool lands `a496b02a` (ExecArithToolB, first C2 file returned, unmodified) → single C2 measurement
(`evidence/c2-after-a496b02a.txt`: 51/51 embed_hits=0 TARGET_MET) → residual call. ExecAnimToolB (41/41 twice, not
landed by the registration's first-returned rule) is a second implementation; ExecArithToolA was cancelled at the
settle point after C2 had landed (no deliverable used). Both measurement runs were launched with `env -i PATH HOME`
so the tool sandbox's `/proc/1/environ` held no credentials (M26-5).

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M26-1 | host safety: oracle on the operator's live session | round-25 `.ufo/waves/round-25/c1/count.py:30-47,124-138` (nested Hyprland with the wayland backend, `WAYLAND_DISPLAY`/`XDG_RUNTIME_DIR` taken from the live session); `coredumpctl`: 1330 `/usr/bin/Hyprland` SIGABRT records between 06:45Z and 08:20Z on 2026-10-23 (w1 `ScribeMistakes`); orchestrator note: windows opened on the operator's desktop | none: QUALITY 1–36 judge sources, receipts and order, not what a counter does to the host; the round-25 spot-check declined to run the counter for this reason but no rule required isolation | `harness/oracle.py`: each nested Hyprland runs under its own private headless tinywl inside bubblewrap (no host `/run`, cleared env, private `XDG_RUNTIME_DIR`, only the amdgpu render node, `RLIMIT_CORE=0`), stopped by `dispatch exit`; every receipt prints `HOST_SAFETY … delta=`. Shown able to fail: `harness/pilot.py` prints `NOT_OK` when the nested process sees `/run/user` or a card node, shares the host netns, or the coredump count moves (w1 `IsolationProbe`: its leftover clause did go red on another seat's leftovers); measured: 288 nested pids, 770/770 without `/run/user` or card nodes, live clients 2→2, coredumps 1335→1335 (`evidence/isolation-probe.txt`). |
| M26-2 | pilot accounting | `harness/pilot-receipt.txt` first version and `registration.md` host-safety paragraph said "four failed pilot runs" for a coredump rise of 1330 → 1335 (five) | w1 `ScribeMistakes` and `ReviewRegistration` (non-author seats) | appended errata in both files: five failed pilot runs (the unpatched-tinywl run was executed twice), each one SIGABRT record; the corrected method added none. Not shown able to fail (no check counts pilot records). |
| M26-3 | counter population: append-only cases | v1 `c1/count.py:233-245` (every case appends to the same snapshot); w1 `CritC1Design` B/E1: a tool caching the snapshot's directives and parsing only appended lines could meet v1; the registration's "every C1 case carries at least one table-changing operation" was false (K1SnapshotCache passed 1–2 unchanged cases; K1NoValidation found seed `f7b35f29…` C32 equal to BASE) | w1 `CritC1Design` (non-author critic) before any data seat | counter v2 (`c1/count-v2.py`): 20 append + 10 edit/delete + 10 independent-tree cases, `ORACLE_VERSION` guard, per-case `changed=` diagnostic; every C1 control re-scored under v2 before data (`controls/v2/`). Shown able to fail: K1SnapshotCache 2/41 under v1 → 4/41 under v2 with every EDIT and SYNTH case failing (`controls/v2/K1SnapshotCache.txt`). |
| M26-4 | dispatch text not byte-identical to the validator's rendering | w1 and w2 task texts: each validated `taskCall.tasks[i].task` was sent with the operator's 2026-10-19 tooling-directive block appended (compare `w1-run.json` / `w2-run.json` with the dispatched transcripts) | none (the wave validator renders the payload; nothing checks the sent text) | disclosed in the report; next round sends the rendered text unchanged (the context already carries the tooling sentence). Not shown able to fail. |
| M26-5 | tool sandbox leaks the launcher's environment | w1 `K1LabelKeyed`: inside the counter's tool sandbox `/proc/1/environ` (bwrap, pid 1) holds the counter's full environment; `/proc/1/cmdline` shows the (random) case path | w1 `K1LabelKeyed` (control seat) | not fixed this round (the harness was frozen and pinned before the finding; changing it would change every counter's rule). Route: run bwrap under `env -i` in a successor harness; the leak reveals no case identity (paths are random), so no claim depends on it. |
| M26-6 | host safety: seats probed configs that crash Hyprland | `coredumpctl`: 1335 → 1338 during wave w2; ExecAnimToolA `dev_overflow.py` (`std::stof` overflow, 2 SIGABRT records) and ExecAnimToolB (self-sourcing root, 1 SIGSEGV record), all inside the isolated sandbox, none in a counter run (every receipt `delta=0`) | none: the w2 context forbade starting Hyprland outside the harness, not feeding it crash inputs | next round's data-seat contract forbids known-crash inputs (overflowing numbers, source cycles) and requires a seat's own coredump delta in its report. Not shown able to fail. Round total: 1330 → 1338 (5 pilot + 3 seat-probe records). |
| M26-7 | shared context gave a cap the oracle cannot run under | w1 context told seats `prlimit --as=4000000000`; the oracle raises its own limit to 8 GB, so hard-capped counter runs exited 2 (`ORACLE_FAIL … sandbox exited rc=1`; K1DoNothing, K2DoNothing guard receipts, K1NaiveGrep) | the counters' own guard (exit 2, nothing measured) | L1 messaged the counter-running seats (soft 4 GB / hard 8 GB); the w2 context carries the corrected form. Shown able to fail: the retained guard receipts `controls/K2DoNothing-base-guard-run{1,2}.txt`. |
| M26-8 | gate checks weaker than their criteria (again) | w2 MutSelftest: 6 of 10 mutants survive `quality/counter-selftest.py` (dropped bezier compare, two non-JSON acceptance, two ≥90% rules, dropped assertion); w2 MutQ37: 3 of 6 survive the committed population fixtures (CASE-anywhere, first-PRED-only, parse-error exit 0); w2 MutQ36: the successor `check-control-receipts.py` exits 1 on round 26 because its receipts must be `controls/*.md` and this round's are `.txt` (chronology itself holds: controls commit 17 s before the w2 registry `createdAt`) | the mutation-testing seats (non-author) | open; route: add the w2 witnesses as committed fixtures, a near-perfect (40/41) tool and a non-JSON tool to the self-test, and a receipt-path option to the Q36 successor. Not fixed this round. |

## Gate

Sources opened this round (access date 2026-10-23, ordinary fetch, pinned raw URLs; each re-opened by a w2 reviewer):

| id | URL | quote (≤25 words, verbatim) | decision |
|---|---|---|---|
| S173 | https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp | "return std::unexpected("Invalid expression type: supported +, -, *, /");" (`src/config.cpp:630`) | mined (w1 SrcHyprlangExpr; w2 ReopenS173) |
| S174 | https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/parse/main.cpp | "EXPECT(std::any_cast<int64_t>(config.getConfigValue("testExpr")), 1335);" (`tests/parse/main.cpp:252`) | mined (w1 SrcHyprlangTests; w2 ReopenS174: agree) |
| S175 | https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Animations.md | "The animations are a tree. If an animation is unset, it will inherit its parent's values." (`:23-24`) | mined (w1 WikiAnimations; w2 ReopenS175: agree). The wiki pin c66e8de2 holds only Lua-era pages; this is the hyprlang-era page at the parent of the rewrite. |
| S176 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/animation/AnimationTree.cpp | "m_animationTree.createNode("windowsIn", "windows");" (`:35`) | mined (w1 SrcAnimTree; w2 ReopenS176: agree) |
| S177 | https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/animation/AnimationConfig.cpp | "if (anim->pParentAnimation == PANIM && !anim->overridden) { // if a child isnt overridden, set the values of the parent" (`:63-64`) | mined (w1 SrcAnimTree; w2 ReopenS177: agree) |

Changes on pre-existing rows (in place, logged old→new):

- S158 `used-by`: `corpus/knowledge/rule-attribution-r24.md` → `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/animation-table-r26.md`. Re-opened (sha256 `798b7c6c…b91fa`, 97582 B = anchor); `animationsRequest` at `src/debug/HyprCtl.cpp:927-985`, outside the row's anchor ranges (anchor cells do not change in place). w2 ReopenS158/S175/S176/S177: agree.
- S162 `used-by`: `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md` → `…, corpus/knowledge/animation-table-r26.md`. Re-opened (sha256 `9db68cf4…be62b`, 90963 B); `handleBezier`/`handleAnimation` at `src/config/legacy/ConfigManager.cpp:1389-1479`, outside the anchor ranges. w2 ReopenS162/S175/S176: agree.

Rejections at the gate this round (with reasons):

- **Counter v1 as C1's rule — rejected before data.** Its population was append-only, so a snapshot-cache-plus-suffix reader could meet it without reading the original bytes, and it did not pin the Hyprland that answered (M26-3). Replaced by v2 before any data seat; v1 and its receipts stay.
- **Duplicate-URL rows for HyprCtl.cpp and the legacy ConfigManager.cpp — rejected**; `used-by` extended instead (w1 SrcHyprctlAnims, SrcAnimConfig).
- **A two-URL S174 row (config.conf + main.cpp) — rejected**: one row, one URL; `tests/parse/main.cpp` kept (its EXPECT lines carry the asserted values), `tests/config/config.conf` stays a fetched artifact (`fetch/SrcHyprlangTests-config.bin`).
- **ExecAnimToolB's implementation — not landed** (41/41 on two fresh seeds; the rule fixed before data lands the
  first file returned); kept in scratch as a second implementation.
- **The registration's "cache bound ≤21/41" — withdrawn as a ceiling** (w2 CritMistakes): an EDIT case whose change
  leaves the table unchanged can also be met by a cache (`controls/v2/K1SnapshotCache.txt` C28 `changed=no`); the
  measured cache controls stay at 1–4/41.

## Correction notes (append-only)

- Round-25 routed defect 8: the before-v4 receipt `.ufo/waves/round-25/evidence/c1-before-v4-41cc04c8.txt` ends with
  `PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED` and contains no `exit=` line. The counter's
  return branch `.ufo/waves/round-25/c1/count.py:298` returns 1 for a non-met predicate, so the receipt's exit status
  is 1, derived from its recorded verdict and the code; the receipt itself is unchanged (w1 R5R6Corrections). Round-26
  counters print `exit=` on every path, including guards.
- Round-25 routed defect 5 (R8): correction appended to `.ufo/waves/round-25/registration.md`.

## What to carry

- Host safety is a counter property: every receipt prints its coredump delta; data seats must not feed Hyprland
  crash inputs (M26-6).
- Successor harness: bwrap under `env -i` (M26-5), symlink-safe snapshot and slot files, disk and tool resource
  bounds (w1 SentinelHarness; w2 ReviewIsolation `HOST_SAFETY concern`).
- Gate-check fixtures for the surviving mutants of the self-test, Q37 and Q36 checks (M26-8).
- Carried unchanged: H2 (L0 `.ufo/l0-questions.md:103`); QUALITY 33–35 survivors.

