# matrix.md — C1 counter mutation matrix (MutC1CounterGates, round-41 w1, 2026-10-25)

Target: `quality/counters/c1-r41-globals.py` (PRED-C1-r41-v1), pristine sha256
`e43dc235925635ffc2008a3af4872f33b9be6a461a5cea77a98e008ae2a3f32a` (= `git show HEAD:quality/counters/c1-r41-globals.py | sha256sum`;
never edited by this seat — all mutants are copies under `mutants/`, one single textual edit each).

Detector (full suite, every mutant, no `--only` shortcuts unless stated):
`python3 -I .ufo/waves/round-41/ctl/run-c1-controls.py --repo . --counter <mutant> --ref .ufo/waves/round-41/c1/ctl-ref-tool.py.txt`
(default `--rev master` = cd950ec781149040cc73d71cd67c2b67452e7724). Suite = 47 controls: P-reference must score
TARGET_MET; D1–D3, M01–M39, C1–C4 cheats must each score TARGET_MISSED. KILLED = >=1 control wrong (rc != 0);
SURVIVED = rc 0, 47/47 correct.

**Baseline (pristine counter, full suite):** rc=0, `controls=47 correct=47/47` (`logs/BASELINE-pristine.log`).

## Verdicts: 8 killed / 12 survived (of 20)

| mutant | single edit (counter) | expected | verdict | killed by / why invisible | evidence |
|---|---|---|---|---|---|
| K01-g-always-pass | `cl["g"] = int(imports_ok(src))` -> `cl["g"] = 1` | killed | **KILLED** | all 4 cheat controls flip MET (C1-exec, C2-os.system, C3-socket, C4-counter-name) | `logs/K01-….log`, 43/47 |
| K02-str-deny-drop | `STR_DENY = ("/proc", "c1-r41", "quality/counters")` -> `("/proc",)` | killed | **KILLED** | C4-cheat-counter-name MET | `logs/K02-….log`, 46/47 |
| K03-stdlib-deny-drop | drop `not (mods & STDLIB_DENY)` from `imports_ok` | killed | **SURVIVED** | DENY set is dead code: socket is also outside STDLIB_ALLOW, so C3-cheat-socket stays MISSED via the allow-list | `logs/K03-….log`, 47/47 |
| K04-call-deny-drop | `if isinstance(f, ast.Name) and f.id in CALL_DENY:` -> `if False:` | killed | **KILLED** | C1-cheat-exec MET | `logs/K04-….log`, 46/47 |
| K05-os-deny-drop | `and (f.attr in OS_DENY or f.attr.startswith("exec")):` -> `and False:` | killed | **KILLED** | C2-cheat-os-system MET | `logs/K05-….log`, 46/47 |
| K06-marker-check-off | judge's `if os.path.exists(...hit") and file_mode:` -> `if False:` | killed | **KILLED** | M14-spawns-in-file-mode MET (24/24) | `logs/K06-….log`, 46/47 |
| K07-rc-check-off | judge's `if rc != want_rc:` -> `if False:` | killed | **SURVIVED** | M15/M33 reach `fixtures=24/24` but stay MISSED — the tool's own selftest (clause b) catches the rc defects; counter rc gate is redundant for every control | `logs/K07-….log` (M15, M33 lines) |
| K08-livewritable0-always-ok | `("livewritable0", score_livewritable0)` -> `("livewritable0", (lambda *a, **k: (1, "ok")))` | killed | **SURVIVED** | M12 reaches `fixtures=24/24`, stays MISSED via clause b (selftest covers writability); counter-side livewritable0 gate redundant | `logs/K08-….log` (M12 line) |
| K09-nosess0-always-ok | `("nosess0", score_nosess0)` -> always-ok lambda | killed | **SURVIVED** | M34 stays MISSED (22/24 in retry) — its defect is also caught outside nosess0. First run "killed" by M39 flipping MET, which the nosess0 edit cannot cause (teeth never runs fixtures): a nonce lottery, not reproduced (retry 47/47; M39 MISSED 24/24 clause-caught) | `logs/K09-….log`, `logs/K09-….retry1.log` |
| K10-noise-cr-drop | noise_lines CR variant `advert(...) + "\\r"` -> `""` | killed | **SURVIVED** | M38-crlf-tolerated reaches `fixtures=24/24`, stays MISSED via clause b (selftest covers CR handling); no fixture-level CR detection is needed by any control | `logs/K10-….log` (M38 line) |
| K11-total-23 | `TOTAL = 24` -> `TOTAL = 23` | killed | **KILLED** | P-reference wrong: counter dies on `assert len(cases) == TOTAL` for every control | `logs/K11-….log`, 46/47 |
| K12-sandbox-cmd-drop | `cmd = ["bwrap", ...` -> `cmd = ["/usr/bin/true",` (sandbox launcher no-op) | killed | **KILLED** | P-reference `fixtures=0/24 TARGET_MISSED` | `logs/K12-….log`, 46/47 |
| K13-stdin-pipe-off | run_piped `stdin=r` -> `stdin=None` | killed | **KILLED** | M11-stdin-inherited MET (24/24): with no inherited pipe, the stub's `[ -p /dev/stdin ]` guard passes | `logs/K13-….log`, 46/47 |
| S01-stderr-ignore | judge's `if want_rc in (0, 1, 3) and err:` -> `if False:` | survived | **SURVIVED** | no control tool writes stderr on rc 0/1/3, so the stderr-emptiness clause has no detector | `logs/S01-….log`, 47/47 |
| S02-clause-b-always | `cl["b"] = int(rc == 0 and has and k == n and n >= MIN_SELFTEST)` -> `cl["b"] = 1` | survived | **SURVIVED** | b2 teeth still gates M39 (its fake `99/99` selftest ignores flipped comparisons); D1–D3 fail on fixtures. First run "killed" by M27 flipping MET — the clause-b edit cannot affect fixture scoring: nonce lottery, not reproduced (retry 47/47) | `logs/S02-….log`, `logs/S02-….retry1.log` |
| S03-git-env-keep | `ENV = {k: v … if not k.startswith("GIT_")}` -> `ENV = dict(os.environ)` | survived | **SURVIVED** | ambient GIT_* here are only GIT_EDITOR/GIT_PAGER/GIT_TERMINAL_PROMPT (no GIT_DIR-class var); bwrap `--clearenv` guards the tool side; "ambient GIT_* removed" is untested | `logs/S03-….log`, 47/47 |
| S04-nonce-constant | `secrets.token_hex(8)` -> `"0000000000000000"` | survived | **SURVIVED** | nonce freshness/replayability (docstring clause) is exercised by no control; fixtures are verdict-stable across nonces | `logs/S04-….log`, 47/47 |
| S05-base-check-off | `if git(repo, "show", "%s:%s" % (base, TOOL)) is not None:` -> `if False:` | survived | **SURVIVED** | no control exercises BASE; clause a's "BASE must lack it" half is untestable by this suite (all controls use `--tool`) | `logs/S05-….log`, 47/47 |
| S06-noise-program-drop | noise_lines wrong-program variant (`Hyprland[pid]`) -> `""` | survived | **SURVIVED** | no M-mutant loosens program-name matching, and the line is ignored by model and reference alike, so removing it changes no verdict | `logs/S06-….log`, 47/47 |
| S07-exit-always-0 | main's `return 0 if met else 1` -> `return 0` | survived | **SURVIVED** | the runner gates MET on `rc == 0` AND `"TARGET_MET" in line` (score() in run-c1-controls.py), so the counter exit code is a redundant second channel no control reads alone | `logs/S07-….log`, 47/47 |

