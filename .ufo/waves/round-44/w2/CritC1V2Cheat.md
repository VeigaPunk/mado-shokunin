# CritC1V2Cheat — cheats against PRED-C1-r44-v2 (round 44, w2)

Seat: `CritC1V2Cheat`. Target: C1's v2 predicate — `quality/counters/c1-r44-geometry-states-v2.py`
(`PRED-C1-r44-v2`), clause set `a b b4 b5 e g r`. Data commit `e46789213830597348fe96a351ae004d10587385`,
base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`, registration-v2 freeze `03fa5c618b089064a657b3d79d3d4272ae4b6894`.

Frozen inputs read only: registration-v2, the v2 counter, the imported `quality/counters/c1-r42-geometry.py`,
`.ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt`, `w1/CritC1Cheat.md`. **No counter, control, registration, pin,
reference or tracked file was edited**; no `git`/`jj` mutation; no package transaction; no compositor call.

Scoring command (exact; `--nonce` is pinned per run so every receipt is reproducible):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r44-geometry-states-v2.py \
  --repo . --rev e46789213830597348fe96a351ae004d10587385 \
  --work /fast/scratch/hyaku/mado-r44/CritC1V2Cheat --tool <file> --nonce <nonce>
```

## Scoreboard (all runs in this seat dir; `log-*.txt` is the verbatim counter output)

| file (seat) | what it cheats | nonce | clauses | verdict | evidence |
|---|---|---|---|---|---|
| `ref-verified.py` (sha256 `1da3ddaed0d6e3cc…`, `= ctl-ref-tool-v2.py.txt` and `= tools/mado-geometry.py` at the data commit) | baseline, no cheat | `ref0001` | `a:1 b:1 b4:1 b5:1 e:1 g:1 r:1` | **26/26 TARGET_MET** | `log-ref-verified.txt` |
| `cheat-h-harness-gate.py` (+15/−0 lines) | state logic enabled only when the **invocation** is the counter's (`cwd` under `mado-c1r44-*`), round-43 logic in real use | `ffe81742541520ec`, `9d4c7e1a2b3f5860` | `a:1 b:1 b4:1 b5:1 e:1 g:1 r:1` (both) | **26/26 TARGET_MET** | `log-cheat-h-harness-gate.txt`, `log-cheat-h-second-nonce.txt` |
| `cheat-i1-vacuous.py` | cheat-h **plus** every state assertion deleted from the selftest (113 padded cases), no detector | `c4569abf8b1e13ca` | `b5:0`, rest 1 | 26/26 fixtures, **TARGET_MISSED** | `log-cheat-i1-vacuous.txt` — `clause=b5 … rc=0 selftest=113/113 failed=0` |
| `cheat-i2-vacuous-detect.py` | i1 **plus** `json.loads` rebinding detection (identity + `object_hook` probe) that aborts the selftest | `6c08f02d53adc065` | `a:1 b:1 b4:1 b5:1 e:1 g:1 r:1` | **26/26 TARGET_MET** | `log-cheat-i2-vacuous-detect.txt` — `clause=b5 … rc=1 selftest=0/0 failed=1` |
| `cheat-j-honest-jsondecoder.py` | honest: parses with `json.JSONDecoder().decode`, capability intact, reference selftest intact | `61e32bc95bc3298a` | `b5:0`, rest 1 | 26/26 fixtures, **TARGET_MISSED** | `log-cheat-j-honest-jsondecoder.txt` — `clause=b5 … rc=0 selftest=94/94 failed=0` |
| `cheat-j2-jsondecoder-gate-detect.py` | j + harness gate + detector (full composition) | `156d1eface1b8134` | `a:1 b:1 b4:1 b5:1 e:1 g:1 r:1` | **26/26 TARGET_MET** | `log-cheat-j2-jsondecoder-gate-detect.txt` |

Cheats are built by `build-cheats.py` from `ref-verified.py` with exactly-once asserted patches (the generator is
the audit trail; `ref-verified.py` is hash-pinned to the reference). All five cheat files scored exactly as predicted
before their runs (h MET, i1 MISSED, i2 MET, j MISSED, j2 MET).

