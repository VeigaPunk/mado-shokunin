# LabRe2Fuzz — Python `re.fullmatch` versus RE2 `FullMatch` over the C1 regex alphabet

Seat `LabRe2Fuzz`, mado round 43 wave `w1`, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`
(base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`, freeze `b2e2efd6…`). Everything below is in this
seat directory except the frozen files the evidence points at; no tracked file was modified.

## 1. The question and the answer

**H:** for every REGEX the C1 contract accepts and every class string, `re.fullmatch(REGEX, class)`
is true exactly when RE2's `FullMatch` is; equivalently no REGEX the contract accepts is rejected
by RE2.

The contract's regex gate is the one executed by the frozen counter and the frozen reference
(their `SAFE` patterns are byte-identical — checked in-process against both files, see §7):
1-200 tokens of `[A-Za-z0-9_.^$()|*+?-]` and the eleven legal escapes, none of the substrings
`(?` `*+` `++` `?+`, and `re.compile` must accept it.

**Verdict, part 1 (match value): H is not falsified.** 466,238 pairs generated, 466,189 compared,
**0** engine divergences. Seed `20261026`, reproducible from the printed seed
(`full-run.txt`; JSON `full-run.json`). The comparator has teeth: 4 of 7 positive controls that lie
*outside* the gate diverge (`\d` vs `٣`, `\w` vs `é`, `\s` vs U+00A0, `\D` vs `٣`) and every one
is refused by the gate.

**Verdict, part 2 (compile acceptance): H is not falsified.** Of 279,249 candidate patterns,
77,690 pass the contract gate; **every** one compiles under RE2 (`both=77690 py_only=0 re2_only=0`,
`gated_out=201559`). So the contract never admits a regex whose `re2::RE2` is `!ok()` — the
direction that would let the tool "evaluate" a rule Hyprland cannot.

**But two divergence classes do survive**, and they are reported in §3 and §4: one is a documented
property of the tool's own predicate (not of either engine), the other is a liveness divergence the
contract's alphabet does not exclude.

## 2. What was compared

Pinned Hyprland call shape (`.ufo/waves/round-43/fetch/Hyprland-RegexMatchEngine.cpp:12,16`):
`m_regex = makeUnique<re2::RE2>(regex);` and
`return re2::RE2::FullMatch(other, *m_regex) != m_negative;` — default options, `ANCHOR_BOTH`.
The `negative:` prefix (`:7-11`) is unreachable through the contract because `:` is not in the
alphabet: `negative:^(a)$` is refused by both gates (§7).

RE2 side: `google-re2` 1.1.20251105 (`uv venv` + `uv pip install`, PyPI wheel, CPython 3.12.15;
pacman not used). Its `_Regexp.fullmatch` matches with `_Anchor.ANCHOR_BOTH`
(`…/site-packages/re2/__init__.py:242-243`), the exact anchoring `RE2::FullMatch` passes, and its
defaults equal the C++ defaults: `one_line=False posix=False encoding=UTF8 dot_nl=False
longest_match=False never_nl=False case_sensitive=True max_mem=8388608` (`versions.txt`).
`log_errors` is on in both: compiling `\Z` printed RE2's own parse error to stderr
(`full-run.stderr.txt`).

Sweeps (all pairs compare `re.compile(rx).fullmatch(cls)` against
`re2.compile(rx).fullmatch(cls)`, `None`-vs-bool normalised):

| sweep | patterns | pairs | what |
|---|---|---|---|
| E1 | 24,999 | 149,994 | exhaustive strings over `a b . ^ $ | ( ) * + ?`, lengths 1-5, gate-filtered |
| E2 | 8,155 | 48,930 | exhaustive over a 16-character representative literal set incl. `\\`, lengths 1-4 |
| E3 | 6,642 | 39,852 | exhaustive over 22 tokens (11 structural characters + all 11 legal escapes), lengths 1-3 |
| R | 60,000 | 227,364 | random, seeded, token length 1-200: nested groups, alternation, empty branches, quantified groups, anchors mid-pattern, escaped punctuation, `.`/quantifier runs |
| L | 14 | 98 | long classes (64-512 chars, ASCII / non-ASCII / astral) against linear patterns |
| X | 8 patterns | 48 + 28 | curated nested-quantifier family, child process, 1-3 s ceiling (the cost stage, §4) |

