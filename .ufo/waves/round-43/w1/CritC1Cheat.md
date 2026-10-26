# CritC1Cheat — cheat designs against C1 (`PRED-C1-r42`), round 43 wave w1

Seat: `CritC1Cheat` (critic, leaf). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, freeze
`b2e2efd6e268920d31f3c32cf52dc097dd6e1d22`, base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`, counter
`quality/counters/c1-r42-geometry.py` (unmodified), reference `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`.
Every cheat below is a single file in this seat directory and was scored with

```
C1R42_TMP=/fast/scratch/hyaku/mado-r43/CritC1Cheat python3 -I quality/counters/c1-r42-geometry.py \
  --repo . --rev b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 --tool .ufo/waves/round-43/w1/CritC1Cheat/cheat-N-*.py
```

Reference calibration under the same conditions: `receipt-reference.txt` — `fixtures=37/37 verdict=TARGET_MET`,
`clause=b2 sites=35 killed=5/6` (the one survivor is `read_regular:95`, the read-loop bound the control
runner also documents as equivalent for regular files), `clauses=a:1 b:1 b2:1 b3:1 g:1`. bwrap 0.13.1.

## Verdict table

| cheat | bytes | capability | fixtures | clauses | verdict | caught by |
|---|---|---|---|---|---|---|
| 1 `cheat-1-rename.py` | 20777 | full model, every identifier renamed | 37/37 | a1 b1 b2:1 b3:1 g1 | **TARGET_MET** | nothing — declared residual |
| 2 `cheat-2-fixed-table.py` | 41955 | none (table over fixture bytes) | **26/37** | a1 b1 **b2:0** b3:1 **g:0** | TARGET_MISSED | the nonce lattice (+ b2, g incidentally) |
| 3 `cheat-3-mirror-selftest.py` | 13223 | full model, selftest mirrors the code | 37/37 | a1 b1 **b2:0** b3:1 g1 | TARGET_MISSED | clause b2 (`killed=0/6 forced_dead=0`) |
| 4 `cheat-4-selfhash-teeth.py` | 14146 | full model, selftest is a source pin | 37/37 | a1 b1 b2:1 b3:1 g1 | **TARGET_MET** | nothing — **HOLE** |
| 4b `cheat-4b-broken-model.py` | 14311 | **none** (report replaced by one constant line) | **5/37** | a1 b1 b2:1 b3:1 g1 | TARGET_MISSED | only the fixture count — every clause passes |
| 5 `cheat-5-cache.py` | 21120 | full model behind a `/tmp` warm marker | **1/37** | all 1 | TARGET_MISSED | fresh tmpfs per run, no cross-run channel |
| 6 `cheat-6-detect.py` | 20756 | full model, only when sandboxed | 37/37 | a1 b1 b2:1 b3:1 g1 | **TARGET_MET** | nothing — **HOLE** (declared residual, under-scoped) |

Receipts: `receipt-cheat-1-rename.txt` … `receipt-cheat-6-detect.txt`, `receipt-cheat-4b-broken-model.txt`, `receipt-reference.txt`,
`receipt-tightening.txt`, `receipt-env.txt`, `receipt-visibility.json`, `receipt-host-vs-sandbox.txt`,
`receipt-sha256.txt`.

## 1. Embed the model, rename everything — MET, and this is the declared residual

`cheat-1-rename.py` is the reference with `read_regular→load_input`, `parse_args→mode_and_paths`,
`report→render_report`, `selftest→selfcheck`, `Setup→ContractError`, every constant renamed, plus the CLI
literal `--selftest` restored (renaming it would break the contract text, not a name check). Result: MET,
all five clauses, `fixtures=37/37` (`receipt-cheat-1-rename.txt` last two lines).

- Why nothing catches it: the registration's own residual — a tool that contains the contract's model *is*
  an implementation (counter docstring, residual paragraph, line 88). No tightening is warranted; a rename
  is not a defect. Report it so the residual is not mistaken for a hole in w2.
- Secondary, real: `clause=b2 sites=64` here vs `sites=35` for the reference and cheat-3/4 — the *same code*
  yields two site inventories because `NOT_SITES = ("selftest", "main", "usage")` (line 837) excludes exact
  names. Renaming the selftest to `selfcheck` turns its 29 `chk` comparisons into mutation sites. Impact is
  benign today (the forced site still lands in `render_report`, the summary-text function), but the site
  inventory is a name artefact, not a structure fact.
- Fragility also visible: this tool killed exactly **4/6** (`KILL_NEED = 4`, line 113) — it MET at the bar.
  Two sampled sites in `drive_cli` survived, as `read_regular:95` does for the reference. Tightening that
  does not reject the reference: require `killed == N_MUT` and drop the two equivalent sites from the
  reference's inventory by construction — or simply raise `KILL_NEED` to 5 (reference kills 5/6; cheat-1
  killed 4/6 on the recorded nonce and would then fail, though the sample varies with the nonce). Command to check any candidate inventory: the `clause=b2 … killed=` lines.

## 2. Special-case the fixed fixtures — 26/37, the lattice defeats it

`cheat-2-fixed-table.py` (`receipt-cheat-2-fixed-table.txt`) implements no join. It hashes
`(argv with the cwd normalised, sha256 of every regular file in cwd, stdin)` and returns the reference's
recorded `(rc, stdout)`; unknown keys get a fixed `NO_SIZE_RULES` line. The table was harvested by importing
the frozen counter and replaying its own 27 fixed fixtures against the reference (100 distinct keys).

Result: **26 of 27 fixed fixtures pass, 0 of the 10 `gen*` pass, `many0` fails** → `fixtures=26/37`,
`verdict=TARGET_MISSED`. The failures in the receipt are exactly `gen0…gen9` and `many0`.

- Answer to "does the lattice defeat it?": **yes, and it is the only thing that does.** Every *nonce-free*
  fixed fixture is table-passable; the 11 nonce-derived cases (`gen0…gen9` from `rng_for(REV:NONCE:gen:i)`,
  and `many0`, which is in `FIXED` but seeds from `rng_for("many", NONCE, …)`, line 764) are not. A table
  needs the nonce, and the nonce is not reachable from inside the sandbox (see §5/§7).
- The two other clause failures are incidental and cheap to fix by an attacker: `b2 sites=1 (<12)`, one
  comparison site in total and `g:0` (`import base64/hashlib`). Neither is load-bearing; the fixture count
  is. Do not let a future re-registration shrink or salt away the gen lattice.
- Tightening: none needed for the counter as frozen; if the fixed set is ever made the whole set (cost
  pressure), C1 becomes table-passable. Salt the fixed fixtures with a nonce-derived (never expected-value
  dependent) variation, or keep ≥1 nonce-derived fixture per fixed edge class.

## 3. Selftest that mirrors the code — caught by b2, exactly as designed

`cheat-3-mirror-selftest.py` (`receipt-cheat-3-mirror-selftest.txt`): model untouched; `selftest` is 31
input pairs, and each check compares a value to **the same code path computed again** (`chk("line", s1, s2)`,
`s1 == s2` from two identical `report()` calls), so every flipped comparison moves both sides.
`clause=b rc=0 selftest=93/93`, `clause=b2 sites=35 killed=0/6 forced_dead=0` → MISSED. Fixtures 37/37.

- This is the designed catch: b3 cannot see it (it is already source-invariant) and only the mutation clause
  b2 separates "counts" from "teeth". No tightening.

## 4. Source-integrity pin instead of teeth — MET. The hole

`cheat-4-selfhash-teeth.py` (`receipt-cheat-4-selfhash-teeth.txt`): model untouched, `selftest` replaced by
(a) a 64-bit FNV-1a digest of its **own source**, read through `sys.argv[:1][0]`, with the `PIN = …` line
stripped before hashing, and (b) 60 checks that cannot fail (mirrored, as in cheat-3). If the digest differs
it prints `MADO_GEOMETRY_SELFTEST: 0/60 passed` and exits 1; the two b3 neutral edits are recognised by their
appended markers (`# b3-neutral …`, `B3_NEUTRAL_… = 1`) and skip the pin so b3 still passes.

