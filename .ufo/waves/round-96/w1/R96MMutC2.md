# R96MMutC2 - C2 selftest weakening panel

Seat `R96MMutC2`, mado round 96, hyaku run 15, wave w1. Leaf seat: no subagent dispatch, no
commit, no mutating git/jj, no tool installs.

**Artifacts**

| file | sha256 | role |
|---|---|---|
| `.ufo/waves/round-96/controls/selftest-panel-r96.json` | `4332b488309309b81eccccabaff9322c5b7a54fcedd74079b58f50926f773982` | the panel: 37 entries (31 hand, 6 neutral) |
| `.ufo/waves/round-96/build/check-receipt-presence.c2.py` | `be716a63662f326a771d96dc5324e89fe07abdff6949029cabb8b7f5d15ca962` | tool under test (R96MExecKillsC2 draft, read-only for me) |
| `.ufo/waves/round-96/build/check-receipt-presence.kills.json` | `305d735fd665ad87566c7983f4e9163eaf323ad1ddb7a99a907e507c8a617495` | kill-set used for every gate measurement |
| `quality/check-selftest-strength.py` | `2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b` | the gate (round-93 frozen, unchanged) |
| `quality/check-receipt-presence.py` | `38a2ea60dc698c45957a3ad4af3132297dd2edb354d815e7ff3433c42bab47ca` | base tool (unchanged; mutants were also measured against it) |

The kill-set was re-pinned by its owner mid-measurement (`aa2a4764...` -> `305d735f...`); the diff is
`must_fail` string -> one-element list only. The gate treats both identically (`sorted(fails) !=
sorted(must_fail)`), and I re-ran the baseline, one shipped hand entry, one neutral and one held-back
entry against the new file: identical verdicts.

## 1. What I attacked

One claimed invariant: *the C2 tool's six selftest checks, once the gate is armed with the frozen
kill-set, still catch production bugs.* `hand` entries weaken the selftest while keeping
`--selftest` at `rc 0` and the result line exactly `RECEIPT_PRESENCE_SELFTEST: checks=6 failed=0`;
`neutral` entries change bytes without touching behaviour and must leave the gate at `OK`.

`green` below always means: rc 0, result line byte-equal to the string above, and no
`RECEIPT_PRESENCE_SELFTEST: FAIL` line on the clean run. Every weakening was applied **alone** to a
copy of the draft; the draft itself was never written.

## 2. Method (verbatim)

```sh
S=/fast/scratch/hyaku/mado-r96/R96MMutC2
cp .ufo/waves/round-96/build/check-receipt-presence.c2.py "$S/draft.py"
sha256sum "$S/draft.py"   # be716a63...
# 1. apply one panel entry in memory -> variant file
# 2. python3 -I "$variant" --selftest                     (green test: rc, result line, FAIL lines)
# 3. python3 -I quality/check-selftest-strength.py --tool "$variant" #        --kills .ufo/waves/round-96/build/check-receipt-presence.kills.json #        --allow-sha-drift --scratch-root "$S/gate"
# 4. own-mutant composition: panel entry + one own production mutant -> selftest (must lose the label)
```

Baseline on the unmutated draft with the frozen kill-set:

```
SELFTEST_STRENGTH: OK tool=quality/check-receipt-presence.py kills=7 held=7 survived=0 wrong_check=0
```

`--allow-sha-drift` is correct here: every panel variant changes the tool's bytes, and the kill-set's
`tool_sha256` pins the draft. A variant keeps every kill `find` unique in the non-selftest prefix, so
the gate never falls back to `SETUP_ERROR`.

## 3. Panel schema (proposal, as implemented)

```json
[ {"id": "<stable slug>", "kind": "hand"|"neutral",
   "find": "<exact source substring, occurs exactly once in the tool>",
   "replace": "<replacement>",
   "why": "<one sentence; names the weakened comparison and the own mutant it hides>"} ]
```

A top-level list keeps it applicable one entry at a time (each entry is measured alone, never
cumulatively). `id` sorts by check; `find` uniqueness is a hard precondition and I verified all 37
against the draft's bytes (`count(find) == 1` for every entry). No optional keys, no "apply
everywhere" flag, no ordering semantics.

## 4. Counts

