# ExecCounterC2R50 — PRED-C2-r50 counter draft + nonce fixtures (mado round 50, w1 build)

Seat `ExecCounterC2R50` (executor, leaf). Lane `mado-shokunin`, base `8ae47b957034ae21012bbf09173cca2c48be345e`, claims
`13631f24050f22db92bf5bd33e0f4d014192992e`. Target: the C2 counter draft `quality/counters/c2-r50-session-gate.py` (`PRED-C2-r50`)
that scores the session-material gate a revision installs, plus its nonce-generated shape fixtures. Nothing here is frozen: the L1
freezes the predicate after `w1`; `w2` attacks it.

## 0. Verdict

**The draft behaves both ways, measured.** At base (v2 gate installed, `82c9053a…`) it returns `TARGET_MISSED`, exit 1. On a scratch
clone with the v3 draft installed at `quality/check-session-material.py` (`ffdc9d62…`) it returns `TARGET_MET`, exit 0 — on two
nonces. Every red family is killed by removing exactly that rule from the gate, every green family survives, and three wrong gates
(over-flagging stub, v2-with-scope-all, v3-rules-with-ufo-default) all miss. The final line is

```
PRED-C2-r50: selftest=.. names=.. red=A/K green=B/K scope=.. verdict=TARGET_MET|TARGET_MISSED rev=<full sha>
```

## 1. Deliverables (seat dir; sha256 of the bytes this report names)

| path | sha256 | what |
|---|---|---|
| `c2-r50-session-gate.py` | `1d52a62cd969aba5…ebd62b298` | the counter draft (577 lines), PRED-C2-r50 |
| `v2-selftest-cases.txt` | `38a8b2c647665b68…8097e725` | the 69 v2 case names, sorted, from the v2 bytes at base |
| `check-cases.py` | `12637958316b691f…9811bf83b` | re-derives those names from `git show <base>:quality/…` and diffs them against the seat file and the counter's embedded tuple |
| `show-shapes.py` | `13dcca9dbc0629ec…a2a6d8c60` | prints one generated instance per family, identities masked |
| `receipts/base-v2.txt` | `8437ba305ac07144…bfba60f4` | base run (v2 gate) — MISS |
| `receipts/target-v3-nonce50117.txt` | `70e595bf586e5ac3…e48fcea` | target run, nonce 50117 — MEET |
| `receipts/target-v3-nonce778899.txt` | `dfe6b0f830cf57a0…62d0d42` | target run, nonce 778899 — MEET |
| `receipts/control-stub.txt` | `d4f20d77b1e67b33…1bbfb1d0` | flag-every-line stub gate — MISS |
| `receipts/control-v2-scope-all.txt` | `4f88016996b5d5e8…1ff431a8` | v2 gate with default scope all — MISS |
| `receipts/control-v3-ufo-default.txt` | `ef444fc58bade1b3…c9e0ded8` | v3 rules with `DEFAULT_SCOPE ufo` — MISS |
| `receipts/mutants.txt` | `4102257320566511…035cea3` | R7/R8/R9 emission removed one at a time — each red family drops exactly |
| `receipts/mutant-renamed-case.txt` | `785405f0dab8e94d…7a733851` | 94/94 selftest with one v2 case renamed — `names=68/69` MISS |
| `receipts/refusals.txt` | `320b25eedf819817…6d460434` | `--work`/`TMPDIR` under `/tmp`, `/var/tmp`, `/dev/shm`, `--work` under the invoking HOME, missing `--work` → exit 2 |
| `receipts/cases-check.txt` | `e722cf914119beec…c9a6ef5fb` | embedded list = seat file = gate output; `verdict=OK` |
| `receipts/control-gates.txt` | `4310b2997a1c4924…ea705290` | control gate sources, their sha256, and the patched lines |
| `receipts/v2-case-names.txt` | `a55e39d2fb61e96d…7c334d` | provenance of the 69 names (command, base sha, count, prefix histogram) |
| `receipts/shapes.txt` | `4d1178cc7be23722…72a6a36b22` | one masked instance per family |

## 2. Clauses as implemented

| clause | instrument | measured |
|---|---|---|
| `s` | gate's own `--selftest`: `passed==total`, `failed==0`, `total>=94`, and every one of the 69 v2 case names present (set containment; names parsed from `SELFTEST ok case=…` lines) | base `69/69` → fail (<94); v3 `94/94` + `names=69/69` → pass; renamed-case mutant `94/94` but `names=68/69` → fail |
| `r` | `K = 40 + nonce%5` fixture git repos (`init -q`, toplevel asserted before and after the commit, one commit each) each holding one instance of one covered shape; run with the gate's **default** scope and `--account <synthetic>` when the gate's bytes name that flag. A repo counts only if the expected rule appears, findings `>=1` and exit non-zero | base `0/42` (v2 sees `.ufo/` only; files=0); v3 `42/42`; nonce 778899 `44/44` |
| `g` | `K = 40 + (nonce//7)%5` counter-shape repos, same construction; a repo counts only if exit 0, findings `0` **and** `files>=1` (a gate that scans nothing cannot pass vacuously) | v3 `44/44` (nonce 50117), `41/41` (778899); base `0/44` (`files=0`); stub `0/44` |
| `d` | a repo whose only red instance is `docs/receipt.txt`; the default run must find it, and `--scope ufo` (when the gate has the flag) must report `files=0 findings=0` | v3 `default_files=1 findings=1` + ufo clean → `seen`; v2 → `blind` |