Empirical result, stable across nonces: `clause=b selftest=60/60`, `clause=b2 killed=6/6 forced_dead=1`,
`clause=b3` both variants `60/60`, `clause=g 1`, `fixtures=37/37`, **TARGET_MET**.

Decisive control — `cheat-4b-broken-model.py` (`receipt-cheat-4b-broken-model.txt`): the same file with
`report()` replaced by one constant line (the capability is gone). Its selftest still prints
`MADO_GEOMETRY_SELFTEST: 60/60 passed`, and the counter still reports the whole clause block
`clauses=a:1 b:1 b2:1 b3:1 g:1` with `b2 killed=6/6 forced_dead=1`; only the fixtures notice
(`fixtures=5/37`). So b/b2/b3 do not attest the behaviour they are named for: they attest that the file's
bytes did not change.

- Why the current clauses do not catch it:
  - `b2` has teeth only if a flipped comparison is observable *behaviourally*. Here the pin turns any textual
    rewrite into a failure, so all six mutants die for the wrong reason. The counter itself forges every
    mutant with `ast.unparse` (line 879), i.e. it hands the tool a new byte string each time.
  - `b3` accepts the neutral variants because the cheat *names the counter's markers*; the two variants are
    the only behaviour-neutral rewrites b3 knows.
  - `g` was meant to stop self-inspection: the docstring forbids the tool to "never name … `sys.argv[0]`"
    (line 81), and `imports_ok` implements it as a `Subscript` whose slice is `ast.Constant(0)`
    (lines 816-821). `sys.argv[:1][0]` is a `Slice` subscript followed by an index, so it passes.
    `__file__` is equally reachable as `sys.argv[:1]`. **Clause g's argv guard is syntactic and evaded.**