## F1 — HIGH, MET: the counter's own invocation is a fingerprint, and clause e holds it fixed

**Attacks:** clause **e** (`quality/counters/c1-r44-geometry-states-v2.py:37`) and, through it, the v2 claim that
w1 cheat E is closed. `cheat-h-harness-gate.py` is the reference plus one predicate:

```
:198  if "mado-c1r44" not in cwd:                 # cwd of every fixture/selftest/e run is under mado-c1r44-*
:200  if "C1R42_TMP" in os.environ and "--selftest" not in sys.argv:   # clause r's runs (v2 sets it, :337)
:214  if not harness():  return 0                 # in client_fsmode, before the state read
```

The counter's tmpdir prefix is fixed (`:427 tmp = tempfile.mkdtemp(prefix="mado-c1r44-", dir=parent)`), and clause
e runs the tool **two ways that are identical in everything a tool can key on except the sandbox**: same `cwd = d`,
same argv (`:387 argv = ["--clients", cpath, "--rules", rpath]`), same file contents; only the wrapper differs
(`:391` plain `python3 -I` vs `old.execute`). So a tool that detects *the invocation* and not the sandbox is
invisible to e: both runs print the state output, `same=1` on all five fixtures.

**The capability is absent in real use** — `receipt-real-use-handrun.txt`, pinned `fs0` client bytes
(`fullscreen: 2`, size `2560x1440`, size rule `420x500`), run as a user would (cwd `$HOME/.config/hypr`,
`HOME=$HOME`, and again `hyprctl`-style with `--clients -` on stdin):

| tool | real-use output (last line) | rc |
|---|---|---|
| `ref-verified.py` | `… maximized=0 fullscreen=1 verdict=NOT_COMPARED` | 5 |
| `cheat-h-harness-gate.py` | `… differ=1 tiled=0 badsize=0 verdict=DIFFER` | 1 |
| `cheat-i2-vacuous-detect.py` | `… verdict=DIFFER` | 1 |
| `cheat-j2-jsondecoder-gate-detect.py` | `… verdict=DIFFER` | 1 |

Both forms agree for each tool, so the gate is not form-specific. Note why the other direction is useless: a tool
that *distinguishes* e's plain run from its sandboxed run has no reason to, because e demands equal stdout and rc; the
profitable detection is of what the two runs share — the invocation — which is what the gate keys on. This is w1
cheat E's class (capability present only
where the instrument looks) with the fingerprint moved from the *environment* (which v2's e now varies, and which
caught E) to the *invocation* (which e does not vary). The note in registration-v2 that e covers "one second
environment" (`registration-v2.md:39`) does not cover it, because the second environment is still the instrument's
own invocation. Reproduced at a second nonce with the same result, so the pass is structural, not lattice luck.

Cheap tightening that is **not** sufficient: adding the prefix to `STR_DENY` (`quality/counters/c1-r42-geometry.py:124`)
— a tool assembles the string at run time (`"c1r" + "44"`), and `STR_DENY` is a substring test on individual string
constants, so it is a speed bump only. The fix has to be behavioural (see T1).

## F2 — HIGH, MET: b5 is satisfied by *detecting* the rebinding, with a selftest that asserts no state verdict

**Attacks:** clause **b5** (`:34`). `cheat-i1` is the probe that b5 still works as designed: reference logic, harness
gate, the state block deleted (15 `chk` sites, 21 runtime cases) and 40 tautologies added; b `113/113`, b4
`sites=16 killed=14 need=12`,
**b5:0** (`rc=0 selftest=113/113`). `cheat-i2` adds eight lines that detect the rebinding and fail the selftest when
they see it:

