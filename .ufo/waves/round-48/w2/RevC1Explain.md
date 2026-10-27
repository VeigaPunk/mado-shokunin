# RevC1Explain — clause `x`: explain `selected= path= cmd= cache=` and the `--observed` comparison

Round 48, wave `w2` (FALSIFY), policy v1. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Frozen instruments: `PRED-C1-r48`
(`.ufo/waves/round-48/l1-draft/c1-r48-terminal-cache.py`, sha256 `2a7d03d9…ccddd4`), the 190 cold + 204 warm fixtures
(`4836cc1d…` / `4d946bd7…`, both equal to the counter's own `SHA256_COLD` / `SHA256_WARM`), and the draft tool
`.ufo/waves/round-48/l1-draft/mado-terminal.py` at the freeze commit (`1dfde36c…`; identical to the tracked
`tools/mado-terminal.py` when this wave opened — the lane's worktree copy moved afterwards, see the drift check in §1).
Nothing in the lane was edited: no counter, fixture, registry, entry, tool or report. All work ran in
`/fast/scratch/hyaku/mado-r48/RevC1Explain` and that directory was deleted; the receipt copies are under
`.ufo/waves/round-48/w2/RevC1Explain/`. Only two path prefixes were written: this report and that directory.

## 1. Answer first

**No — not every bad explain control misses the frozen counter. Three of the eleven miss-candidates MEET it:**

| bad control | final counter line |
|---|---|
| `observed-basename` (compares captures by basename: root-insensitive) | `PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET` |
| `cmd-empty-word-dropped` (drops an empty word from the printed command) | `… explained=394/394 … verdict=TARGET_MET` |
| `cmd-argv0-newline` (flattens a newline inside the *first* command word) | `… explained=394/394 … verdict=TARGET_MET` |

The other eight miss: six on clause `x` alone, one on the warm clause `w`, one on the cold clause `f`. For the six
`x`-only rows the rest of the instrument stays at full marks — clause `x` is the only thing doing the work, exactly as
registered:

| bad control | what it gets wrong | final counter line |
|---|---|---|
| `explain-cache-path` | `explain` derives `cache=` from `$HOME/.cache` instead of `$XDG_CACHE_HOME` | `… explained=244/394 … TARGET_MISSED` |
| `explain-selected-cold` | `explain` names the **cold** id, not the cached id | `… explained=385/394 … TARGET_MISSED` |
| `explain-action-dropped` | `explain` drops the cached `:action` from `selected=`/`path=` | `… explained=387/394 … TARGET_MISSED` |
| `explain-cmd-cold` | `explain` names the **cold** command word, not the cached one | `… explained=378/394 … TARGET_MISSED` |
| `explain-path-cold` | `explain` names the **cold** path, not the cached (lying) one | `… explained=382/394 … TARGET_MISSED` |
| `observed-id-path-only` | `--observed` compares only the id and path items (the round-47 hole, rebuilt) | `… explained=47/394 … TARGET_MISSED` |
| `print-content-rc0` | `--print-content` over a vanished cached path exits 0, not the pin's 1 | `… warm=201/204 explained=394/394 … TARGET_MISSED` (clause `w`) |
| `cmd-multiline-flattened` | a newline inside **any** command word is printed as a space | `… cold=189/190 … TARGET_MISSED` (clause `f`) |

Baseline on the frozen bytes, same instrument, same recipe:

```
PRED-C1-r48 clause=a tool=present
PRED-C1-r48 clause=s rc=0 last='MADO_TERMINAL_SELFTEST: 69/69 passed'
PRED-C1-r48 clause=f cold=190/190
PRED-C1-r48 clause=w warm=204/204
PRED-C1-r48 clause=x explained=394/394
PRED-C1-r48 clause=g generated=230/230
PRED-C1-r48 clause=r trips=0
PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
```

Every control is a full `tools/mado-terminal.py` built from the draft by one anchored patch (anchor asserted to occur
exactly once; patch text and per-mutant sha256 in `RevC1Explain/patch.py` and `RevC1Explain/mutant-sha256.txt`), scored by
the frozen counter in its own sparse clone at BASE with the draft counter and the draft fixture file overlaid. Command:

```
cd <clone> && python3 -I quality/counters/c1-r48-terminal-cache.py --repo <clone> --rev HEAD --work <work> --nonce 4848
```

### Drift check on the post-freeze draft

The twelve runs above score the draft as committed in the freeze: `git show HEAD:.ufo/waves/round-48/l1-draft/mado-terminal.py`
= `1dfde36c…`. The lane's worktree draft then changed at 22:53 to `d60831ac…` (uncommitted; 436 insertions: docstring,
`TZ`, the `find -o` group rule, `ls`-model notes). Re-scored on that byte with the same counter and fixtures — baseline
still MET, and the three permissive controls still MEET, so F1/F2/F3 are not artefacts of the frozen version:

```
ref3        PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
basen3      PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
emptyword3  PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
argv0nl3    PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
```

The instrument probe was run on both versions with identical output (`probe-explain-frozen.txt`, `probe-explain-post.txt`).
The clone takes only committed objects and the tool file is copied in explicitly, so a worktree edit cannot leak into a
run; the scored byte of every row is named.

## 2. The drill the seat asked for, case by case

| required case | how it was built | result |
|---|---|---|
| cache **path** differs | `explain` re-derives `cache=` with `XDG_CACHE_HOME=$HOME/.cache` | **misses**, clause `x`, 150 fixtures. `W-01 FAIL explain got=(…, 'absent', 'OK', 0) want=(…, 'hit', 'OK', 0)` |
| cache **id** differs | on a hit, `selected=` is the `XTE_CACHE_ENABLED=false` re-resolution's id | **misses**, clause `x`, 9 fixtures. `W-10 FAIL got=('kitty.desktop', …, 'foot', …) want=('foot.desktop', …, 'foot', …)` |
| cache **action** differs | `explain` omits the action suffix | **misses**, clause `x`, 7 fixtures. `W-12 FAIL got=('foot.desktop', '$ROOT/usr/share/applications/foot.desktop', …) want=('foot.desktop:new', '$ROOT/usr/share/applications/foot.desktop:new', …)` |
| cache **command** differs | on a hit, `cmd=` is the cold entry's first command word | **misses**, clause `x`, 16 fixtures. `W-10 FAIL got=(…, 'kitty', 'hit', 'OK', 0) want=(…, 'foot', 'hit', 'OK', 0)` |
| command carries an **empty argument** | cache-hit fixture whose exec is `foot␟␟--a` | **not caught** — `cmd-empty-word-dropped` MEETS (see F2) |
| command carries a **newline** | cache-hit fixture whose first word is `fo\not` | later-word newline **is** caught (clause `f`, fixture `w7-command-with-newline-arg`); first-word newline **is not** (F3) |
| **entry path missing** | on a hit, `path=` is the cold path, not the cached `$ROOT/nope.desktop` | **misses**, clause `x`, 12 fixtures. `W-10 FAIL got=(…, '$ROOT/usr/share/applications/kitty.desktop', …) want=(…, '$ROOT/usr/share/applications/foot.desktop', …)`; the frozen set also carries it in `v2-mf-22-lying-path` and `L1-01..03` |
| `--print-content` **fails** | cached path replaced by `$ROOT/nope.desktop`; tool returns 0 instead of the pin's 1 | **misses**, clause `w`, 3 fixtures: `L1-01-gone-path-content FAIL oracle=(1, '') tool=(0, '')`, same for `L1-02-gone-path-id-content` and `L1-03-gone-path-content-cmd`. Clause `x` is not the place: it never runs `--print-content` |
| **observed capture truncated** | `--observed` compares only items 1-2 (id, path) | **misses**, clause `x`, 347 fixtures, all `observed DIFFER: got AGREE/0` — the third capture (cut to id+path) is what kills it |
| **observed capture root-relative** | `--observed` compares captures by basename | **not caught** — `observed-basename` MEETS (F1) |

## 3. Findings

### F1 (freeze-blocking) — the `--observed` comparison never sees a capture from another tree, so a root-insensitive comparator agrees

Clause `x` writes all three captures itself, each rooted in the **tool's own** tree (`o_norm` with `$ROOT` → `rt`), so a
tool that compares only tree-relative names agrees with every capture and still passes. The bad control
`observed-basename` patches the verdict line to

```python
def _rel(t):
    return "\n".join(os.path.basename(x.rstrip(":")) if "/" in x else x for x in t.split("\n"))
verdict = "AGREE" if _rel(mine) == _rel(observed) else "DIFFER"
```

Counter: `TARGET_MET` (all clause lines at full marks). What it wrongly accepts, measured with the frozen counter's own
sandbox and the frozen tool as the judge (`probe-explain.txt`, "P3/P4" block), with the oracle's real
`--print-id --print-path --print-cmd` capture:

```
draft              observed=foreign-root   verdict=DIFFER  rc=1
observed-basename  observed=foreign-root   verdict=AGREE   rc=0
draft              observed=root-relative  verdict=DIFFER  rc=1
observed-basename  observed=root-relative  verdict=AGREE   rc=0
```

The contract (`registration.md`, clause `x`; tool docstring lines 21-23) is AGREE only "when the three printed items
equal this tool's". A capture produced in a different root has different `path=` items and MUST differ. Repair
suggested by the evidence: a fourth capture taken from a *second* prepared tree (or with the root prefix stripped) whose
expected verdict is `DIFFER`/1 — the same shape as the two existing negative captures, which are correctly built.

### F2 (freeze-blocking) — an empty command word is in contract, is printable, and is not in any fixture or generated case

The draft's cache reader joins cache lines 11+ with `\n` and splits on `\x1f`, so a hit cache with `foot␟␟--a` carries an
empty word; the pin prints it (a blank line between words). Instrument probe on such a case, built by the counter's own
`schema v2` preparation (prime with the pin, then `after.cache_lines {"11": "foot\x1f\x1f--a\x1eEND_OF_EXEC_USEP"}`):

```
draft                    probe-empty-word   clause-w ok=True  state=hit oracle=(0,'foot\n\n--a\n') why=''
draft                    probe-empty-word   clause-x ok=True  why=''
cmd-empty-word-dropped   probe-empty-word   clause-w ok=False why="oracle=(0, 'foot\\n\\n--a\\n') tool=(0, 'foot\\n--a\\n')"
cmd-empty-word-dropped   probe-empty-word   clause-x ok=False why='observed AGREE: got DIFFER/1'
```

So the clauses have teeth on the case; the frozen set simply contains none. Checked over both fixture files: no expected
stdout in the 190 cold + 204 warm fixtures carries an empty command word — no expect has two consecutive newlines
outside the `--print-content` body of `u6-print-content-and-cmd`, and the two `--test` fixtures (`l1-test-mode`,
`L1-04-cached-test-mode`) have no empty `><` argument. `cmd-empty-word-dropped` therefore MEETS the frozen counter
(`explained=394/394`). Repair: one warm fixture with the cache line above; the schema already supports it.

### F3 (freeze-blocking, instrument defect first) — a newline inside the **first** command word is unscored, and cannot be scored as frozen: the draft tool fails clause `x` on it

Instrument probe, same preparation, cache line 11 `fo\not\x1f--a\x1eEND_OF_EXEC_USEP`:

```
draft                    probe-newline-word clause-w ok=True  state=hit oracle=(0,'fo\not\n--a\n') why=''
draft                    probe-newline-word clause-x ok=False why="unparseable MADO_TERM line: 'MADO_TERM: selected=foot.desktop path=$ROOT/usr/share/applications/foot.desktop cmd=fo'"
cmd-multiline-flattened  probe-newline-word clause-w ok=False why="oracle=(0, 'fo\\not\\n--a\\n') tool=(0, 'fo ot\\n--a\\n')"
cmd-argv0-newline        probe-newline-word clause-w ok=False why="oracle=(0, 'fo\\not\\n--a\\n') tool=(0, 'fo ot\\n--a\\n')"
```

`explain` prints `cmd=` verbatim, so a newline inside it splits the `MADO_TERM:` record; `explain_case` looks only at
lines that start with `MADO_TERM: ` and then requires `cache=`/`verdict=` on that same line, so the faithful draft is
rejected with "unparseable MADO_TERM line". This is the round-47 F3 shape (a record that is not one line) surviving in
the *scored* path: the counter takes `cmd=` from the `--print-cmd=\036` probe (correct), but the record it prints can
itself span lines. Consequences, both measured:

* a tool that flattens newlines **only in the first word** (`cmd-argv0-newline`) MEETS the frozen counter
  (`explained=394/394`), because no fixture has one;
* adding such a fixture without repairing `explain_case`/`term_line` would make the tool that does the work MISS.

A newline inside a **later** word is already scored and works: the frozen cold fixture `w7-command-with-newline-arg`
fails `cmd-multiline-flattened` with `oracle=(0, 'alacritty\n-e\nline1\nline2\n') tool=(0, 'alacritty\n-e\nline1 line2\n')`
(clause `f`, `cold=189/190`) — so the *writer* of a newline is in contract and the pin prints it verbatim.

### F4 (confirmations, not defects)

* The four "cache … differs" explain mutants are caught by clause `x` and by **nothing else** (`w`, `f`, `g` at full
  marks), which is the separability the registration claims: the warm clause compares the tool's `print` output, the
  explain clause compares the trace's four fields. `cache=` alone kills 150 fixtures (`explain-cache-path`), the cached
  id/action/path/command each have their own kill set (9 / 7 / 12 / 16).
* The truncated-capture defence (the round-47 `w2/CritC1Explain` hole) works: 347 fixtures report
  `observed DIFFER: got AGREE/0` for `observed-id-path-only`. The cut-to-two-items capture is the only one that catches
  an id+path comparator, and it does.
* `--print-content` failure is scored by clause `w` on exactly the three `L1-0x` fixtures and by nothing else; clause `x`
  does not run `--print-content`, which is correct (the observed capture is always the print trio).

## 4. Risks, residuals, what I did not test

* **Residual (mine):** I did not build a separate control for the `NO_TERMINAL`/exit-3 half of clause `x` (the oracle's
  `expect.rc == 1` branch) or for an `--observed` capture that carries a marker of a later field (explicitly declared
  out of parser scope in `term_line`'s docstring). Both remain un-attacked by this seat.
* **Residual (instrument):** `observed_case` writes the three captures into a fresh `mkdtemp` inside the tool tree's
  `.rw` with `O_EXCL|O_NOFOLLOW`; a tool that pre-creates names cannot influence them, but a tool that *deletes* the
  directory would surface as a clause-`x` failure, which is the declared behaviour.
* **Residual (evidence):** every control is a one-anchor deviation of the draft, and the baseline `TARGET_MET` on the
  same bytes shows the deviations are what the counter sees (no fixture was re-generated, no nonce changed: `--nonce 4848`
  for all runs).
* Root-insensitivity (F1) is a *permissiveness* hole, not a false miss: the tool that did the work still passes. F3 is
  both — permissive for first-word newlines today, and false-missing for the faithful tool the moment such a fixture is
  added.
* Per the registration's own control rule ("a control that meets triggers a fixture/counter repair before freeze"),
  F1, F2 and F3 are pre-data repairs: F1 needs a foreign-root/root-relative capture in clause `x`; F2 needs the
  empty-word warm fixture; F3 needs both the fixture and a `MADO_TERM` parser that accepts a value spanning lines.

## 5. Receipts

All under `.ufo/waves/round-48/w2/RevC1Explain/`:

| file | content |
|---|---|
| `receipts/out-ref2.txt`, `out-cachepath.txt`, `out-selcold.txt`, `out-actdrop.txt`, `out-cmdcold.txt`, `out-pathcold.txt`, `out-idpath.txt`, `out-basen.txt`, `out-contentrc.txt`, `out-emptyword.txt`, `out-newline.txt`, `out-argv0nl.txt` | full counter stdout per run on the frozen draft `1dfde36c…` (per-fixture lines + clause lines + final line) |
| `receipts/out-ref3.txt`, `out-basen3.txt`, `out-emptyword3.txt`, `out-argv0nl3.txt` | the drift check on the worktree draft `d60831ac…` |
| `receipts/log-*.txt` | the runner's final/clause echo per run |
| `clause-summary.txt` | clause `f`/`w`/`x`/`g`/`r` + final line for all twelve frozen-draft runs |
| `clause-failures.txt` | first eight `clause=x/w/f ... FAIL` lines per missing control |
| `probe-explain.txt` (frozen draft), `probe-explain-frozen.txt`, `probe-explain-post.txt` | the instrument probe: P1 empty command word, P2 first-word newline, P3 foreign-root capture, P4 root-relative capture |
| `probe.py`, `patch.py`, `run-one.sh`, `mutant-sha256.txt`, `receipts/regen-frozen.txt` | the probe driver, the anchored patcher (takes `SRC [OUTDIR]`), the scoring runner, every sha256, and the mutant-regeneration output that matches the recorded hashes |
| `environment.txt` | digests, replay recipe, the 1 MiB-cap conflicts and their measured fixes, largest files, timings |

Evidence runs: `--nonce 4848`, sparse clone of the lane at `579f694`, draft counter + draft warm fixtures overlaid,
`--rev HEAD` in that clone. The lane, its registry, counters, fixtures, entry and report were not touched; the scratch
tree was removed.
