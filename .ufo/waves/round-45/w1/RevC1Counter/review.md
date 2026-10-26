# RevC1Counter — review of `quality/counters/c1-r45-monitors.py` (mado round 45, w1)

Reviewed 2026-10-26. Object: the frozen C1 counter at the working tree, sha256
`c69ddee44a9fa3c442b910541038a9440ac72c2b5f21fe4899cb8f5df9213f34`, byte-identical to the freeze blob
(`git cat-file -p 22a8dedd02f507689c567777e0f20b5e645c8ce0:quality/counters/c1-r45-monitors.py | sha256sum`
→ same hash). Contract: the reference docstring `.ufo/waves/round-45/l1-draft/mado-monitors.py:3-90`.
Method: full read of all 392 counter lines + docstring-vs-code clause audit, then six live runs in
`/fast/scratch/hyaku/mado-r45/RevC1Counter` (scratch clones of the lane at the freeze commit; receipts copied
to `receipts/` here). No lane file was written; no mutating git in the lane; all fixture commits were made in
scratch clones after asserting `git rev-parse --show-toplevel` equals the clone.

Line references below are `c1-r45-monitors.py:<line>` unless prefixed `ref:` (the reference docstring).

## Findings (severity-ranked)

### F1 — MEDIUM: the read-only clause never observes the `--selftest` run; a scored tool can execute host binaries via PATH and clause r still passes
- The selftest is spawned with `env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": sd}` and no
  HYPRLAND_INSTANCE_SIGNATURE (c1-r45-monitors.py:343). The marker-guarded fakebin PATH exists only for
  fixtures (`"PATH": fakebin + ":/usr/bin:/bin"`, :311), the four stubs touch the marker unconditionally when
  run (:272-278), and the marker is checked once after the fixture loop (:354-356, :362). The docstring scopes
  clause r to fixtures: "after all fixtures no marker exists" (:20) — so the code matches the frozen docstring;
  the hole is in the clause itself.
- Repro (receipt `receipts/toy-selftest-gap-run.txt`): a tool whose `--selftest` runs
  `shutil.which("hyprctl")` + `subprocess.run(["hyprctl","version"])` executed the real host
  `/usr/bin/hyprctl` (this host has Hyprland installed) inside the counter's selftest environment — the
  counter's own clause-s line shows `SELFTEST-PROBE hyprctl=/usr/bin/hyprctl rc=1 outlen=61 errlen=0` — while
  the same run prints `clause=r marker=absent`. A tool scored by this counter can therefore run
  hyprctl/journalctl/wlr-randr/wayland-info during selftest with clause r reported "ok", which contradicts the
  registration's plain predicate summary "r no hyprctl/journalctl/wlr-randr/wayland-info on PATH run".
- Secondary effect: the selftest env (no HIS, no fakebin) is distinguishable from the fixture env
  (HIS=mado-r45-fixture, fakebin first, :13-14) and from real use, so a tool can fork behavior between
  "being scored" and production; the fixtures never see the selftest-only branch. Not a sandbox — any tool
  under test is arbitrary Python with user privileges — but the clause is a detection device and its detection
  has a hole. (My probe ran `hyprctl version`, an allowed read, with HIS unset so no compositor connection;
  only rc/byte-lengths were recorded — session material kept shape-only.)
- Fix requires re-registration (v2): run the selftest under the same fakebin PATH/marker and require the
  marker absent after both phases. Not fixable inside the frozen counter.

### F2 — LOW-MEDIUM: no global deadline; a hanging tool costs ~9.5 minutes for an already-decided MISS
- Selftest timeout is 60 s (:343) and is caught at :352 — clause s flips to fail, but the fixture loop
  (:358-361) still runs all 49 fixtures, each able to burn its full 10 s (:315): ≈ 550 s wall for a verdict
  that is already MISSED. The timeout path itself is handled correctly — receipt
  `receipts/chaos2-run.txt` shows `fixture=chaos-slow FAIL timeout`, a clean final line and rc=1 — so this is
  operational latency, not correctness.

