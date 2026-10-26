# ExecIndepC — an independent `mado-geometry.py` written from the contract docstring alone (C1, round 43, w1)

Seat: `mado-shokunin/.ufo/waves/round-43/w1/ExecIndepC`. Base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`, freeze
`b2e2efd6e268920d31f3c32cf52dc097dd6e1d22`. Claim C1 (`PRED-C1-r42`), predicate read at `quality/counters/c1-r42-geometry.py`
(the docstring at :3-95 is the contract). **The reference control `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` was never opened**:
no command in this seat names that path, and the implementation below was written from the docstring plus the fixtures' own
description, not from a reference source.

Two reads in this file are quotes of the frozen counter's docstring, each on one line and each machine-checked by
`quote-check.py` (output `receipt-quotes.txt`). Everything else is a path, a command and its output, or a hash.

## 1. Deliverable and score

| file | sha256 |
|---|---|
| `w1/ExecIndepC/mado-geometry.py` | `8d43cb446172975d50509315a23aaffbb06d17d2091cb611bc38ae1a29dd9dbc` |
| `w1/ExecIndepC/site-kill-probe.py` | `46ff5a435666caf0d17550593ae858a5747281c9a9882c8db64a08817843eb33` |
| `w1/ExecIndepC/variants/build-variants.py` | `fa4742b40f9c71c4111cfdef0d47edbaae9eb0998709685c55a25f5b81456938` |

Scoring command (verbatim, run from the lane root; `C1R42_TMP` points into the seat scratch):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && C1R42_TMP=/fast/scratch/hyaku/mado-r43/ExecIndepC \
  python3 -I quality/counters/c1-r42-geometry.py --repo . \
  --rev b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 \
  --tool /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w1/ExecIndepC/mado-geometry.py
```

Result (`receipt-score.txt`, counter exit 0):

```
PRED-C1-r42 clause=b rc=0 selftest=100/100
PRED-C1-r42 clauses=a:1 b:1 b2:1 b3:1 g:1
PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=0389079f9b8a303d
```

All 37 fixture classes pass, including the 10 nonce-lattice `gen` fixtures, `regex0`, `size0`, `space0`, `boundary0`,
`stdinbig0`/`stdinok0`, `fifo0`, `unreadable0`, `many0` (20 000 clients) and `unicode0`. Clause b2 sampled
`mutant=0 site=summarize:... forced` plus five others and killed 6/6 at this nonce (`receipt-score.txt`); clause b3 passed
both neutral variants.

## 2. The failing fixture seen while implementing, verbatim

The first scored run of my draft was 36/37 with a single failing class: my restricted-alphabet set had been transcribed with
the literal `?` dropped (`...|*+-` instead of `...|*+?-`), so `a+?`, `a*?` and `a??` were called unsafe. The defect
reproduces from a one-character deletion of the delivered tool (`variants/pre-fix-missing-question-mark.py`, sha256
`6c18c27153147d433de9a8b528f8dd3f7f550e755f570afcfd167d43c1654d10`); the decisive fixture line is, verbatim from
`receipt-prefix.txt`:

```
PRED-C1-r42 fixture=regex0 ok=0 stdout line 4 got='MADO_GEOM_RULE: n=4 file=1 effect=size arg=22x7 class=a|' want='MADO_GEOM_RULE: n=4 file=1 effect=size arg=17x7 class=a+?'
```

That is also the line the first draft produced. The replay at a different nonce additionally exposes `gen1`, `gen7` and
`gen8` (33/37), because `RX_POOL` contains `a?b?`: the defect was nonce-sensitive in the lattice and always fatal in
`regex0`.

## 3. Shape: two passes, one stream, stdlib only

* First pass — `collect(texts)` returns an ordered list of supported rules `(file, effect, arg, want, regex, compiled)`
  across all rules files in argument order. `render_rules` walks that list once for the `MADO_GEOM_RULE:` lines.
* Second pass — `evaluate(document, rules)` iterates the clients array exactly once (`for client in document`), applying
  the ordered rule list; no second materialisation, no per-client rule re-parse (the pattern is compiled in pass one).
* Imports are `json os re stat sys` only; no subprocess, no `getattr`/`eval` family, no `sys.argv[0]`, no `**` unpacking,
  no banned literal (`clause=g:1`).
* `--selftest` prints `MADO_GEOMETRY_SELFTEST: 100/100 passed` and exits 0; it drives the real `collect`, `evaluate`,
  `summarize`, `parse_args`, `parse_clients`, `is_safe_regex`, `read_stream`/`read_path`/`load_source`, `too_big` and
  `has_control` (not re-implementations), so a flipped comparison anywhere in those functions is observable.

