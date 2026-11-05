# R86LabRunbook — the round-86 `border-size-int` runbook row, read against the source

Seat: `R86ScoutRunbook` (scout, leaf member — no dispatch).
Lane: `mado-shokunin`, round 86 (hyaku run 15), wave 1.
Freeze revision named by the dispatch: `237ecf4e69a4986108f719f3beeafe111adaa033`.
Scope of this file: the single falsifiable hypothesis about the r86 runbook row
`set -o pipefail; hyprctl getoption general:border_size -j | jq -r .int`.

**Verdict on the hypothesis: PARTLY CONFIRMED, one clause FALSIFIED.**

* CONFIRMED — the row is a real, live Hyprland read verb; it is bound exactly once in
  `SKILL.md`'s round-86 section and the counter binds it as case `border-size-int`; the
  unanchored `[0-9]+` pattern does accept `0 extra` under `re.search` while the
  whole-line rule refuses it, and that difference is what kills the two round-85 anchor
  survivors.
* FALSIFIED — `0 extra` is **not** a plausible producer output of this row. It is a
  synthetic negative string the counter injects into the matcher, not an observed or
  reachable output of `hyprctl … -j | jq -r .int`. The "plausible next-day output"
  framing in the hypothesis does not survive contact with the producer (evidence in §4).
* NO OBSERVED MIS-REFUSAL — no live output of this row that I could produce is wrongly
  refused by the whole-line rule (§4.2).

No file was edited by this seat. The two frozen instruments, the control sets, the
declaration and the other seats' reports were read and executed only.

---

## 1. The exact row, run read-only in the lane root

Command (verbatim from `SKILL.md:320`), run from `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```console
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ { set -o pipefail; hyprctl getoption general:border_size -j | jq -r .int; } > $S/row.out 2> $S/row.err; echo "rc=$?"
rc=0
$ od -c $S/row.out
0000000   0  \n
0000002
$ cat $S/row.err          # empty
```

Observed: **rc 0, stdout exactly `0\n` (2 bytes), stderr empty.** The value is host
state and is deliberately **not** frozen by this seat.

Producer chain, each stage observed separately:

```console
$ hyprctl getoption general:border_size -j
{"option": "general:border_size", "int": 0, "set": true }
rc=0
$ hyprctl getoption general:border_size          # without -j
int: 0
set: true
```

The `-j` flag is what makes the JSON shape `{"option": …, "int": N, "set": …}`; `jq -r .int`
then prints the raw JSON value of the `int` key as a bare decimal string.

Tooling facts (relevant because the harness shell and the counter's child differ):

* `hyprctl` — Hyprland **0.56.2** (build 2026-08-05), `/usr/bin/hyprctl`.
* `jq` — the counter's child runs `/bin/sh -c …`; inside that shell `jq` resolves to
  `/usr/bin/jq` (**jq-1.8.2**) and `~/.local/bin/jq` is also jq-1.8.2. The harness'
  interactive shell exposes `jq` as a *shell builtin* backed by **jaq 3.1.1**; that builtin
  does not exist for `/bin/sh`, so it does not affect the row. Verified byte-identical
  output under `/usr/bin/jq` and `~/.local/bin/jq` (`od -c` → `0 \n`).
* `hyprctl` needs the compositor's instance signature. Without `XDG_RUNTIME_DIR` /
  `HYPRLAND_INSTANCE_SIGNATURE` it prints `HYPRLAND_INSTANCE_SIGNATURE not set! (is
  hyprland running?)` and exits 1, and `jq` then fails to parse it (jq rc 5, empty
  stdout). The counter's `run()` (counter lines 220–262) passes `XDG_RUNTIME_DIR` /
  `HYPRLAND_INSTANCE_SIGNATURE` through and locates a live socket under
  `$XDG_RUNTIME_DIR/hypr`, so the row runs live inside the instrument.

## 2. The row exists once, in the right section, bound as `border-size-int`

```console
$ grep -n "Executable runbook rows (round 86)" SKILL.md
301:### Executable runbook rows (round 86)
$ grep -n "hyprctl getoption general:border_size -j" SKILL.md
320:| `set -o pipefail; hyprctl getoption general:border_size -j \| jq -r .int` | ok | unanchored `[0-9]+` matched against one whole line: a bare non-negative integer | 2 / 3 |
$ grep -c "hyprctl getoption general:border_size -j" SKILL.md
1
```

* The row appears **exactly once in the whole of `SKILL.md`** (`grep -c` → 1), at line 320.
* It sits inside the section that opens at line 301; the next `###` heading after it is
  line 322 (`### Advertised Wayland globals`), so the section spans 301–321 and the row is
  its only table row.