Classes used with E1-E3 are `""`, `"a"`, `"ab"`, `"a\n"`, `"é"`, `"😀"`; R draws from a pool with
`"\n"`, `"\x00"`, `"\x01"`, `"\t"`, `é`, `Ω`, `😀`, `\u00a0`, host class names (`Alacritty`,
`zcode`, `grok-bot`, `chromium`, `org.omarchy.gkeep`) and random strings of length ≤ 8; L adds
64-512-character classes. Classes containing a control character are included deliberately.

**Why newlines and `$` do not diverge**, though Python's `$` also matches before a trailing
newline: `fullmatch`/`FullMatch` must consume the whole class, and no pattern in the alphabet can
consume a literal newline (`.`, in both engines, does not match `\n`). So a class containing `\n`
matches nothing in either engine — confirmed by 0 divergences among the many such pairs.

## 3. Divergence class D1 — the contract's own guard, not an engine difference (767 pairs)

The tool's client predicate is `no character below U+0020 AND re.fullmatch(...)`, while Hyprland
runs `RE2::FullMatch` on the raw class. Where a class holds a control character and the pattern
matches it, the two predicates disagree: the tool declines a rule the compositor applies.

* 767 of 466,189 pairs; **all 37 feature buckets contain `class-control-char`** (no bucket without
  it); zero divergences where the class is control-character-free.
* Minimised, each re-verified as divergent (`full-run.json` → `tool_level_divergences`):
  `.` vs `"\x01"`; `.` vs `"\x00"`; `a*.` vs `"\x01"`; `..` vs `"Ω\x00"`; `..(b)` vs `"a\x00b"`.
  In every case Python and RE2 agree with each other (`python=True re2=True`) — only the guard
  makes the tool say "no match".
* This is **documented** in the contract (`quality/counters/c1-r42-geometry.py:39`), so it is not a
  defect of the implementation; it is a statement about what the tool models. If parity with
  Hyprland is intended for control-character classes, only the newline case *needs* a guard (and
  that case cannot match anyway, §2), so the guard could be dropped without value divergences —
  worth a w2 look, not changed here (frozen files).

## 4. Divergence class D2 — Python `re` is exponential where RE2 is linear (liveness)

`re` is a backtracking engine; RE2 is not. The contract's alphabet admits the classic
catastrophic-backtracking family, and its gate cannot see it: `(a*)*` is five characters, is
`regex_valid`/`regex_ok`-accepted by the frozen counter and the frozen reference (§7), and the
banned substrings (`(?` `*+` `++` `?+`) do not cover it.

Measured with the contract's own inputs (`full-run.txt`, `COST-NEAR-MISS`; each Python value from a
child process or an in-process signal-bounded call, RE2 timed alongside):

| regex | class | Python `re` | RE2 |
|---|---|---|---|
| `(a*)*` | `"a"*8 + "b"` | 0.000008 s | 0.000016 s |
| `(a*)*` | `"a"*16 + "b"` | 0.0016 s | 0.000016 s |
| `(a*)*` | `"a"*24 + "b"` | 0.43 s | 0.000021 s |
| `(a*)*` | `"a"*64 + "b"` | > 1 s (capped) | 0.000021 s |
| `(a*)*` | `"a"*200 + "b"` | > 1 s (capped) | 0.000025 s |
| `(a+)+` | `"a"*24 + "b"` | 0.31 s | 0.000019 s |
| `(a|a)*` | `"a"*24 + "b"` | 0.61 s | 0.000017 s |
| `(a|aa)*` | `"a"*64 + "b"` | > 1 s (capped) | 0.000024 s |

Cost roughly ×16 per four extra class characters; a 200-character class is therefore ~2^44 times
the 24-character case, i.e. the tool never returns while RE2 answers in ~30 µs. The value, when
Python finally answers, agrees (False = False), so this is not a falsification of H — it is a
liveness divergence the contract's "the alphabet is restricted so the two agree on it" sentence
does not cover (`quality/counters/c1-r42-geometry.py:89`).

This is not hypothetical: the seeded random sweep hit it **49 times** out of 466,189 pairs at a
0.05 s budget — patterns of 40-200 characters (nested quantified groups, empty branches) against
classes as short as 3 characters (`"a😀b"`, `"-éa"`), with RE2 answering every one in ≤ 33 µs
(`full-run.txt` → `SLOW`). Python's `sre` loop is signal-interruptible, which is how the sweep
records them instead of hanging (verified: a 0.2 s `SIGALRM` aborted `(a*)*` on `"a"*30+"b"` at
0.200 s).