- Why it matters: the capability claim C1 rests on `--selftest` being evidence. b/b2/b3 currently accept an
  integrity hash as that evidence. The tool still implements the join (so this is not a table-style bypass),
  but a tool with a **broken or absent self-verification** reaches MET.
- Tightenings (both measured against the frozen reference; nothing was edited):
  - **T1 (structural, recommended):** run clause b/b2/b3 selftests with the source on a **pipe to
    `python -I - --selftest`**, never as a bound file — `receipt-tightening.txt` E1/E2/E3: reference passes
    fed on stdin (`73/73`, E1); the pin cheat also passes fed on stdin (`60/60`, E2) — and so does a beaten
    mutant of it (`60/60`, E3). Under T1 the pin cannot read itself (fd 0 is an exhausted pipe, `argv[0]` is
    `-`), so mutants survive and b2 fails. The mechanism costs one sandbox variant: no `ro` bind of the tool
    directory and a stdin write in `run_sandboxed`/`selftest_result` (`run_sandboxed:200-217`,
    `selftest_result:883-890`). Feed a pipe, not a seekable file.
  - **T2 (cheap, partial):** add one b3 variant that renames a module-level function and its `Name` call sites
    at AST level, then `ast.unparse`. Clause g already forbids `getattr`/`globals`/`locals`, so a pure AST
    rename cannot change behaviour. `receipt-tightening.txt` E4/E5: reference `73/73` (E4), pin cheat
    `0/60` (E5). A pin that normalises identifiers away (a "semantic fingerprint") would still pass T2; T1
    does not depend on the rewrite being unrecognisable, so T1 is the load-bearing fix.
- Clause-g tightening that does not reject the reference (smaller, independent): the reference touches
  `sys.argv` only as `sys.argv[1:]` in `main` (line 410). Restrict the allowed `sys.argv` access to a slice
  with a constant lower bound ≥ 1 (or to subscriptions inside `main` only) and reject `sys.argv` passed as a
  whole value. `[INFERENCE]` that this alone is sound: a tool could reach argv[0] via `os.environ["PWD"]`?
  no — `PWD` is the cwd, not the script; via `sys.orig_argv`? that is a `sys` attribute (`orig_argv`) the
  same restriction covers. T1 makes the question moot.

## 5. Cross-run cache — structurally impossible; 1/37