## 4. Teeth beyond clause b2: every comparison site, not six

b2 samples 6 of 47 sites per run. A sampled set is only representative by luck, so `site-kill-probe.py` reimplements the
counter's own `function_sites`/`mutate_source` rules (counter :838-881: every single-operator `ast.Compare` outside
`selftest`/`main`/`usage` and outside functions nested in `selftest`, operator flipped, `ast.unparse`, copy at the real
layout) and runs **all** of them:

```
SITES total=47 killed=47 survivors=[]
```

(`receipt-site-kill.txt`, probe exit 0; 47 `dead=1`, 0 `dead=0`.) Three sites live in `summarize`, the function whose body
holds the summary text, so the forced site is killed for any nonce; the remaining 44 are killed too, so any 5-of-6 sample
passes b2 whatever the nonce.

## 5. The ten places where the contract text most needed a second reading

Each item: the sentence (quote + locator), the two readings, and the decision. Decisions marked **DECIDED** are backed by a
one-reading variant scored against the same frozen fixture set (`receipt-variants.txt`); **UNDECIDED** means both readings
score `37/37`, i.e. a hole in the predicate.

### 5.1 The `1-200` limit: characters or alphabet tokens?
> "REGEX fully matches 1-200 characters" — c1-r42-geometry.py:34

* Reading A: the `{1,200}` is a repeat count over *alternatives* (one literal character or one two-character escape), so
  `200` escaped pairs — 400 characters — pass, and 201 fail.
* Reading B: it is a count of characters of the REGEX string, so at 201 characters the rule is unsupported even if it is
  only 101 escapes.

**UNDECIDED.** `variants/vA-length-chars.py` implements B (limit on `len(text)`) and still scores
`fixtures=37/37 … TARGET_MET` (`receipt-variants.txt`). The only long-regex fixtures are `regex0`'s `"a"*200`/`"a"*201`
(counter :649-658), where tokens equal characters, and the longest `RX_POOL` entry is 20 characters. Any tool may choose
either reading and be scored MET. A v2 fixture needs one rule of ≥101 escapes (e.g. `"\\.\\."*100` inside the 200 cap and
one beyond it).

### 5.2 `bad_json` versus an unreadable rules file
> "Order of checks: usage, then the clients input (unreadable, too_large, bad_json), then the rules files in argument order" — c1-r42-geometry.py:22-23

* Reading A: the clients input is judged completely — including `bad_json` — before any rules path is touched, so
  `--clients <malformed> --rules <missing>` prints `SETUP bad_json`.
* Reading B: the sentence orders the *kinds* per input, not the inputs against each other, so an unreadable rules file may
  win over a malformed clients dump.

**UNDECIDED.** `variants/vB-rules-before-badjson.py` (rules loaded first, `bad_json` judged after) scores 37/37. `toolarge0`
(:599-613) pins only `too_large`-versus-unreadable, both on the clients side, and no fixture pairs a bad clients input with
a bad rules path. A v2 fixture needs one case: malformed `--clients` file plus a `--rules` path that does not exist.

### 5.3 "in argument order (unreadable, too_large)": per file, or per reason?
> "the rules files in argument order (unreadable, too_large)" — c1-r42-geometry.py:23-24

* Reading A: each file is judged completely (unreadable, then too_large) before the next file is opened, so a too_large
  first file plus a missing second file prints `too_large`.
* Reading B: both dimensions are swept over all files: any unreadable file outranks any too_large file.

**UNDECIDED.** `variants/vE-all-unreadable-before-too-large.py` implements B and scores 37/37. `toolarge0` (:604-611)
passes exactly one bad rules file per case. A v2 fixture needs two rules files, the first `> 1048576` bytes and the second
missing.

### 5.4 A non-UTF-8 rules file: replaced bytes, or an error?
> "Each rules file is decoded as UTF-8 with errors replaced" — c1-r42-geometry.py:26

* Reading A: invalid bytes become U+FFFD and parsing continues; every such REGEX is outside the alphabet, so the line is
  *unsupported* and the rest of the file still counts.
* Reading B: "codec error" is a setup failure of that file; the contract names no reason for it, so a strict tool must pick
  one (`unreadable` is the natural one) — and its tally and exit code differ from A.

**UNDECIDED.** `variants/vG-strict-rule-decode.py` (strict `decode("utf-8")`) scores 37/37: no fixture writes non-UTF-8
bytes into a rules file — `badjson0` (:626-642) only does that for the clients dump, and every rules text in the fixture set
is ASCII. A v2 fixture needs one rules file with a stray `0xff` byte in a `match:class` field.