* Section prose (lines 309–313) states the intent: *"the border size read as a bare
  integer under `anchor: line` with an unanchored pattern … a negative sample that carries
  the value with trailing text (`0 extra`) or a sign (`-1`) is accepted by a substring
  search and refused by the whole-line rule. The value itself is host state (`0` here,
  reported as frozen with churn samples 1 and 2), not a claim about the theme."*
  The churn/negative column `2 / 3` matches the control set (2 samples, 3 negatives).

Counter binding:

* `quality/counters/c2-r86-clause-observations.py:83` → `NEW_CASE = "border-size-int"`.
* Control set `.ufo/waves/round-86/controls/c2-cases-r86.json` → case
  `name="border-size-int"`, `kind="regex"`, `value="[0-9]+"`, `anchor="line"`,
  `status={"class":"ok"}`, `skill_anchor` = the row command verbatim,
  `argv=["/bin/sh","-c","set -o pipefail; hyprctl getoption general:border_size -j | jq -r .int"]`,
  `samples=[{"rc":0,"out":"1"},{"rc":0,"out":"2"}]`,
  `negatives=[{"rc":0,"out":"0 extra"},{"rc":0,"out":"-1"},{"rc":127,"out":"0"}]`.
  The binding is exact: the counter requires `skill_anchor` to equal the row cell
  (counter lines 856–870) and rejects the case set otherwise.
* Live probe from the instrument:

```console
$ python3 -I quality/counters/c2-r86-clause-observations.py --repo . --rev b33afc08 \
    --controls .ufo/waves/round-86/controls/c2-cases-r86.json \
    --carried .ufo/waves/round-85/controls/c2-cases-r85.json \
    --scratch-root $S/c2 --no-mutants
MADO_R86_CONTROLS: sha256=a87f0ea480b36a8eec8592ccdffb6b1e3d60b183c343af2cc5c4563c23bd57d8 cases=37
MADO_R86_PROBE: name=border-size-int row=36 kind=regex match=yes clauses=anchors:1,samples:2,negatives:3 declared=anchors:1,samples:2,negatives:3 rc=0 stdout-bytes=2
MADO_R86_CONTROL: … held_rule_new_case=0/1 new_case=border-size-int held_rule=round85(regex-kind-search,no-clause-observation)
MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37 clauses_observed=37/37 … verdict=MUTANTS_SKIPPED rev=b33afc08… tree=bound
rc=0
```

`stdout-bytes=2` is the live `0\n`, `row=36` is the row index in the union of the two
bound sections (36 r85 rows + 1 r86 row), and `held_rule_new_case=0/1` is the declared
control: the round-85 substring rule scores this new case **0/1**.

## 3. The semantics, against the pinned CPython bytes

```console
$ python3 -c "
import re
p='[0-9]+'
for s in ['0 extra','0','1','2','-1']:
    print(repr(s), 'search=', re.search(p,s) is not None, 'fullmatch=', re.fullmatch(p,s) is not None)
"
'0 extra' search= True fullmatch= False
'0' search= True fullmatch= True
'1' search= True fullmatch= True
'2' search= True fullmatch= True
'-1' search= True fullmatch= False
$ python3 -c "import re; print(re.search('[0-9]+','0 extra'))"
<re.Match object; span=(0, 1), match='0'>
$ python3 -c "import re; print(re.fullmatch('[0-9]+','0 extra'))"
None
```

`re.search` matches `0 extra` at span (0,1) — the leading `0` only; `re.fullmatch`
returns `None`.

**The counter does not call `re.fullmatch`.** It implements the whole-line rule itself
(`quality/counters/c2-r86-clause-observations.py:387–395`):

```python
def line_anchored(pattern, text):
    """True when the pattern matches one complete line of the output, never a prefix of one."""
    rx = re.compile(pattern)
    for line in text.splitlines():
        found = rx.search(line)
        if found is not None and found.group(0) == line:
            return True
    return False
```