| measure | value |
|---|---|
| hand weakenings written | 39 |
| hand weakenings green when applied alone | 38 |
| hand weakenings red (not candidates) | 1 |
| hand weakenings shipped (green **and** gate `WEAK` rc 1 under the frozen kill-set) | 31 |
| hand weakenings held back (green, but gate `OK` because the kill-set is one-sided) | 7 |
| neutral edits shipped (green, gate `OK`) | 6 |
| checks represented among shipped hand entries | 6/6 |
| production mutants recorded as hidden | 10 |
| gate-blind hand weakenings after the 4-kill extension proposed in section 6 | 0 |

Per check among shipped entries: `okrc` 6, `oklines` 7, `missingrc` 3, `missinglines` 4,
`setup-rc` 3, `setuplines` 3, plus 5 cross-cutting weakenings of the `failed`/`checks`/exit path.

## 5. Every entry, measured

Status: `shipped` = in the panel file; `held` = green, hidden from the frozen kill-set (section 6);
`red` = turns the selftest red (section 7).
"kill ids lost" is what the gate stopped holding for that variant (`SURVIVED` or `WRONG_CHECK`);
either one makes the gate print `WEAK` rc 1.

| check | id | status | green | gate rc | kill ids lost (survived/wrong_check) | aimed mutant | hidden |
|---|---|---|---|---|---|---|---|
| okrc | `okrc-abs-genuine` | shipped | yes | 1 | ok-rc-exit-polarity:survived | `M-ok-rc` | yes |
| okrc | `okrc-ge-zero` | shipped | yes | 1 | ok-rc-exit-polarity:survived | `M-ok-rc` | yes |
| okrc | `okrc-input-pinned` | shipped | yes | 1 | ok-rc-exit-polarity:survived | `M-ok-rc` | yes |
| okrc | `okrc-label-renamed` | shipped | yes | 1 | ok-rc-exit-polarity:wrong_check | `M-ok-rc` | yes |
| okrc | `okrc-not-setup` | shipped | yes | 1 | ok-rc-exit-polarity:survived | `M-ok-rc` | yes |
| okrc | `okrc-true` | shipped | yes | 1 | ok-rc-exit-polarity:survived | `M-ok-rc` | yes |
| oklines | `oklines-expected-first-token` | shipped | yes | 1 | ok-lines-verdict-polarity:survived | `M-ok-present` | yes |
| oklines | `oklines-expected-shortened` | shipped | yes | 1 | cited-count-double:survived | `M-ok-lines` | yes |
| oklines | `oklines-first-token` | shipped | yes | 1 | ok-lines-verdict-polarity:survived | `M-ok-present` | yes |
| oklines | `oklines-label-renamed` | shipped | yes | 1 | cited-count-double:wrong_check,ok-lines-verdict-polarity:wrong_check | `M-ok-lines` | yes |
| oklines | `oklines-missing-zero` | shipped | yes | 1 | cited-count-double:survived,ok-lines-verdict-polarity:survived | `M-ok-lines` | yes |
| oklines | `oklines-nonempty` | shipped | yes | 1 | cited-count-double:survived,ok-lines-verdict-polarity:survived | `M-ok-lines` | yes |
| oklines | `oklines-verdict-only` | shipped | yes | 1 | cited-count-double:survived | `M-ok-lines` | yes |
| missingrc | `missingrc-ge-zero` | shipped | yes | 1 | missing-rc-exit-2:survived | `M-missing-rc` | yes |
| missingrc | `missingrc-in-0-1` | held | yes | 0 | - | `M-missing-rc` | yes |
| missingrc | `missingrc-label-renamed` | shipped | yes | 1 | missing-rc-exit-2:wrong_check | `M-missing-rc` | yes |
| missingrc | `missingrc-not-setup` | held | yes | 0 | - | `M-missing-rc` | yes |
| missingrc | `missingrc-true` | shipped | yes | 1 | missing-rc-exit-2:survived | `M-missing-rc` | yes |
| missinglines | `missinglines-exact-only` | held | yes | 0 | - | `M-missing-verdict` | yes |
| missinglines | `missinglines-expected-shortened` | red | NO | 2 | - | `M-missing-text` | yes |
| missinglines | `missinglines-label-renamed` | shipped | yes | 1 | missing-lines-off-by-one:wrong_check | `M-missing-lines` | yes |
| missinglines | `missinglines-nonempty` | shipped | yes | 1 | missing-lines-off-by-one:survived | `M-missing-lines` | yes |
| missinglines | `missinglines-prefix-only` | shipped | yes | 1 | missing-lines-off-by-one:survived | `M-missing-lines` | yes |
| missinglines | `missinglines-verdict-only` | shipped | yes | 1 | missing-lines-off-by-one:survived | `M-missing-lines` | yes |
| setup-rc | `setup-rc-ge-zero` | shipped | yes | 1 | setup-rc-exit-0:survived | `M-setup-rc` | yes |
| setup-rc | `setup-rc-label-renamed` | shipped | yes | 1 | setup-rc-exit-0:wrong_check | `M-setup-rc` | yes |
| setup-rc | `setup-rc-not-zero` | held | yes | 0 | - | `M-setup-rc` | yes |
| setup-rc | `setup-rc-positive` | held | yes | 0 | - | `M-setup-rc` | yes |
| setup-rc | `setup-rc-true` | shipped | yes | 1 | setup-rc-exit-0:survived | `M-setup-rc` | yes |
| setuplines | `setuplines-family` | held | yes | 0 | - | `M-setup-tail` | yes |
| setuplines | `setuplines-label-renamed` | shipped | yes | 1 | setup-lines-marker-drift:wrong_check | `M-setup-lines` | yes |
| setuplines | `setuplines-nonempty` | shipped | yes | 1 | setup-lines-marker-drift:survived | `M-setup-lines` | yes |
| setuplines | `setuplines-prefix` | shipped | yes | 1 | setup-lines-marker-drift:survived | `M-setup-lines` | yes |
| setuplines | `setuplines-substring` | held | yes | 0 | - | `M-setup-tail` | yes |
| all | `all-checks-pinned` | shipped | yes | 1 | cited-count-double:survived,missing-lines-off-by-one:survived,missing-rc-exit-2:survived,ok-lines-verdict-polarity:survived,ok-rc-exit-polarity:survived,setup-lines-marker-drift:survived,setup-rc-exit-0:survived | `M-setup-rc` | yes |
| all | `all-exit-zero` | shipped | yes | 1 | cited-count-double:survived,missing-lines-off-by-one:survived,missing-rc-exit-2:survived,ok-lines-verdict-polarity:survived,ok-rc-exit-polarity:survived,setup-lines-marker-drift:survived,setup-rc-exit-0:survived | `M-setup-rc` | yes |
| all | `all-fail-print-dropped` | shipped | yes | 1 | cited-count-double:survived,missing-lines-off-by-one:survived,missing-rc-exit-2:survived,ok-lines-verdict-polarity:survived,ok-rc-exit-polarity:survived,setup-lines-marker-drift:survived,setup-rc-exit-0:survived | `M-setup-rc` | yes |
| all | `all-failed-emptied` | shipped | yes | 1 | cited-count-double:survived,missing-lines-off-by-one:survived,missing-rc-exit-2:survived,ok-lines-verdict-polarity:survived,ok-rc-exit-polarity:survived,setup-lines-marker-drift:survived,setup-rc-exit-0:survived | `M-setup-rc` | yes |
| all | `all-failed-filtered` | shipped | yes | 1 | cited-count-double:survived,missing-lines-off-by-one:survived,missing-rc-exit-2:survived,ok-lines-verdict-polarity:survived,ok-rc-exit-polarity:survived,setup-lines-marker-drift:survived,setup-rc-exit-0:survived | `M-setup-rc` | yes |