### 5.5 The verdict order: is `NO_SIZE_RULES` first, or are the conditions labels?
> "OK (exit 0), tested in that order." — c1-r42-geometry.py:56

* Reading A: the four conditions are tested in the printed order, so a run with no size rule at all is `NO_SIZE_RULES`
  (exit 4) even though nothing matched.
* Reading B: "no matching client" is the more specific fact about an empty result and wins (exit 3); the list is only a
  catalogue.

**DECIDED** by `empty0` case 0 (counter :770-775: clients `[]` with an empty rules text). `variants/vH-no-match-before-no-size.py`
scores 32/37 and fails, verbatim, `fixture=empty0 ok=0 case 0: rc=3 want=4` (also `size0` `'100000 1'`, `space0`'s CR
line, and `gen2`/`gen8`). Note the DIFFER-versus-NO_MATCHING_CLIENT precedence inside that list is provably inert
(`differ>0` implies `matched>0`), so `NO_SIZE_RULES`' position is the only observable part.

### 5.6 `BADSIZE` versus `TILED`: which condition is tested first?
> "BADSIZE (size none) | TILED (not floating)" — c1-r42-geometry.py:47

* Reading A: the list is an ordered test — an unusable reported size outranks the floating state.
* Reading B: the parentheticals label the verdicts independently, so a client that is both non-floating and has no usable
  size is `TILED`.

**DECIDED** by `client0` (:718-726), element `{}`: its class `""` is matched by the rule `a|`, its `size` is absent and its
`floating` is absent, so the expected line is `verdict=BADSIZE`. `variants/vC-tiled-before-badsize.py` scores 35/37 with,
verbatim, `fixture=client0 ok=0 stdout line 3 got='MADO_GEOM_CLIENT: addr="-" class="" floating=false size=- want=1x2
float_rule=- verdict=TILED' want='… verdict=BADSIZE'` (plus `gen1`).

### 5.7 A malformed `size`/`float` line: `other` or `unsupported`?
> "Any other size or float line adds one to `unsupported`" — c1-r42-geometry.py:36-37

and its neighbour
> "`size` and `float` adds one to `other`" — c1-r42-geometry.py:30-31

* Reading A: the two counters partition by *effect* — a line whose effect is `size` or `float` but whose body is malformed
  is `unsupported`; `other` is for a different effect only.
* Reading B: `other` is the catch-all for every rule line that did not become a supported rule.

**DECIDED** by `space0` (:683-697) line `windowrule = size 1 2,, match:class a` (three fields, expected
`rules=0 float_rules=0 other=0 unsupported=1`) and by `regex0`'s tally (`rules=21 … other=0 unsupported=33`).
`variants/vD-malformed-is-other.py` scores 35/37, failing `space0` on exactly that line and `regex0` on that tally.

### 5.8 `rules=` in the summary: size rules only, or all supported rules?
> "rules=<size rules>" — c1-r42-geometry.py:53

* Reading A: the field counts size rules only; float rules have their own field.
* Reading B: the phrase repeats the preceding "supported rules are numbered n=1.." and counts every supported rule, with
  `<size rules>` as a gloss.

**DECIDED**, and heavily: `variants/vI-rules-counts-all-supported.py` scores 28/37, failing `multi0` (`got rules=4 want 3`),
`float0`, `order0`, `client0` and eight `gen` fixtures (`receipt-variants.txt`).

### 5.9 The stdin cap: is 1048577 accepted or rejected?
> "an input larger than 1048576 bytes is too_large" — c1-r42-geometry.py:20

> "at most 1048577 bytes" — c1-r42-geometry.py:21

* Reading A: the read is capped at MAX+1 so the size test can fire; the accept threshold stays 1048576, i.e. a stream
  holding exactly 1048577 bytes is `too_large` and one holding exactly 1048576 is parsed.
* Reading B: "at most 1048577" is itself an acceptance statement, so 1048577 is legal and the whole rule shifts by one.

**DECIDED** by `stdinbig0` (:515-521), whose payload is `b"[]" + b" " * (MAX_BYTES + 1)` minus one byte — exactly 1048577
bytes — and expects `SETUP too_large`, together with `stdinok0` (:523-527), which sends exactly 1048576 bytes and expects
normal output; `boundary0` (:615-624) pins the file boundary at exactly MAX.