**Does the frozen counter reach this?** No — and that matters for the target's measurability.
Its fixture regexes come from `RX_POOL` (`quality/counters/c1-r42-geometry.py:348-350`:
`^(org.omarchy.gkeep)$`, `org\.omarchy\..*`, `Alacritty|kitty`, `a`, `a|ab`, `.*`, `a\.b`,
`^(a|ab)$`, `(x y)?`, `x.y`, `firefox+`, `org.a.b`, `\(a\)`, `a?b?`, `k.*y`, `^$`) — no nested
quantifier — and its classes come from `CLASS_POOL` (`:345-347`, longest 17 characters, no
near-miss against those regexes). So `fixtures=37/37` remains obtainable and this finding does not
by itself break either target.

**Restriction proposals, scored on the same seed and population** (`restrict-score.txt`; population
77,690 accepted patterns = the run's `GATE contract_accepted`, plus the 49 recorded slow pairs and
the 28 curated near-miss pairs):

| restriction (construct refused) | refuses | cost | curated family 8 | organic slow 49 | reference selftest |
|---|---|---|---|---|---|
| R1 quantifier on a group whose body has `*`/`+`/`?` | 3,447 | 4.44 % | 5/8 | 47/49 | 0 refused |
| R2 quantifier on any group with `|` | 5,990 | 7.71 % | 3/8 | 46/49 | refuses `^(a|b)+\.c$` |
| R3 R1 + duplicate `|`-branches | 4,777 | 6.15 % | 7/8 | 47/49 | 0 refused |
| R5 R1 + branches sharing a first character | 4,819 | 6.20 % | 8/8 | 47/49 | 0 refused |
| R4 quantifier on any group | 12,155 | 15.65 % | 8/8 | 49/49 | refuses `^(a|b)+\.c$` |

Near-miss re-run under each (1 s ceiling): R1 → 4 timeouts, R2 → 4, R3 → 2, R5 → 0, R4 → 0.
**No narrow construct is both cheap and total**: R5 removes the whole curated family, costs 6.2 %
of accepted patterns and refuses none of the reference's 17 selftest regexes, yet 2 of the 49
organically slow patterns survive it; only R4 covers all 49, at 15.7 % and at the price of the
reference's own `^(a|b)+\.c$` selftest. A substring ban cannot express this family — the property
"this regex is exponential in a backtracking engine" is not a substring property.

**What the tool can actually do about it.** Clause g permits only `json os re stat sys`, so the
tool cannot import `signal` or `threading` and has no way to bound `re`'s work internally. The
concrete options, in order of what I would check first:
1. add a liveness clause to `PRED-C1-r42`'s contract — the tool must not evaluate a regex whose
   construct set can backtrack exponentially (R4/R5 as written), which forces the reference's
   `^(a|b)\.c$` selftest case to be restated;
2. or relax clause g to allow `signal` and require a wall-clock ceiling per (regex, class) pair;
3. or accept the residual explicitly and keep the alphabet as it is, with the note that a
   contract-legal input can make the tool non-terminating.

Per the wave-shape rule this is a hole found in `w1`, before any data commit: the decision
(v2 re-registration of **PRED-C1-r42** with a liveness clause, versus a documented residual)
belongs to the L1. **PRED-C2-r43** is unaffected — this seat touched no C2 path, and C2's census
lines do not evaluate regexes.

## 5. Boundary observations (no scoring impact)

* **1-200 tokens is 1-400 characters.** `SAFE` quantifies over tokens, so `"\\("*200` (400
  characters) is accepted and `"\\("*201` is not — verified against the frozen counter's
  `regex_valid` and the frozen reference's `regex_ok` (§7). The docstring's "1-200 characters of
  `[...]` and the escapes" (`ctl-ref-tool.py.txt:33-37`) reads as characters. Counter model and
  tool share the same regex, so nothing disagrees; only the sentence is imprecise.
* **`negative:`** is excluded (`:` not in the alphabet), so a negated rule is counted `unsupported`
  rather than evaluated with the wrong polarity.
* **Escapes** are safe: all eleven (`\.` `\-` `\(` `\)` `\|` `\*` `\+` `\?` `\^` `\$` `\\`) compile
  and match identically in both engines (`\-` is accepted by both, contrary to a plausible guess
  that RE2 would reject it).
* **The gate is load-bearing**: `\d`, `\w`, `\s`, `\D`, `\Z`, `[ab]`, `a{2}` all diverge or fail to
  compile on the RE2 side and are all outside the gate. That is why the alphabet restriction exists
  and why the 4/7 control divergences above are controls, not findings.

## 6. Limits of this evidence

* The comparator is the `google-re2` 1.1.20251105 binding, not Hyprland's vendored RE2 build. The
  anchoring (`ANCHOR_BOTH`) and every observable default option match the pinned call site, and
  this language subset is stable across RE2 versions, but the build is not the host's.