| id | green | gate rc | kill ids lost |
|---|---|---|---|
| `n-comment` | yes | 0 | - |
| `n-docstring` | yes | 0 | - |
| `n-whitespace` | yes | 0 | - |
| `n-quote-style` | yes | 0 | - |
| `n-local-alias` | yes | 0 | - |
| `n-continuation-space` | yes | 0 | - |

### Shipped hand entries by weakening family

- exit-code assertions relaxed: `>= 0`, `!= 2`->`!= 0`, pinned `True`, `abs(rc) >= 0`, expected rc
  overwritten with the observed value (`okrc-input-pinned`: the `want_rc` compared to itself);
- expected finding text shortened: `ok_line = "verdict=OK"`, `= "cited=1"`, first-token
  comparisons, `bool(out_ok)` / `bool(out_missing)` / `bool(out_setup)`;
- a check that only exits: `failed = []`, `checks = [(n, True) ...]`, a filter prefix no label
  matches, FAIL lines no longer printed, `return 0`.

## 6. Held-back weakenings, and the four kills that surface them

These seven are green and each hides a real production mutant, but the frozen kill-set cannot see
them: its mutants do not exercise the direction the weakening removes.

| id | hides | why the frozen kill misses it |
|---|---|---|
| `missingrc-not-setup` (`rc_missing != 2`) | a MISSING run exiting 0 | the kill only flips `else 1` -> `else 2` |
| `missingrc-in-0-1` (`in (0, 1)`) | a MISSING run exiting 0 | same |
| `setup-rc-not-zero` (`rc_setup != 0`) | a setup path exiting 1 | the kill only flips `return 2` -> `return 0` |
| `setup-rc-positive` (`rc_setup > 0`) | a setup path exiting 1 | same |
| `setuplines-substring` (`any("SETUP_ERROR" in ln)`) | message-tail drift, marker intact | the kill drifts the marker |
| `setuplines-family` (`ln.startswith("RECEIPT_PRESENCE: SETUP_ERROR")`) | message-tail drift | same |
| `missinglines-exact-only` (drops the verdict term) | a run printing the finding line but `verdict=OK` | the kill only shifts the line number |

