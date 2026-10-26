# RevC1Counter — scoped findings: `quality/counters/c1-r46-devices.py` (frozen 8c5434c6)

Reviewed line-by-line; every suspicion executed. Baseline: the frozen counter reproduces `receipts/ctl-c1.txt`
REF (TARGET_MET, 90/90 + 150/150, exit 0, nonce 46; byte-identical rerun; nonce 999 also MET). All defects
below need an adversarial tool or a future re-pin — none changes this round's honest scoring. Detailed annex
with receipts: `.ufo/waves/round-46/w1/RevC1Counter/report.md` (+ `receipts/`, 17 files).

- **F1 MEDIUM — clause r erasable (unfair pass).** `sandbox()` (c1-r46-devices.py:251-257) leaves the work
  tree visible and marker_dir is its only writable bind (:256); a tool can run the fake `hyprctl` then unlink
  `../../mk-*/marker`. Demo: control rev c8be289 → `marker=present`/`readonly=fail`; erasing rev 84d1f83 →
  `marker=absent`/`readonly=ok` (receipts/probe-r-erase.txt, tool source receipts/fake-erase.py). Undeclared
  residual; fix: tmpfs the work dir or use a nonce-valued marker name.
- **F2 MEDIUM — "model invisible" is lane-local.** Sandbox sees `/fast/scratch/hyaku/mado-r46/*`
  (probe-hide.txt: 7 sibling seat dirs) where sibling freeze-checkouts expose `l1-draft/mado-devices.py` (the
  clause-g oracle) and the fixtures as plain files. Corroborates SentTool-3 F1/F2 (live `hyprland.sock` via
  the env_b-given `/run/user/<uid>` (:268); absolute-path execs; selftest env without fakebin (:375)). Fix:
  tmpfs {work parent, /run/user/<uid>, $HOME}; ro-bind fakes over /usr/bin.
- **F3 MEDIUM-LOW — selftest parse crash.** `n[0].isdigit() and int(n[0])` (:382): `³/³ passed` → ValueError,
  traceback, exit 1 with no clause=s and no verdict line (probe-sup.txt, run on the frozen counter); exit 1
  reads as an honest miss to exit-code consumers. Fix: isascii guard + always print clause=s.
- **F4 LOW — vacuous fixture count.** `fixtures_ok == len(fixtures)` (:402) is 0==0-true on an empty pinned
  file: demo re-pin to sha of `[]` → `fixtures=0/0 … verdict=TARGET_MET` exit 0 (probe-empty.txt). Only the
  fixtures sha256 (:66) stands between the round and this; enforce a minimum count.
- **F5 LOW — stdin dropped by the usage branch.** `:300-301` resets `args=["--devices", dp]`, discarding the
  stdin `-` while data stays piped; proven by DEBUGPROBE on a synthetic stdin+usage fixture
  (probe-argv.txt). Unreachable in the pinned 90 (no stdin+usage combo) and observationally identical output —
  coverage hole, not a wrong verdict.
- **F6 INFO — 20 s per-run timeout is undeclared** (:275); hanging tool ⇒ ~2h20 m worst case; behavior honest
  (timeout FAIL labels, TARGET_MISSED exit 1, no orphan processes — probe-timeout.txt).

Cleared (no defect): pinning (fixtures/model sha + freeze-commit blobs), {A}..{D} substitution safety (ASCII
mutually non-substring names, uniform application, pre-escaped `unicode-name` expect), BIG sentinels
(exercised, expect too_large rc 2), stdin fixtures, env A/B fidelity and per-nonce determinism, generated-case
model alignment (no leak: dump = f(texts, rng); oracle computed from the exact bytes the tool receives; model
in-process and hidden), verdict conjunction and exit codes.

Residual risk: F1+clause f/g composition (marker erased AND fixtures passed) would be an undetected MET
nothing in the frozen harness catches; AF_UNIX/absolute-path TARGET_MET demos are SentTool-3's receipts, not
mine; clause-g distribution re-derivation not attempted (controls V01–V20 cover it); findings carry verbatim
to the in-flight v2 counter if it keeps sandbox()/hidden_paths()/make_fakebin()/the clause-s env.

Tooling: nothing installed (bwrap 0.13.1 preexisting); no pacman; scratch deleted after receipts copied.

Report: .ufo/waves/round-46/w1/RevC1Counter.md