i.e. *search, then require the matched span to equal the whole line* — a per-line
whole-line rule, which for a single-line producer output coincides with `fullmatch`.
Two consequences worth recording:

* it is **not** `re.fullmatch` over the whole stdout: for a multi-line stdout containing
  a bare integer on one line and noise on another, `line_anchored` accepts while
  `re.fullmatch` over the whole text would not (checked: `'0\n0 extra'` → `line_anchored
  True`, whole-text `fullmatch False`). This is the intended "one whole line" semantics,
  and the row's live output is one line, so no divergence arises here.
* it is *not* `re.fullmatch` over the whole line either: `fullmatch` anchors at the
  start, while this rule only requires that *some* search hit span the whole line. For
  the pattern `[0-9]+` the two coincide on every input I tested; the difference would
  only show for patterns whose search hit can start mid-line.

### The pinned CPython bytes (S492)

`.ufo/waves/round-86/fetch/S492.bin` — 78,262 B, sha256
`d252cc185dfc1014e1b4a8087b2515b71c76527f0f2f6dfddba9a880537e6a48` (matches the
declaration's `d252cc18…`). The file is CPython `Doc/library/re.rst`
(`:mod:`!re` --- Regular expression operations`).

Quote with its line number, as requested:

```console
$ grep -n "whole \*string\* matches" .ufo/waves/round-86/fetch/S492.bin
957:   If the whole *string* matches the regular expression *pattern*, return a
1299:   If the whole *string* matches this regular expression, return a corresponding
$ awk 'NR<957{n+=length($0)+1} END{print n}' .ufo/waves/round-86/fetch/S492.bin
39782
```

> **S492.bin line 957** (0-based byte offset 39782; the `fullmatch` function directive is
> line 955, the sentence continues onto line 958):
> *"If the whole \*string\* matches the regular expression \*pattern*, return a"*
> … *"corresponding :class:`~re.Match`."*

Two supporting sentences in the same pinned bytes:

* line 927 (the `search()` directive at line 925): *"Scan through \*string\* looking for
  the first location where the regular expression \*pattern\* produces a match"* — the
  substring semantics the round-85 rule used.
* line 1714: *"+:func:`re.fullmatch` checks for entire string to be a match"*.

The declaration cites S492 at line 957; that locator is **correct** (the sentence opens at
957, the directive at 955 — the lesson row in `corpus/lessons/round-86.md:77` states the
same).

**Semantic caveat (finding, not a fix):** the pinned sentence grounds *whole **string***
semantics, while the instrument implements *whole **line*** semantics
(`line_anchored` splits the output into lines and accepts if any one line matches
completely). For this row — and for every `anchor: line` row in the control set, all of
which are single-line producers — the two coincide, and `SKILL.md:320` itself says
*"matched against one whole line"*, so the prose is accurate to the code. The citation is
a slight mismatch of granularity between the cited sentence and the implemented rule; it
does not change any verdict here. It is recorded because the r87/r88 rounds may widen
`anchor: line` to multi-line producers.

## 4. Is `0 extra` plausible producer output? Are other live outputs wrongly refused?

### 4.1 `0 extra` is NOT producible by this row

The row is `hyprctl getoption general:border_size -j | jq -r .int`. For the output to be
`0 extra`, the JSON value of the `int` key would have to be the *string* `"0 extra"`
(jq `-r` prints a JSON string raw, unquoted):

```console
$ echo '{"int":"0 extra"}' | jq -r .int
0 extra
```

But hyprctl types `general:border_size` as an **int** option and emits it as a JSON
number:

```console
$ hyprctl getoption general:border_size -j
{"option": "general:border_size", "int": 0, "set": true }
```

so `jq -r .int` yields `0`, never `0 extra`. The only producer change that would produce
it is hyprctl switching that option to a *string* type — a format change, not a
next-day value change, and one that would break `jq -r .int` for every consumer of that
option.

Two further checks on producer shapes:

* `jq -r .int` on a **float-typed** hyprland option yields `null`, not a number, because
  hyprctl emits the key `float` for those (`{"option": "decoration:fullscreen_opacity",
  "float": 1.000000, …}` → `jq -r .int` → `null`). `null` is refused by the whole-line
  rule **and** by the substring rule (no digit in it), so it is not a differential.
* The **non-JSON** shape `int: 0` (what `hyprctl getoption general:border_size` prints
  without `-j`) *is* accepted by the substring rule and refused by the whole-line rule —
  but it is unreachable for the bound row, which pipes `-j` through `jq -r .int`.

**Therefore:** `0 extra` is a **synthetic negative** — a literal string the counter feeds
to the matcher as `negatives[0].out`, never an observed producer output. It is a
*legitimate discriminating negative* (it separates substring search from whole-line
matching), but calling it "the plausible next-day output" of this row is not supported.
The declaration's own wording is careful and correct: *"A substring search accepts
`0 extra`; the whole-line rule refuses it"* — it never claims the producer emits it.
`SKILL.md:309–313` likewise says *"a negative sample that carries the value with trailing
text"* — i.e. a sample, not an observation.

### 4.2 No observed live output of this row is wrongly refused

Failure modes I could actually produce, with how the bound rule treats each:

| producer situation | stdout | rc | whole-line rule | is that right? |
|---|---|---|---|---|
| live, int option (observed) | `0\n` | 0 | **accept** (`0` is a bare integer) | yes |
| live, value changed (1, 2, 12, 100) | `1\n` … | 0 | accept | yes |
| jq not installed (`PATH=/nonexistent`) | empty | 127 | refuse | yes — status class `ok` requires rc 0; the control set's `{"rc":127,"out":"0"}` negative covers exactly this |
| hyprctl absent / no compositor signature | empty (jq parse error) | 5 | refuse | yes |
| option missing (`getoption general:no_such_option`) | empty (jq parse error) | 5 | refuse | yes |
| option is float-typed (hypothetical for this option) | `null` | 0 | refuse | yes — `null` is not an integer; note the substring rule refuses it too |
| option is float-valued in JSON (`"int": 2.0`, hypothetical) | `2.0` | 0 | refuse | defensible — `2.0` is not a bare integer — but note the **substring** rule would have accepted it, so the whole-line rule is the stricter and more correct of the two here |

The only shapes the whole-line rule refuses that the substring rule would accept are
exactly the synthetic negatives the case declares (`0 extra`, `-1`) plus hypothetical
producer format changes (`int: 0` without `-j`, `2.0`). **No live output of this row that
I could produce is wrongly refused.** The row's live output is a bare integer, and the
rule accepts a bare integer.

### 4.3 The difference is load-bearing: it is what kills the two round-85 survivors

I confirmed the negative does the work by running the two anchor mutants (scratch copies
only; the frozen file was not touched — the mutants are the counter's own two anchor
mutations, re-derived with the counter's own literal-region exclusion):

```console
$ python3 -I $S/mutant-regex-anchor-dropped.py --repo . --rev b33afc08 … --no-mutants
MADO_R86_PROBE: name=border-size-int row=36 kind=regex match=no clauses=anchors:1,samples:2,negatives:3 …
MADO_R86_RUNBOOK: cases=37 executed=37 matched=36 shapes=26/27 … verdict=TARGET_MISSED
rc=1
$ python3 -I $S/mutant-line-anchor-prefix.py --repo . --rev b33afc08 … --no-mutants
MADO_R86_PROBE: name=border-size-int row=36 kind=regex match=no clauses=anchors:1,samples:2,negatives:3 …
MADO_R86_RUNBOOK: cases=37 executed=37 matched=36 shapes=26/27 … verdict=TARGET_MISSED
rc=1
```

Both mutants drop **exactly** `border-size-int` (36/37, shapes 26/27) — the new witness is
the discriminator for the anchor branch, and it is the reason the four round-85 survivors
can die. Full population, run once against the tree tip:

```console
$ python3 -I quality/counters/c2-r86-clause-observations.py --repo . --rev b33afc08 \
    --controls .ufo/waves/round-86/controls/c2-cases-r86.json \
    --carried .ufo/waves/round-85/controls/c2-cases-r85.json --scratch-root $S/c2full
rc=0
… MADO_R86_MUTANT: name=regex-anchor-dropped matched=36/37 killed=yes
… MADO_R86_MUTANT: name=line-anchor-prefix matched=36/37 killed=yes
… MADO_R86_MUTANT: name=negatives-skipped matched=0/37 killed=yes
… MADO_R86_MUTANT: name=samples-skipped matched=5/37 killed=yes
MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37 clauses_observed=37/37 … mutants=37 killed=37 verdict=TARGET_MET rev=b33afc08… tree=bound
```

(Reproduced independently of the committed receipt `receipts/control-c2-r86.txt`, whose
`held_rule_new_case=0/1` line matches mine.)

## 5. Findings

**F1 — `0 extra` is a synthetic negative, not plausible producer output (falsifies the
"plausible next-day output" clause of the hypothesis).**
`jq -r .int` over `hyprctl getoption general:border_size -j` cannot emit `0 extra`:
hyprctl types the option as int and emits a JSON number (`{"option": …, "int": 0, "set":
true }`), and `jq -r .int` prints that number raw. The only producer change that would
yield `0 extra` is hyprctl switching the option to a string type. The declaration
(`claims-declaration-r86.md`, C2 paragraph) and `SKILL.md:309–313` both word this
correctly as a *negative sample*; no document claims it is live output, so this is a
finding about the hypothesis's framing, not a defect in the landed claim. Confidence:
**high** (producer shape observed directly; the negative is a literal in the control set).

**F2 — no live output of this row is wrongly refused by the whole-line rule.**
Every failure mode I could produce (rc 127 / jq parse error / `null` / float-valued int)
is refused for the right reason, and the observed live output `0` is accepted. The
whole-line rule is strictly stricter than the substring rule on exactly the declared
negatives. Confidence: **high** for the modes reproduced; **medium** for hypothetical
future producer format changes (`"int": 2.0`, option re-typed as string), which no
present command can produce.

**F3 — the instrument's whole-line rule is *line*-granular, not *string*-granular;
S492 grounds *string* granularity.** `line_anchored` (counter 387–395) accepts if **any
one line** of the output matches completely; `re.fullmatch` over the whole stdout would
not. Every current `anchor: line` row is single-line, so no verdict changes, and
`SKILL.md:320` says "one whole line" (accurate to the code). Recorded so that a future
round that binds a multi-line producer to `anchor: line` does not read S492 as licence
for whole-string `fullmatch`. Confidence: **high** (both readings executed).

**F4 — the declared freeze revision cannot be used as `--rev` for this counter against
the current tree; the measurable revision is `b33afc08`.**
The dispatch names freeze revision `237ecf4e69a4986108f719f3beeafe111adaa033`. Running
the frozen counter with `--rev 237ecf4e…` against this tree fails closed:

```console
$ python3 -I quality/counters/c2-r86-clause-observations.py --repo . --rev 237ecf4e69a4986108f719f3beeafe111adaa033 …
MADO_R86_RUNBOOK: ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)
rc=2
```

Cause: commit `b33afc08` ("round-86: register the counters at SKILL.md and the ledger…")
added two ledger rows to `SKILL.md` **after** the freeze, so `SKILL.md`'s whole-file
bytes differ from `237ecf4e`'s. The round-86 **runbook section itself is byte-identical**
between the two (`diff` of lines 301–321 at `237ecf4e` vs the tree → identical; the row
sits at line 320 in both), and `tools/mado-barfoot.py` is identical too. So the runbook
row is unaffected; only the `--rev` argument must be the tree tip `b33afc08` for
`tree=bound` to hold. Reported as a finding with the exact commands; no fix attempted.
Confidence: **high** (reproduced; cause isolated by `git diff`).

## 6. What I could not run / limits

* I did not run the C1 instrument (`quality/counters/c1-r86-refusal-records.py`) — out of
  this seat's scope; it neither binds nor is bound by this row.
* I did not verify the r85 instrument's own 36-row contract at the freeze tree
  (`held instrument at the new tree` control, declaration C2 control 2). I did read
  `receipts/control-held-rule-r86.txt`, which reports the r85 run at 33/37 kills with
  the four survivors named; that is a receipt read, not my own re-measurement.
* `S492.bin` is the pinned CPython `re.rst`; I verified its sha256 and content, not its
  provenance from github.com (no network fetch performed).
* The live value `0` is host state observed at report time; it is not frozen here and
  must not be frozen in any report.

## 7. Reproduction

All commands above are reproducible from the lane root with the scratch root passed
explicitly; every path is absolute. No git mutation was performed (read-only `git log`,
`git show`, `git diff`, `git status` only). The two mutant files were written under this
seat's scratch directory and deleted with it.