Four measured kills close all seven. Each is a production mutant whose own `--selftest` fails exactly
that one label (measured on the draft):

```json
[
 {"id": "missing-rc-exit-0",       "find": "    return 0 if missing == 0 else 1",
  "replace": "    return 0",                                            "must_fail": ["MISSING-rc"]},
 {"id": "setup-rc-exit-1",         "find": "RECEIPT_PRESENCE: SETUP_ERROR {msg}\")\n        return 2",
  "replace": "RECEIPT_PRESENCE: SETUP_ERROR {msg}\")\n        return 1", "must_fail": ["SETUP-rc"]},
 {"id": "setup-lines-tail-drift",  "find": "return setup(f\"bad --rev {a.rev}\")",
  "replace": "return setup(f\"bad rev {a.rev}\")",                     "must_fail": ["SETUP-lines"]},
 {"id": "missing-lines-verdict-stuck", "find": "verdict = \"OK\" if missing == 0 else \"MISSING\"",
  "replace": "verdict = \"OK\"",                                       "must_fail": ["MISSING-lines"]}
]
```

Measured with the landed 7 kills plus these four: baseline `SELFTEST_STRENGTH: OK ... kills=11
held=11 survived=0 wrong_check=0`, and all seven held-back entries become `WEAK` rc 1:

```
missingrc-not-setup      -> SURVIVED missing-rc-exit-0
missingrc-in-0-1         -> SURVIVED missing-rc-exit-0
missinglines-exact-only  -> SURVIVED missing-lines-verdict-stuck
setup-rc-not-zero        -> SURVIVED setup-rc-exit-1
setup-rc-positive        -> SURVIVED setup-rc-exit-1
setuplines-substring     -> SURVIVED setup-lines-tail-drift
setuplines-family        -> SURVIVED setup-lines-tail-drift
```

Decision for the L1: (a) extend the frozen kill-set with the four kills and append the seven entries
to the panel (`hand_flagged == hand` becomes 38/38), or (b) leave the kill-set at 7 and keep the
panel at 31 hand entries, which is what the shipped file does. The shipped file is correct under
**both** kill-sets; it is deliberately the intersection.

## 7. Red weakenings (measured, not candidates)

Applied to the draft, these change the result line or the exit code and are excluded:

| id | selftest output |
|---|---|
| `missinglines-expected-shortened` (`gone_line = "missing "`) | rc 1, `FAIL MISSING-lines`, `checks=6 failed=1` (the observation is a list-membership test, so shortening the expected line breaks it) |
| expected OK rc pinned to 1 (`rc_ok = 1`) | rc 1, `FAIL OK-rc` |
| `MISSING-rc` expected 0 | rc 1, `FAIL MISSING-rc` |
| `SETUP-rc` expected 0 | rc 1, `FAIL SETUP-rc` |
| a seeded `failed` entry | rc 1, `FAIL seed`, `checks=6 failed=1` |
| FAIL printed for every check while the counter is untouched | rc 0, six `FAIL` lines, result line `checks=6 failed=0` (green by result line, red by emitted FAIL lines - rejected) |
| `return 1` | rc 1 with `checks=6 failed=0` |
| `checks` truncated to the first three observations | rc 0, `checks=3 failed=0` (the `checks=6` pin is what catches it) |