### 5.10 A `\r` at the end of a line: stripped, or inside the REGEX?
> "a line is stripped of spaces and tabs at both ends" — c1-r42-geometry.py:26-27

* Reading A: only spaces and tabs are stripped, so in a CRLF file the `\r` stays in the line; `.` matches `\r`, the capture
  ends with CR, and the alphabet rejects the rule — it is `unsupported`.
* Reading B: "stripped … at both ends" is meant as whitespace-stripping, so `\r` goes and the rule is supported.

**DECIDED** by `space0` (:687) line `"windowrule = size 1 2,match:class a\r"`: the fixture's expected verdict for that
one-line file is exit 4 with `rules=0`, i.e. no rule supported — visible verbatim in the `vH` failure line
`fixture=space0 ok=0 line 'windowrule = size 1 2,match:class a\r': rc=3 want=4`.

The frozen text also carries a doubled word, which is harmless (a token is a token) but is the reason this sentence
needed a second read at all:

> "The effect is the first first token of field 0" — c1-r42-geometry.py:29-30

The parenthetical "(the empty string when there is none)" is what settles the empty-field case, and `other0`'s
`windowrule =` line decides it.

## 6. The four holes, stated as holes

| # | reading that should be pinned | what a v2 fixture needs | evidence both readings pass |
|---|---|---|---|
| 5.1 | 200-unit for the REGEX alphabet | one rule at 100 escapes and one at 101 | `receipt-variants.txt` `vA … 37/37` |
| 5.2 | clients `bad_json` before rules readability | malformed clients dump + missing rules path | `vB … 37/37` |
| 5.3 | per-file versus per-reason rules checks | rules file 1 over the cap, rules file 2 missing | `vE … 37/37` |
| 5.4 | non-UTF-8 rules file | one rules file with a `0xff` byte | `vG … 37/37` |

These are under-determined readings, not scoring false positives: each pair of implementations differs on an input no
fixture contains, so `PRED-C1-r42` cannot separate them. Under the registration's "a hole `w1` finds before any data commit
re-registers as v2 with a new freeze", the four are candidates for a v2 fixture list; this seat does not judge or widen
scope, and reports them as predicate holes for the L1.

## 7. Risks, limits, and housekeeping

* Clause g is a name heuristic (declared residual); my tool imports only the five allowed modules and uses `re.compile` on
  the restricted alphabet, never on arbitrary input.
* Whether Hyprland *applies* a rule's size to a live window is not scored by the counter and not asserted here. This seat
  made no compositor calls at all: every input was synthetic, and no host file was read (`~/.config/hypr/gkeep.conf` is
  C2's business, not C1's).
* `--selftest`'s real-file case reads `<cwd>/mado-geometry.py` when it exists and tolerates its absence, so the selftest
  reports 100/100 from any working directory (verified from `/tmp` and from the seat directory). The counter always runs it
  with `cwd` = the tool's directory.
* Tools installed: **none** (no `uv tool`, `npx`, cargo or pacman use; the task needed only the system `python3` 3.14.8 and
  `bwrap` that the counter requires).
* Scratch `/fast/scratch/hyaku/mado-r43/ExecIndepC` was removed after the receipts were copied into this seat; nothing under
  `/tmp` is cited.
* C2 (the gkeep entry, its registry rows, its lesson) was not read for editing and not touched; the only files written are
  the ones listed below plus this report.

Everything this seat wrote, all under `.ufo/waves/round-43/w1/ExecIndepC/` (`__pycache__` removed):

| file | role |
|---|---|
| `mado-geometry.py` | the deliverable: the independent tool (`8d43cb44…`) |
| `receipt-score.txt` | frozen counter over the deliverable: `fixtures=37/37 … TARGET_MET`, 49 lines |
| `receipt-site-kill.txt` | exhaustive one-flip-per-comparison probe: `SITES total=47 killed=47 survivors=[]` |
| `receipt-variants.txt` | the eight reading variants scored against the frozen set |
| `receipt-prefix.txt` | the pre-fix replay (§2) with the decisive `regex0` line |
| `receipt-quotes.txt` | `quote-check.py` over this report: 13 quotes, 0 failed, plus a negative control that fails (exit 1) |
| `site-kill-probe.py` | reimplementation of the counter's site/mutation rules over all 47 sites |
| `quote-check.py` | greps each `> "…" — c1-r42-geometry.py:A[-B]` blockquote against its cited lines |
| `variants/build-variants.py`, `variants/vA…vI*.py`, `variants/pre-fix-missing-question-mark.py` | the one-reading variants (§5) |

Report: .ufo/waves/round-43/w1/ExecIndepC.md