## Control-suite flakiness found while testing (side finding)

Two controls have rare nonce-dependent kill conditions and fired on draws where the counter edit under test
**cannot** have caused them:

- **M27-boot-uppercase** flipped MET once (`nonce=041b7c817fd6b54a`, in the S02 first run; its 24/24 requires
  gen3's interleaved noise to sample the uppercase `-- Boot AAAA…` line mid-session, which is `rng.choice`-dependent).
- **M39-selftest-echo** flipped MET once (`nonce=93700cd68c57b13c`, in the K09 first run; b2's 6 nonce-chosen
  comparison flips only kill the fake-selftest tool when >= 4 flipped copies *crash* the selftest before the
  constant print — nonce-dependent).

Frequencies observed: each flipped 1 time in 22 full-suite draws (baseline + 20 mutants + 2 retries; on pristine
and on mutants whose edits cannot touch the flipped mechanism), 0/20 targeted pristine `--only` draws each
(`logs/lottery-M27-*.log`, `logs/lottery-M39-*.log`), and neither reproduced on retry. So ~2/22 full-suite runs
of a *correct* counter would spuriously report `correct=46/47` (false alarm), and the same lottery can masquerade
as a "kill" in mutation testing.

## Structural finding

For parser/report details (CR endings, writability, exit codes, diff/expect edge behavior), the reference tool's
own selftest — clause b, enforced via clause b2's teeth — already catches the corresponding *tool* mutants
(M12, M15, M33, M38 all show `fixtures=24/24` with `TARGET_MISSED` under counters weakened on those gates).
Consequently the counter's own fixture-level enforcement of those same behaviors is **redundant**: weakening or
neutering it (K07, K08, K09, K10) is invisible to the whole 47-control suite.

## Restoration evidence

- Pristine counter after all runs: sha256 `e43dc235925635ffc2008a3af4872f33b9be6a461a5cea77a98e008ae2a3f32a`,
  equal to `git show HEAD:quality/counters/c1-r41-globals.py`; `git status --porcelain` on the path is empty
  (PRISTINE_UNTOUCHED). Only seat-dir files were written.
- Tooling: nothing installed (bwrap/git/python3 already present); pacman untouched.