## 8. Findings

### F1 (contract, lifted): the gate could not arm the six labels before the draft moved the selftest

`check-selftest-strength.py` restricts kill mutants to `text[:text.find("def selftest(")]`
(`non_selftest_prefix`). With the base layout (selftest defined *before* `main`), the whole main path
was outside that region. Measured: a kill whose `find` is setup()'s `return 2` gives

```
SELFTEST_STRENGTH: SETUP_ERROR kill singleton-setup-rc find occurs 0 times in non-selftest code
```

and the reachable FAIL label sets from eight prefix mutants were:

```
CITE `quality/` branch dropped          -> [OK-lines]
HUNK header skipped                     -> [MISSING-lines]
`.ufo/waves/round-N/` branch dropped    -> [MISSING-rc, MISSING-lines]
`.txt` dropped from the extension list  -> [OK-lines, MISSING-rc, MISSING-lines]
synthetic cite injected in added_lines  -> [OK-rc, OK-lines]
git() made a fixed dummy                -> [OK-lines, MISSING-rc, MISSING-lines, SETUP-rc, SETUP-lines]
```

So `OK-rc`, `MISSING-rc`, `SETUP-rc` and `SETUP-lines` had no singleton kill, and per-label
neutralisation could not be observed: PRED-C2-r96-v1 legs (ii) and (vi) were unsatisfiable as the
base layout stood. The landed draft defines `selftest()` after `main()`; I verified the prefix now
contains `def main(` and `def setup(`, and the frozen 7-kill set holds with six distinct singleton
labels (`kills=7 held=7`). The move is what makes (vi) reachable - keep it in the freeze.

### F2 (draft regression): a fixture failure is no longer reported

The draft dropped the base's `except (OSError, RuntimeError)` arm. Measured with one forced
`RuntimeError` inside the fixture:

```
draft: rc 1, stdout EMPTY, stderr RuntimeError: probe: fixture broke   (no FAIL line, no result line)
base : rc 1, stdout "RECEIPT_PRESENCE_SELFTEST: FAIL fixture probe: fixture broke"
              "RECEIPT_PRESENCE_SELFTEST: checks=1 failed=1"
```

