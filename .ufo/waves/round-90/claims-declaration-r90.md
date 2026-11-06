# mado round 90 — claims declaration

L1: MadoR90 (planner seat held by the L1). Base revision `5041acf99e27263872bf0441ad5f9d4316152605` (master, = the
round-89 closure tip). Hyaku run 15, attempt 1. Round shape: ONE v1 wave `w1` (13 seats, settled before the freeze) + at
most one residual call `r1` (≤3 attack seats) on the frozen and measured bytes; total ≤16. This file is frozen by the
freeze commit; anything after it is an appended erratum.

**Attempt 2 (L1 `MadoR90a2`, 2026-11-06, before the freeze).** Attempt 1 (`MadoR90`) wrote this declaration, the
counters and the frozen controls, then ended before any commit (`.ufo/watchdog.log`: `lane-dead-no-report mado
round=90` 20:22:51). Attempt 2 inherits them unchanged after re-checking every pin above by `sha256sum` (all equal) and
re-running both draft controls on the frozen bytes: C1 `DRAFT_TARGET_MET cases=229 correct=229 blind=66/66 fresh=120/120
mutants=60 killed=60 r12_rule_correct=70 host_table_correct=10 do_nothing_correct=35 base_correct=0`
(`receipts/c1-controls-prefreeze-r90.txt`; attempt 1 had written only its argv); C2 `DRAFT_TARGET_MET expectations=83
met=83 defects_detected=4/4 population=38 mutants=28 killed=28 base_met=0 do_nothing_met=44 smart_always_ok_met=46
always_missing_met=0` (`receipts/c2-controls-prefreeze-r90.txt`). No case, mutant, oracle, counter or predicate byte
changed. The residual `r1` named above is not dispatched in attempt 2; the round total is the 13 w1 seats.

## Inputs read before declaring