### F3 — LOW: SETUP-reason teeth are partial — no fixture forces `too_large`, FIFO inputs, or invalid UTF-8
- The tool contract lists `usage | unreadable | too_large | bad_json` (ref:26) with MAX_BYTES = 1048576
  (ref:98, ref:139, ref:151), but the 49 fixtures never exceed ~a few hundred bytes, cover only a directory as
  the non-regular case (`setup-config-dir`), and the bad-JSON fixture is truncated-but-ASCII JSON. A tool that
  accepts arbitrarily large inputs, reads stdin unbounded, or mislabels its SETUP reason passes clause f. The
  counter docstring never promises per-reason fixtures, so this is a coverage limit of the frozen 49, not a
  code defect — but the headline "49 fixtures" overstates SETUP coverage.

### F4 — LOW: unhandled exceptions produce an undocumented third exit state (traceback, code 1, no final line)
- `run_fixture` catches only `subprocess.TimeoutExpired` (:316); any other exception (e.g. OSError from exec
  on a hostile mount, or a missing `git` binary raising FileNotFoundError inside `git()` :240-243) propagates
  through `score()`; the `finally: shutil.rmtree(work, ignore_errors=True)` (:384-385) still cleans scratch,
  but the process dies with a traceback, exit 1 and no final line — colliding with the documented
  "exit 0 iff TARGET_MET, 1 if missed, 2 on setup failure" (:22-23). Distinguishable only by the missing final
  line / stderr. Not triggerable on this host (git present; /fast mounted `rw,nosuid,nodev` — exec allowed);
  portability note. [INFERENCE on the exact OSError trigger; the uncaught-propagation path is certain from
  code.]

### F5 — INFO: a noexec `--work` mount silently voids clause r
- The stubs are `chmod 0o755` shell scripts (:274-278) invoked through PATH (:311); on a noexec mount their
  exec fails with EACCES, no marker is ever created, and a PATH-invoking tool reports clause r "ok". `/fast`
  on this host allows exec (findmnt: `rw,nosuid,nodev,noatime`), so not triggerable at the documented scratch;
  guard for other mounts.

### F6 — INFO: the tool blob is extracted once and shared by all 49 fixtures
- Extraction happens once into `tool-<rand>` (:336-339) and every fixture invokes the same file; a tool can
  persist state next to itself to sense being scored or order-depend. The docstring promises only "its own
  fresh working directory" per fixture (:13) — code matches contract; recorded as a residual detection limit.

### F7 — INFO: clause-s counter accepts non-ASCII decimal digits
- `n[0].isdigit()` and `int(n[0])` (:349) accept e.g. `٣٣/٣٣ passed`. Cosmetic; unreachable in practice.

## Fixture re-derivation (the 10 assigned teeth, hand-derived against the reference docstring)
FIXTURES has exactly 49 entries and all ten named teeth are present (verified by import:
`len(m.FIXTURES) == 49`; labels matched). All ten expectations re-derived and AGREE with the frozen contract:

1. `scale-1.3-corrected` — S=1.3, live 3440x1440. 3440/1.3 and 1440/1.3 non-whole, so K=round-half-up(156.0)=156;
   156/120 divides neither; first hit scanning `(K+i)` then `(K-i)` (ref:71-73) is i=4 → 160/120 = 4/3
   (3440/(4/3)=2580, 1440/(4/3)=1080) → E=1.3333…; live scale 1.33333333 differs by ~3.3e-9 < 1e-4 → AGREE.
   The rule line prints the rule's own scale `1.3000`. Matches fixture. (Counterpart `scale-1.3-as-written`
   with live 1.3: |1.3−4/3|≈0.0333 → scale DIFFER ✓.)
2. `readd-moves-last` — adding the third `desc:{D}` line erases the first same-selector rule and appends
   (ref:8-9), so the final list is [{A}@60 n=1, desc:{D}@100 n=2}; output {A} (desc exactly {D}) takes the LAST
   match n=2 → 3440x1440@100 vs live 99.997 (|Δ|<1, ref:68) → AGREE; lines=3 rules=2 ✓ rc 0.
3. `fallback-first-empty-and-named` — {A} matches no named selector → first empty-selector rule (ref:60-61):
   preferred/auto/scale "1"; scale explicit → compared, live 1 → AGREE. {C} rule n=2: position 0x0 vs live
   x=3440 → position DIFFER. matched=2, so DIFFER (rc 1), not NO_MATCHING_MONITOR ✓.