```
:320  if fn.__name__ != "loads":                      # identity: the b5 prefix's _b5_patched wins the name test
:323  probe = fn('{"fullscreen": 2}')                 # object_hook sniff: b5 renames the key to _b5_fullscreen
```
plus, at the head of `selftest()`, `if not json_intact(): print(...); return 1`. Under b5 the copy exits 1 with no
summary line (`rc=1 selftest=0/0 failed=1`) → **b5:1**, and the tool is **26/26 TARGET_MET** while its selftest
contains one `fullscreen` string (an unused helper) and zero state assertions. So b5 proves only that *something*
in the selftest depends on the `json.loads` path — not that the shipped tool's state logic is asserted. A detector
that fires on tampering is a two-line substitute for the capability.

Also measured: b4 has no teeth against either cheat (`i1`: 14 of 16 sites killed by ordinary cases, need 12 — the
survivors are exactly the state-bearing site `client_fsmode:217` and one summary comparison, so the 75 % fraction is
met by accident, the w1 finding 2 mechanism); and b4's census still
skips functions that name `fullscreen` only via concatenation (`:304 and "fullscreen" in c.value.lower()`), so the
w1 finding 3 blind spot is unchanged in v2.

## F3 — MEDIUM, OPEN PREDICATE DEFECT: b5 refuses an honest implementation (false negative)

**Attacks:** the residual sentence at `quality/counters/c1-r44-geometry-states-v2.py:53` — "parses JSON without
json.loads, or detects the rebinding, defeats it". Measured, the first half is inverted: a tool that parses JSON
without `json.loads` does not defeat b5, it **fails** b5 and is refused. `cheat-j-honest-jsondecoder.py` is the
reference with `parse_clients` decoding through `json.JSONDecoder()` (`:187 doc = DEC.decode(data.decode("utf-8"))`)
— same semantics, capability fully present, reference selftest intact: `26/26` fixtures, `b:1 b4:1 e:1 g:1 r:1`,
**`b5:0` (`rc=0 selftest=94/94`)**, `TARGET_MISSED`. `json.load` is *not* a second route (the stdlib `load` calls the
module-global `loads`, `/usr/lib/python3.14/json/__init__.py:298`, which b5 rebinds), but `json.JSONDecoder()` is.

So the clause penalises a parser choice that has nothing to do with the capability, while admitting a detector
(F2). That is a hole in the predicate in both directions: it rejects honest work and accepts a lie. Exact corrected
sentence (replaces `:52-54`, locator computed by `grep -n`, verified in `receipt-quotes.txt`):

> functions naming `fullscreen`; b5 is satisfiable by a tool that detects the rebinding and aborts its selftest, and
> is unsatisfiable by a tool that decodes with `json.JSONDecoder` while holding the capability (w2/CritC1V2Cheat F2,
> F3) — the capability clause must be the semantic mutant, not the binding of `json.loads` to the selftest; e compares
> one second environment **with the invocation held fixed** (a tool can detect either); whether a live maximized or
> fullscreen window reports the work-area or monitor box is the pinned sources' fact, not scored; the documentation
> rows (SKILL.md, PROVINCE.md) are not scored.

`registration-v2.md:39` ("b5 binds the `json.loads` path only; e compares one second environment") is not false, but
it omits both consequences; if a round record is corrected, the same sentence applies there.

## T1 — the smallest safe tightening (measured, admits both honest tools)

Both clauses were implemented as a **probe**, not as an edit (`probe-tighten.py`, 1.9 s total for six tools;
`receipt-tighten-probe.txt`). It imports the counter's own `INVARIANT_INPUTS`/`GKCONF` so the inputs are identical
to clause e's.

* **E′ — invocation invariance (extends clause e).** The same bytes and rule text must give identical stdout and rc
  (i) inside the sandbox with the counter's fixture paths and (ii) as a user runs it: tool copied to a non-temp
  install path (`$HOME/.local/lib/mado/mado-geometry.py`), clients on stdin (`--clients -`), rule file at
  `$HOME/.config/hypr/hyprland.conf`, `cwd` = that config dir, `HOME` = a temp home. This closes F1 because the two
  profiles differ in *everything* the tool can key on (path, argv form, cwd, HOME, env), while the reference is
  unchanged in both.