`cheat-5-cache.py` (`receipt-cheat-5-cache.txt`): the reference behind a warm marker — on the first run it
writes `/tmp/mado-geometry-warm` and returns a fixed line; if the marker is ever read back it runs the model.
Result `fixtures=1/37` (the single pass is `usage0`, which the inherited `parse_args` still answers), all
clauses 1. The marker
is never seen: `execute` builds a **new bwrap per fixture** (`sandbox_cmd:153-170`, `--tmpfs /tmp` at line
158; `ro=[d, dirname(tool)]`, `rw=[]` at `execute:431-441`), so `/tmp` and even the writable parent directory
are per-run tmpfs. `receipt-cheat-5-cache.txt` shows the cold path on all 37.
Control that the mechanism is otherwise sound: on the host, where `/tmp` persists, the same tool is cold on
its first invocation (`NO_SIZE_RULES`, rc 4) and warm and correct on its second (`receipt-host-vs-sandbox.txt`,
runs 3 and 4). Keep `--tmpfs /tmp`, `rw=[]` and one sandbox per fixture; that is the whole defence.

## 6. Sandbox detection — detectable *and* it buys a MET

`cheat-6-detect.py` (`receipt-cheat-6-detect.txt`): `_sandboxed()` is true iff `HOME == "/nonexistent"` and
`PATH == "/usr/bin"` (the exact pair `sandbox_cmd` sets, lines 163-164); every non-selftest run outside that
environment raises `Setup("usage")`. Scored: `fixtures=37/37`, all clauses, **TARGET_MET**. Outside the
sandbox the same binary is useless: `receipt-host-vs-sandbox.txt` — reference answers the gkeep fixture
(`verdict=OK`, rc 0), cheat-6 prints `MADO_GEOMETRY: SETUP usage`, rc 2.

- Why nothing catches it: the residual says "the sandbox is detectable (fresh /proc, HOME=/nonexistent)"
  (docstring line 88), but the residual is written as a caveat about *cheating*, not as the operability
  consequence: an operability tool that only works where it is scored is worthless to the operator, and the
  predicate records it as `TARGET_MET`.
- Tightening (T4, cheap, reference-safe): run **one nonce-derived fixture with a perturbed environment**
  (`extra_env={"HOME": "/tmp/h"}`, everything else identical) and require byte-identical stdout and rc.
  `receipt-env.txt`: reference `env-default` and `env-HOME-tmp` stdout identical, rc 0/0; cheat-6 changes to
  `SETUP usage`, rc 2. Cost: one extra sandboxed run. `[INFERENCE]` that PATH perturbation is not needed as
  well — HOME alone separated the two; perturb both to also close "PATH-only" detectors.

## 7. "Paths it should not see" — nothing leaks (probe receipt)

`probe-visibility.py` run through the counter's exact `sandbox_cmd` shape (`receipt-visibility.json`):

- root is `['bin','dev','fast','lib','lib64','proc','tmp','usr']`; `/home`, `/home/vgpnk`, the lane, the
  counter and the reference are all `FileNotFoundError`; `/proc` has only the two namespace pids.
- the cwd's parent lists **only the two mount destinations** (`<opaque-real>`, `<opaque-cwd>`), never the
  sibling fixture directories that exist on the host at that moment, and a sibling created at a **known host
  path** (`<parent>/sibling-fixed/c.json`) is `FileNotFoundError` inside. So the opaque nonce hashes of other
  fixtures are not readable, and the fixture *name* behind `sha256(nonce:name)[:12]` is not derivable from
  one observation.
- `cwd_write = OSError` (fixture dir read-only); `tmp_write = True` and `parent_write = True` but both are
  per-run tmpfs (§5). `env` is only `HOME=/nonexistent, PATH=/usr/bin, PWD=<cwd>, LC_CTYPE` — no nonce.
- `[INFERENCE]` recovering the nonce from opaque names is a 64-bit preimage; not attempted.

## Findings, axes, and the smallest safe correction