* Exhaustive coverage is over representative alphabets (11 structural characters ≤ 5; 16 characters
  ≤ 4; 22 tokens ≤ 3), not the full 73-character literal set — the full set at length 4 is 28M
  candidates and was cut for cost. The random sweep (60,000 patterns, 227,364 pairs) covers the full
  literal set at lengths up to 400 characters.
* "Slow" means "> 0.05 s of Python", not "non-terminating"; the curated stage shows the > 1 s and
  "never returns" region at 64 and 200 class characters.
* Value comparison excludes the 49 slow pairs (their Python value is unknown by construction); their
  RE2 answers are recorded. Classes are ≤ 8 characters in R and ≤ 2 in E1-E3 precisely so the
  exponential family stays inside the 0.05 s budget; long classes are covered only with linear
  patterns (98 pairs) and the near-miss stage (28 pairs).
* Nothing here says anything about Hyprland applying a rule's `size` to a live window, about
  `negative:` rules, multiline flags, character classes, backreferences — all outside the contract.

## 7. Exact retained evidence

| file (this seat dir unless absolute) | content |
|---|---|
| `full-run.txt` | the cited run: gate/compile/pair/slow/cost lines, `RE2FUZZ VERDICT: NO_VALUE_DIVERGENCE value_pairs=466189 seed=20261026` |
| `full-run.json` | the same run, machine-readable: per-sweep counts, compile acceptance, 37 tool-divergence buckets, minimised examples with re-verification flags, the 49 slow pairs with their RE2 answers, cost stage |
| `restrict-score.txt` | restriction scoring: population 77,690; R1-R5 cost and coverage; the 49 slow pairs per restriction; near-miss re-run |
| `full-run.stderr.txt` | the only stderr emitted by the run: RE2's own `Error parsing '\Z'` log line from the positive control |
| `versions.txt` | CPython 3.12.15, `google-re2` 1.1.20251105, uv 0.13.0, wrapper path, RE2 default options |
| `quotes-check.txt` | output of `verify-quotes.sh`: every quote in this report found verbatim at the cited line |

Gate verification performed in-process against the frozen files (output quoted in §4/§5):

```
counter.regex_valid=True  ref.regex_ok=True  rx='(a*)*'
counter.regex_valid=True  ref.regex_ok=True  rx='(a|a)*'
counter.regex_valid=True  ref.regex_ok=True  rx='\\(\\(\\(\\(\\(\\(\\(\\(\\(\\('   (400 chars)
counter.regex_valid=False ref.regex_ok=False rx='negative:^(a)$'
identical SAFE patterns: True
```

Quotes, each ≤ 25 words, located and grepped by `verify-quotes.sh`:
* `Hyprland-RegexMatchEngine.cpp:16` — "return re2::RE2::FullMatch(other, *m_regex) != m_negative;"
* `Hyprland-RegexMatchEngine.cpp:12` — "m_regex = makeUnique<re2::RE2>(regex);"
* `quality/counters/c1-r42-geometry.py:89` — "the REGEX alphabet is restricted so the two agree on it, and a regex outside it is `unsupported`"
* `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt:40` — "`re.fullmatch(REGEX, class)` succeeds (Hyprland: `RE2::FullMatch`)."

Reproduction (scratch venv, no lane file written):

```
S=/fast/scratch/hyaku/mado-r43/LabRe2Fuzz
uv venv --python 3.12 $S/.venv && . $S/.venv/bin/activate && uv pip install google-re2
cd <this seat dir>
python re2fuzz.py --mode full --random-patterns 60000 --json $S/result.json   # exit 0
python restrict-score.py --mode full --slow-json $S/result.json
```

## 8. Files written by this seat

All under `.ufo/waves/round-43/w1/LabRe2Fuzz/`: `report.md`, `re2fuzz.py`, `restrict-score.py`,
`full-run.txt`, `full-run.json`, `full-run.stderr.txt`, `restrict-score.txt`, `versions.txt`,
`verify-quotes.sh`, `quotes-check.txt`. Plus the trailer copy
`.ufo/waves/round-43/w1/LabRe2Fuzz.md`. No frozen file, no registry row, no lane index touched;
scratch (`/fast/scratch/hyaku/mado-r43/LabRe2Fuzz`) is removed after the receipts were copied here.

## 9. Tooling record

`uv venv` (CPython 3.12.15) + `uv pip install google-re2` (1.1.20251105, PyPI wheel) — reason: a
RE2 binding to compare against; official channel, no pacman (host-wide pause honoured). No other
install or update.