Fixture identities are synthetic by construction: home users `someoneNNN`, accounts `fixtureNNNN`, word paths; the account is never
the invoking account, and no fixture derives from host state. Gate bytes come from `git show <rev>:quality/check-session-material.py`
(never the working tree), are written to `--work/gates/gate-<sha12>.py`, and run as `python3 -I <gate>` with `HOME`,
`XDG_CACHE_HOME`, `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME` and `TMPDIR` under `--work`, `cwd=--work`. Fixtures are
removed at exit; the gate copy stays for inspection. `--work` is refused (exit 2) under `/tmp`, `/var/tmp`, `/dev/shm`, under the
invoking `HOME`, or when an inherited `TMPDIR` sits in those three roots.

## 3. Runs (receipts in `receipts/`)

| run | gate at rev | rev scored | final line |
|---|---|---|---|
| base | v2 `82c9053a…` | `8ae47b95…` | `selftest=69/69 names=69/69 red=0/42 green=0/44 scope=blind verdict=TARGET_MISSED` exit 1 |
| target nonce 50117 | v3 draft `ffdc9d62…` | `22dd5068…` (clone) | `selftest=94/94 names=69/69 red=42/42 green=44/44 scope=seen verdict=TARGET_MET` exit 0 |
| target nonce 778899 | v3 draft `ffdc9d62…` | `22dd5068…` | `selftest=94/94 names=69/69 red=44/44 green=41/41 scope=seen verdict=TARGET_MET` exit 0 |
| control stub | `3c0a46b9…` | `f32bbfeb…` | `selftest=94/94 names=69/69 red=0/42 green=0/44 scope=seen verdict=TARGET_MISSED` exit 1 |
| control v2-scope-all | `8e2b8e43…` | `ea76645d…` | `selftest=65/69 names=69/69 red=0/42 green=44/44 scope=blind verdict=TARGET_MISSED` exit 1 |
| control v3-ufo-default | `3758808c…` | `495babd9…` | `selftest=93/94 names=69/69 red=0/42 green=0/44 scope=blind verdict=TARGET_MISSED` exit 1 |
| mutant R7 | `1ec97f9d…` | `f297b902…` | `red=14/42 families=r7-prefix=0/7 r7-header=0/7 r7-diag=0/7 r7-row=0/7 r8-account=7/7 r9-cache=7/7 scope=blind` MISS |
| mutant R8 | `ae769d30…` | `5313ff3d…` | `red=35/42 … r8-account=0/7 … scope=seen` MISS |
| mutant R9 | `24447520…` | `69080957…` | `red=35/42 … r9-cache=0/7 … scope=seen` MISS |
| mutant renamed case | `fe8abfdb…` | `c0020051…` | `selftest=94/94 names=68/69 red=42/42 green=44/44 scope=seen verdict=TARGET_MISSED` exit 1 |

What each control buys: the stub proves `g` is not decorative (it passes the selftest and the scope shape but over-flags every green
repo, and its findings name no R7/R8/R9 rule); v2-with-default-all proves the *rules* (not the scope) are what `r` needs, and shows
the v2 selftest pins the ufo default (4 cases fail: `e2e-outside-ufo-not-scanned`, `e2e-empty-ufo-clean`, the two
`waiver-gate-copy-*`); v3-with-ufo proves clause `d` is load-bearing (one v3 case, `v3-default-scope-all-sees-outside-ufo`, fails
and `r` goes `0/42`). Mutants and the renamed case prove `r` and `s` are rule/case-specific rather than "any finding / any count".

## 4. Fixture families (`receipts/shapes.txt`, identities masked)

Red (6 families, cycled so each gets ≥ 5 of K): `r7-prefix` `/home/U/Projects/echo/echo.py:110: SyntaxWarning: …`; `r7-header`
`/home/U/.cache/xdg-terminal-exec/:`; `r7-diag` `xkbcommon: INFO: could not open "/home/U/.config/november.kc"`; `r7-row`
`-rw-r--r-- 1 root root 516250 Oct 26 19:50 /home/U/quebec.txt`; `r8-account`
`-rw-r--r-- 1 fixtureN fixtureN 322157 … xdg-terminal-exec` (own `--account`); `r9-cache` `--dir=/home/U/victor` +
`--title=… window title`.

Green (7 families): `Copied ~/Projects/X to ~/Backups/X …`; `$HOME/.config/hypr/hyprland.conf`; a home path inside a prose sentence;
`-rw-r--r-- 1 1547 1325 434313 … xdg-terminal-exec` (numeric ids); one `--title=` field; two-space-indented usage text;
`~/Projects/X/X.py:12: …` (masked prefix form).