- `corpus/lessons/round-89-verifier-spotcheck.md` (non-author, round 89 admitted): routed D1 (records commit `51bf076f`
  cited receipts first committed in `16ee97b5`; repeat of round-88 R4 / lesson M89-4 — "land the proposed receipt-presence
  check in round 90"), D2 (`SKILL.md` gate registry rows stop at `mado-r86-*`), D3 (R89MResidMut survivors RS01, RS05, RS12).
- `considerthese/2026-11-06.md` proposal 4: "Widen desktop coverage past bar + mako … xdg-desktop-portal / screen-share …".
- `corpus/knowledge/xdg-portal-routing-r12.md` (round 12): a hand-derived table of 16 interfaces (15 with a named candidate;
  Secret unresolved at :62) from the host's `hyprland-portals.conf` + descriptors; no tool, no `none`/`*`/UseIn/last-resort
  rules, no multi-directory precedence. It does not list Background, Wallpaper, RemoteDesktop, Clipboard, Usb, and its
  ":37 UseIn is not used for routing" is refuted for multi-desktop values (w1 R90MExecHost H2). (Draft 1 said "14 rows,
  no Settings/Secret" — wrong; R90MCritic F6, R90MExecHost H1.)
- Upstream xdg-desktop-portal tag 1.22.1 (tarball sha256 `5afeda953c3743efaa1160e73d62c5bfcac2ceca60e0e134e9b48ed651783625`,
  `src/xdp-portal-config.c` 1-1004, `src/xdp-context.c` 354/368 + the `init_*` sequence querying 21 impl interfaces); GLib
  2.90.1 `glib/gkeyfile.c` (installed `glib2 2.90.1-1`); host `portals.conf(5)`; host package `xdg-desktop-portal 1.22.1-2`.

Stagnation nudge: not claimed (a capability row entered at round 89). Every owned axis sits at 10, so the lowest-axis
obligation is a tie; C1 works coverage, C2 works operability.

## C1 — coverage (capability acquisition): portal backend routing resolved the way xdg-desktop-portal 1.22.1 resolves it

Claim type: **capability acquisition**, axis verdict **coverage**. The surface moved is the portal-routing plane's edge
classes the lane did not govern: `none`, `*`, interface keys vs `default`, Settings' find-all, the UseIn fallback, the gtk
last resort, per-directory config selection across the XDG search path, descriptor validity, and the GKeyFile rules
(Encoding, CR, escapes, whitespace) — plus the five interfaces the round-12 table never listed. The lane had no runnable
instrument on this plane: `git show 5041acf9:tools/mado-portals.py` fails. Deliverable: `tools/mado-portals.py` (candidate
`.ufo/waves/round-90/build/mado-portals.c1.py`, sha256 `d1bd9b9a7c98f9e573bf8ba0594d796853f81539eed1d87052aa7906195e6ab1`,
copied to `tools/` only after the freeze), a capability row and a knowledge entry. (The draft's regex "count" over the
tool's own `IFACES` literal is withdrawn: a stub passes it — R90MCritic F5. The count is the counter below.)

- Oracle (labels): the production binary `/usr/lib/xdg-desktop-portal` (sha256
  `e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8`) run `-v -r` on a private bus without service
  activation (`controls/portal-oracle-r90.py`, sha256 `e495b2d2…1419`); its whole-line decision lines (`xdp-portal-config.c`
  817/846/879/891/915) are the labels; a run counts only if the exact line `XDP: org.freedesktop.portal.Desktop acquired`
  appears (R90MReviewC1 O1: a substring test was forgeable through echoed file names). Modes `dir` and `xdg` (host tail
  `/usr/share/xdg-desktop-portal` digest `4a4cf31921e25dc6e60b283cc1aa1b79f743096bfdfc9dbb77df887c16f0fbf9`;
  `/etc/xdg-desktop-portal` absent). Labelling twice gave identical labels.
- Cases: `controls/portal-cases-r90.json`, sha256 `66d4ffff70bd092bd2c900658b3b9a7566f8dedc2aacd4b334102acebc192da2`,
  **N = 229**: 103 L1 (`controls/gen-c1-cases-r90.py`, incl. w01–w11 from w1 findings), 66 `bl-` (R90MScoutCases, authored
  without opening the candidate), 24 `fz-` (R90MExecFuzz minimised disagreements), 19 `mc-` (R90MMutC1), 17 `rv-`
  (R90MReviewC1 battery). Merged by `controls/merge-c1-cases-r90.py` (seat labels dropped); every label is from one oracle run.
  Seat labels were reproduced: mc 19/19, fz 24/24, bl 66/66, rv 16/17 (rv-d11 differs because the hardened oracle labels
  it correctly). `controls/check-fixture-lines-r90.py` on the file: `merged=0` (M90-1).
- Blind first run (stated before the freeze, F7): the pre-w1 candidate (`build/mado-portals.c1-pre-w1.py`, sha256
  `dee65d3a…6f17`, unchanged since before the wave) agrees with the oracle on **66/66** blind cases.
- Mutants: `controls/portal-mutants-r90.json`, sha256 `e761a4e44ec6d8a692d8ac9b2feec7ef8609b4d30f5ed40c11f7c332129c2451`,
  **M = 60** (L1 M01–M38 less M07/M11, 27 R90MMutC1 X-mutants); `equivalent_not_counted`: M07, M11, X22, X28, X30, each with
  its argument. A mutant that only crashes is reported `crashed-not-killed`, never killed (QUALITY 148; R90MConnector §4.1).
- Fresh leg (F10): 120 cases generated at measurement time by `controls/fuzz-gen-r90.py` (sha256 `f5cbb11f…dcd6`, the
  R90MExecFuzz generator) from seed = first 8 hex of the measured tool's sha256, labelled by the oracle then; a tool that
  stores the frozen labels cannot know them.
- Sandbox (F10): the tool runs under bubblewrap with read-only `/usr` (oracle binary, `dbus-run-session`, `dbus-daemon`
  masked), the fixture and the tool file only; the lane, labels and oracle are invisible. Draft replay: the w1 label-lookup
  and oracle-shell-out forgeries score 0/229 and fresh 0/30 (`receipts/c1-controls-prefreeze-r90.txt`).
- Counter: `quality/counters/c1-r90-portal-routing.py` (sha256 `a92f4c3d…51a2`), PRED-C1-r90-v1.
- **Predicate PRED-C1-r90-v1 (verbatim, = counter docstring):** TARGET_MET iff the tool at --rev answers every frozen case
  exactly as the oracle labels it (correct == cases), answers every fresh case exactly as the oracle labels it at
  measurement time (fresh_correct == fresh …), every frozen mutant is killed on the frozen cases (killed == mutants), and
  every control scores below the case count (r12_rule_correct, host_table_correct, do_nothing_correct, base_correct < cases).
- **Measurement argv:** `python3 -I quality/counters/c1-r90-portal-routing.py --repo . --rev <C1 commit> --base-rev
  5041acf99e27263872bf0441ad5f9d4316152605 --cases .ufo/waves/round-90/controls/portal-cases-r90.json --mutants
  .ufo/waves/round-90/controls/portal-mutants-r90.json --expect-cases-sha256 66d4ffff70bd092bd2c900658b3b9a7566f8dedc2aacd4b334102acebc192da2
  --expect-mutants-sha256 e761a4e44ec6d8a692d8ac9b2feec7ef8609b4d30f5ed40c11f7c332129c2451 --expect-oracle-binary-sha256
  e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8 --scratch-root DIR` (`--fresh` default 120).
- Concrete after-state: `cases=229 correct=229 fresh=120/120 mutants=60 killed=60`; controls (draft, frozen bytes):
  r12_rule 39-ish of 163 on the pre-merge draft — the receipt states the values on the frozen 229; each must be < 229;
  `base_tool=absent base_correct=0`.
- Before: tool absent (`base_correct=0`); interfaces resolvable by a lane tool 0 → 21.
- Kill rule: any case FAIL, any fresh FAIL, any surviving mutant, a control reaching N, or a setup error at the measured
  revision → TARGET_MISSED; no case, mutant, oracle or counter byte is edited after the freeze.

## C2 — operability: a runnable receipt-presence gate over the lane's records changes

Surface: `quality/check-receipt-presence.py` (candidate `build/check-receipt-presence.c2.py`, sha256
`04b8be60415f2e505f6a1414099402203eb3a1fd17b21542c3afdd24b38a1d6c`), a new runnable pre-commit gate (`--worktree`) and
history audit (`--rev`). Axis: operability (the surface is a runnable artifact; its effect on records is noted in the
SCORECARD row, never scored as calibration — F12). Before: no lane check reports the class — at base the file is absent,
and `quality/check-deliverables.py` (`CHECK101 … verdict=OK`) and `quality/check-evidence-pointers.py` (round-36 scoped,
`TARGET_MET`) say nothing about `498855cb` / `51bf076f` (`receipts/c2-existing-checks-prefreeze-r90.txt`).

- Expectations: `controls/receipt-presence-set-r90.json`, sha256 `f7ab86c25edbb806a9f947af09fab5cf971a42602c252966c0075b9aeefa7939`:
  6 lane revisions (D85 `942365c8`, D86 `01be4234`, D88 `498855cb`, D89 `51bf076f` with exact missing sets; C88 `8e8f7ea3`,
  C89 `16ee97b5` clean), 35 worktree fixtures (W1–W11 L1, X1–X13 R90MMutC2, Y1–Y11 from R90MCritic F3, R90MReviewC2 G1/W1/W2
  and the L1), each evaluated under a clean git config and under `diff.mnemonicPrefix=true` + `diff.noprefix=true` (F2), plus
  the population: every non-merge commit of `5f174ca4..5041acf9` (38) must be flagged exactly on {D85, D86, D88, D89}.
  D85/D86 labels: R90MCritic F4, R90MReviewC2 §1, and `git log --diff-filter=A` (each cited receipt is first added by a
  later commit). = **83 expectations**.
- Mutants: `controls/receipt-mutants-r90.json`, sha256 `68b39a805755f7685c00c847a48b0f8f679fdca2710773efb5f4469b7bebe82d`, **28**.
- Counter: `quality/counters/c2-r90-receipt-presence.py` (sha256 `255cb8b6…f06c`), PRED-C2-r90-v1.
- **Predicate PRED-C2-r90-v1 (verbatim, = counter docstring):** TARGET_MET iff `<rev>:quality/check-receipt-presence.py`
  meets every frozen expectation of the set … under BOTH a clean git configuration and one with diff.mnemonicPrefix=true and
  diff.noprefix=true; every frozen mutant of the check fails at least one expectation (killed == mutants); and each control
  meets fewer expectations than the set holds (base check, do-nothing OK check, smart always-OK, always-MISSING).
- **Measurement argv:** `python3 -I quality/counters/c2-r90-receipt-presence.py --repo . --rev <C2 commit> --base-rev
  5041acf99e27263872bf0441ad5f9d4316152605 --set .ufo/waves/round-90/controls/receipt-presence-set-r90.json --mutants
  .ufo/waves/round-90/controls/receipt-mutants-r90.json --expect-set-sha256 f7ab86c25edbb806a9f947af09fab5cf971a42602c252966c0075b9aeefa7939
  --expect-mutants-sha256 68b39a805755f7685c00c847a48b0f8f679fdca2710773efb5f4469b7bebe82d --scratch-root DIR`.
- Concrete after-state: `expectations=83 met=83 defects_detected=4/4 population=38 mutants=28 killed=28`; controls (draft,
  frozen bytes): base 0, do-nothing 44, smart always-OK 46, always-MISSING 0 — each < 83.
- Use in this round: the round-90 records commit is gated by `--worktree --base <branch tip> --round 90 --commit-path
  <the helper's path list>`; that run's output is a receipt in the same commit.

Causal separability: C1 touches `tools/mado-portals.py` and its counter only; C2 touches `quality/check-receipt-presence.py`
and its counter only; each counter reads only its own file at `--rev`.

## §2b frontier step (F14)

- Census start: `receipts/census-start-r90.txt` (`mado ok`, rc 0); end: same command, `receipts/census-end-r90.txt`.
- Sourced claim: C1. Rows opened this round (R90MScoutSources + L1 re-open): S501 xdg-desktop-portal 1.22.1 tag tarball,
  S502 GLib 2.90.1 `glib/gkeyfile.c`, S503 host `portals.conf(5)`; the entry `corpus/knowledge/xdg-portal-routing-resolver-r90.md`
  cites them.
- Mistake mined: M90-1 (fixture concatenation onto a host file without a final newline), with
  `controls/check-fixture-lines-r90.py` shown able to fail on the pre-fix generator (`build/gen-c1-cases-r90.pre-M90-1.py`).

## Routed items (work, not claims)

- D2: `SKILL.md` registry rows for the r87–r90 counters and the two new instruments.
- D3: killing selftest checks for RS01/RS05/RS12 in `tools/mado-mako.py` (R90MExecMako, `build/mado-mako.d3.py`, 14 added
  lines, 0 removed); harm watch re-runs the round-89 counters.

## Named limits (declared before data)

C1:
- GLib behaviours the oracle harness cannot express (R90MReviewC1 CAND-3–6): empty XDG_*_DIRS elements are modelled as
  cwd-relative like GLib but not oracle-tested; non-UTF-8 file bytes make the tool skip the whole file where GLib fails only
  the getter; HOME unset falls back to `/`. Locale-suffixed keys are dropped (C locale); a kept `key[C]` is not observable.
- Labels are g_debug/g_warning lines of 1.22.1-2 (pinned binary sha256); another build is not modelled. Source names
  containing a newline or the text `.portal for ` are not labellable.
- The resolver answers what the configuration selects; it does not prove a backend is running or answers D-Bus calls.
C2:
- Only added lines of SCORECARD.md, LOG.md, corpus/QUALITY.md, corpus/README.md, corpus/lessons/*.md, corpus/knowledge/*.md;
  only `receipts/<name>.{txt,json,jsonl,md,log,csv,tsv}` (braces and `*` handled); nested `receipts/<dir>/…`, seat-dir
  receipts and w1 evidence paths are not checked; pre-existing citations on unchanged lines are not re-checked.
- `--worktree` carriage = the commit-path list (directory entries exclude git-ignored files) plus the base tree; `--base`
  must be the branch tip the helper commits on (a later commit carrying the file is not modelled — R90MMutC2 P4).
- A bare name without `-r<k>` resolves by the change round; suffixless names in commits whose subject lacks `round-N`
  resolve only to `quality/receipts/` (R90MReviewC2 G3).

## Draft revisions (w1 findings applied before the freeze)

1. C1 tool: UseIn read error-tolerant (R90MCritic F1, R90MReviewC1 CAND-2, R90MExecFuzz: all 24 fuzz disagreements);
   first-group `Encoding` rule (CAND-1); one CR erased only before LF (R90MMutC1 X03); sort compares bytes (CAND-5); empty
   XDG_*_DIRS elements kept (CAND-3). Selftest 19 → 22.
2. Oracle: whole-line completion marker and decision regexes (O1); source names with spaces labellable (F9); labels
   unchanged on the 92 L1 cases.
3. C1 counter: sandbox, oracle-binary pin, fresh leg, do-nothing control, crash-is-not-a-kill (F8, F10, R90MExecForgery,
   R90MConnector §4.1).
4. C2 check: explicit diff prefixes (F2); covered receipts must exist on disk (F3); braces/globs (G1); check-ignore for
   directory-covered files (W1); commit paths normalised (W2); `-r<k>` tokens anywhere in the name (D85 false positive on
   `control-c2-r84-unguarded.txt`); sentence-final period.
5. C2 counter: population + D85/D86 (F4), dual git config (F2), cited/present/location expectations (R90MMutC2 P1–P3),
   controls bound in the predicate with the smart always-OK (F15), crash-is-not-a-kill.
6. Declaration: r12 baseline corrected (F6/H1), regex count withdrawn (F5), capability framing (F11), C2 axis wording (F12),
   limits for both claims (F13), §2b section (F14).