| # | finding | attacks | smallest correction |
|---|---|---|---|
| F1 | `--selftest` evidence is forgeable: a source-integrity pin + mirrored checks passes b, b2 (6/6 forced dead) and both b3 variants, with zero behavioural checks (cheat-4, MET). Clause g's `sys.argv[0]` guard is a `Constant(0)` subscript and is evaded by `sys.argv[:1][0]`. | C1 operability, `PRED-C1-r42` clauses b/b2/b3/g | **T1**: feed selftest sources on a pipe (`python -I -`); reference passes (E1), the cheat and a mutated cheat both pass, so b2 fails (E2/E3). Optional T2 (AST rename b3 variant: E4/E5) and the argv guard restriction. |
| F2 | A tool can score `TARGET_MET` while refusing to run outside the counter's sandbox (cheat-6). | C1 operability: the capability is supposed to be usable by the operator | **T4**: one nonce-derived fixture under `HOME=/tmp/h` must be byte-identical (receipt-env.txt). |
| F3 | `b2`'s site inventory is name-derived (`NOT_SITES` exact names, line 837): the same code gives 35 or 64 sites; and `KILL_NEED=4/6` is met by a tool whose selftest misses 2 of 6 sites (cheat-1 MET at exactly 4/6). | C1 operability, clause b2 strength | Raise the bar to `killed == N_MUT − equivalent` (reference kills 5/6; the survivor is documented equivalent) or add the "mutant must change a fixture output" cross-check (below). |
| F4 | A byte-table passes **every** nonce-free fixed fixture (26/27, the 27th is nonce-seeded) and fails only the 11 nonce-derived cases. | C1 operability, fixture design | No change now; keep the gen lattice and `many0`'s nonce seeding, and never make the fixed set the whole set. |
| F5 | Cheat-1 (rename-only) MET — the declared residual, not a defect; rename also proves the site inventory is nominal. | none beyond F3 | Report only. |

Not defects (tested): cross-run caching (no writable persistent path, §5); reading neighbours/opaque names
(§7); a mirrored selftest (b2 catches it, §3).

Suggested cross-check for F1/F3 (not scored today, so `[INFERENCE]`): after mutating a site, also run one
nonce-derived fixture and require the mutant's stdout to differ from the reference's `model_out`. A pin or a
dead-site theatre cannot move a fixture's output; the reference's real sites can. Cost: 6 mutants × 1
fixture ≈ one extra `execute` per mutant.

Registration consequence: per the round-43 text, a hole found in w1 **before any data commit** re-registers
the claim as v2 with a new freeze. The hole is in `PRED-C1-r42`; the v2 predicate should carry T1 (and T4),
with T2/the argv guard and F3's kill bar as cheap extras. C2 (`PRED-C2-r43`) is untouched by this seat.

## Reproduction

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
C1R42_TMP=/fast/scratch/hyaku/mado-r43/CritC1Cheat python3 -I quality/counters/c1-r42-geometry.py \
  --repo . --rev b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 --tool .ufo/waves/round-43/w1/CritC1Cheat/cheat-4-selfhash-teeth.py
grep -E 'clauses=|verdict=' .ufo/waves/round-43/w1/CritC1Cheat/receipt-cheat-*.txt
sha256sum -c .ufo/waves/round-43/w1/CritC1Cheat/receipt-sha256.txt   # run from the lane root
```

Quotes used above are from the frozen counter and verify by grep: docstring line 81 for the `sys.argv[0]`
guard, line 88 for the sandbox residual, line 837 for `NOT_SITES`, line 113 for `KILL_NEED`, line 163 for
`HOME=/nonexistent`, lines 937-938 for the two b3 markers, line 764 for `many0`'s nonce seeding, line 879 for
the `ast.unparse` used to forge every b2 mutant. The reference's `sys.argv[1:]` is at
`.ufo/waves/round-42/c1/ctl-ref-tool.py.txt:410`.

Cleanup: all generators, harvested fixtures and bwrap working trees lived under
`/fast/scratch/hyaku/mado-r43/CritC1Cheat/` and are deleted; nothing outside this seat directory and the
`/tmp/mado-geometry-warm` marker (removed) was written. No counter, control, registration, reference or fetch
receipt was edited; no pacman/uv/npx install was needed (stdlib only, Python 3.13, bwrap 0.13.1).