* **M — capability teeth (replaces b5).** A copy whose `client_fsmode` always returns 0 must fail its own selftest
  (the w1/CritC1V2Cheat §2 recommendation, which v2 did not adopt). This closes F2 (a padded selftest has nothing to
  lose) and F3 (parser choice is irrelevant).

| tool | E′ | M | admitted by E′∧M? |
|---|---|---|---|
| `ref-verified.py` | ok (5/5 fixtures byte-identical) | killed (`rc=1 85/94`) | **yes** |
| `cheat-j-honest-jsondecoder.py` | ok | killed (`rc=1 85/94`) | **yes** (false negative fixed) |
| `cheat-h-harness-gate.py` | FAIL (4 of 5 fixtures differ; `fsclient0` is state-neutral) | killed | no |
| `cheat-i1-vacuous.py` | FAIL | survives (`rc=0 113/113`) | no |
| `cheat-i2-vacuous-detect.py` | FAIL | survives | no |
| `cheat-j2-jsondecoder-gate-detect.py` | FAIL | survives | no |

Proposed clause text (for a round-45 registration; the v2 counter is frozen and there is no re-registration after
data, so this is an **open predicate defect**, not an edit):

```
e  environment and invocation invariance: the inputs fs0, max0, fsmix0, fsclient0, fsagree0 produce identical
   stdout and exit code (i) sandboxed with this counter's fixture paths, (ii) unsandboxed with the same paths, and
   (iii) unsandboxed as a user invokes it - the tool at a non-temp install path, clients on stdin, a rule file under
   $HOME/.config/hypr, cwd = that directory, HOME = a temp home;
b5 capability teeth: a copy whose state read always returns 0 must FAIL its own selftest (non-zero exit, k != n, or
   no summary line) - parser choice is free;
```

Cost: E′ adds ten subprocess runs (≤0.3 s); M replaces six b5-free runs, so the counter's wall time is unchanged in
practice (13.4 s per tool for the reference today). Neither clause touches the model, the 26 fixtures, clause g or
clause r, so the reference and the honest decoder tool stay admitted and nothing about the landed data moves.

## Reproduction

```
S=.ufo/waves/round-44/w2/CritC1V2Cheat
python3 "$S/build-cheats.py"                     # rebuild the six-scorer family from the pinned reference
python3 "$S/verify-quotes.py"                    # 20/20 report quotes checked against their cited lines
python3 "$S/probe-tighten.py" /fast/scratch/hyaku/mado-r44/CritC1V2Cheat/probe   # T1 table
```

and the per-tool scoring command above; each cheat's log names its nonce.

## What this seat did not do

No edit to any tracked file, counter, control, registration, pin or reference; no re-registration of the predicate;
no `git`/`jj` write; no package transaction (pacman is paused); no compositor dispatch; no subagent. The cheat files
are scoring artifacts for the L1 and the w2 falsifiers, **not** proposals for `tools/mado-geometry.py`. Scratch
`/fast/scratch/hyaku/mado-r44/CritC1V2Cheat` deleted after the receipts were copied into this seat dir; all cited
evidence lives here.

## Verdict for the L1

C1's **fixture** clause f is still the strong part: every MET cheat above contains the full round-44 model, because
13 of 26 fixture slots are nonce-derived. What is not strong is the capacity of the *teeth* to distinguish "the tool
can do it" from "the tool can do it where the counter looks": clause e varies the sandbox but not the invocation
(F1, MET, capability absent in real use), and b5 is simultaneously satisfiable by a detector (F2, MET) and
unsatisfiable by an honest non-`json.loads` parser (F3, MISSED). The landed data is unaffected — the committed
`tools/mado-geometry.py` is byte-identical to the reference and C1's after-state is honest — so this is an OPEN
predicate defect to carry into round 45: adopt E′ and M, and replace the two sentences at
`quality/counters/c1-r44-geometry-states-v2.py:52-54` with the corrected text in F3.