4. `transform-modifier-bad` — value 9 ∉ 0-7 → badrules=1, no copy (ref:38-39); rules stays 1, lines=2, verdict
   OK rc 0 — badrules correctly does NOT feed NOT_COMPARED (only v2/unsupported do, ref:86-87) ✓.
5. `addreserved-keeps-rule` — a rule with selector SEL exists → addreserved changes nothing (ref:41-42);
   rules=1 lines=2, explicit 1920x1080@60 vs live 3440x1440@99.997 → mode DIFFER rc 1 ✓. (Companion
   `addreserved-adds-default`: default preferred/auto/auto leaves live x=50/scale=1.5 uncompared → AGREE ✓.)
6. `mirror-missing` — only {B} ruled with `mirror, {A}`; A → UNRULED; B's mirrorOf must equal the decimal id of
   the dump output named {A} ("4") vs live "none" → mirror DIFFER; summary DIFFER outputs=2 matched=1
   unruled=1 rc 1 ✓.
7. `comments` — `# monitor = …` does not fullmatch `monitor[ \t]*=(.*)` (anchored); trailing ` # main` is cut
   before the comma split (ref:34-35) → lines=1 rules=1 AGREE rc 0 ✓.
8. `wrong-types` — live x="0" (string) fails position; transform=true fails transform ("booleans are never
   numbers", ref:82-83); differ joined in check order → `position,transform` DIFFER rc 1 ✓.
9. `monitorv2` — the block opener counts v2=1 (first-token rule, ref:33); the monitor line is still parsed and
   its rule added (rules=1, AGREE counted) but the verdict is NOT_COMPARED rc 5 because v2>0 can change which
   rule applies (ref:86-87) ✓.
10. `sdr-eotf-drops-rule` — `sdr_eotf` is not one of the eight known keys (ref:46-47) → badrules=1, rule not
    added; lines=1 with v2=0/unsupported=0 → not NO_RULES, not NOT_COMPARED → NO_MATCHING_MONITOR rc 3,
    output UNRULED ✓. This is exactly the source-over-wiki tooth the registration describes (efb50993's
    handleMonitor reads sdr_eotf only in monitorv2).

## Seeded name generator
- `names(seed)` (:245-257): three distinct names from 6 prefixes × digits 1-9 (54-name space), distinctness
  enforced by the loop; {D} = vendor + 6 chars of a 34-char alnum alphabet. Deterministic, default seed 45
  (:18, :376) — satisfies the round-44 D4 closure (bare run reproduces).
- Verified over seeds 0..500: {A}{B}{C} always pairwise distinct, never a prefix of another (single-digit
  suffixes make "DP-1" vs "DP-11" impossible), never the sentinel `none` (which would collide with the
  mirrorOf no-mirror value), always well-formed; `names(45)` = `DP-5`, `eDP-7`, `DVI-D-5`,
  `Dell Inc. 6AHUHV`. Substitution is applied to configs, dumps AND expected lines (:300, :324), so any
  assignment of the shuffled triple stays consistent with the asymmetric fixtures (e.g. mirror ids 4/5).

## Read-only clause mechanics (beyond F1)
- For the fixture phase the mechanics are sound: four stubs (`hyprctl`, `journalctl`, `wlr-randr`,
  `wayland-info`), each touching the absolute marker path unconditionally (:272-278); PATH puts fakebin first
  (:311); marker checked once after all fixtures (:362). Verified live: the toy tool (which invokes hyprctl
  only in selftest) leaves `marker=absent`; the clean REF run reports `clause=r marker=absent`; and the
  counter honors `--work` only — every `tempfile.mkdtemp` call passes `dir=` explicitly (:283, :336, :340,
  :355, :381), no `gettempdir()` fallback exists.
- Relative `--work` is safe: `tempfile.mkdtemp(dir="relsub")` returns an absolute path (tested), so the
  fakebin PATH entry and the marker stay absolute. Confirmed by a full run with cwd=scratch and
  `--work wrel`: rc=0, `fixtures=49/49 … TARGET_MET` (`receipts/ref-run-relwork.txt`).

## Scratch hygiene
- The counter creates everything under one `mkdtemp(dir=a.work, prefix="c1r45-")` (:381) and deletes it in a
  `finally` (:384-385), including on the Setup/bad-rev path. Empirically: after four full counter runs, zero
  `c1r45-*` dirs remain in the work dir. (The `fx-*`/`bin-*`/`st-*`/`tool-*` dirs currently in my scratch `w/`
  are from my own patched `score()` calls that bypassed `main()` — harness residue, removed in cleanup, not a
  counter leak.) The marker and fakebin live under `--work` too (:354-355). The fixture env has no TMPDIR
  (frozen four-key env, :13-14, :311-312), so a tool's own `tempfile` use would go to /tmp — outside the
  counter's control and outside its claims.

## Crash paths (all exercised live)
| Case | Behavior | Receipt |
|---|---|---|
| bad rev | `PRED-C1-r45: SETUP bad rev`, exit 2 | receipts/badrev-run.txt |
| tool absent (base 0c89478) | `fixtures=0/49 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED`, exit 1 — exactly the registration's "Before" line | receipts/base-run.txt |
| binary stdout (selftest) | clause-s fail, decoded-with-replace repr, no crash | receipts/chaos-run.txt |
| binary stdout (fixture) | `FAIL rc=9 … got='\ufffd\x00\ufffd binary\n'`, no crash | receipts/chaos2-run.txt |
| 64 MB stdout | captured, compared, `FAIL rc=7`, no crash | receipts/chaos-run.txt |
| 15 s hang | `FAIL timeout` at 10 s, run completes, clean final line | receipts/chaos2-run.txt |
| relative --work | safe (mkdtemp absolutizes); rc=0 full run | receipts/ref-run-relwork.txt |
| tool blob not Python | selftest/fixture rc/stderr mismatch → fail (code read; graceful paths identical to rc-mismatch case) | — |

## Verified-good (docstring vs code, every clause)
- a (:9 → :330-331): `ls-tree` mode in {100644,100755} and type blob; symlink/submodule/tree → absent ✓.
- s (:10-12 → :340-353): rc==0, exact last line `MADO_MONITORS_SELFTEST: N/N passed`, N==N, isdigit, N>=30
  (:53), 60 s timeout; observed 33/33 for the reference ✓.
- f (:12-18 → :281-323): fresh per-fixture cwd and HOME (:283-285), env exactly the four keys (:311-312),
  10 s timeout (:315), exact stdout / exit / empty-stderr comparison (:320), seed substitution in configs,
  dumps and expectations (:309, :290, :318), all 49 fixtures individually reported (:358-361) ✓.
- r (:19-20 → :272-278, :311, :354-356, :362): correct for the fixture phase (gap = F1) ✓.
- Final line/exits (:21-23 → :365-368, :378-388): byte-format matches; exit 0/1/2 verified live ✓.
- Positive control: reference installed as `tools/mado-monitors.py` in a scratch clone at the freeze →
  `fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, rc 0, ~0.7 s — the counter is not
  vacuous and the R/O/S line formats line up byte-exactly (`receipts/ref-run.txt`).

## Residual risk and verification gaps
- F1 is unremediable inside the frozen counter (any edit = re-registration as v2). It does not weaken the
  TARGET_MET semantics for an honest tool, but w1/the L1 should carry it as a declared limitation of clause r
  alongside the already-declared "catches PATH lookups only" residual.
- I did not fuzz the fixture table or the substitution engine beyond the reference control; the 49/49 REF run
  is the format cross-check.
- The 16 K-controls were not re-run here (out of scope; registration reports 0/16 MET in
  `receipts/ctl-c1.txt`).
- F4's OSError trigger and F5's noexec scenario are host-untestable here (git present, /fast exec-allowed);
  both are code-certain, trigger-conditional.

## Receipts (copied to `.ufo/waves/round-45/w1/RevC1Counter/receipts/`)
`base-run.txt`, `badrev-run.txt`, `ref-run.txt`, `ref-run-relwork.txt`, `toy-selftest-gap-run.txt`,
`chaos-run.txt`, `chaos2-run.txt`, `locator-check.txt` (script-verified quote locators). Scratch
`/fast/scratch/hyaku/mado-r45/RevC1Counter` deleted after receipt copy.

Locator verification: every quoted line above was re-grepped at its cited line by
`receipts/locator-check.txt` (all PASS); locators computed with `grep -n`, never typed.