Clause `d` uses the `r7-prefix` shape at `docs/receipt.txt`, outside `.ufo/`.

## 5. Risks, limits, declared gaps (the w2 attack surface)

1. **Single-shape, single-line fixtures.** Each red repo carries one clean instance of one form. A gate that whitelists an exact
   line pattern would pass; a shape embedded mid-paragraph, wrapped across lines, CRLF, or a path containing a space is not tested
   here (R7 `prefix` with a space is a declared gate gap, round-49 shapes §6.4). Attacking this is the natural w2 move.
2. **No waiver registry in fixtures.** Fixture repos have no `quality/session-material-waivers.txt` and no `quality/gate.py`, so the
   `kind=gate-copy` and waiver paths are outside this counter (the gate's own selftest covers them).
3. **`g` requires `files>=1`.** Deliberate: it stops a gate with an empty default scope from passing `g` vacuously. A gate that
   omits the `files=` field on its `SESSION_MATERIAL:` line reads as `None` and fails `g` — that line is part of the contract.
4. **`--account` is passed only when the gate's bytes contain the flag.** A gate that renames it (e.g. `--user`) leaves R8 inert →
   that family misses → MISS. Declared, because the C2 claim names R8's account behaviour.
5. **K is nonce-derived in a narrow band** (40–44 per clause) so a run costs ~4–5 s; families cycle, not sample.
6. **A `.ufo/`-only gate cannot pass**: red fixtures live outside `.ufo/` and clause `d` fails. That is the v2 blindness the claim
   is about.
7. **No knob for the gate under test**: the gate is whatever `--repo`/`--rev` installs, so a control run is always a named repo and
   revision in the receipt. Freeze risk is a wrong `--rev`, not a hidden flag.
8. Not scored: gate stderr, timing, `--home-limit`, `--serial-from-host` (host reads), and R1–R6 (no fixture family).
9. Cost and state: ~4–5 s/run, ~20 MB of fixtures created and removed under `--work`. Nothing is written to `HOME`, `XDG_*`, the
   lane or the fleet; `--work` under a home is refused rather than allowed (host-guard direction).

## 6. What this attacks / supports

- **Supports C2** (operability: the gate v3 installed): the instrument a freeze can hang on — detection of every covered red shape at
  a revision, no false positive on the green counter-shapes, v2 selftest names kept, default scope covering non-`.ufo/` files.
- **Supports D7** (host guard installed with a both-ways receipt) in form: same both-ways pattern, three controls plus four mutants.
- **Attacks the round-49 gate evidence** where it is thin: `w1/ExecSessionShapes` measured 5 findings on one hand-built fixture; this
  counter measures 42–44 single-shape repos with random identities and proves per-rule discrimination, so a shape-specific
  regression in a later edit fails one family, not the whole clause silently.
- **Freeze proposal** (L1 wording): `PRED-C2-r50 = at the data revision, c2-r50-session-gate.py prints verdict=TARGET_MET (exit 0),
  with a base run at 8ae47b95 printing TARGET_MISSED (exit 1)`; the instrument is the four clauses above, unmodified, with the
  stub / v2-scope-all / v3-ufo gates as the do-nothing controls.

## 7. Reproduce

Scratch: `/fast/scratch/hyaku/mado-r50/ExecCounterC2R50` (removed at the end of the seat); `ulimit -f 65536`; `HOME`, `XDG_*` and
`TMPDIR` inside it; no pacman, no compositor verb, no host write.

```
# base (v2 installed) — MISS
python3 -I .ufo/waves/round-50/w1/ExecCounterC2R50/c2-r50-session-gate.py \
  --repo <lane> --rev 8ae47b957034ae21012bbf09173cca2c48be345e --work <scratch>/w1 --nonce 50117
# target — clone the lane, cp the v3 draft over quality/check-session-material.py, commit, then:
python3 -I .ufo/waves/round-50/w1/ExecCounterC2R50/c2-r50-session-gate.py \
  --repo <clone> --rev HEAD --work <scratch>/w2 --nonce 778899
# case-list provenance
python3 -I .ufo/waves/round-50/w1/ExecCounterC2R50/check-cases.py --repo <lane> --work <scratch>/w3
# the shapes each fixture holds
python3 -I .ufo/waves/round-50/w1/ExecCounterC2R50/show-shapes.py --seed 50117
```

Tooling: none installed or upgraded. `python3 3.14.8` (`/usr/bin/python3`), `git 2.56.0`. No pacman transaction, no host service,
no input injection, no GUI. Session material stays shape-only: every receipt masks the home user (`/home/U`) and the synthetic
account (`fixtureN`); no raw binds, titles, serials, device names, process tables or account names appear.

## 8. Self-scan (the seat dir under its own gate)

`receipts/self-scan.txt` runs the v3 gate (`ffdc9d62…`, from `quality/check-session-material.py` at the target clone's HEAD) with
`--scope all` over a fixture repo holding **every file in this seat dir, this report included**, and reports each file's sha256 with
the finding count. It runs after the last byte of this report is written, so the bytes it scanned are the bytes on disk.