Consequence for the claim: a broken fixture (git missing, TMPDIR unwritable) makes the gate see
`rc != 0` with **no** FAIL lines for every kill, which the gate records as `SURVIVED` - the verdict
becomes `WEAK` for every kill rather than a `SETUP_ERROR`. The tool also no longer has a label for
that state, so the six-label contract is silent exactly when nothing ran. Not in my write scope
(the tool is the draft owner's); recorded for the counter's `--selftest` leg and for the L1.

### F3 (coverage): seven production mutants survive the unmodified selftest

Measured on the draft with no panel entry applied (`rc 0`, no FAIL lines):

```
--worktree carried()  exact = p in cpaths            -> True          SURVIVED
--worktree untracked loop iterates an empty list                      SURVIVED
--worktree check-ignore branch disabled                               SURVIVED
--worktree universe() on-disk listing disabled                        SURVIVED
candidates(): the bare `receipts/` fallback removed                   SURVIVED
expand(): only the first brace group is expanded                      SURVIVED
added_lines(): `n += 2` after an added line (consecutive + lines)     SURVIVED
```

The selftest exercises `--rev` mode only: no case uses `--worktree`, no cite has a `{a,b}` brace
group, no cite is a bare `receipts/...` path, and every fixture hunk holds exactly one added line
(so the hunk counter's increment is unobservable). These lines cannot get kills and cannot be
guarded by the panel; they are the honest limit of the six checks.

### F4 (kill-set breadth): four labels are tested on one side only

See section 6. `MISSING-rc`, `SETUP-rc`, `SETUP-lines` and `MISSING-lines` each have exactly one
kill, and in each case a plausible weakening of the *other* direction passes the gate. The panel
proves this with seven green weakenings.

### What survived the panel

None of the shipped hand entries was gate-blind: 31/31 print `WEAK` rc 1. Under the shipped file and
the frozen kill-set the tuple (i) unmodified `OK` rc 0, (iii) `hand_flagged == 31/31`, (iv)
`neutral_ok == 6/6` all hold as measured.

## 9. Own mutants used as the hidden reference

All ten are production edits (no selftest bytes), measured on the draft; each fails exactly the one
label named:

| id | edit | FAIL set |
|---|---|---|
| `M-ok-rc` | `return 0 if missing == 0 else 1` -> `... and cited > 1 ...` | `[OK-rc]` |
| `M-ok-lines` | `cited += 1` -> `cited += 2` | `[OK-lines]` |
| `M-ok-present` | `present_n += 1` -> `present_n += 2` | `[OK-lines]` |
| `M-missing-rc` | the same exit line -> `return 0` | `[MISSING-rc]` |
| `M-missing-lines` | `{path}:{n}` -> `{path}:{n + 1}` | `[MISSING-lines]` |
| `M-missing-verdict` | `verdict = "OK" if missing == 0 else "MISSING"` -> `verdict = "OK"` | `[MISSING-lines]` |
| `M-missing-text` | `print(f"missing ...` -> `print(f"lost ...` | `[MISSING-lines]` |
| `M-setup-rc` | setup()'s `return 2` -> `return 0` | `[SETUP-rc]` |
| `M-setup-lines` | `SETUP_ERROR` -> `SETUP-ERROR` | `[SETUP-lines]` |
| `M-setup-tail` | `setup(f"bad --rev {a.rev}")` -> `bad rev` | `[SETUP-lines]` |

The frozen kill-set's own mutants are the `k-...`-independent ids quoted in section 5
(`ok-rc-exit-polarity`, `ok-lines-verdict-polarity`, `missing-rc-exit-2`,
`missing-lines-off-by-one`, `setup-rc-exit-0`, `setup-lines-marker-drift`, `cited-count-double`).

## 10. Restoration and write scope

- I wrote only `.ufo/waves/round-96/controls/selftest-panel-r96.json` and this report. Nothing under
  `tools/`, `quality/`, `corpus/`, the git index, jj state, or the fleet root.
- The tool and the kill-set were never written: their hashes at the end of the work equal the hashes
  I measured against (`be716a63...`, `305d735f...`); the base tool and the gate also still hash
  `38a2ea60...` and `2d6f1219...`.
- Every variant lived in `$S` (scratch) and is deleted with the scratch root; no fixture repository
  was created outside it, and the gate's own scratch root was `$S/gate`.
- Tool installs: none (no pacman, no `uv tool`, no binary fetch). No network access was needed.

## 11. Reproduce

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
S=$(mktemp -d "${HYAKU_SCRATCH:-/fast/scratch/hyaku}/r96-replay.XXXXXX")
cp .ufo/waves/round-96/build/check-receipt-presence.c2.py "$S/tool.py"
python3 - "$S" <<'EOF'
import json, subprocess, sys
S = sys.argv[1]
src = open(f"{S}/tool.py", encoding="utf-8").read()
for e in json.load(open(".ufo/waves/round-96/controls/selftest-panel-r96.json")):
    assert src.count(e["find"]) == 1, e["id"]
    open(f"{S}/v.py", "w", encoding="utf-8").write(src.replace(e["find"], e["replace"], 1))
    r = subprocess.run([sys.executable, "-I", f"{S}/v.py", "--selftest"], capture_output=True, text=True)
    assert r.returncode == 0 and "checks=6 failed=0" in r.stdout and "FAIL" not in r.stdout, e["id"]
    g = subprocess.run([sys.executable, "-I", "quality/check-selftest-strength.py", "--tool", f"{S}/v.py",
                        "--kills", ".ufo/waves/round-96/build/check-receipt-presence.kills.json",
                        "--allow-sha-drift", "--scratch-root", f"{S}/gate"], capture_output=True, text=True)
    want = "WEAK" if e["kind"] == "hand" else "OK"
    assert f"SELFTEST_STRENGTH: {want} " in g.stdout, (e["id"], g.stdout)
print("panel ok: 31 hand WEAK, 6 neutral OK")
EOF
```
